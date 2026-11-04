import asyncio
import re
import json
import os
from typing import List, Optional
from dotenv import load_dotenv
from fastapi import BackgroundTasks, FastAPI, File, Form, Request, UploadFile
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from google import genai
from google.genai import types
import mysql.connector
import httpx
import requests

load_dotenv()

app = FastAPI(title="Motor Central IA - Euroaberturas")
client = genai.Client()

# --- MIDDLEWARE CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
EVOLUTION_API_URL = os.getenv("EVOLUTION_API_URL", "http://127.0.0.1:8085")
EVOLUTION_API_KEY = os.getenv("EVOLUTION_API_KEY", "")
INSTANCE_NAME = "euroaberturas"

# --- BRIDGE DIPA (WhatsApp) ---
# Si BRIDGE_API_KEY esta definida, se usa el bridge en lugar de Evolution directo.
BRIDGE_URL = os.getenv("BRIDGE_URL", "https://bot.dipa.ar/bridge").rstrip("/")
BRIDGE_API_KEY = os.getenv("BRIDGE_API_KEY", "")
BRIDGE_INSTANCE = os.getenv("BRIDGE_INSTANCE", "euroaberturas")
BRIDGE_WEBHOOK_URL = os.getenv("BRIDGE_WEBHOOK_URL", "")  # URL publica (o interna) de /webhook/whatsapp

# Si es 1, el bot NUNCA responde por WhatsApp (solo guarda todo para analisis).
WHATSAPP_SOLO_ESCUCHA = os.getenv("WHATSAPP_SOLO_ESCUCHA", "0") == "1"

# Multimedia: se guarda en disco. MEDIA_ANALISIS=1 transcribe audios / describe imagenes con Gemini.
import base64, uuid, mimetypes
MEDIA_DIR = os.getenv("MEDIA_DIR", os.path.join(os.path.dirname(os.path.abspath(__file__)), "media"))
MEDIA_ANALISIS = os.getenv("MEDIA_ANALISIS", "0") == "1"
MEDIA_MAX_BYTES = 25 * 1024 * 1024
MEDIA_TIPOS = ("imageMessage", "videoMessage", "audioMessage", "documentMessage", "stickerMessage")

def _bridge_headers():
    return {"Authorization": f"Bearer {BRIDGE_API_KEY}", "Content-Type": "application/json"}

def cargar_prompt_sistema():
    path = "/var/www/dipa/bot_euroaberturas/prompt.txt"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return "Sos el asistente virtual de Euroaberturas. Atendé con amabilidad."

def get_db():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        user=os.getenv("DB_USER", ""),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "bot_euroaberturas"),
        use_pure=True
    )

def init_log_table():
    """Registro crudo de TODO lo que entra y sale (para analisis)."""
    try:
        db = get_db()
        c = db.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS mensajes_log (
            id BIGINT AUTO_INCREMENT PRIMARY KEY,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            canal VARCHAR(30),
            instancia VARCHAR(80),
            session_id VARCHAR(80),
            es_grupo TINYINT(1) DEFAULT 0,
            direccion VARCHAR(20),
            tipo VARCHAR(40),
            texto MEDIUMTEXT,
            push_name VARCHAR(120),
            wa_message_id VARCHAR(120),
            raw LONGTEXT,
            UNIQUE KEY uq_wa (wa_message_id),
            KEY ix_sess (session_id, fecha)
        ) CHARACTER SET utf8mb4""")
        db.commit()
        for col in ("archivo VARCHAR(255)", "mime VARCHAR(100)", "analisis MEDIUMTEXT"):
            try:
                c.execute(f"ALTER TABLE mensajes_log ADD COLUMN {col}")
                db.commit()
            except Exception:
                pass  # ya existe
        c.close(); db.close()
        os.makedirs(MEDIA_DIR, exist_ok=True)
    except Exception as e:
        print(f"❌ No se pudo crear mensajes_log: {e}")

def extraer_media(msg_data, message_content):
    """Devuelve (nombre_archivo, mime, bytes) si el mensaje trae multimedia en base64."""
    try:
        for k in MEDIA_TIPOS:
            sub = message_content.get(k)
            if not sub:
                continue
            b64 = message_content.get("base64") or msg_data.get("base64") or sub.get("base64")
            if not b64:
                return None
            if "," in b64[:80]:
                b64 = b64.split(",", 1)[1]
            datos = base64.b64decode(b64)
            if len(datos) > MEDIA_MAX_BYTES:
                return None
            mime = (sub.get("mimetype") or "application/octet-stream").split(";")[0]
            ext = mimetypes.guess_extension(mime) or ".bin"
            if mime.startswith("audio/ogg"):
                ext = ".ogg"
            nombre = f"{uuid.uuid4().hex}{ext}"
            with open(os.path.join(MEDIA_DIR, nombre), "wb") as f:
                f.write(datos)
            return nombre, mime, datos
    except Exception as e:
        print(f"❌ Error extrayendo media: {e}")
    return None

def analizar_media_sync(wa_id, mime, datos):
    """Transcribe audio / describe imagen o PDF con Gemini y lo guarda en mensajes_log.analisis."""
    try:
        if mime.startswith("audio/"):
            pedido = "Transcribi este audio en español, literal. Solo el texto."
        elif mime.startswith("image/") or mime == "application/pdf":
            pedido = "Describi brevemente este contenido y transcribi cualquier texto visible, en español."
        else:
            return
        r = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[types.Content(role="user", parts=[
                types.Part.from_text(text=pedido),
                types.Part.from_bytes(data=datos, mime_type=mime)])],
        )
        db = get_db(); c = db.cursor()
        c.execute("UPDATE mensajes_log SET analisis=%s WHERE wa_message_id=%s", (r.text, wa_id))
        db.commit(); c.close(); db.close()
    except Exception as e:
        print(f"❌ Error analizando media: {e}")

def log_mensaje(canal, instancia, session_id, direccion, tipo, texto,
                es_grupo=0, push_name=None, wa_id=None, raw=None, archivo=None, mime=None):
    try:
        db = get_db()
        c = db.cursor()
        c.execute(
            "INSERT IGNORE INTO mensajes_log (canal, instancia, session_id, es_grupo, direccion, tipo, texto, push_name, wa_message_id, raw, archivo, mime) "
            "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            (canal, instancia, session_id, es_grupo, direccion, tipo, texto, push_name, wa_id,
             json.dumps(raw, ensure_ascii=False) if raw is not None else None, archivo, mime)
        )
        db.commit(); c.close(); db.close()
    except Exception as e:
        print(f"❌ Error log_mensaje: {e}")

init_log_table()

async def enviar_respuesta_whatsapp(numero: str, texto: str):
    # OJO: WHATSAPP_SOLO_ESCUCHA se controla en el webhook (respuestas automaticas);
    # los mensajes del operador desde el panel siempre se envian.
    if BRIDGE_API_KEY:
        try:
            async with httpx.AsyncClient() as http_client:
                res = await http_client.post(
                    f"{BRIDGE_URL}/api/instancias/{BRIDGE_INSTANCE}/send-text",
                    headers=_bridge_headers(),
                    json={"number": numero, "text": texto},
                    timeout=15.0
                )
                if res.status_code >= 300:
                    print(f"❌ Bridge send-text {res.status_code} a {numero}: {res.text[:300]}")
        except Exception as e:
            print(f"❌ Error enviando por bridge: {e}")
        return
    async with httpx.AsyncClient() as http_client:
        try:
            await http_client.post(
                f"{EVOLUTION_API_URL}/message/sendText/{INSTANCE_NAME}",
                headers={"apikey": EVOLUTION_API_KEY, "Content-Type": "application/json"},
                json={"number": numero, "text": texto},
                timeout=10.0
            )
        except Exception as e:
            print(f"❌ Error enviando respuesta a WhatsApp: {e}")

async def enviar_respuesta_telegram(chat_id: str, texto: str):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {"chat_id": chat_id, "text": texto}
        async with httpx.AsyncClient() as http_client:
            await http_client.post(url, json=payload, timeout=10.0)
    except Exception as e:
        print(f"❌ Error enviando respuesta a Telegram: {e}")

async def procesar_mensaje_core(
    session_id: str,
    mensaje_cliente: str,
    archivos_bytes: Optional[List[dict]] = None,
    origen_rol: str = "user",
    canal_slug: str = "whatsapp"
):
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute("SELECT modo FROM canales WHERE slug = %s", (canal_slug,))
        canal = cursor.fetchone()
        modo_global = canal["modo"] if canal else "ia_hibrida"

        # SOLO WhatsApp nace mudo (humano). Web, Telegram y el resto nacen con IA activa.
        if canal_slug == "whatsapp":
            estado_bot_inicial = "humano"
        else:
            estado_bot_inicial = "activo"

        cursor.execute("SELECT id, estado_bot FROM conversaciones WHERE session_id = %s", (session_id,))
        conv = cursor.fetchone()
        if not conv:
            cursor.execute(
                "INSERT INTO conversaciones (session_id, ultimo_mensaje, empresa_id, estado_atencion, estado_bot) VALUES (%s, %s, 'euroaberturas', 'nuevo', %s)",
                (session_id, mensaje_cliente[:100] if mensaje_cliente else "Archivo adjunto", estado_bot_inicial)
            )
            db.commit()
            conv_id = cursor.lastrowid
            estado_bot = estado_bot_inicial
        else:
            conv_id = conv["id"]
            estado_bot = conv["estado_bot"]

        cursor.execute(
            "INSERT INTO mensajes (conversacion_id, rol, texto) VALUES (%s, %s, %s)",
            (conv_id, origen_rol, mensaje_cliente or "Archivo adjunto")
        )
        cursor.execute(
            "UPDATE conversaciones SET ultimo_mensaje = %s WHERE id = %s",
            (mensaje_cliente[:100] if mensaje_cliente else "Archivo adjunto", conv_id)
        )
        db.commit()

        if origen_rol == 'human_operator' or estado_bot == 'humano':
            cursor.close()
            db.close()
            return None, 0

        if modo_global in ['solo_humano', 'desactivado'] and (estado_bot != 'activo' or canal_slug == 'whatsapp'):
            cursor.close()
            db.close()
            return None, 0

        cursor.execute(
            "SELECT rol, texto FROM mensajes WHERE conversacion_id = %s ORDER BY id ASC LIMIT 20",
            (conv_id,)
        )
        filas_historial = cursor.fetchall()

        contenidos = []
        for fila in filas_historial:
            rol_gemini = "user" if fila["rol"] in ["user", "human_operator"] else "model"
            contenidos.append(
                types.Content(
                    role=rol_gemini,
                    parts=[types.Part.from_text(text=fila["texto"])]
                )
            )

        partes_actuales = []
        if mensaje_cliente:
            partes_actuales.append(types.Part.from_text(text=mensaje_cliente))

        if archivos_bytes:
            for arch in archivos_bytes:
                partes_actuales.append(
                    types.Part.from_bytes(data=arch["data"], mime_type=arch["mime"])
                )

        contenidos.append(types.Content(role="user", parts=partes_actuales))

        system_prompt = cargar_prompt_sistema()
        max_reintentos = 3
        respuesta_bot = None

        for intento in range(max_reintentos):
            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=contenidos,
                    config=types.GenerateContentConfig(
                        system_instruction=system_prompt, 
                        temperature=0.3
                    ),
                )
                respuesta_bot = response.text
                break
            except Exception as e_api:
                if intento < max_reintentos - 1:
                    await asyncio.sleep(2)
                else:
                    respuesta_bot = None

        if respuesta_bot:
            cursor.execute(
                "INSERT INTO mensajes (conversacion_id, rol, texto) VALUES (%s, 'model', %s)",
                (conv_id, respuesta_bot)
            )
            cursor.execute(
                "UPDATE conversaciones SET ultimo_mensaje = %s WHERE id = %s",
                (respuesta_bot[:100], conv_id)
            )
            db.commit()
            mensaje_id = cursor.lastrowid
        else:
            mensaje_id = 0

        cursor.close()
        db.close()
        return respuesta_bot, mensaje_id

    except Exception as e:
        print(f"❌ Error en procesar_mensaje_core: {str(e)}")
        return None, 0

# --- VISTAS HTML ---
@app.get("/")
@app.get("/index.html")
async def ver_index():
    if os.path.exists("index.html"):
        return FileResponse("index.html")
    return HTMLResponse("<h2>Bot Euroaberturas Activo 🪟</h2>")

@app.get("/admin")
@app.get("/admin.html")
async def ver_admin():
    if os.path.exists("admin.html"):
        return FileResponse("admin.html")
    return HTMLResponse("<h2>Archivo admin.html no encontrado</h2>")

@app.get("/canales")
@app.get("/canales.html")
async def vista_canales():
    if os.path.exists("canales.html"):
        return FileResponse("canales.html")
    return HTMLResponse("<h2>Archivo canales.html no encontrado</h2>")

# --- RECEPTOR WEB UNIFICADO (SOPORTA NGINX / CUALQUIER RUTA POST) ---
@app.post("/")
@app.post("/index.html")
@app.post("/api/motor-ia")       # <--- LA LLAVE MAESTRA PARA NGINX
@app.post("/api/motor-ia/")
@app.post("/bot_euroaberturas/api/motor-ia")
@app.post("/bot_euroaberturas/api/motor-ia/")
@app.post("/motor-ia")
@app.post("/motor-ia/")
@app.post("/bot_euroaberturas")
@app.post("/bot_euroaberturas/")
@app.post("/bot_euroaberturas/motor-ia")
@app.post("/bot_euroaberturas/motor-ia/")
@app.post("/chat")
@app.post("/api/chat")
async def receptor_web_unificado(
    request: Request,
    session_id: Optional[str] = Form(None),
    mensaje_cliente: Optional[str] = Form(None),
    archivos: Optional[List[UploadFile]] = File(None)
):
    archivos_bytes = []
    
    if not session_id or mensaje_cliente is None:
        try:
            form = await request.form()
            session_id = session_id or form.get("session_id") or form.get("sessionId")
            mensaje_cliente = mensaje_cliente or form.get("mensaje_cliente") or form.get("mensaje") or form.get("texto")
        except Exception:
            pass

    if not session_id or mensaje_cliente is None:
        try:
            json_data = await request.json()
            session_id = session_id or json_data.get("session_id") or json_data.get("sessionId")
            mensaje_cliente = mensaje_cliente or json_data.get("mensaje_cliente") or json_data.get("mensaje") or json_data.get("texto")
        except Exception:
            pass

    session_id = session_id or "sesion_web"
    mensaje_cliente = mensaje_cliente or "Consulta desde web"

    if archivos:
        for file in archivos:
            content = await file.read()
            archivos_bytes.append({"data": content, "mime": getattr(file, "content_type", "image/jpeg")})

    respuesta, mensaje_id = await procesar_mensaje_core(
        session_id=session_id,
        mensaje_cliente=mensaje_cliente,
        archivos_bytes=archivos_bytes,
        origen_rol="user",
        canal_slug="web"
    )

    resp_text = respuesta or "¡Hola! Gracias por comunicarte con Euroaberturas."

    return {
        "status": "ok",
        "respuesta": resp_text,
        "response": resp_text,
        "texto": resp_text,
        "mensaje_id": mensaje_id
    }

# --- FEEDBACK UNIFICADO ---
@app.post("/api/motor-ia/feedback") # <--- LA LLAVE MAESTRA PARA NGINX
@app.post("/bot_euroaberturas/api/motor-ia/feedback")
@app.post("/feedback")
@app.post("/feedback/")
@app.post("/motor-ia/feedback")
@app.post("/motor-ia/feedback/")
@app.post("/bot_euroaberturas/feedback")
@app.post("/bot_euroaberturas/motor-ia/feedback")
async def recibir_feedback(mensaje_id: int = Form(0), rating: int = Form(0)):
    try:
        if mensaje_id > 0:
            db = get_db()
            cursor = db.cursor()
            cursor.execute("UPDATE mensajes SET rating = %s WHERE id = %s", (rating, mensaje_id))
            db.commit()
            cursor.close()
            db.close()
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "detalle": str(e)}

# --- WEBHOOK WHATSAPP ---
@app.post("/webhook/whatsapp")
@app.post("/webhook/")
async def webhook_whatsapp(request: Request, background_tasks: BackgroundTasks):
    try:
        data = await request.json()
        event = data.get("event")

        if event in ["messages.upsert", "MESSAGES_UPSERT"]:
            msg_data = data.get("data", {})
            key = msg_data.get("key", {})

            remote_jid = key.get("remoteJid", "")
            es_grupo = "@g.us" in remote_jid
            numero = remote_jid.split("@")[0]
            is_from_me = key.get("fromMe", False)
            rol_asignado = "human_operator" if is_from_me else "user"

            message_content = msg_data.get("message", {}) or {}
            tipo = msg_data.get("messageType") or (next(iter(message_content), "desconocido"))
            mensaje = ""
            if "conversation" in message_content:
                mensaje = message_content["conversation"]
            elif "extendedTextMessage" in message_content:
                mensaje = message_content["extendedTextMessage"].get("text", "")
            else:
                for k in ("imageMessage", "videoMessage", "documentMessage"):
                    if k in message_content:
                        mensaje = message_content[k].get("caption", "") or ""
                        break

            media = extraer_media(msg_data, message_content)
            # No guardar el base64 gigante dentro del raw
            try:
                for contenedor in (message_content, msg_data):
                    contenedor.pop("base64", None)
                for k in MEDIA_TIPOS:
                    if k in message_content:
                        message_content[k].pop("base64", None)
            except Exception:
                pass

            # Registro completo (incluye grupos, multimedia y mensajes propios)
            log_mensaje(
                "whatsapp", data.get("instance") or BRIDGE_INSTANCE, numero,
                "saliente_operador" if is_from_me else "entrante", tipo, mensaje,
                es_grupo=1 if es_grupo else 0, push_name=msg_data.get("pushName"),
                wa_id=key.get("id"), raw=data,
                archivo=media[0] if media else None, mime=media[1] if media else None
            )
            if media and MEDIA_ANALISIS and key.get("id"):
                background_tasks.add_task(asyncio.to_thread, analizar_media_sync, key.get("id"), media[1], media[2])

            if es_grupo:
                return {"status": "ignored_group"}

            if mensaje:
                respuesta, _ = await procesar_mensaje_core(
                    session_id=numero,
                    mensaje_cliente=mensaje,
                    origen_rol=rol_asignado,
                    canal_slug="whatsapp"
                )

                if respuesta and not is_from_me and not WHATSAPP_SOLO_ESCUCHA:
                    log_mensaje("whatsapp", BRIDGE_INSTANCE, numero, "saliente_bot", "conversation", respuesta)
                    background_tasks.add_task(enviar_respuesta_whatsapp, numero, respuesta)

        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "detalle": str(e)}

# --- CONEXION WHATSAPP VIA BRIDGE ---
async def _bridge(metodo: str, ruta: str, body=None):
    if not BRIDGE_API_KEY:
        return 0, {"error": "Falta BRIDGE_API_KEY en .env"}
    async with httpx.AsyncClient() as http_client:
        res = await http_client.request(
            metodo, f"{BRIDGE_URL}{ruta}", headers=_bridge_headers(), json=body, timeout=20.0
        )
        try:
            return res.status_code, res.json()
        except Exception:
            return res.status_code, {"raw": res.text}

@app.get("/api/media/{nombre}")
@app.get("/bot_euroaberturas/api/media/{nombre}")
async def ver_media(nombre: str):
    if not re.fullmatch(r"[0-9a-f]{32}\.[A-Za-z0-9]{1,8}", nombre):
        return {"error": "nombre invalido"}
    ruta = os.path.join(MEDIA_DIR, nombre)
    if not os.path.isfile(ruta):
        return {"error": "no existe"}
    return FileResponse(ruta)

@app.post("/api/conexion-crear")
@app.post("/bot_euroaberturas/api/conexion-crear")
async def conexion_crear():
    """Crea la instancia (si no existe) y configura el webhook hacia este bot."""
    try:
        cod, crear = await _bridge("POST", "/api/instancias", {"nombre": BRIDGE_INSTANCE})
        if cod not in (200, 201, 409):
            return {"status": "error", "paso": "crear", "detalle": crear}
        webhook = None
        if BRIDGE_WEBHOOK_URL:
            _, webhook = await _bridge(
                "POST", f"/api/instancias/{BRIDGE_INSTANCE}/webhook",
                {"url": BRIDGE_WEBHOOK_URL, "events": ["MESSAGES_UPSERT"], "base64": True}
            )
        return {"status": "ok", "instancia": BRIDGE_INSTANCE, "crear": crear, "webhook": webhook}
    except Exception as e:
        return {"status": "error", "detalle": str(e)}

@app.get("/api/conexion-qr")
@app.get("/bot_euroaberturas/api/conexion-qr")
async def conexion_qr():
    try:
        _, data = await _bridge("GET", f"/api/instancias/{BRIDGE_INSTANCE}/qr")
        return data
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/conexion-estado")
@app.get("/bot_euroaberturas/api/conexion-estado")
async def conexion_estado():
    try:
        _, data = await _bridge("GET", f"/api/instancias/{BRIDGE_INSTANCE}/estado")
        return data
    except Exception as e:
        return {"error": str(e)}

# --- ENDPOINTS API ERP / ADMIN ---
@app.get("/api/chats")
async def listar_chats():
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM conversaciones ORDER BY id DESC")
        chats = cursor.fetchall()
        cursor.close()
        db.close()
        return {"status": "ok", "chats": chats}
    except Exception as e:
        return {"status": "error", "detalle": str(e)}

@app.get("/api/chat/{session_id}")
async def obtener_historial_chat(session_id: str):
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT m.* FROM mensajes m
            JOIN conversaciones c ON m.conversacion_id = c.id
            WHERE c.session_id = %s
            ORDER BY m.id ASC
        """, (session_id,))
        mensajes = cursor.fetchall()
        cursor.close()
        db.close()
        return {"status": "ok", "mensajes": mensajes}
    except Exception as e:
        return {"status": "error", "detalle": str(e)}

@app.post("/api/actualizar-chat")
async def actualizar_chat(
    session_id: str = Form(...),
    nombre_cliente: Optional[str] = Form(None),
    etiquetas: Optional[str] = Form(None),
    estado_atencion: Optional[str] = Form("nuevo")
):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("""
            UPDATE conversaciones 
            SET nombre_cliente = %s, etiquetas = %s, estado_atencion = %s 
            WHERE session_id = %s
        """, (nombre_cliente, etiquetas, estado_atencion, session_id))
        db.commit()
        cursor.close()
        db.close()
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "detalle": str(e)}

@app.post("/api/cambiar-estado")
async def cambiar_estado_bot(session_id: str = Form(...), estado: str = Form(...)):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("UPDATE conversaciones SET estado_bot = %s WHERE session_id = %s", (estado, session_id))
        db.commit()
        cursor.close()
        db.close()
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "detalle": str(e)}

@app.post("/api/enviar-mensaje")
async def enviar_mensaje_operador(session_id: str = Form(...), texto: str = Form(...), background_tasks: BackgroundTasks = None):
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT id FROM conversaciones WHERE session_id = %s", (session_id,))
        conv = cursor.fetchone()
        
        if not conv:
            cursor.execute(
                "INSERT INTO conversaciones (session_id, ultimo_mensaje, empresa_id, estado_atencion) VALUES (%s, %s, 'euroaberturas', 'progreso')",
                (session_id, texto[:100])
            )
            db.commit()
            conv_id = cursor.lastrowid
        else:
            conv_id = conv["id"]

        cursor.execute(
            "INSERT INTO mensajes (conversacion_id, rol, texto) VALUES (%s, 'human_operator', %s)",
            (conv_id, texto)
        )
        cursor.execute("UPDATE conversaciones SET ultimo_mensaje = %s WHERE id = %s", (texto[:100], conv_id))
        db.commit()

        cursor.close()
        db.close()

        if background_tasks:
            if session_id.startswith("tg_"):
                chat_id_telegram = session_id.replace("tg_", "")
                background_tasks.add_task(enviar_respuesta_telegram, chat_id_telegram, texto)
            elif not session_id.startswith("sesion_"):
                background_tasks.add_task(enviar_respuesta_whatsapp, session_id, texto)

        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "detalle": str(e)}

@app.get("/api/admin/canales")
async def obtener_canales():
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM canales")
        canales = cursor.fetchall()
        
        totales = len(canales)
        activos = sum(1 for c in canales if c["activo"])
        configurados = sum(1 for c in canales if c["modo"] != "desactivado")
        
        cursor.close()
        db.close()
        return {
            "status": "ok",
            "resumen": {"totales": totales, "activos": activos, "configurados": configurados},
            "canales": canales
        }
    except Exception as e:
        return {"status": "error", "detalle": str(e)}

@app.post("/api/admin/canales/cambiar-modo")
async def cambiar_modo_canal(slug: str = Form(...), modo: str = Form(...)):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("UPDATE canales SET modo = %s WHERE slug = %s", (modo, slug))
        db.commit()
        cursor.close()
        db.close()
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "detalle": str(e)}

@app.get("/api/admin/evolution-instancias")
async def listar_instancias_evolution():
    async with httpx.AsyncClient() as http_client:
        try:
            res = await http_client.get(
                f"{EVOLUTION_API_URL}/instance/fetchInstances",
                headers={"apikey": EVOLUTION_API_KEY},
                timeout=5.0
            )
            return res.json()
        except Exception as e:
            return {"error": str(e)}

@app.get("/api/admin/respuestas-rapidas")
async def obtener_respuestas_rapidas():
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM respuestas_rapidas WHERE activo = 1 ORDER BY atajo ASC")
        data = cursor.fetchall()
        cursor.close()
        db.close()
        return {"status": "ok", "items": data}
    except Exception as e:
        return {"status": "error", "detalle": str(e)}

@app.post("/api/admin/respuestas-rapidas/crear")
async def crear_respuesta_rapida(atajo: str = Form(...), texto: str = Form(...), descripcion: Optional[str] = Form("")):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO respuestas_rapidas (atajo, texto, descripcion) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE texto=%s, descripcion=%s",
            (atajo, texto, descripcion, texto, descripcion)
        )
        db.commit()
        cursor.close()
        db.close()
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "detalle": str(e)}

@app.get("/api/admin/etiquetas")
async def obtener_etiquetas():
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM etiquetas_catalogo ORDER BY id DESC")
        data = cursor.fetchall()
        cursor.close()
        db.close()
        return {"status": "ok", "items": data}
    except Exception as e:
        return {"status": "error", "detalle": str(e)}

@app.post("/api/admin/etiquetas/crear")
async def crear_etiqueta(nombre: str = Form(...), color_hex: str = Form("#ca0b0f"), tipo: str = Form("manual")):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO etiquetas_catalogo (nombre, color_hex, tipo) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE color_hex=%s",
            (nombre, color_hex, tipo, color_hex)
        )
        db.commit()
        cursor.close()
        db.close()
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "detalle": str(e)}

@app.get("/api/admin/departamentos")
async def obtener_departamentos():
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM departamentos ORDER BY id ASC")
        data = cursor.fetchall()
        cursor.close()
        db.close()
        return {"status": "ok", "items": data}
    except Exception as e:
        return {"status": "error", "detalle": str(e)}

@app.post("/api/admin/departamentos/crear")
async def crear_departamento(nombre: str = Form(...), codigo: str = Form(...), agentes_count: int = Form(1)):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO departamentos (nombre, codigo, agentes_count) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE nombre=%s, agentes_count=%s",
            (nombre, codigo, agentes_count, nombre, agentes_count)
        )
        db.commit()
        cursor.close()
        db.close()
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "detalle": str(e)}

@app.get("/api/admin/flujos")
async def obtener_flujos():
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM flujos_config")
        data = cursor.fetchall()
        cursor.close()
        db.close()
        return {"status": "ok", "items": data}
    except Exception as e:
        return {"status": "error", "detalle": str(e)}

@app.post("/api/admin/flujos/guardar")
async def guardar_flujo(clave: str = Form(...), activo: int = Form(1), config_json: str = Form(...)):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO flujos_config (clave, activo, config_json) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE activo=%s, config_json=%s",
            (clave, activo, config_json, activo, config_json)
        )
        db.commit()
        cursor.close()
        db.close()
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "detalle": str(e)}