"""
Importa el historial de WhatsApp (chats y mensajes) desde el bridge DIPA.

Uso (en el servidor, dentro de la carpeta del bot):
    venv/bin/python importar_historial.py --probe              # solo muestra que devuelve el bridge
    venv/bin/python importar_historial.py --importar           # importa (hasta 500 mensajes por chat)
    venv/bin/python importar_historial.py --importar --limite 2000

- No duplica: usa el ID de WhatsApp (mensajes_log.wa_message_id es UNIQUE).
- Las conversaciones importadas quedan en estado_bot='humano' (la IA NO contesta).
- Imagenes/audios anteriores se registran como texto "[imagen anterior]" (no se bajan los archivos).
"""
import os
import sys
import json
import argparse
from datetime import datetime

import requests
import mysql.connector
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))

BRIDGE_URL = os.getenv("BRIDGE_URL", "https://bot.dipa.ar/bridge").rstrip("/")
BRIDGE_API_KEY = os.getenv("BRIDGE_API_KEY", "")
INSTANCIA = os.getenv("BRIDGE_INSTANCE", "euroaberturas")
HEADERS = {"Authorization": f"Bearer {BRIDGE_API_KEY}", "Content-Type": "application/json"}

ETIQUETAS_MEDIA = {
    "imageMessage": "[imagen anterior]",
    "videoMessage": "[video anterior]",
    "audioMessage": "[audio anterior]",
    "documentMessage": "[documento anterior]",
    "stickerMessage": "[sticker anterior]",
}


def get_db():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        user=os.getenv("DB_USER", ""),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "bot_euroaberturas"),
        use_pure=True,
    )


def bridge_post(ruta, body):
    r = requests.post(f"{BRIDGE_URL}/api/instancias/{INSTANCIA}{ruta}", headers=HEADERS, json=body, timeout=120)
    try:
        return r.status_code, r.json()
    except Exception:
        return r.status_code, {"raw": r.text[:500]}


def como_lista(d):
    """Saca la lista de registros de respuestas con formas distintas."""
    if isinstance(d, list):
        return d
    if isinstance(d, dict):
        for k in ("records", "messages", "chats", "data", "items", "result"):
            v = d.get(k)
            if isinstance(v, list):
                return v
            if isinstance(v, dict):
                sub = como_lista(v)
                if sub:
                    return sub
    return []


def timestamp_a_datetime(ts):
    if isinstance(ts, dict):
        ts = ts.get("low")
    try:
        ts = int(ts)
        if ts > 10**12:
            ts //= 1000
        return datetime.fromtimestamp(ts)
    except Exception:
        return None


def extraer_texto_y_tipo(msg):
    contenido = msg.get("message") or {}
    tipo = msg.get("messageType") or (next(iter(contenido), "desconocido"))
    texto = ""
    if "conversation" in contenido:
        texto = contenido["conversation"]
    elif "extendedTextMessage" in contenido:
        texto = contenido["extendedTextMessage"].get("text", "")
    else:
        for k in ("imageMessage", "videoMessage", "documentMessage"):
            if k in contenido:
                texto = contenido[k].get("caption", "") or ""
                break
    for k, etiqueta in ETIQUETAS_MEDIA.items():
        if k in contenido:
            texto = (etiqueta + (" " + texto if texto else ""))
            break
    return tipo, texto.strip()


def obtener_chats():
    cod, d = bridge_post("/chats", {})
    if cod >= 300:
        sys.exit(f"Error /chats ({cod}): {json.dumps(d)[:300]}")
    return como_lista(d), d


def obtener_mensajes(jid, limite):
    cod, d = bridge_post("/mensajes", {"where": {"remoteJid": jid}, "limit": limite})
    if cod >= 300:
        print(f"  ! Error /mensajes {jid} ({cod}): {json.dumps(d)[:200]}")
        return [], d
    return como_lista(d), d


def probar():
    chats, crudo = obtener_chats()
    print(f"Chats devueltos: {len(chats)}")
    if not chats:
        print("Respuesta cruda (recortada):", json.dumps(crudo)[:800])
        return
    print("Ejemplo de chat:", json.dumps(chats[0], ensure_ascii=False)[:600])
    jid = chats[0].get("remoteJid") or chats[0].get("id")
    msgs, crudo_m = obtener_mensajes(jid, 5)
    print(f"Mensajes de prueba para {jid}: {len(msgs)}")
    if msgs:
        m = json.dumps(msgs[0], ensure_ascii=False)
        print("Ejemplo de mensaje (recortado):", m[:800])
    else:
        print("Respuesta cruda (recortada):", json.dumps(crudo_m)[:800])


def importar(limite):
    chats, _ = obtener_chats()
    print(f"Chats a procesar: {len(chats)}")
    db = get_db()
    cur = db.cursor()
    total_nuevos = 0
    total_chats = 0

    for ch in chats:
        jid = ch.get("remoteJid") or ch.get("id") or ""
        if not jid or "@g.us" in jid or jid.startswith("status@") or "@broadcast" in jid:
            continue
        numero = jid.split("@")[0]
        msgs, _ = obtener_mensajes(jid, limite)
        if not msgs:
            continue

        # ordenar cronologicamente
        def clave(m):
            f = timestamp_a_datetime(m.get("messageTimestamp"))
            return f or datetime.min
        msgs.sort(key=clave)

        conv_id = None
        nuevos = 0
        for m in msgs:
            key = m.get("key", {}) or {}
            wa_id = key.get("id")
            from_me = bool(key.get("fromMe"))
            tipo, texto = extraer_texto_y_tipo(m)
            if not texto:
                continue  # reacciones, protocolo, etc.
            fecha = timestamp_a_datetime(m.get("messageTimestamp")) or datetime.now()

            cur.execute(
                "INSERT IGNORE INTO mensajes_log (fecha, canal, instancia, session_id, es_grupo, direccion, tipo, texto, push_name, wa_message_id) "
                "VALUES (%s,'whatsapp',%s,%s,0,%s,%s,%s,%s,%s)",
                (fecha, INSTANCIA, numero, "saliente_operador" if from_me else "entrante",
                 tipo, texto, m.get("pushName"), wa_id),
            )
            if cur.rowcount != 1:
                continue  # ya estaba

            if conv_id is None:
                cur.execute("SELECT id FROM conversaciones WHERE session_id = %s", (numero,))
                fila = cur.fetchone()
                if fila:
                    conv_id = fila[0]
                else:
                    cur.execute(
                        "INSERT INTO conversaciones (session_id, ultimo_mensaje, empresa_id, estado_atencion, estado_bot) "
                        "VALUES (%s, %s, 'euroaberturas', 'progreso', 'humano')",
                        (numero, texto[:100]),
                    )
                    conv_id = cur.lastrowid

            cur.execute(
                "INSERT INTO mensajes (conversacion_id, rol, texto, `timestamp`) VALUES (%s, %s, %s, %s)",
                (conv_id, "human_operator" if from_me else "user", texto, fecha),
            )
            nuevos += 1

        if conv_id and nuevos:
            # ultimo_mensaje solo si el importado es mas reciente que lo que ya hay
            cur.execute(
                "SELECT texto FROM mensajes WHERE conversacion_id=%s ORDER BY `timestamp` DESC, id DESC LIMIT 1",
                (conv_id,),
            )
            ult = cur.fetchone()
            if ult:
                cur.execute("UPDATE conversaciones SET ultimo_mensaje=%s WHERE id=%s", (ult[0][:100], conv_id))
        db.commit()
        if nuevos:
            total_chats += 1
            total_nuevos += nuevos
            print(f"  {numero}: {nuevos} mensajes nuevos")

    cur.close()
    db.close()
    print(f"Listo. {total_nuevos} mensajes importados en {total_chats} chats.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--probe", action="store_true", help="solo probar el bridge")
    ap.add_argument("--importar", action="store_true", help="importar el historial")
    ap.add_argument("--limite", type=int, default=500, help="mensajes por chat")
    a = ap.parse_args()
    if not BRIDGE_API_KEY:
        sys.exit("Falta BRIDGE_API_KEY en .env")
    if a.probe:
        probar()
    elif a.importar:
        importar(a.limite)
    else:
        ap.print_help()
