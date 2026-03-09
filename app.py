from flask import Flask, request, jsonify, render_template_string
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# --- 1. CONFIGURACIÓN ---
RUTA_BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(RUTA_BASE, "stardew_saas.db")

PERSONAJES_RPG = {
    "Alex": "Deportista y egocéntrico.", "Elliott": "Escritor romántico.", "Harvey": "Médico miedoso.",
    "Sam": "Músico alegre.", "Sebastian": "Programador introvertido.", "Shane": "Rudo que ama gallinas.",
    "Abigail": "Aventurera mística.", "Emily": "Espiritual y costurera.", "Haley": "Fotógrafa de moda.",
    "Leah": "Artista del bosque.", "Maru": "Científica inventora.", "Penny": "Tímida y educada.",
    "Robin": "Carpintera alegre.", "Willy": "Pescador experto."
}

# --- 2. DISEÑO MANDARINA GARANTIZADO (PIXELADO) ---
DISENO_MANTENIMIENTO = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mandarina Valley AI</title>
    <style>
        body {
            margin: 0; padding: 0;
            background: linear-gradient(to bottom, #ffd18a 0%, #ff8f29 100%);
            font-family: 'Courier New', Courier, monospace;
            display: flex; justify-content: center; align-items: center;
            height: 100vh; overflow: hidden; image-rendering: pixelated;
        }
        .mandarin-world { position: relative; width: 100%; height: 100%; }
        
        .mountains {
            position: absolute; bottom: 0; width: 100%; height: 350px;
            background: #e67a00; /* Naranja tierra para el valle */
            clip-path: polygon(0% 100%, 20% 50%, 45% 75%, 70% 40%, 100% 100%);
            z-index: 1; border-top: 5px solid #ff9933;
        }
        
        .mandarin-trees {
            position: absolute; bottom: 150px; left: 0; width: 100%; height: 100px;
            background-image: radial-gradient(circle, #ffa500 15%, transparent 16%), radial-gradient(circle, #55aa33 45%, transparent 46%);
            background-size: 60px 60px; z-index: 2;
        }
        
        .flower-field {
            position: absolute; bottom: 0; left: 0; width: 100%; height: 120px;
            background-image: radial-gradient(circle, #ff55cc 10%, transparent 11%), radial-gradient(circle, #ffffff 10%, transparent 11%), radial-gradient(circle, #aa33ff 10%, transparent 11%);
            background-size: 20px 20px; background-color: #aaee44; z-index: 3;
        }
        
        .winged-mandarin {
            position: absolute; width: 25px; height: 25px;
            background: radial-gradient(circle, #ff8800 60%, #cc6600 61%);
            border-radius: 50%; z-index: 5;
            animation: fly 6s infinite ease-in-out;
        }
        
        .winged-mandarin::before, .winged-mandarin::after {
            content: ''; position: absolute; width: 15px; height: 10px;
            background: #ffffff; top: 0px; border-radius: 50%;
        }
        .winged-mandarin::before { left: -18px; transform: rotate(-30deg); }
        .winged-mandarin::after { right: -18px; transform: rotate(30deg); }
        
        @keyframes fly {
            0% { left: 10%; top: 40%; } 25% { left: 30%; top: 30%; }
            50% { left: 50%; top: 45%; } 75% { left: 70%; top: 35%; } 100% { left: 10%; top: 40%; }
        }
        
        .dialog-container { text-align: center; z-index: 10; margin-top: -50px; position: relative; }
        
        .chica-mandarina-icon {
            width: 120px; height: 120px; margin-bottom: 20px;
            border-radius: 50%; border: 6px solid #ff8800;
            image-rendering: pixelated; box-shadow: 0 0 15px rgba(255, 136, 0, 0.7);
        }
        
        .dialog-box {
            background: #f5deb3; border: 4px solid #cc6600;
            padding: 20px; width: 380px; box-shadow: 6px 6px 0px rgba(0,0,0,0.2);
            position: relative;
        }
        
        .decor-mandarin {
            position: absolute; width: 30px; height: 30px;
            background: radial-gradient(circle, #ffaa00 60%, transparent 61%);
            border-radius: 50%; z-index: 11;
        }
        .decor-mandarin::before {
            content: ''; position: absolute; width: 15px; height: 15px;
            background: #4ac94a; border-radius: 5px 15px 5px 15px;
            top: -5px; left: 5px;
        }
        
        .decor-top-left { top: -20px; left: -20px; }
        .decor-bottom-right { bottom: -20px; right: -20px; }
        
        p { color: #5c3317; font-weight: bold; margin: 0; font-size: 1.2em; }
        .title { font-size: 0.9em; font-style: italic; color: #8b4513; margin-top: 10px; }
    </style>
</head>
<body>
    <div class="mandarin-world">
        <div class="winged-mandarin" style="animation-delay: 0s;"></div>
        <div class="winged-mandarin" style="animation-delay: 2s; top: 30%; animation-duration: 8s;"></div>
        <div class="winged-mandarin" style="animation-delay: 4s; left: 60%; top: 25%;"></div>
        
        <div class="mountains"></div>
        <div class="mandarin-trees"></div>
        <div class="flower-field"></div>
        
        <div class="dialog-container">
            <img src="https://lh3.googleusercontent.com/pw/AP1GczMVY7p_q8P1K4b5bC6u8S3Y9R8U_U0N0f9mG0v1E2r3T4b5S6u8S3=w1024" class="chica-mandarina-icon" alt="Chica Mandarina">
            <div class="dialog-box">
                <div class="decor-mandarin decor-top-left"></div>
                <div class="decor-mandarin decor-bottom-right"></div>
                <p>¡Hola! Soy la Chica Mandarina.</p>
                <p>El equipo está cultivando el Valle, ¡vuelve pronto!</p>
                <p class="title">[ Aviso de la Chica Mandarina ]</p>
            </div>
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
