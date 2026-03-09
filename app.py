from flask import Flask, request, jsonify, render_template_string
import os

app = Flask(__name__)

# --- ENLACES A TUS ARCHIVOS EN GITHUB ---
# Usamos el formato 'raw' para que Render pueda leer las imágenes directamente
URL_FONDO = "https://raw.githubusercontent.com/aizawauwunun/stardew-ia-web/main/fondo%20pagina%20web.png"
URL_CHICA = "https://raw.githubusercontent.com/aizawauwunun/stardew-ia-web/main/chica%20mandarina.png"

DISENO_MANTENIMIENTO = f'''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mandarina Valley</title>
    <style>
        * {{
            margin: 0; padding: 0; box-sizing: border-box;
            /* Esto evita que las imágenes se vean borrosas */
            image-rendering: pixelated;
        }}

        body, html {{
            width: 100%; height: 100%;
            overflow: hidden;
            display: flex; justify-content: center; align-items: center;
            /* Tu imagen de fondo cubriendo todo */
            background: url('{URL_FONDO}') no-repeat center center fixed;
            background-size: cover;
            font-family: 'Courier New', Courier, monospace;
        }}

        .main-container {{
            display: flex; flex-direction: column; align-items: center;
            gap: 10px;
            animation: float 3s infinite ease-in-out;
        }}

        @keyframes float {{
            0%, 100% {{ transform: translateY(0); }}
            50% {{ transform: translateY(-15px); }}
        }}

        /* Tu imagen de la Chica Mandarina */
        .avatar {{
            width: 180px; height: auto;
            display: block;
        }}

        /* Cuadro de diálogo estilo madera */
        .dialog-box {{
            background: #e5b061; 
            border: 6px solid #633524;
            padding: 20px;
            width: 350px;
            text-align: center;
            box-shadow: 8px 8px 0 rgba(0,0,0,0.3);
        }}

        p {{
            color: #3c2015;
            font-weight: bold;
            font-size: 1.2em;
            margin: 5px 0;
            line-height: 1.2;
        }}

        .footer {{
            font-size: 0.8em;
            color: #633524;
            margin-top: 10px;
            display: block;
            opacity: 0.8;
        }}
    </style>
</head>
<body>
    <div class="main-container">
        <img src="{URL_CHICA}" class="avatar" alt="Chica Mandarina">
        
        <div class="dialog-box">
            <p>¡BIENVENIDOS AL VALLE!</p>
            <p>Soy la Chica Mandarina.</p>
            <p>Estamos trabajando para ti.</p>
            <span class="footer">Aviso de la Chica Mandarina</span>
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
