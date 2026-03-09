from flask import Flask, request, jsonify, render_template_string
import sqlite3
import os
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# --- 1. CONFIGURACIÓN DE RUTAS Y BASE DE DATOS ---
# Esto asegura que la base de datos se cree en la carpeta correcta de Render
RUTA_BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(RUTA_BASE, "stardew_saas.db")

PERSONAJES_RPG = {
    "Alex": "Deportista y egocéntrico.", "Elliott": "Escritor romántico.", "Harvey": "Médico miedoso.",
    "Sam": "Músico alegre.", "Sebastian": "Programador introvertido.", "Shane": "Rudo que ama gallinas.",
    "Abigail": "Aventurera mística.", "Emily": "Espiritual y costurera.", "Haley": "Fotógrafa de moda.",
    "Leah": "Artista del bosque.", "Maru": "Científica inventora.", "Penny": "Tímida y educada.",
    "Caroline": "Ama su té.", "Clint": "Herrero solitario.", "Demetrius": "Científico formal.",
    "Evelyn": "Abuela cariñosa.", "George": "Abuelo gruñón.", "Gus": "Cocinero del salón.", 
    "Jas": "Niña tímida.", "Jodi": "Madre dedicada.", "Kent": "Ex-militar serio.", 
    "Leo": "Niño de la selva.", "Lewis": "Alcalde del pueblo.", "Linus": "Ermitaño sabio.", 
    "Marnie": "Ganadera amable.", "Pam": "Conductora de bus.", "Pierre": "Tendero ambicioso.", 
    "Robin": "Carpintera alegre.", "Sandy": "Dueña del Oasis.", "Vincent": "Niño juguetón.", "Willy": "Pescador experto."
}

# --- 2. DISEÑO "AMONONADO" CON MONTAÑAS Y PÁJAROS ---
# Este es el diseño que se verá mientras la página esté en mantenimiento
DISENO_MANTENIMIENTO = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Valley Character AI</title>
    <link href="https://fonts.googleapis.com/css2?family=VT323&display=swap" rel="stylesheet">
    <style>
        body, html { margin: 0; padding: 0; height: 100%; overflow: hidden; font-family: 'VT323', monospace; }
        
        /* CIELO Y FONDO */
        .scene {
            position: relative;
            width: 100%;
            height: 100vh;
            background: linear-gradient(to bottom, #4facfe 0%, #00f2fe 100%);
            z-index: -1;
        }

        /* MONTAÑAS TIPO PIXEL */
        .mountains {
            position: absolute;
            bottom: 0;
            width: 100%;
            height: 45vh;
            background-color: #3e2712;
            clip-path: polygon(0% 100%, 0% 25%, 10% 45%, 20% 20%, 30% 55%, 40% 15%, 50% 40%, 60% 20%, 70% 60%, 80% 10%, 90% 45%, 100% 25%, 100% 100%);
        }

        /* NUBES ANIMADAS */
        .cloud {
            position: absolute;
            background: white;
            border-radius: 50px;
            opacity: 0.8;
            animation: moveClouds linear infinite;
        }
        .cloud::after, .cloud::before { content: ''; position: absolute; background: white; border-radius: 50px; }
        .cloud1 { width: 100px; height: 40px; top: 15%; animation-duration: 35s; }
        .cloud1::after { width: 50px; height: 50px; top: -25px; left: 15px; }
        .cloud2 { width: 140px; height: 50px; top: 30%; animation-duration: 50s; animation-delay: -10s; }
        .cloud2::after { width: 70px; height: 70px; top: -35px; left: 30px; }

        @keyframes moveClouds {
            from { left: -200px; }
            to { left: 100%; }
        }

        /* PÁJAROS VOLANDO */
        .birds {
            position: absolute;
            width: 60px;
            animation: fly 25s linear infinite;
        }
        @keyframes fly {
            from { left: 110%; top: 20%; }
            to { left: -100px; top: 25%; }
        }

        /* CUADRO DE DIÁLOGO ESTILO STARDEW */
        .main-container {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            z-index: 10;
            width: 90%;
            max-width: 500px;
        }
        .stardew-box {
            background-color: #fcead3;
            border: 6px solid #5d3a1a;
            outline: 4px solid #b26c39;
            box-shadow: 8px 8px 0px rgba(0,0,0,0.3);
            padding: 35px;
            text-align: center;
            position: relative;
        }
        .stardew-box::before {
            content: ""; position: absolute; top: 4px; left: 4px; right: 4px; bottom: 4px;
            border: 2px solid #e7c294; pointer-events: none;
        }
        h1 { color: #5d3a1a; font-size: 3.5rem; margin: 0; text-shadow: 3px 3px #e7c294; text-transform: uppercase; }
        p { color: #3e2712; font-size: 1.8rem; line-height: 1.1; margin: 15px 0; }
        .status-tag {
            background: #b26c39; color: #fcead3; border: 3px solid #5d3a1a;
            padding: 8px 15px; font-size: 1.4rem; display: inline-block; margin-top: 15px;
        }
    </style>
</head>
<body>
    <div class="scene">
        <div class="cloud cloud1"></div>
        <div class="cloud cloud2"></div>
        <svg class="birds" viewBox="0 0 100 60">
            <path d="M10,30 Q40,10 50,30 Q60,10 90,30" stroke="#3e2712" stroke-width="6" fill="none"/>
        </svg>
        <div class="mountains"></div>
    </div>

    <div class="main-container">
        <div class="stardew-box">
            <img src="https://stardewvalleywiki.com/mediawiki/images/4/45/Junimo.png" width="80" style="margin-bottom:10px;">
            <h1>¡AVISO DE ROBIN!</h1>
            <p>Alexia está sincronizando los mods con la IA.</p>
            <div class="status-tag">Sincronizando conexión local...</div>
            <p style="font-size: 1rem; opacity: 0.7; margin-top: 20px;">Página privada hasta nuevo aviso.</p>
        </div>
    </div>
</body>
</html>
'''

# --- 3. RUTAS Y LÓGICA DEL SISTEMA ---

@app.before_request
def modo_privado():
    # Mientras estemos "amononando", todas las rutas mostrarán el aviso de Robin
    if request.path.startswith('/static'): return None
    # Si quieres entrar al chat real, comenta la línea de abajo después
    return render_template_string(DISENO_MANTENIMIENTO), 503

@app.route('/')
def home():
    return "Stardew Chat SaaS Activo" # Esto no se verá mientras esté el modo_privado arriba

@app.route('/registro', methods=['POST'])
def registro():
    d = request.json
    h = generate_password_hash(d['password'])
    try:
        with sqlite3.connect(DB_PATH) as c:
            c.execute("INSERT INTO usuarios (id, password_hash) VALUES (?,?)", (d['usuario'], h))
        return jsonify({"mensaje": "¡Bienvenido al Valle!"}), 201
    except: return jsonify({"error": "Usuario ya existe"}), 400

@app.route('/login', methods=['POST'])
def login():
    d = request.json
    with sqlite3.connect(DB_PATH) as c:
        u = c.execute("SELECT password_hash, plan, fecha_vencimiento FROM usuarios WHERE id=?", (d['usuario'],)).fetchone()
    if u and check_password_hash(u[0], d['password']):
        plan = u[1]
        if plan == 'premium' and u[2]:
            if datetime.now() > datetime.strptime(u[2], '%Y-%m-%d'):
                with sqlite3.connect(DB_PATH) as c:
                    c.execute("UPDATE usuarios SET plan='free' WHERE id=?", (d['usuario'],))
                plan = 'free'
        return jsonify({"mensaje": "Logueado", "plan": plan}), 200
    return jsonify({"error": "Fallo de login"}), 401

@app.route('/chat', methods=['POST'])
def chat():
    d = request.json
    user, npc, msg = d['user'], d['npc'], d['msg']
    hoy = datetime.now().strftime('%Y-%m-%d')
    with sqlite3.connect(DB_PATH) as c:
        u = c.execute("SELECT mensajes_hoy, plan, ultima_actividad FROM usuarios WHERE id=?", (user,)).fetchone()
        plan = u[1]
        m_hoy = u[0] if u[2] == hoy else 0
        if plan == 'free':
            if m_hoy >= 100: return jsonify({"reply": "Límite diario (100) agotado. ¡Pásate a Premium!"})
            un_min = (datetime.now() - timedelta(minutes=1)).strftime('%Y-%m-%d %H:%M:%S')
            if c.execute("SELECT COUNT(*) FROM memoria_chat WHERE usuario=? AND fecha > ?", (user, un_min)).fetchone()[0] >= 15:
                return jsonify({"reply": "¡Demasiado rápido! (Max 15/min)"})
        perfil = PERSONAJES_RPG.get(npc, "Aldeano")
        res = f"({npc}): {msg}... ¡Jeje! Soy {perfil}"
        c.execute("INSERT INTO memoria_chat (usuario, npc, mensaje, respuesta_ia) VALUES (?,?,?,?)", (user, npc, msg, res))
        c.execute("UPDATE usuarios SET mensajes_hoy = ?, ultima_actividad = ? WHERE id=?", (m_hoy + 1, hoy, user))
    return jsonify({"reply": res})

# --- 4. ARREGLO TÉCNICO PARA RENDER ---
if __name__ == '__main__':
    # Esto soluciona el error "No open ports detected"
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
