from flask import Flask, request, jsonify, render_template_string
import sqlite3
import os
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
# Esto busca la carpeta donde esté el archivo automáticamente, sin usar tu nombre
RUTA_BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(RUTA_BASE, "stardew_saas.db")
# --- 1. DICCIONARIO DE PERSONAJES (Filtrado) ---
PERSONAJES_RPG = {
    # Solteros
    "Alex": "Deportista y egocéntrico.", "Elliott": "Escritor romántico.", "Harvey": "Médico miedoso.",
    "Sam": "Músico alegre.", "Sebastian": "Programador introvertido.", "Shane": "Rudo que ama gallinas.",
    # Solteras
    "Abigail": "Aventurera mística.", "Emily": "Espiritual y costurera.", "Haley": "Fotógrafa de moda.",
    "Leah": "Artista del bosque.", "Maru": "Científica inventora.", "Penny": "Tímida y educada.",
    # No disponibles para matrimonio (Filtrados: sin Krobus, Rasmodius ni Enano)
    "Caroline": "Ama su té.", "Clint": "Herrero solitario.", "Demetrius": "Científico formal.",
    "Evelyn": "Abuela cariñosa.", "George": "Abuelo gruñón.", "Gus": "Cocinero del salón.", 
    "Jas": "Niña tímida.", "Jodi": "Madre dedicada.", "Kent": "Ex-militar serio.", 
    "Leo": "Niño de la selva.", "Lewis": "Alcalde del pueblo.", "Linus": "Ermitaño sabio.", 
    "Marnie": "Ganadera amable.", "Pam": "Conductora de bus.", "Pierre": "Tendero ambicioso.", 
    "Robin": "Carpintera alegre.", "Sandy": "Dueña del Oasis.", "Vincent": "Niño juguetón.", "Willy": "Pescador experto."
}

# --- 2. BLOQUE DE PRIVACIDAD / MANTENIMIENTO ---
@app.before_request
def modo_privado():
    if request.path.startswith('/static'): return None
    return '''
    <body style="background:#2e7d32; color:white; font-family:'Courier New', monospace; text-align:center; padding:100px;">
        <img src="https://stardewvalleywiki.com/mediawiki/images/4/45/Junimo.png" width="100">
        <h1>🚜 EL VALLE ESTÁ EN CONSTRUCCIÓN</h1>
        <p>Alexia está sincronizando los mods de SMAPI con la Inteligencia Artificial.</p>
        <div style="border: 2px dashed #fdd835; display:inline-block; padding: 20px; margin-top:20px;">
            ESTADO: <b>Configurando conexión local con el juego...</b>
        </div>
        <p style="margin-top:50px; font-size: 0.8em; opacity: 0.7;">Página privada hasta nuevo aviso.</p>
    </body>
    ''', 503

# --- 3. INTERFAZ WEB ---
HTML_WEB = '''
<!DOCTYPE html>
<html>
<head>
    <title>Stardew Chat SaaS</title>
    <style>
        body { background: #2e7d32; font-family: 'Courier New', monospace; color: white; display: flex; flex-direction: column; align-items: center; }
        .box { background: #8d6e63; border: 4px solid #fdd835; width: 450px; padding: 20px; border-radius: 10px; margin-top: 20px; }
        #chat-section { display: none; background: #f5f5dc; color: #5d4037; padding: 15px; }
        #logs { height: 300px; overflow-y: auto; background: white; padding: 10px; border: 2px solid #8d6e63; margin-bottom: 10px; }
        .premium-tag { background: #fdd835; color: #5d4037; padding: 2px 5px; font-weight: bold; border-radius: 3px; }
        input, select { width: 95%; padding: 8px; margin-bottom: 10px; }
        button { width: 100%; padding: 10px; background: #4caf50; color: white; border: none; cursor: pointer; font-weight: bold; }
    </style>
</head>
<body>
    <div id="login-section" class="box">
        <h2 style="text-align:center">LOGIN VALLE</h2>
        <input type="text" id="u" placeholder="Usuario">
        <input type="password" id="p" placeholder="Contraseña">
        <button onclick="auth('login')">ENTRAR</button>
        <button onclick="auth('registro')" style="background:#795548; margin-top:10px;">REGISTRARSE</button>
    </div>

    <div id="chat-section" class="box">
        <div style="margin-bottom:10px;"><b>Usuario:</b> <span id="userName"></span> <span id="userPlan" class="premium-tag"></span></div>
        <select id="npc">
            <optgroup label="Candidatos (Solteros)">
                <option value="Alex">Alex</option><option value="Elliott">Elliott</option><option value="Harvey">Harvey</option>
                <option value="Sam">Sam</option><option value="Sebastian">Sebastian</option><option value="Shane">Shane</option>
            </optgroup>
            <optgroup label="Candidatas (Solteras)">
                <option value="Abigail">Abigail</option><option value="Emily">Emily</option><option value="Haley">Haley</option>
                <option value="Leah">Leah</option><option value="Maru">Maru</option><option value="Penny">Penny</option>
            </optgroup>
            <optgroup label="Otros Habitantes">
                <option value="Caroline">Caroline</option><option value="Clint">Clint</option><option value="Demetrius">Demetrius</option>
                <option value="Evelyn">Evelyn</option><option value="George">George</option><option value="Gus">Gus</option>
                <option value="Jas">Jas</option><option value="Jodi">Jodi</option><option value="Kent">Kent</option>
                <option value="Leo">Leo</option><option value="Lewis">Lewis</option><option value="Linus">Linus</option>
                <option value="Marnie">Marnie</option><option value="Pam">Pam</option><option value="Pierre">Pierre</option>
                <option value="Robin">Robin</option><option value="Sandy">Sandy</option><option value="Vincent">Vincent</option>
                <option value="Willy">Willy</option>
            </optgroup>
        </select>
        <div id="logs"></div>
        <input type="text" id="m" placeholder="Escribe un mensaje...">
        <button onclick="send()">ENVIAR MENSAJE</button>
    </div>

    <script>
        let curUser = "";
        async function auth(t) {
            const res = await fetch('/'+t, {
                method:'POST', headers:{'Content-Type':'application/json'},
                body: JSON.stringify({usuario: document.getElementById('u').value, password: document.getElementById('p').value})
            });
            const data = await res.json();
            if(res.ok) {
                if(t==='login') {
                    curUser = document.getElementById('u').value;
                    document.getElementById('login-section').style.display='none';
                    document.getElementById('chat-section').style.display='block';
                    document.getElementById('userName').innerText = curUser;
                    document.getElementById('userPlan').innerText = data.plan;
                }
                alert(data.mensaje);
            } else alert(data.error);
        }

        async function send() {
            const m = document.getElementById('m');
            const res = await fetch('/chat', {
                method:'POST', headers:{'Content-Type':'application/json'},
                body: JSON.stringify({msg: m.value, user: curUser, npc: document.getElementById('npc').value})
            });
            const data = await res.json();
            document.getElementById('logs').innerHTML += `<p><b>Tú:</b> ${m.value}</p><p style="color:red"><b>IA:</b> ${data.reply}</p>`;
            m.value = "";
        }
    </script>
</body>
</html>
'''

# --- 4. RUTAS DEL SISTEMA ---
@app.route('/')
def home(): return render_template_string(HTML_WEB)

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

if __name__ == '__main__':
    # Esto hace que la página sea 100% privada para tu PC
    app.run(host='127.0.0.1', port=5000)