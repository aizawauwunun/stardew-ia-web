import sqlite3
import os
from flask import Flask, request, render_template_string, session, redirect, url_for
from cerebro_ia import generar_respuesta_stardew

# 1. RUTA DE LA BASE DE DATOS (AJUSTADA PARA RENDER)
# En Render no usamos C:\Users..., usamos una ruta relativa para que funcione en Linux
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
# Usamos una clave secreta segura desde las variables de entorno de Render
app.secret_key = os.environ.get("SECRET_KEY", "stardew_v_77_security_fallback")

# --- CONFIGURACIÓN ---
ADMIN_EMAIL = "cuentasoloparajuegos0909@gmail.com"

def raw(link):
    return link.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")

# --- ENLACES DE IMAGEN ---
URL_FONDO = raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/fondo%20pagina%20web.png")
URL_CHICA = raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/chica%20mandarina.png")

# --- 3. GRAN BASE DE DATOS DE HABITANTES COMPLETA ---
HABITANTES = {
    "alex": {"nombre": "Alex", "desc": "Deportista y egocéntrico.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/120px-Alex.png"), "color": "#4287f5"},
    "haley": {"nombre": "Haley", "desc": "Fotógrafa de moda.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/120px-Haley.png"), "color": "#f2a1c8"},
    "harvey": {"nombre": "Harvey", "desc": "Médico miedoso.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/120px-Harvey.png"), "color": "#5c8a5c"},
    "leah": {"nombre": "Leah", "desc": "Artista del bosque.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/120px-Leah.png"), "color": "#91c83f"},
    "sam": {"nombre": "Sam", "desc": "Músico alegre.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/120px-Sam.png"), "color": "#f2c811"},
    "sebastian": {"nombre": "Sebastian", "desc": "Programador introvertido.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/120px-Sebastian.png"), "color": "#7554a3"},
    "abigail": {"nombre": "Abigail", "desc": "Aventurera mística.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/72px-Abigail_.png"), "color": "#8d5da1"},
    "elliott": {"nombre": "Elliott", "desc": "Escritor romántico.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/Elliott.png"), "color": "#a14d3f"},
    "emily": {"nombre": "Emily", "desc": "Espiritual y costurera.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/Emily.png"), "color": "#3fa1f2"},
    "shane": {"nombre": "Shane", "desc": "Rudo que ama gallinas.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/Shane.png"), "color": "#5c6fb1"},
    "maru": {"nombre": "Maru", "desc": "Científica inventora.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/Maru.png"), "color": "#a13f63"},
    "penny": {"nombre": "Penny", "desc": "Tímida y educada.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/20160222182301!Penny.png"), "color": "#f2a13f"},
    "marnie": {"nombre": "Marnie", "desc": "Ganadera amable.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/20160222182224!Marnie.png"), "color": "#f28c8c"},
    "clint": {"nombre": "Clint", "desc": "Herrero solitario.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/20170225194818!Clint_Happy.png"), "color": "#888"},
    "caroline": {"nombre": "Caroline", "desc": "Ama su té.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/Caroline_Happy.png"), "color": "#6bc08a"},
    "demetrius": {"nombre": "Demetrius", "desc": "Científico formal.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/Demetrius.png"), "color": "#714a36"},
    "evelyn": {"nombre": "Evelyn", "desc": "Abuela cariñosa.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/Evelyn.png"), "color": "#eec"},
    "george": {"nombre": "George", "desc": "Abuelo gruñón.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/George.png"), "color": "#888"},
    "gus": {"nombre": "Gus", "desc": "Cocinero del salón.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/Gus_Happy.png"), "color": "#d87e50"},
    "jas": {"nombre": "Jas", "desc": "Niña tímida.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/Jas.png"), "color": "#d8a0d8"},
    "jodi": {"nombre": "Jodi", "desc": "Madre dedicada.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/Jodi_Happy.png"), "color": "#4facfe"},
    "kent": {"nombre": "Kent", "desc": "Ex-militar serio.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/Kent_Happy.png"), "color": "#4a5a2a"},
    "leo": {"nombre": "Leo", "desc": "Niño de la selva.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/Leo_Happy.png"), "color": "#b0a060"},
    "lewis": {"nombre": "Lewis", "desc": "Alcalde del pueblo.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/Lewis_Happy.png"), "color": "#633524"},
    "linus": {"nombre": "Linus", "desc": "Ermitaño sabio.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/Linus_Happy.png"), "color": "#f2a13f"},
    "pam": {"nombre": "Pam", "desc": "Conductora de bus.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/Pam.png"), "color": "#9b59b6"},
    "pierre": {"nombre": "Pierre", "desc": "Tendero ambicioso.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/Pierre_Happy.png"), "color": "#d35400"},
    "robin": {"nombre": "Robin", "desc": "Carpintera alegre.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/Robin_Happy.png"), "color": "#e67e22"},
    "sandy": {"nombre": "Sandy", "desc": "Dueña del Oasis.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/Sandy.png"), "color": "#e91e63"},
    "vincent": {"nombre": "Vincent", "desc": "Niño juguetón.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/Vincent.png"), "color": "#e74c3c"},
    "willy": {"nombre": "Willy", "desc": "Pescador experto.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/Willy_Happy.png"), "color": "#2980b9"},
    "marlon": {"nombre": "Marlon", "desc": "Cazador de monstruos.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/Marlon.png"), "color": "#27ae60"},
    "mr_qi": {"nombre": "Mr. Qi", "desc": "Misterioso y poderoso.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/Mr._Qi.png"), "color": "#2c3e50"}
}

# --- ESTILOS ---
ESTILOS = f'''
<style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; image-rendering: pixelated; }}
    body {{
        height: 100vh; display: flex; justify-content: center; align-items: center;
        background: #4facfe url('{URL_FONDO}') no-repeat center center fixed;
        background-size: cover; font-family: 'Courier New', monospace;
    }}
    .dialog-box {{
        background: #e5b061; border: 6px solid #633524;
        padding: 20px; width: 600px; text-align: center;
        box-shadow: 10px 10px 0 rgba(0,0,0,0.3);
        max-height: 90vh; overflow-y: auto;
    }}
    .btn {{
        display: block; width: 100%; padding: 10px; margin: 5px 0;
        background: #fff3d6; border: 4px solid #633524;
        color: #3c2015; font-weight: bold; text-decoration: none; cursor: pointer; text-transform: uppercase;
    }}
    input {{ width: 100%; padding: 10px; margin-bottom: 10px; border: 3px solid #633524; }}
</style>
'''

@app.route('/nuevo_hijo', methods=['GET', 'POST'])
def nuevo_hijo():
    if 'user' not in session: return redirect(url_for('login'))
    if request.method == 'POST':
        nombre = request.form['nombre']
        personalidad = request.form['personalidad']
        ejecutar_consulta("INSERT INTO hijos_custom (usuario, nombre, personalidad) VALUES (?, ?, ?)", 
                          (session['user'], nombre, personalidad))
        with open('datos.txt', 'a', encoding='utf-8') as f:
            f.write(f"\n{nombre} ({personalidad}): ¡Hola! Acabo de llegar a la granja.\n")
            f.write(f"{nombre} ({personalidad}): Soy una persona {personalidad}.\n")
        return redirect(url_for('perfiles'))
    return render_template_string(f'''
        {ESTILOS}
        <div class="dialog-box">
            <h2>Nueva llegada a la granja</h2>
            <form method="POST">
                <input name="nombre" placeholder="Nombre del niño/a" required>
                <textarea name="personalidad" placeholder="Ej: Es valiente y le gusta explorar" style="width:100%; height:120px; border:4px solid #633524; background:#fff3d6; padding:10px; margin-bottom:10px;" required></textarea>
                <button type="submit" class="btn" style="background:#bdecb6;">Confirmar Nacimiento</button>
            </form>
            <a href="/perfiles">Cancelar</a>
        </div>
    ''')

@app.route('/')
def home():
    if 'user' not in session: return redirect(url_for('login'))
    boton_admin = '<a href="/admin_panel" class="btn" style="background:#ffd700;">⚙️ Panel de Alcalde</a>' if session.get('plan') == 'admin' else ""
    return render_template_string(f'''
        {ESTILOS}
        <div class="dialog-box">
            <img src="{URL_CHICA}" width="80">
            <h1>Stardew IA</h1>
            <p>Hola, {session["user"]}</p>
            <a href="/perfiles" class="btn">Hablar con NPCs</a>
            {boton_admin}
            <a href="/logout" style="color:#633524; display:block; margin-top:10px;">Cerrar Sesión</a>
        </div>
    ''')

@app.route('/perfiles')
def perfiles():
    if 'user' not in session: return redirect(url_for('login'))
    botones_vecinos = "".join([f'<a href="/npc/{k}" class="btn" style="border-left:10px solid {v["color"]};">{v["nombre"]}</a>' for k,v in HABITANTES.items()])
    hijos = ejecutar_consulta("SELECT nombre FROM hijos_custom WHERE usuario = ?", (session['user'],), fetchall=True)
    botones_hijos = "".join([f'<a href="/chat/{h[0]}" class="btn" style="border-left:10px solid #ffcc00; background:#fff3d6;">👶 {h[0]}</a>' for h in hijos])
    return render_template_string(f'''
        {ESTILOS}
        <div class="dialog-box">
            <h2>Vecinos del Pueblo</h2>
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:5px;">{botones_vecinos}</div>
            {"<h2 style='margin-top:20px;'>Tus Hijos</h2>" if hijos else ""}
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:5px;">{botones_hijos}</div>
            <a href="/nuevo_hijo" class="btn" style="background:#bdecb6; margin-top:15px;">+ Registrar Hijo/a</a>
            <a href="/" class="btn" style="margin-top:10px;">Volver al Inicio</a>
        </div>
    ''')

@app.route('/npc/<name>')
def npc(name):
    char = HABITANTES.get(name.lower())
    if not char: return redirect(url_for('perfiles'))
    return render_template_string(f'''
        {ESTILOS}
        <div class="dialog-box">
            <div style="background:#1a1a1a; padding:15px; border:4px solid {char["color"]};">
                <img src="{char["img"]}" width="80">
                <h2 style="color:{char["color"]}">{char["nombre"]}</h2>
                <p style="color:#00ff00; font-size:0.7em;">{char["desc"]}</p>
            </div>
            <a href="/chat/{name}" class="btn">Enviar Mensaje</a>
            <a href="/perfiles" class="btn">Atrás</a>
        </div>
    ''')

@app.route('/chat/<name>', methods=['GET', 'POST'])
def chat(name):
    if 'user' not in session: return redirect(url_for('login'))
    char = HABITANTES.get(name.lower())
    if not char:
        hijo = ejecutar_consulta("SELECT nombre FROM hijos_custom WHERE nombre = ?", (name,), fetchone=True)
        if hijo:
            char = {"nombre": hijo[0], "color": "#ffcc00"}
        else:
            return redirect(url_for('perfiles'))
    respuesta = ""
    user_data = ejecutar_consulta("SELECT plan, mensajes_hoy FROM usuarios WHERE id = ?", (session['user'],), fetchone=True)
    if not user_data: return redirect(url_for('login'))
    plan, mensajes_hoy = user_data[0], user_data[1]
    limite = 10 if plan == "free" else 9999
    bloqueado = mensajes_hoy >= limite
    if request.method == 'POST' and not bloqueado:
        user_msg = request.form.get('msg')
        respuesta = generar_respuesta_stardew(user_msg, name)
        ejecutar_consulta("INSERT INTO memoria_chat (usuario, npc, mensaje, respuesta_ia) VALUES (?, ?, ?, ?)", (session['user'], name, user_msg, respuesta))
        ejecutar_consulta("UPDATE usuarios SET mensajes_hoy = mensajes_hoy + 1 WHERE id = ?", (session['user'],))
    return render_template_string(f'''
        {ESTILOS}
        <div class="dialog-box">
            <h3 style="color:{char['color']}">{char['nombre']}</h3>
            <p style="font-size:0.7em;">Mensajes hoy: {mensajes_hoy}/{limite if limite < 9000 else "∞"}</p>
            <div style="background:#fff3d6; padding:15px; margin:15px 0; border:2px solid #633524; text-align:left;">
                {respuesta if respuesta else "*(Te mira esperando...)*"}
            </div>
            {"<p style='color:red;'>¡Has agotado tus mensajes diarios!</p>" if bloqueado else 
            '<form method="POST"><input name="msg" placeholder="Dile algo..." required><button type="submit" class="btn">Enviar</button></form>'}
            <a href="/perfiles">Atrás</a>
        </div>
    ''')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

def inicializar_tablas():
    ejecutar_consulta('''CREATE TABLE IF NOT EXISTS usuarios (id TEXT PRIMARY KEY, password_hash TEXT, plan TEXT, mensajes_hoy INTEGER DEFAULT 0)''')
    ejecutar_consulta('''CREATE TABLE IF NOT EXISTS memoria_chat (id INTEGER PRIMARY KEY AUTOINCREMENT, usuario TEXT, npc TEXT, mensaje TEXT, respuesta_ia TEXT, fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    ejecutar_consulta('''CREATE TABLE IF NOT EXISTS hijos_custom (id INTEGER PRIMARY KEY AUTOINCREMENT, usuario TEXT, nombre TEXT, personalidad TEXT, color TEXT DEFAULT '#ffcc00')''')

@app.route('/admin_panel')
def admin_panel():
    if session.get('plan') != 'admin': return "Acceso Denegado", 403
    usuarios = ejecutar_consulta("SELECT id, plan, mensajes_hoy FROM usuarios", fetchall=True)
    chats = ejecutar_consulta("SELECT usuario, npc, mensaje, respuesta_ia, fecha FROM memoria_chat ORDER BY fecha DESC LIMIT 50", fetchall=True)
    return render_template_string(f'''
        {ESTILOS}
        <div class="dialog-box" style="width: 800px;">
            <h2>Panel del Alcalde</h2>
            {"".join([f"<p>{u[0]} | {u[1]}</p>" for u in usuarios])}
            <a href="/" class="btn">Volver</a>
        </div>
    ''')

# --- INICIO DE LA APP (ESTO ES LO MÁS IMPORTANTE PARA RENDER) ---
if __name__ == '__main__':
    inicializar_tablas()
    # Render usa la variable de entorno PORT
    puerto = int(os.environ.get("PORT", 5000))
    # Escuchamos en 0.0.0.0 para que sea accesible públicamente
    app.run(host='0.0.0.0', port=puerto)
