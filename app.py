import sqlite3
import os
from flask import Flask, request, render_template_string, session, redirect, url_for
from cerebro_ia import generar_respuesta_stardew

# 1. RUTA AUTOMÁTICA
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "stardew_saas.db")

def ejecutar_consulta(query, params=(), fetchone=False, fetchall=False):
    conn = sqlite3.connect(DB_PATH)
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        if fetchone: return cursor.fetchone()
        if fetchall: return cursor.fetchall()
        conn.commit()
    except Exception as e:
        print(f"Error en la base de datos: {e}")
    finally:
        conn.close()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "stardew_v_77_security_fallback")

def raw(link):
    return link.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")

URL_FONDO = raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/fondo%20pagina%20web.png")
URL_CHICA = raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/chica%20mandarina.png")

HABITANTES = {
    "alex": {"nombre": "Alex", "desc": "Deportista.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/120px-Alex.png"), "color": "#4287f5"},
    "haley": {"nombre": "Haley", "desc": "Fotógrafa.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/120px-Haley.png"), "color": "#f2a1c8"},
    "harvey": {"nombre": "Harvey", "desc": "Médico.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/120px-Harvey.png"), "color": "#5c8a5c"},
    "leah": {"nombre": "Leah", "desc": "Artista.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/120px-Leah.png"), "color": "#91c83f"},
    "sam": {"nombre": "Sam", "desc": "Músico.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/120px-Sam.png"), "color": "#f2c811"},
    "sebastian": {"nombre": "Sebastian", "desc": "Programador.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/120px-Sebastian.png"), "color": "#7554a3"},
    "abigail": {"nombre": "Abigail", "desc": "Aventurera.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/72px-Abigail_.png"), "color": "#8d5da1"},
    "elliott": {"nombre": "Elliott", "desc": "Escritor.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/Elliott.png"), "color": "#a14d3f"},
    "emily": {"nombre": "Emily", "desc": "Espiritual.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/Emily.png"), "color": "#3fa1f2"},
    "shane": {"nombre": "Shane", "desc": "Galinheiro.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/Shane.png"), "color": "#5c6fb1"},
    "maru": {"nombre": "Maru", "desc": "Científica.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/Maru.png"), "color": "#a13f63"},
    "penny": {"nombre": "Penny", "desc": "Tímida.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/20160222182301!Penny.png"), "color": "#f2a13f"},
    "marnie": {"nombre": "Marnie", "desc": "Ganadera.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/20160222182224!Marnie.png"), "color": "#f28c8c"},
    "clint": {"nombre": "Clint", "desc": "Herrero.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/20170225194818!Clint_Happy.png"), "color": "#888"},
    "caroline": {"nombre": "Caroline", "desc": "Té.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/Caroline_Happy.png"), "color": "#6bc08a"},
    "demetrius": {"nombre": "Demetrius", "desc": "Científico.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/Demetrius.png"), "color": "#714a36"},
    "evelyn": {"nombre": "Evelyn", "desc": "Abuela.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/Evelyn.png"), "color": "#eec"},
    "george": {"nombre": "George", "desc": "Abuelo.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/George.png"), "color": "#888"},
    "gus": {"nombre": "Gus", "desc": "Cocinero.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/Gus_Happy.png"), "color": "#d87e50"},
    "jas": {"nombre": "Jas", "desc": "Niña.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/Jas.png"), "color": "#d8a0d8"},
    "jodi": {"nombre": "Jodi", "desc": "Madre.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/Jodi_Happy.png"), "color": "#4facfe"},
    "kent": {"nombre": "Kent", "desc": "Militar.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/Kent_Happy.png"), "color": "#4a5a2a"},
    "leo": {"nombre": "Leo", "desc": "Selva.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/Leo_Happy.png"), "color": "#b0a060"},
    "lewis": {"nombre": "Lewis", "desc": "Alcalde.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/Lewis_Happy.png"), "color": "#633524"},
    "linus": {"nombre": "Linus", "desc": "Ermitaño.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/Linus_Happy.png"), "color": "#f2a13f"},
    "pam": {"nombre": "Pam", "desc": "Bus.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/Pam.png"), "color": "#9b59b6"},
    "pierre": {"nombre": "Pierre", "desc": "Tendero.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/Pierre_Happy.png"), "color": "#d35400"},
    "robin": {"nombre": "Robin", "desc": "Carpintera.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/Robin_Happy.png"), "color": "#e67e22"},
    "sandy": {"nombre": "Sandy", "desc": "Oasis.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/Sandy.png"), "color": "#e91e63"},
    "vincent": {"nombre": "Vincent", "desc": "Niño.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/Vincent.png"), "color": "#e74c3c"},
    "willy": {"nombre": "Willy", "desc": "Pescador.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/Willy_Happy.png"), "color": "#2980b9"},
    "marlon": {"nombre": "Marlon", "desc": "Cazador.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/Marlon.png"), "color": "#27ae60"},
    "mr_qi": {"nombre": "Mr. Qi", "desc": "Misterio.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/Mr._Qi.png"), "color": "#2c3e50"},
    "gunther": {"nombre": "Gunther", "desc": "Museo.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/Gunther.png"), "color": "#2980b9"},
    "morris": {"nombre": "Morris", "desc": "Joja.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/Morris.png"), "color": "#2c3e50"},
    "bouncer": {"nombre": "Gorila", "desc": "Casino.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/Bouncer.png"), "color": "#111"},
    "governor": {"nombre": "Gobernador", "desc": "Banquete.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/Governor.png"), "color": "#714a36"},
    "birdie": {"nombre": "Birdie", "desc": "Costa.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/Birdie.png"), "color": "#d35400"},
    "professor_snail": {"nombre": "Prof. Snail", "desc": "Isla.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/Professor_Snail.png"), "color": "#5c8a5c"},
    "gil": {"nombre": "Gil", "desc": "Gremio.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/Gil.png"), "color": "#888"},
    "fizz": {"nombre": "Fizz", "desc": "Vendedor.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/Fizz.png"), "color": "#4facfe"}
}

ESTILOS = f'''<style> * {{ margin: 0; padding: 0; box-sizing: border-box; image-rendering: pixelated; }} body {{ height: 100vh; display: flex; justify-content: center; align-items: center; background: #4facfe url('{URL_FONDO}') no-repeat center center fixed; background-size: cover; font-family: 'Courier New', monospace; }} .dialog-box {{ background: #e5b061; border: 6px solid #633524; padding: 20px; width: 600px; text-align: center; box-shadow: 10px 10px 0 rgba(0,0,0,0.3); max-height: 90vh; overflow-y: auto; }} .btn {{ display: block; width: 100%; padding: 10px; margin: 5px 0; background: #fff3d6; border: 4px solid #633524; color: #3c2015; font-weight: bold; text-decoration: none; cursor: pointer; text-transform: uppercase; }} input {{ width: 100%; padding: 10px; margin-bottom: 10px; border: 3px solid #633524; }} </style>'''
@app.route('/nuevo_hijo', methods=['GET', 'POST'])
def nuevo_hijo():
    if 'user' not in session: session['user'] = "Alexia"
    if request.method == 'POST':
        nombre = request.form['nombre']
        personalidad = request.form['personalidad']
        ejecutar_consulta("INSERT INTO hijos_custom (usuario, nombre, personalidad) VALUES (?, ?, ?)", 
                          (session['user'], nombre, personalidad))
        return redirect(url_for('perfiles'))
    
    return render_template_string(f'''
        {ESTILOS}
        <div class="dialog-box">
            <h2>Nueva llegada a la granja</h2>
            <form method="POST">
                <input name="nombre" placeholder="Nombre del niño/a" required>
                <textarea name="personalidad" placeholder="Ej: Es valiente y le gusta explorar" 
                          style="width:100%; height:100px; border:4px solid #633524; background:#fff3d6; padding:10px; margin-bottom:10px;" required></textarea>
                <button type="submit" class="btn" style="background:#bdecb6;">Confirmar Nacimiento</button>
            </form>
            <a href="/perfiles">Cancelar</a>
        </div>
    ''')
@app.route('/')
def home():
    if 'user' not in session:
        session['user'], session['plan'] = "Alexia", "admin"
    boton_admin = '<a href="/admin_panel" class="btn" style="background:#ffd700;">⚙️ Panel de Alcalde</a>' if session.get('plan') == 'admin' else ""
    return render_template_string(f'{ESTILOS}<div class="dialog-box"><img src="{URL_CHICA}" width="80"><h1>Stardew IA</h1><p>Hola, {session["user"]}</p><a href="/perfiles" class="btn">Hablar con NPCs</a>{boton_admin}<a href="/logout" style="color:#633524; display:block; margin-top:10px;">Cerrar Sesión</a></div>')

@app.route('/perfiles')
def perfiles():
    botones = "".join([f'<a href="/npc/{k}" class="btn" style="border-left:10px solid {v["color"]};">{v["nombre"]}</a>' for k,v in HABITANTES.items()])
    hijos = ejecutar_consulta("SELECT nombre FROM hijos_custom WHERE usuario = ?", (session.get('user', 'Alexia'),), fetchall=True) or []
    btn_hijos = "".join([f'<a href="/chat/{h[0]}" class="btn" style="border-left:10px solid #ffcc00; background:#fff3d6;">👶 {h[0]}</a>' for h in hijos])
    return render_template_string(f'{ESTILOS}<div class="dialog-box"><h2>Vecinos</h2><div style="display:grid; grid-template-columns: 1fr 1fr; gap:5px;">{botones}</div><h2 style="margin-top:20px;">Hijos</h2><div style="display:grid; grid-template-columns: 1fr 1fr; gap:5px;">{btn_hijos}</div><a href="/nuevo_hijo" class="btn" style="background:#bdecb6; margin-top:15px;">+ Registrar Hijo/a</a><a href="/" class="btn">Volver</a></div>')

@app.route('/npc/<name>')
def npc(name):
    char = HABITANTES.get(name.lower())
    if not char: return redirect(url_for('perfiles'))
    return render_template_string(f'{ESTILOS}<div class="dialog-box"><div style="background:#1a1a1a; padding:15px; border:4px solid {char["color"]};"><img src="{char["img"]}" width="80"><h2 style="color:{char["color"]}">{char["nombre"]}</h2><p style="color:#00ff00; font-size:0.7em;">{char["desc"]}</p></div><a href="/chat/{name}" class="btn">Enviar Mensaje</a><a href="/perfiles" class="btn">Atrás</a></div>')

@app.route('/chat/<name>', methods=['GET', 'POST'])
def chat(name):
    char = HABITANTES.get(name.lower()) or {"nombre": name, "color": "#ffcc00"}
    res = ""
    if request.method == 'POST':
        msg = request.form.get('msg')
        res = generar_respuesta_stardew(msg, name)
        ejecutar_consulta("INSERT INTO memoria_chat (usuario, npc, mensaje, respuesta_ia) VALUES (?, ?, ?, ?)", (session.get('user', 'Alexia'), name, msg, res))
    return render_template_string(f'{ESTILOS}<div class="dialog-box"><h3 style="color:{char.get("color")}">{char.get("nombre")}</h3><div style="background:#fff3d6; padding:15px; margin:15px 0; border:2px solid #633524; text-align:left;">{res if res else "*(Esperando...)*"}</div><form method="POST"><input name="msg" placeholder="Dile algo..." required><button type="submit" class="btn">Enviar</button></form><a href="/perfiles">Atrás</a></div>')

@app.route('/admin_panel')
def admin_panel():
    u = ejecutar_consulta("SELECT id, plan FROM usuarios", fetchall=True) or []
    c = ejecutar_consulta("SELECT usuario, npc, mensaje FROM memoria_chat ORDER BY fecha DESC LIMIT 10", fetchall=True) or []
    list_u = "".join([f"<p>👤 {x[0]} - {x[1]}</p>" for x in u])
    list_c = "".join([f"<p style='font-size:0.8em;'>{x[0]} a {x[1]}: {x[2][:20]}...</p>" for x in c])
    return render_template_string(f'{ESTILOS}<div class="dialog-box"><h2>Panel Alcalde</h2><div style="text-align:left; background:#fff3d6; padding:10px; border:2px solid #633524;"><h3>Usuarios</h3>{list_u}<h3>Mensajes</h3>{list_c}</div><a href="/" class="btn">Volver</a></div>')

def inicializar_tablas():
    ejecutar_consulta("CREATE TABLE IF NOT EXISTS usuarios (id TEXT PRIMARY KEY, plan TEXT)")
    ejecutar_consulta("CREATE TABLE IF NOT EXISTS memoria_chat (id INTEGER PRIMARY KEY AUTOINCREMENT, usuario TEXT, npc TEXT, mensaje TEXT, respuesta_ia TEXT, fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
    ejecutar_consulta("CREATE TABLE IF NOT EXISTS hijos_custom (id INTEGER PRIMARY KEY AUTOINCREMENT, usuario TEXT, nombre TEXT, personalidad TEXT)")
    ejecutar_consulta("INSERT OR IGNORE INTO usuarios (id, plan) VALUES (?, ?)", ("Alexia", "admin"))

if __name__ == '__main__':
    inicializar_tablas()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)), debug=True)
