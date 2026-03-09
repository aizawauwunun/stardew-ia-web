from flask import Flask, request, jsonify, render_template_string
import os

app = Flask(__name__)

# --- DISEÑO PIXEL ART (ESTILO START SCREEN) ---
DISENO_MANTENIMIENTO = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mandarina Valley AI</title>
    <style>
        body, html {
            margin: 0; padding: 0; width: 100%; height: 100%;
            overflow: hidden; background: #5da3f5; /* Azul cielo Stardew */
            font-family: 'Courier New', Courier, monospace;
            display: flex; justify-content: center; align-items: center;
        }

        /* --- PAISAJE CON BORDES DENTADOS (PIXEL STYLE) --- */
        .sky {
            position: absolute; width: 100%; height: 100%;
            background: #5da3f5; z-index: 1;
        }

        /* MONTAÑAS CON EFECTO ESCALONADO */
        .mountains {
            position: absolute; bottom: 80px; width: 100%; height: 300px;
            background: #4b8a2d;
            /* Clip-path con muchos puntos para simular escalones de píxeles */
            clip-path: polygon(
                0% 100%, 0% 40%, 5% 40%, 5% 30%, 10% 30%, 10% 20%, 15% 20%, 
                20% 40%, 25% 40%, 25% 50%, 30% 50%, 35% 30%, 40% 30%, 45% 10%, 
                50% 10%, 55% 30%, 60% 30%, 65% 50%, 70% 50%, 75% 20%, 80% 20%, 
                85% 40%, 90% 40%, 95% 60%, 100% 60%, 100% 100%
            );
            border-top: 8px solid #6ab446;
            z-index: 2;
        }

        /* SUELO DE HIERBA CON TEXTURA DE PUNTOS */
        .grass {
            position: absolute; bottom: 0; width: 100%; height: 120px;
            background: #5ba339;
            background-image: radial-gradient(#4b8a2d 2px, transparent 2px);
            background-size: 16px 16px;
            border-top: 6px solid #1e3f1a;
            z-index: 4;
        }

        /* ÁRBOLES DE MANDARINA (BLOQUES CUADRADOS) */
        .tree {
            position: absolute; width: 40px; height: 60px;
            background: #2d5a27;
            box-shadow: 
                8px -8px #2d5a27, -8px -8px #2d5a27,
                4px 4px #ff8800, -10px 12px #ff8800, 8px 25px #ff8800; /* Frutas */
            z-index: 5;
        }

        /* MANDARINAS CON ALAS (PIXELADAS) */
        .winged-mandarin {
            position: absolute; width: 24px; height: 20px;
            background: #ff8800; border: 4px solid #000;
            z-index: 6; animation: fly 12s infinite linear;
        }
        .winged-mandarin::before, .winged-mandarin::after {
            content: ''; position: absolute; width: 16px; height: 8px;
            background: #fff; border: 3px solid #000; top: -6px;
            animation: flap 0.2s infinite alternate;
        }
        .winged-mandarin::before { left: -16px; }
        .winged-mandarin::after { right: -16px; }

        @keyframes flap { from { top: -6px; } to { top: 2px; } }
        @keyframes fly { from { left: -100px; } to { left: 110%; } }

        /* --- UI CENTRAL --- */
        .main-ui {
            position: relative; z-index: 10;
            display: flex; flex-direction: column; align-items: center;
        }

        .chica-mandarina-img {
            width: 140px; height: 140px;
            border: 6px solid #633524;
            background: #fff;
            image-rendering: pixelated;
            box-shadow: 8px 8px 0 rgba(0,0,0,0.2);
        }

        .dialog-box {
            margin-top: 15px;
            background: #e5b061; 
            border: 6px solid #633524;
            padding: 20px; width: 300px;
            box-shadow: 10px 10px 0 rgba(0,0,0,0.3);
            text-align: center;
            position: relative;
        }

        /* ESQUINAS CON MINI MANDARINAS */
        .corner {
            position: absolute; width: 20px; height: 20px;
            background: #ff8800; border: 4px solid #633524;
        }

        p { color: #3c2015; font-weight: bold; margin: 5px 0; font-size: 1.1em; text-transform: uppercase; }
    </style>
</head>
<body>
    <div class="sky"></div>
    <div class="mountains"></div>
    <div class="grass"></div>

    <div class="tree" style="bottom: 110px; left: 15%;"></div>
    <div class="tree" style="bottom: 90px; right: 20%;"></div>

    <div class="winged-mandarin" style="top: 20%; animation-delay: 0s;"></div>
    <div class="winged-mandarin" style="top: 35%; animation-delay: 6s;"></div>

    <div class="main-ui">
        <img src="https://raw.githubusercontent.com/aizawauwunun/stardew-ia-web/main/Gemini_Generated_Image_p43yd2p43yd2p43y.jpg" 
             onerror="this.src='https://stardewvalleywiki.com/mediawiki/images/b/b7/Robin.png'" 
             class="chica-mandarina-img">
        
        <div class="dialog-box">
            <div class="corner" style="top: -12px; left: -12px;"></div>
            <div class="corner" style="bottom: -12px; right: -12px;"></div>
            <p>¡Hola! Soy la Chica Mandarina.</p>
            <p style="font-size: 0.9em;">Aviso de la Chica Mandarina</p>
        </div>
    </div>
</body>
</html>
'''

@app.before_request
def modo_privado():
    if request.path.startswith('/static'): return None
    return render_template_string(DISENO_MANTENIMIENTO), 503

@app.route('/')
def home():
    return "OK"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
