from flask import Flask, request, render_template_string, session, redirect, url_for
import os

app = Flask(__name__)
# Llave de seguridad para las sesiones
app.secret_key = os.environ.get("SECRET_KEY", "stardew_v_77_security")

# --- 1. CONFIGURACIÓN DE NEGOCIO ---
ADMIN_EMAIL = "cuentasoloparajuegos0909@gmail.com"
MI_PAYPAL = "cuentasoloparajuegos0909@gmail.com"
PRECIO_CLP = "4500"

# Función para que los links de GitHub funcionen como imágenes reales
def raw(link):
    return link.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")

# Base de datos de usuarios (Solo tú eres admin por defecto)
USUARIOS = {
    "admin": {
        "password": "220506", 
        "email": ADMIN_EMAIL, 
        "rango": "admin", 
        "mensajes_usados": 0
    }
}

# --- 2. ENLACES DE IMAGEN ---
URL_FONDO = raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/fondo%20pagina%20web.png")
URL_CHICA = raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/chica%20mandarina.png")

# --- 3. GRAN BASE DE DATOS DE HABITANTES (CON TODOS TUS LINKS) ---
HABITANTES = {
    # SOLTEROS (Con Romance)
    "alex": {"nombre": "Alex", "desc": "Deportista y egocéntrico.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/120px-Alex.png"), "color": "#4287f5", "romance": True},
    "haley": {"nombre": "Haley", "desc": "Fotógrafa de moda.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/120px-Haley.png"), "color": "#f2a1c8", "romance": True},
    "harvey": {"nombre": "Harvey", "desc": "Médico miedoso.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/120px-Harvey.png"), "color": "#5c8a5c", "romance": True},
    "leah": {"nombre": "Leah", "desc": "Artista del bosque.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/120px-Leah.png"), "color": "#91c83f", "romance": True},
    "sam": {"nombre": "Sam", "desc": "Músico alegre.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/120px-Sam.png"), "color": "#f2c811", "romance": True},
    "sebastian": {"nombre": "Sebastian", "desc": "Programador introvertido.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/120px-Sebastian.png"), "color": "#7554a3", "romance": True},
    "abigail": {"nombre": "Abigail", "desc": "Aventurera mística.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/72px-Abigail_.png"), "color": "#8d5da1", "romance": True},
    "elliott": {"nombre": "Elliott", "desc": "Escritor romántico.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/Elliott.png"), "color": "#a14d3f", "romance": True},
    "emily": {"nombre": "Emily", "desc": "Espiritual y costurera.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/Emily.png"), "color": "#3fa1f2", "romance": True},
    "shane": {"nombre": "Shane", "desc": "Rudo que ama gallinas.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/Shane.png"), "color": "#5c6fb1", "romance": True},
    "maru": {"nombre": "Maru", "desc": "Científica inventora.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/Maru.png"), "color": "#a13f63", "romance": True},
    "penny": {"nombre": "Penny", "desc": "Tímida y educada.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/20160222182301!Penny.png"), "color": "#f2a13f", "romance": True},

    # VECINOS Y ESPECIALES (Charla Normal)
    "marnie": {"nombre": "Marnie", "desc": "Ganadera amable.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/20160222182224!Marnie.png"), "color": "#f28c8c", "romance": False},
    "clint": {"nombre": "Clint", "desc": "Herrero solitario.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/20170225194818!Clint_Happy.png"), "color": "#888", "romance": False},
    "caroline": {"nombre": "Caroline", "desc": "Ama su té.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/Caroline_Happy.png"), "color": "#6bc08a", "romance": False},
    "demetrius": {"nombre": "Demetrius", "desc": "Científico formal.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/Demetrius.png"), "color": "#714a36", "romance": False},
    "evelyn": {"nombre": "Evelyn", "desc": "Abuela cariñosa.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/Evelyn.png"), "color": "#eec", "romance": False},
    "george": {"nombre": "George", "desc": "Abuelo gruñón.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/George.png"), "color": "#888", "romance": False},
    "gus": {"nombre": "Gus", "desc": "Cocinero del salón.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/Gus_Happy.png"), "color": "#d87e50", "romance": False},
    "jas": {"nombre": "Jas", "desc": "Niña tímida.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/Jas.png"), "color": "#d8a0d8", "romance": False},
    "jodi": {"nombre": "Jodi", "desc": "Madre dedicada.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/Jodi_Happy.png"), "color": "#4facfe", "romance": False},
    "kent": {"nombre": "Kent", "desc": "Ex-militar serio.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/Kent_Happy.png"), "color": "#4a5a2a", "romance": False},
    "leo": {"nombre": "Leo", "desc": "Niño de la selva.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/Leo_Happy.png"), "color": "#b0a060", "romance": False},
    "lewis": {"nombre": "Lewis", "desc": "Alcalde del pueblo.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/Lewis_Happy.png"), "color": "#633524", "romance": False},
    "linus": {"nombre": "Linus", "desc": "Ermitaño sabio.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/Linus_Happy.png"), "color": "#f2a13f", "romance": False},
    "pam": {"nombre": "Pam", "desc": "Conductora de bus.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/Pam.png"), "color": "#9b59b6", "romance": False},
    "pierre": {"nombre": "Pierre", "desc": "Tendero ambicioso.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/Pierre_Happy.png"), "color": "#d35400", "romance": False},
    "robin": {"nombre": "Robin", "desc": "Carpintera alegre.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/Robin_Happy.png"), "color": "#e67e22", "romance": False},
    "sandy": {"nombre": "Sandy", "desc": "Dueña del Oasis.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/Sandy.png"), "color": "#e91e63", "romance": False},
    "vincent": {"nombre": "Vincent", "desc": "Niño juguetón.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/Vincent.png"), "color": "#e74c3c", "romance": False},
    "willy": {"nombre": "Willy", "desc": "Pescador experto.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/Willy_Happy.png"), "color": "#2980b9", "romance": False},
    "marlon": {"nombre": "Marlon", "desc": "Cazador de monstruos.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/Marlon.png"), "color": "#27ae60", "romance": False},
    "mr_qi": {"nombre": "Mr. Qi", "desc": "Misterioso y poderoso.", "img": raw("https://github.com/aizawauwunun/stardew-ia-web/blob/main/Mr._Qi.png"), "color": "#2c3e50", "romance": False}
}

# --- 4. ESTILOS Y MAQUETACIÓN ---
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
        padding: 20px; width: 500px; text-align: center;
        box-shadow: 10px 10px 0 rgba(0,0,0,0.3);
        max-height: 90vh; overflow-y: auto;
    }}
    .btn {{
        display: block; width: 100%; padding: 10px; margin: 5px 0;
        background: #fff3d6; border: 4px solid #633524;
        color: #3c2015; font-weight: bold; text-decoration: none; cursor: pointer; text-transform: uppercase;
    }}
</style>
'''
# --- 5. RUTAS DE SESIÓN ---

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        user = request.form['user']
        email = request.form['email']
        pw = request.form['pw']
        rango = "admin" if email == ADMIN_EMAIL else "free"
        USUARIOS[user] = {
            "password": pw, "email": email, "rango": rango, 
            "mensajes_usados": 0, "inicio_premium": None, "fin_premium": None
        }
        return redirect(url_for('login'))
    
    return render_template_string(f'''
        {ESTILOS}
        <div class="dialog-box">
            <h2>Crear Cuenta</h2>
            <form method="POST">
                <input name="user" placeholder="Nombre de granjero/a" required style="width:100%; margin-bottom:10px; padding:5px;">
                <input name="email" type="email" placeholder="Tu Email" required style="width:100%; margin-bottom:10px; padding:5px;">
                <input name="pw" type="password" placeholder="Crea una clave" required style="width:100%; margin-bottom:10px; padding:5px;">
                <button type="submit" class="btn">Empezar aventura</button>
            </form>
            <a href="/login" style="font-size:0.7em; color:#633524;">¿Ya tienes cuenta? Entra aquí</a>
        </div>
    ''')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['user']
        pw = request.form['pw']
        if user in USUARIOS and USUARIOS[user]['password'] == pw:
            session['user'] = user
            return redirect(url_for('home'))
        else:
            return render_template_string(f'{ESTILOS}<div class="dialog-box"><h2>Error</h2><p>Usuario o clave incorrecta</p><a href="/login" class="btn">Reintentar</a></div>')
            
    return render_template_string(f'''
        {ESTILOS}
        <div class="dialog-box">
            <h2>Entrar al Valle</h2>
            <form method="POST">
                <input name="user" placeholder="Usuario" required style="width:100%; margin-bottom:10px; padding:5px;">
                <input name="pw" type="password" placeholder="Clave" required style="width:100%; margin-bottom:10px; padding:5px;">
                <button type="submit" class="btn">Entrar</button>
            </form>
            <a href="/registro" style="font-size:0.7em; color:#633524;">¿No tienes cuenta? Regístrate</a>
        </div>
    ''')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))
# --- 6. RUTAS DEL JUEGO ---

@app.route('/')
def home():
    if 'user' not in session:
        return render_template_string(f'{ESTILOS}<div class="dialog-box"><img src="{URL_CHICA}" width="100"><h1>Stardew IA</h1><a href="/login" class="btn">Login</a><a href="/registro" class="btn">Registro</a></div>')
    
    u = USUARIOS[session['user']]
    return render_template_string(f'''
        {ESTILOS}
        <div class="dialog-box">
            <div class="status-bar">MODO: {u['rango'].upper()} | USUARIO: {session['user']}</div>
            <img src="{URL_CHICA}" width="80">
            <h1>Panel de Control</h1>
            <a href="/perfiles" class="btn">Hablar con NPCs</a>
            { f'<a href="/suscripcion" class="btn" style="background:#ffd700;">👑 PREMIUM (4.500 CLP)</a>' if u['rango'] == "free" else "" }
            <a href="/logout" style="font-size:0.6em; color:#633524;">Cerrar Sesión</a>
        </div>
    ''')

@app.route('/suscripcion')
def suscripcion():
    return render_template_string(f'''
        {ESTILOS}
        <div class="dialog-box">
            <h2>Membresía Mensual</h2>
            <p style="font-size:0.8em; margin:10px 0;">Mensajes ilimitados por 30 días.</p>
            <form action="https://www.paypal.com/cgi-bin/webscr" method="post">
                <input type="hidden" name="cmd" value="_xclick">
                <input type="hidden" name="business" value="{MI_PAYPAL}">
                <input type="hidden" name="item_name" value="Stardew IA Premium">
                <input type="hidden" name="amount" value="{PRECIO_CLP}">
                <input type="hidden" name="currency_code" value="CLP">
                <input type="submit" class="btn" style="background:#ffd700;" value="PAGAR 4.500 CLP">
            </form>
            <a href="/" style="font-size:0.7em;">Volver</a>
        </div>
    ''')

@app.route('/perfiles')
def perfiles():
    if 'user' not in session: return redirect(url_for('login'))
    botones = "".join([f'<a href="/npc/{k}" class="btn" style="border-left:10px solid {v["color"]};">{v["nombre"]}</a>' for k,v in HABITANTES.items()])
    return render_template_string(f'{ESTILOS}<div class="dialog-box"><h2>Vecinos</h2><div style="display:grid; grid-template-columns: 1fr 1fr; gap:5px;">{botones}</div><a href="/" style="margin-top:10px; display:block; color:#633524;">Volver</a></div>')

@app.route('/npc/<name>')
def npc(name):
    if 'user' not in session: return redirect(url_for('login'))
    char = HABITANTES.get(name.lower())
    u = USUARIOS[session['user']]
    
    if u['rango'] == "admin":
        limite = "∞ (Administradora)"
    elif u['rango'] == "premium":
        limite = "∞ (Premium)"
    else:
        quedan = 200 - u['mensajes_usados']
        limite = f"{quedan} restantes"
    
    return render_template_string(f'''
        {ESTILOS}
        <div class="dialog-box">
            <div style="background:#1a1a1a; padding:15px; border:4px solid {char['color']};">
                <img src="{char['img']}" width="80">
                <h2 style="color:{char['color']};">{char['nombre']}</h2>
                <p style="color:#00ff00; font-size:0.7em;">{char['desc']}</p>
            </div>
            <p style="font-size:0.7em; margin:10px 0;">Tu límite: <b>{limite}</b></p>
            <a href="/chat/{name}" class="btn">Enviar Mensaje</a>
            <a href="/perfiles" style="color:#633524; font-size:0.7em;">Volver</a>
        </div>
    ''')
# --- 7. RUTA DEL CHAT ---

@app.route('/chat/<name>', methods=['GET', 'POST'])
def chat(name):
    if 'user' not in session: return redirect(url_for('login'))
    
    char = HABITANTES.get(name.lower())
    if not char: return redirect(url_for('perfiles'))
    
    u = USUARIOS[session['user']]
    respuesta = ""

    if request.method == 'POST':
        user_msg = request.form.get('msg')
        # Lógica de mensajes: Solo sumamos si no es admin/premium
        if u['rango'] == "free":
            u['mensajes_usados'] += 1
        
        # Respuesta Temporal (Aquí es donde conectarás la API de IA más adelante)
        respuesta = f"Oh, hola {session['user']}. He estado trabajando en la granja y me pillas justo descansando. ¡Es un buen día!"

    return render_template_string(f'''
        {ESTILOS}
        <div class="dialog-box">
            <div style="display:flex; align-items:center; background:#1a1a1a; padding:10px; border:4px solid {char['color']}; margin-bottom:15px;">
                <img src="{char['img']}" width="60" style="margin-right:15px;">
                <h3 style="color:{char['color']};">{char['nombre']}</h3>
            </div>
            
            <div style="background:#fff3d6; border:3px solid #633524; padding:15px; text-align:left; min-height:100px; margin-bottom:15px; font-size:0.9em;">
                {respuesta if respuesta else "*(Te mira esperando a que digas algo...)*"}
            </div>

            <form method="POST">
                <input name="msg" placeholder="Dile algo a {char['nombre']}..." required 
                       style="width:100%; padding:10px; border:3px solid #633524; margin-bottom:10px;">
                <button type="submit" class="btn">Enviar Mensaje</button>
            </form>
            
            <a href="/npc/{name}" style="color:#633524; font-size:0.7em; display:block; margin-top:10px;">Atrás</a>
        </div>
    ''')
if __name__ == '__main__':
    app.run(debug=True)
