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
KINDS_MEDIA = {
    "image": "[imagen anterior]",
    "video": "[video anterior]",
    "audio": "[audio anterior]",
    "ptt": "[audio anterior]",
    "document": "[documento anterior]",
    "sticker": "[sticker anterior]",
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
        for k in ("records", "messages", "chats", "data", "items", "result", "mensajes"):
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


def es_numero(jid):
    return isinstance(jid, str) and jid.endswith("@s.whatsapp.net")


def normalizar(m):
    """Devuelve dict(wa_id, from_me, texto, tipo, fecha, nombre, numero) para los dos formatos conocidos."""
    # Formato del bridge: id, fromMe, chat, sender, nombre, kind, text, caption, timestamp, _media
    if "kind" in m or "chat" in m:
        media_key = ((m.get("_media") or {}).get("key") or {})
        from_me = bool(m.get("fromMe"))
        chat = m.get("chat") or ""
        if es_numero(media_key.get("remoteJidAlt")):
            numero_jid = media_key["remoteJidAlt"]
        elif es_numero(chat):
            numero_jid = chat
        elif not from_me and es_numero(m.get("sender")):
            numero_jid = m["sender"]
        else:
            numero_jid = chat
        texto = (m.get("text") or "").strip()
        caption = (m.get("caption") or "").strip()
        kind = m.get("kind") or "desconocido"
        if kind in KINDS_MEDIA:
            extra = caption or texto
            texto = KINDS_MEDIA[kind] + ((" " + extra) if extra else "")
        elif not texto:
            texto = caption
        return {
            "wa_id": m.get("id"), "from_me": from_me, "texto": texto, "tipo": kind,
            "fecha": timestamp_a_datetime(m.get("timestamp")), "nombre": m.get("nombre"),
            "numero": numero_jid.split("@")[0], "chat": chat,
        }
    # Formato Evolution: key{remoteJid,fromMe,id}, message{...}, messageTimestamp
    key = m.get("key") or {}
    contenido = m.get("message") or {}
    tipo = m.get("messageType") or (next(iter(contenido), "desconocido"))
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
            texto = etiqueta + ((" " + texto) if texto else "")
            break
    jid = key.get("remoteJidAlt") if es_numero(key.get("remoteJidAlt")) else key.get("remoteJid", "")
    return {
        "wa_id": key.get("id"), "from_me": bool(key.get("fromMe")), "texto": texto.strip(), "tipo": tipo,
        "fecha": timestamp_a_datetime(m.get("messageTimestamp")), "nombre": m.get("pushName"),
        "numero": (jid or "").split("@")[0], "chat": key.get("remoteJid", ""),
    }


def jid_de_chat(ch):
    if not isinstance(ch, dict):
        return None
    for k in ("remoteJid", "jid", "chat", "id"):
        v = ch.get(k)
        if isinstance(v, str) and "@" in v:
            return v
    return None


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
    print("Claves del chat:", list(chats[0].keys()) if isinstance(chats[0], dict) else type(chats[0]))
    jid = jid_de_chat(chats[0])
    print("JID detectado:", jid)
    msgs, crudo_m = obtener_mensajes(jid, 5)
    print(f"Mensajes de prueba para {jid}: {len(msgs)}")
    if msgs:
        for mm in msgs[:5]:
            print("  normalizado:", normalizar(mm))
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
        jid = jid_de_chat(ch)
        if not jid or "@g.us" in jid or jid.startswith("status@") or "@broadcast" in jid:
            continue
        msgs, _ = obtener_mensajes(jid, limite)
        norm = [n for n in (normalizar(m) for m in msgs) if n and n["texto"] and n["wa_id"]]
        if not norm:
            continue
        norm.sort(key=lambda n: n["fecha"] or datetime.min)

        conv_id = None
        nuevos = 0
        numero = norm[0]["numero"]
        for n in norm:
            fecha = n["fecha"] or datetime.now()
            cur.execute(
                "INSERT IGNORE INTO mensajes_log (fecha, canal, instancia, session_id, es_grupo, direccion, tipo, texto, push_name, wa_message_id) "
                "VALUES (%s,'whatsapp',%s,%s,0,%s,%s,%s,%s,%s)",
                (fecha, INSTANCIA, n["numero"], "saliente_operador" if n["from_me"] else "entrante",
                 n["tipo"], n["texto"], n["nombre"], n["wa_id"]),
            )
            if cur.rowcount != 1:
                continue  # ya estaba

            if conv_id is None:
                cur.execute("SELECT id FROM conversaciones WHERE session_id = %s", (n["numero"],))
                fila = cur.fetchone()
                if fila:
                    conv_id = fila[0]
                else:
                    cur.execute(
                        "INSERT INTO conversaciones (session_id, ultimo_mensaje, empresa_id, estado_atencion, estado_bot) "
                        "VALUES (%s, %s, 'euroaberturas', 'progreso', 'humano')",
                        (n["numero"], n["texto"][:100]),
                    )
                    conv_id = cur.lastrowid

            cur.execute(
                "INSERT INTO mensajes (conversacion_id, rol, texto, `timestamp`) VALUES (%s, %s, %s, %s)",
                (conv_id, "human_operator" if n["from_me"] else "user", n["texto"], fecha),
            )
            nuevos += 1

        if conv_id and nuevos:
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
