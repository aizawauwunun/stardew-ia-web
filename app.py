from flask import Flask, request, jsonify, render_template_string
import os

app = Flask(__name__)

# --- DISEÑO PIXEL ART REAL (Estilo Inicio Stardew Valley) ---
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
            overflow: hidden; background: #60a5fa; /* Cielo Stardew */
            font-family: 'Courier New', Courier, monospace;
            display: flex; justify-content: center; align-items: center;
            image-rendering: pixelated; /* Fuerza texturas pixel art */
        }

        /* --- CAPAS DEL PAISAJE (PARALLAX CON TEXTURAS DE PÍXELES) --- */
        .sky {
            position: absolute; width: 100%; height: 100%;
            background: linear-gradient(to bottom, #4facfe 0%, #00f2fe 100%);
            z-index: 1;
        }

        /* MONTAÑAS LEJANAS CON TEXTURA DE PÍXELES DE TIERRA */
        .mountains {
            position: absolute; bottom: 150px; width: 200%; height: 350px;
            /* Patrón de píxeles para simular tierra/roca pixelada */
            background-image: 
                linear-gradient(45deg, #4b8a2d 25%, transparent 25%), 
                linear-gradient(-45deg, #4b8a2d 25%, transparent 25%),
                linear-gradient(45deg, transparent 75%, #4b8a2d 75%),
                linear-gradient(-45deg, transparent 75%, #4b8a2d 75%);
            background-size: 8px 8px; /* Tamaño del píxel */
            background-color: #3d7324; /* Color base */
            clip-path: polygon(0% 100%, 10% 20%, 25% 60%, 40% 10%, 60% 70%, 75% 5%, 90% 60%, 100% 30%, 100% 100%);
            z-index: 2;
            opacity: 0.9;
        }

        /* BOSQUE DE MANDARINAS FRONTAL CON PATRÓN DE ÁRBOLES PIXELADOS */
        .forest {
            position: absolute; bottom: 0; width: 100%; height: 180px;
            /* Patrón de píxeles para simular árboles y mandarinas en el suelo */
            background-image: 
                radial-gradient(#ff8800 3px, transparent 4px), /* Mandarinas */
                radial-gradient(#2d5a27 10px, transparent 11px); /* Árboles pixel */
            background-size: 60px 60px;
            background-color: #5ba339; /* Suelo de hierba pixel */
            border-top: 8px solid #4b8a2d;
            z-index: 4;
        }

        /* FLORES PIXELADAS EN EL SUELO */
        .flowers {
            position: absolute; bottom: 5%; width: 100%; height: 10%;
            background-image: radial-gradient(#ff55ee 2px, transparent 3px), radial-gradient(#ffffff 2px, transparent 3px);
            background-size: 30px 30px;
            z-index: 5;
        }

        /* --- MANDARINAS VOLADORAS CON ALAS (FLAMENCO STYLE) --- */
        .winged-mandarin {
            position: absolute; width: 35px; height: 25px;
            background: #ff8800;
            border: 4px solid #000;
            border-radius: 50% 50% 40% 40%;
            z-index: 6;
            animation: fly-across 12s infinite linear;
        }

        /* Alas pixeladas animadas */
        .winged-mandarin::before, .winged-mandarin::after {
            content: ''; position: absolute; width: 22px; height: 12px;
            background: white; border: 3px solid #000; top: -8px;
            animation: flap 0.3s infinite alternate;
        }
        .winged-mandarin::before { left: -18px; transform-origin: right; }
        .winged-mandarin::after { right: -18px; transform-origin: left; }

        @keyframes flap { 
            from { transform: rotate(20deg); } to { transform: rotate(-40deg); } 
        }

        @keyframes fly-across {
            from { left: -150px; transform: translateY(0); }
            to { left: 110%; transform: translateY(-50px); }
        }

        /* --- UI CENTRAL (IMAGEN + DIÁLOGO) --- */
        .main-container {
            position: relative; z-index: 10;
            display: flex; flex-direction: column; align-items: center;
            animation: float 3s infinite ease-in-out;
        }

        @keyframes float {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-15px); }
        }

        .chica-mandarina-img {
            width: 150px; height: 150px;
            border: 6px solid #633524; /* Marco de madera oscuro pixel */
            border-radius: 12px;
            background: white;
            image-rendering: pixelated; /* Fuerza pixelado en la imagen */
            box-shadow: 0 10px 20px rgba(0,0,0,0.3);
            object-fit: cover;
        }

        .dialog-box {
            margin-top: 20px;
            background: #e5b061; /* Madera clara */
            border: 6px solid #633524;
            padding: 25px; width: 350px;
            box-shadow: 10px 10px 0 rgba(0,0,0,0.4);
            position: relative;
            text-align: center;
        }

        /* DETALLES DE MANDARINA PIXELADA EN EL CUADRO */
        .corner-m {
            position: absolute; width: 25px; height: 25px;
            background: #ff8800; border: 4px solid #633524;
        }
        .leaf {
            position: absolute; width: 12px; height: 8px;
            background: #4ac94a; top: -10px; left: 6px; border: 3px solid #633524;
        }

        p { color: #3c2015; font-weight: bold; margin: 8px 0; font-size: 1.2em; }
        .footer-text { font-size: 0.8em; color: #633524; margin-top: 15px; display: block; }
    </style>
</head>
<body>
    <div class="sky"></div>
    <div class="mountains"></div>
    <div class="forest"></div>
    <div class="flowers"></div>

    <div class="winged-mandarin" style="top: 20%; animation-delay: 0s;"></div>
    <div class="winged-mandarin" style="top: 10%; animation-delay: 4s; scale: 0.7;"></div>
    <div class="winged-mandarin" style="top: 30%; animation-delay: 8s; scale: 1.2;"></div>

    <div class="main-container">
        <img src="https://raw.githubusercontent.com/aizawauwunun/stardew-ia-web/main/Gemini_Generated_Image_p43yd2p43yd2p43y.jpg" 
             onerror="this.src='https://stardewvalleywiki.com/mediawiki/images/b/b7/Robin.png'" 
             class="chica-mandarina-img" 
             alt="Chica Mandarina">
        
        <div class="dialog-box">
            <div class="corner-m" style="top: -15px; left: -15px;"><div class="leaf"></div></div>
            <div class="corner-m" style="bottom: -15px; right: -15px;"><div class="leaf"></div></div>
            
            <p>¡Hola! Soy la Chica Mandarina.</p>
            <p>El equipo está cultivando el Valle, ¡vuelve pronto!</p>
            <span class="footer-text">Aviso de la Chica Mandarina</span>
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
