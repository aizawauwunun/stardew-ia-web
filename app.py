from flask import Flask, request, jsonify, render_template_string
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# --- 1. CONFIGURACIÓN ---
RUTA_BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(RUTA_BASE, "stardew_saas.db")

PERSONAJES_RPG = {
    "Alex": "Deportista y egocéntrico.", "Elliott": "Escritor romántico.", 
    "Harvey": "Médico miedoso.", "Sam": "Músico alegre.", 
    "Sebastian": "Programador introvertido.", "Shane": "Rudo que ama gallinas.",
    "Abigail": "Aventurera mística.", "Emily": "Espiritual y costurera.", 
    "Haley": "Fotógrafa de moda.", "Leah": "Artista del bosque.", 
    "Maru": "Científica inventora.", "Penny": "Tímida y educada.",
    "Robin": "Carpintera alegre.", "Willy": "Pescador experto."
}

# --- 2. DISEÑO ---
DISENO_MANTENIMIENTO = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Valley Character AI</title>
    <style>
        body {
            margin: 0; padding: 0;
            background: linear-gradient(to bottom, #4facfe 0%, #00f2fe 100%);
            font-family: 'Courier New', Courier, monospace;
            display: flex; justify-content: center; align-items: center;
            height: 100vh; overflow: hidden;
        }
        .mountains {
            position: absolute; bottom: 0; width: 100%; height: 300px;
            background: #448032;
            clip-path: polygon(0% 100%, 20% 40%, 45% 70%, 70% 30%, 100% 100%);
            z-index: 1;
        }
        .tree {
            position: absolute; bottom: 50px; width: 0; height: 0;
            border-left: 20px solid transparent; border-right: 20px solid transparent;
            border-bottom: 50px solid #1e3f1a; z-index: 2;
        }
        .dialog-container {
            text-align: center; z-index: 10; margin-top: -50px;
        }
        .robin-icon {
            width: 80px; height: 80px; image-rendering: pixelated; margin-bottom: 10px;
        }
        .dialog-box {
            background: #e5b061; border: 4px solid #633524;
            padding: 20px; width: 350px; box-shadow: 6px 6px 0px rgba(0,0,0,0.2);
        }
        p { color: #3c2015; font-weight: bold; margin: 0; font-size: 1.1em; }
    </style>
</head>
<body>
    <div class="mountains"></div>
    <div class="tree" style="left: 20%;"></div>
    <div class="tree" style="right: 25%;"></div>
    <div class="dialog-container">
        <img src="https://stardewvalleywiki.com/mediawiki/images/b/b7/Robin.png" class="robin-icon">
        <div class="dialog-box">
            <p>¡Hola! Soy Robin. El equipo está trabajando en el Valle. ¡Vuelve pronto!</p>
        </div>
    </div>
</body>
</html>
'''

# --- 3. RUTAS ---
@app.before_request
def modo_privado():
    if request.path.startswith('/static'): return None
    return render_template_string(DISENO_MANTENIMIENTO), 503

@app.route('/')
def home():
    return "OK"

# --- 4. ARRANQUE ---
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
