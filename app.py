import sqlite3
import os
import time
from flask import Flask, request, session, redirect

from cerebro_ia import generar_respuesta_stardew

app = Flask(__name__)
app.secret_key = "stardew_secret"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR,"stardew_saas.db")

# ----------------------------
# NPCs y URLs de imagen
# ----------------------------
NPCS = {
    "alex": {"nombre":"Alex","desc":"Deportista y seguro de sí mismo","img":"https://raw.githubusercontent.com/aizawauwunun/stardew-ia-web/main/npc_alex.png"},
    "haley": {"nombre":"Haley","desc":"Fotógrafa con estilo, algo engreída","img":"https://raw.githubusercontent.com/aizawauwunun/stardew-ia-web/main/npc_haley.png"},
    "harvey": {"nombre":"Harvey","desc":"Médico del pueblo, muy precavido","img":"https://raw.githubusercontent.com/aizawauwunun/stardew-ia-web/main/npc_harvey.png"},
    "leah": {"nombre":"Leah","desc":"Artista talentosa que ama la naturaleza","img":"https://raw.githubusercontent.com/aizawauwunun/stardew-ia-web/main/npc_leah.png"},
    "sam": {"nombre":"Sam","desc":"Músico alegre y bromista","img":"https://raw.githubusercontent.com/aizawauwunun/stardew-ia-web/main/npc_sam.png"},
    "sebastian": {"nombre":"Sebastian","desc":"Programador solitario y rebelde","img":"https://raw.githubusercontent.com/aizawauwunun/stardew-ia-web/main/npc_sebastian.png"},
    "abigail": {"nombre":"Abigail","desc":"Aventurera que ama lo oculto","img":"https://raw.githubusercontent.com/aizawauwunun/stardew-ia-web/main/npc_abigail.png"},
    "elliott": {"nombre":"Elliott","desc":"Escritor romántico y sofisticado","img":"https://raw.githubusercontent.com/aizawauwunun/stardew-ia-web/main/npc_elliott.png"},
    "emily": {"nombre":"Emily","desc":"Espíritu libre, ama la costura","img":"https://raw.githubusercontent.com/aizawauwunun/stardew-ia-web/main/npc_emily.png"},
    "shane": {"nombre":"Shane","desc":"Trabaja en Joja, ama sus gallinas","img":"https://raw.githubusercontent.com/aizawauwunun/stardew-ia-web/main/npc_shane.png"},
    "maru": {"nombre":"Maru","desc":"Científica e inventora brillante","img":"https://raw.githubusercontent.com/aizawauwunun/stardew-ia-web/main/npc_maru.png"},
    "penny": {"nombre":"Penny","desc":"Tímida, le encanta leer a los niños","img":"https://raw.githubusercontent.com/aizawauwunun/stardew-ia-web/main/npc_penny.png"},
    "marnie": {"nombre":"Marnie","desc":"Ganadera amable, cuida animales","img":"https://raw.githubusercontent.com/aizawauwunun/stardew-ia-web/main/npc_marnie.png"},
    "clint": {"nombre":"Clint","desc":"Herrero solitario y algo melancólico","img":"https://raw.githubusercontent.com/aizawauwunun/stardew-ia-web/main/npc_clint.png"},
    "caroline": {"nombre":"Caroline","desc":"Amante del té y de su jardín","img":"https://raw.githubusercontent.com/aizawauwunun/stardew-ia-web/main/npc_caroline.png"},
    "demetrius": {"nombre":"Demetrius","desc":"Científico que estudia la fauna local","img":"https://raw.githubusercontent.com/aizawauwunun/stardew-ia-web/main/npc_demetrius.png"},
    "gus": {"nombre":"Gus","desc":"Dueño del salón y gran cocinero","img":"https://raw.githubusercontent.com/aizawauwunun/stardew-ia-web/main/npc_gus.png"},
    "jas": {"nombre":"Jas","desc":"Niña pequeña, algo tímida y curiosa","img":"https://raw.githubusercontent.com/aizawauwunun/stardew-ia-web/main/npc_jas.png"},
    "jodi": {"nombre":"Jodi","desc":"Madre dedicada, siempre está ocupada","img":"https://raw.githubusercontent.com/aizawauwunun/stardew-ia-web/main/npc_jodi.png"},
    "kent": {"nombre":"Kent","desc":"Militar que regresó recientemente","img":"https://raw.githubusercontent.com/aizawauwunun/stardew-ia-web/main/npc_kent.png"},
    "leo": {"nombre":"Leo","desc":"Niño que creció en la selva con aves","img":"https://raw.githubusercontent.com/aizawauwunun/stardew-ia-web/main/npc_leo.png"},
    "lewis": {"nombre":"Lewis","desc":"El alcalde, siempre cuida el pueblo","img":"https://raw.githubusercontent.com/aizawauwunun/stardew-ia-web/main/npc_lewis.png"},
    "linus": {"nombre":"Linus","desc":"Ermitaño que vive en armonía natural","img":"https://raw.githubusercontent.com/aizawauwunun/stardew-ia-web/main/npc_linus.png"},
    "pam": {"nombre":"Pam","desc":"Conductora del bus, ama la taberna","img":"https://raw.githubusercontent.com/aizawauwunun/stardew-ia-web/main/npc_pam.png"},
    "pierre": {"nombre":"Pierre","desc":"Tendero que compite con JojaMart","img":"https://raw.githubusercontent.com/aizawauwunun/stardew-ia-web/main/npc_pierre.png"},
    "robin": {"nombre":"Robin","desc":"Carpintera experta y muy trabajadora","img":"https://raw.githubusercontent.com/aizawauwunun/stardew-ia-web/main/npc_robin.png"},
    "sandy": {"nombre":"Sandy","desc":"Regenta el Oasis en el desierto","img":"https://raw.githubusercontent.com/aizawauwunun/stardew-ia-web/main/npc_sandy.png"},
    "vincent": {"nombre":"Vincent","desc":"Niño travieso, hermano de Sam","img":"https://raw.githubusercontent.com/aizawauwunun/stardew-ia-web/main/npc_vincent.png"},
    "willy": {"nombre":"Willy","desc":"Pescador experto, ama el mar","img":"https://raw.githubusercontent.com/aizawauwunun/stardew-ia-web/main/npc_willy.png"},
    "marlon": {"nombre":"Marlon","desc":"Líder del gremio, cazador veterano","img":"https://raw.githubusercontent.com/aizawauwunun/stardew-ia-web/main/npc_marlon.png"},
    "mr_qi": {"nombre":"Mr. Qi","desc":"Personaje misterioso de gafas azules","img":"https://raw.githubusercontent.com/aizawauwunun/stardew-ia-web/main/npc_mr_qi.png"},
    "gunther": {"nombre":"Gunther","desc":"Encargado del museo y la biblioteca","img":"https://raw.githubusercontent.com/aizawauwunun/stardew-ia-web/main/npc_gunther.png"},
    "morris": {"nombre":"Morris","desc":"Gerente ambicioso de JojaMart","img":"https://raw.githubusercontent.com/aizawauwunun/stardew-ia-web/main/npc_morris.png"},
    "bouncer": {"nombre":"Bouncer","desc":"Guardián serio del Casino","img":"https://raw.githubusercontent.com/aizawauwunun/stardew-ia-web/main/npc_bouncer.png"},
    "governor": {"nombre":"Gobernador","desc":"Visita el pueblo para los banquetes","img":"https://raw.githubusercontent.com/aizawauwunun/stardew-ia-web/main/npc_governor.png"},
    "birdie": {"nombre":"Birdie","desc":"Anciana solitaria que vive en la costa","img":"https://raw.githubusercontent.com/aizawauwunun/stardew-ia-web/main/npc_birdie.png"},
    "professor_snail": {"nombre":"Prof. Snail","desc":"Investigador atrapado en la isla","img":"https://raw.githubusercontent.com/aizawauwunun/stardew-ia-web/main/npc_professor_snail.png"},
    "gil": {"nombre":"Gil","desc":"Miembro del gremio, siempre sentado","img":"https://raw.githubusercontent.com/aizawauwunun/stardew-ia-web/main/npc_gil.png"},
    "fizz": {"nombre":"Fizz","desc":"Vendedor especial de servicios raros","img":"https://raw.githubusercontent.com/aizawauwunun/stardew-ia-web/main/npc_fizz.png"},
    "evelyn": {"nombre":"Evelyn","desc":"La abuela del pueblo, ama las flores","img":"https://raw.githubusercontent.com/aizawauwunun/stardew-ia-web/main/npc_evelyn.png"},
    "george": {"nombre":"George","desc":"Abuelo cascarrabias pero de buen corazón","img":"https://raw.githubusercontent.com/aizawauwunun/stardew-ia-web/main/npc_george.png"},
}

CHICA_AVATAR = "https://raw.githubusercontent.com/aizawauwunun/stardew-ia-web/main/chica%20mandarina.png"
FONDO_WEB = "https://raw.githubusercontent.com/aizawauwunun/stardew-ia-web/main/fondo%20pagina%20web.png"

# ----------------------------
# Funciones DB
# ----------------------------
def db(query,params=(),fetchone=False,fetchall=False):
    conn=sqlite3.connect(DB_PATH)
    cur=conn.cursor()
    cur.execute(query,params)
    if fetchone:
        r=cur.fetchone()
        conn.close()
        return r
    if fetchall:
        r=cur.fetchall()
        conn.close()
        return r
    conn.commit()
    conn.close()

def init_db():
    db("""
    CREATE TABLE IF NOT EXISTS usuarios(
    id TEXT PRIMARY KEY,
    plan TEXT,
    mensajes_dia INTEGER DEFAULT 0,
    mensajes_minuto INTEGER DEFAULT 0,
    ultimo_minuto INTEGER DEFAULT 0,
    premium_hasta INTEGER DEFAULT 0
    )""")
    db("""
    CREATE TABLE IF NOT EXISTS memoria_chat(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT,
    npc TEXT,
    mensaje TEXT,
    respuesta TEXT
    )""")
    db("""
    CREATE TABLE IF NOT EXISTS hijos_custom(
    nombre TEXT PRIMARY KEY,
    personalidad TEXT
    )""")
    # Insertar personalidades si no existen
    for npc in NPCS:
        db("INSERT OR IGNORE INTO hijos_custom(nombre,personalidad) VALUES (?,?)",
           (NPCS[npc]["nombre"], NPCS[npc]["desc"]))
    db("""INSERT OR IGNORE INTO usuarios(id,plan) VALUES("Alexia","owner")""")

# ----------------------------
# Premium y limites
# ----------------------------
def revisar_premium(user):
    data=db("SELECT plan,premium_hasta FROM usuarios WHERE id=?",(user,),fetchone=True)
    if not data: return
    plan,exp=data
    if plan=="premium" and time.time()>exp:
        db("UPDATE usuarios SET plan='free' WHERE id=?",(user,))

def verificar_limite(user):
    data=db("SELECT plan,mensajes_dia,mensajes_minuto,ultimo_minuto FROM usuarios WHERE id=?",(user,),fetchone=True)
    if not data: return True
    plan,md,mm,ultimo=data
    if plan in ["premium","owner"]: return True
    ahora=int(time.time())
    if ahora-ultimo>60:
        db("UPDATE usuarios SET mensajes_minuto=0,ultimo_minuto=? WHERE id=?",(ahora,user))
        mm=0
    if mm>=15 or md>=800: return False
    db("UPDATE usuarios SET mensajes_dia=mensajes_dia+1,mensajes_minuto=mensajes_minuto+1 WHERE id=?",(user,))
    return True

def activar_premium(user):
    dias30=30*24*60*60
    db("UPDATE usuarios SET plan='premium',premium_hasta=? WHERE id=?",(int(time.time())+dias30,user))

# ----------------------------
# Rutas Flask
# ----------------------------
@app.route("/")
def home():
    if "user" not in session: session["user"]="Alexia"
    user=session["user"]
    botones=""
    for npc in NPCS:
        botones+=f"<a href='/chat/{npc}'>{NPCS[npc]['nombre']}</a><br>"
    return f"""
    <html>
    <head>
        <title>Stardew AI</title>
        <style>
            body {{
                background-image: url('{FONDO_WEB}');
                background-size: cover;
                color: white;
                font-family: sans-serif;
                text-align:center;
            }}
            a {{ color: #FFD700; text-decoration: none; font-size: 18px; }}
            h1 {{ color: #00FFAA; }}
        </style>
    </head>
    <body>
        <img src="{CHICA_AVATAR}" width="150"><br>
        <h1>Stardew AI</h1>
        Usuario: {user}<br><br>
        {botones}<br>
        <a href='/premium'>Comprar premium</a>
    </body>
    </html>
    """

@app.route("/chat/<npc>",methods=["GET","POST"])
def chat(npc):
    user=session["user"]
    revisar_premium(user)
    respuesta=""
    if request.method=="POST":
        msg=request