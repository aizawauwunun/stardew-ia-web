from flask import Flask, request, jsonify, render_template_string
import sqlite3
import os
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# --- 1. CONFIGURACIÓN DE RUTAS Y BASE DE DATOS ---
RUTA_BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(RUTA_BASE, "stardew_saas.db")

# Aquí están todos los habitantes del Valle con sus personalidades
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

# --- 2. DISEÑO TOTALMENTE PIXELADO - MODO MANDARINA ---
DISENO_MANTENIMIENTO = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Valley Character AI - Modo Mandarina</title>
    <link href="https://fonts.googleapis.com/css2?family=VT323&display=swap" rel="stylesheet">
    <style>
        html, body {
            margin: 0; padding: 0; width: 100%; height: 100%;
            overflow: hidden; font-family: 'VT323', monospace;
            background-color: #4facfe;
        }

        img, .pixel-bg, .pixel-mountains, .pixel-tree, .pixel-flower, .mandarin-ornament, .mandarin-bird {
            image-rendering: pixelated;
            image-rendering: crisp-edges;
        }

        .pixel-bg {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background-image: url('https://stardewvalleywiki.com/mediawiki/images/5/5a/Stardew_Valley_Map.png');
            background-size: cover; background-position: center; z-index: -3; filter: blur(2px) brightness(0.8);
        }

        .pixel-mountains {
            position: fixed; bottom: 0; left: 0; width: 100%; height: 50%;
            background-image: url('https://stardewvalleywiki.com/mediawiki/images/4/4c/Background_Mountains.png');
            background-size: cover; background-position: bottom center; background-repeat: repeat-x; z-index: -2;
        }

        .pixel-tree {
            position: absolute; width: 48px; height: 64px;
            background-image: url('https://stardewvalleywiki.com/mediawiki/images/3/3a/Oak_Tree_Stage_5.png');
            background-size: contain; background-repeat: no-repeat; z-index: -1;
        }
        
        .pixel-tree::after {
            content: ""; position: absolute; top: 10px; left: 10px; width: 28px; height: 28px;
            background-image: radial-gradient(#ff9800 2px, transparent 3px);
            background-size: 8px 8px;
        }

        .pixel-flower {
            position: absolute; width: 16px; height: 16px;
            background-size: contain; background-repeat: no-repeat; z-index: -1;
        }

        .mandarin-bird {
            position: absolute; width: 24px; height: 18px;
            background-image: radial-gradient(#ff9800 80%, transparent 85%);
            z-index: 10; opacity: 0.9;
            box-shadow: -6px -2px 0px 0px #aaa, 6px -2px 0px 0px #aaa;
            animation: mandarin-fly 15s linear infinite, mandarin-wing-flap 0.3s steps(2, end) infinite;
        }

        @keyframes mandarin-wing-flap { to { box-shadow: -6px 2px 0px 0px #999, 6px 2px 0px 0px #999; } }
        @keyframes mandarin-fly { 0% { transform: translate(-50px, 20%); } 100% { transform: translate(110vw, 25%); } }

        .dialog-container {
            display: flex; flex-direction: column; align-items: center; justify-content: center;
            width: 100%; height: 100%; z-index: 20;
        }

        .robin-icon {
            width: 96px; height: 96px; margin-bottom: 20px;
            border: 4px solid #633524; background-color: #e5b061;
            padding: 5px; box-shadow: 5px 5px 0px rgba(0,0,0,0.5);
        }

        .dialog-box {
            background-color: #e5b061; border: 6px solid #633524;
            padding: 25px; width: 480px; max-width: 90%;
            box-shadow: 8px 8px 0px rgba(0,0,0,0.6); text-align: center; position: relative;
        }

        .dialog-box::before {
            content: ""; position: absolute; top: 4px; left: 4px; right: 4px; bottom: 4px;
            border: 3px solid #ffde9b; pointer-events: none;
        }

        .mandarin-ornament {
            position: absolute; width: 20px; height: 20px; z-index: 5;
            background-image: radial-gradient(#ff9800 80%, transparent 85%);
            border-radius: 50%; box-shadow: 0px -4px 0px 0px #4caf50;
        }

        .dialog-box p { color: #3c2015; font-size: 1.8em; margin: 0; line-height: 1.4; }
        .dialog-box h2 { font-size: 2.2em; color: #6d4c41; margin: 0 0 10px 0; }
    </style>
</head>
<body>
    <div class="pixel-bg"></div>
    <div class="pixel-mountains"></div>
    
    <div class="pixel-tree" style="left: 10%; bottom: 15%;"></div>
    <div class="pixel-tree" style="left: 28%; bottom: 20%;"></div>
    <div class="pixel-tree" style="right: 18%; bottom: 18%;"></div>
    
    <div class="pixel-flower" style="left: 18%; bottom: 10%; background-image: url('https://stardewvalleywiki.com/mediawiki/images/f/f1/Tulip.png');"></div>
    <div class="pixel-flower" style="right: 20%; bottom: 11%; background-image: url('https://stardewvalleywiki.com/mediawiki/images/d/d7/Blue_Jazz.png');"></div>

    <div class="mandarin-bird" style="top: 25%; animation-delay: 1s;"></div>
    <div class="mandarin-bird" style="top: 45%; animation-delay: 10s;"></div>

    <div class="dialog-container">
        <img src="https://stardewvalleywiki.com/mediawiki/images/d/df/Chica_Mandarina_Retrato.png" class="robin-icon" alt="Chica Mandarina">
        <div class="dialog-box">
            <div class="mandarin-ornament" style="top: -10px; left: -10px;"></div>
            <div class="mandarin-ornament" style="top: -10px; right: -10px;"></div>
            <h2>AVISO DE LA CHICA MANDARINA</h2>
            <p>¡Holi! El equipo técnico está usando sus picos pixelados para plantar árboles con mandarinas y flores. ¡Vuelve pronto!</p>
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
    return "Stardew Chat SaaS Activo - Modo Mandarina"

# --- 4. CONFIGURACIÓN DEL PUERTO ---
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
