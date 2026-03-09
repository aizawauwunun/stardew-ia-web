from flask import Flask, request, jsonify, render_template_string
import os

app = Flask(__name__)

# --- DISEÑO PIXELADO MANDARINA ---
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
            background: #60a5fa; /* Cielo */
            font-family: 'Courier New', Courier, monospace;
            display: flex; justify-content: center; align-items: center;
            height: 100vh; overflow: hidden;
            image-rendering: pixelated;
        }

        /* FONDO PIXELADO: MONTAÑAS Y ÁRBOLES */
        .world {
            position: absolute; width: 100%; height: 100%;
            background: 
                /* Flores y Mandarinas en el suelo */
                radial-gradient(circle, #ff8800 2px, transparent 1px) 10px 10px / 40px 40px,
                radial-gradient(circle, #ff55ee 1px, transparent 1px) 25px 25px / 30px 30px,
                /* Suelo de hierba */
                linear-gradient(to bottom, transparent 70%, #5ba339 70%);
            z-index: 1;
        }

        /* MONTAÑAS CON TEXTURA */
        .mountains {
            position: absolute; bottom: 30%; width: 100%; height: 40%;
            background: #4b8a2d;
            clip-path: polygon(0% 100%, 15% 20%, 35% 60%, 55% 10%, 80% 50%, 100% 20%, 100% 100%);
            box-shadow: inset 0 20px 0 #6ab446;
            z-index: 2;
        }

        /* ÁRBOLES DE MANDARINA (Puntos naranjas sobre verde) */
        .tree {
            position: absolute; bottom: 30%; width: 60px; height: 80px;
            background: #2d5a27; border-radius: 10px 10px 0 0;
            box-shadow: 
                inset -10px -10px #1e3f1a,
                4px 10px #ff8800, -8px 25px #ff8800, 10px 40px #ff8800; /* Las mandarinas */
            z-index: 3;
        }

        /* MANDARINAS VOLADORAS PIXELADAS */
        .winged-mandarin {
            position: absolute; width: 20px; height: 18px;
            background: #ff8800; border: 2px solid #000;
            box-shadow: -10px -5px #fff, 10px -5px #fff; /* Alas simples pixel */
            z-index: 5; animation: fly 5s infinite linear;
        }

        @keyframes fly {
            0% { transform: translate(-100vw, 20vh); }
            100% { transform: translate(100vw, 10vh); }
        }

        /* CONTENEDOR CENTRAL (IMAGEN + DIÁLOGO) */
        .main-ui {
            position: relative; z-index: 10;
            display: flex; flex-direction: column; align-items: center;
            gap: 15px;
        }

        .avatar {
            width: 120px; height: 120px;
            border: 6px solid #633524;
            border-radius: 10px;
            background: #fff;
            image-rendering: pixelated;
        }

        .dialog-box {
            background: #e5b061; border: 6px solid #633524;
            padding: 20px; width: 320px; text-align: center;
            box-shadow: 8px 8px 0 rgba(0,0,0,0.3);
            position: relative;
        }

        /* MANDARINAS DE DECORACIÓN EN EL CUADRO */
        .corner-mandarin {
            position: absolute; width: 25px; height: 25px;
            background: #ff8800; border: 3px solid #633524; border-radius: 4px;
        }
        .leaf {
            position: absolute; width: 10px; height: 6px;
            background: #4ac94a; top: -8px; left: 5px;
        }

        p { color: #3c2015; font-weight: bold; margin: 5px 0; font-size: 1.1em; line-height: 1.2; }
        .footer { font-size: 0.8em; color: #633524; opacity: 0.8; }
    </style>
</head>
<body>
    <div class="world"></div>
    <div class="mountains"></div>
    
    <div class="tree" style="left: 10%;"></div>
    <div class="tree" style="left: 25%; bottom: 28%; scale: 0.8;"></div>
    <div class="tree" style="right: 15%;"></div>
    
    <div class="winged-mandarin" style="animation-delay: 0s; top: 15%;"></div>
    <div class="winged-mandarin" style="animation-delay: 2.5s; top: 25%;"></div>

    <div class="main-ui">
        <img src="https://raw.githubusercontent.com/aizawauwunun/stardew-ia-web/main/Gemini_Generated_Image_p43yd2p43yd2p43y.jpg" class="avatar">
        
        <div class="dialog-box">
            <div class="corner-mandarin" style="top: -15px; left: -15px;"><div class="leaf"></div></div>
            <div class="corner-mandarin" style="bottom: -15px; right: -15px;"><div class="leaf"></div></div>
            
            <p>¡Hola! Soy la Chica Mandarina.</p>
            <p>El equipo está cultivando el Valle, ¡vuelve pronto!</p>
            <p class="footer">Aviso de la Chica Mandarina</p>
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
