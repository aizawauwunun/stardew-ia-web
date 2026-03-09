from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

# --- ENLACES RAW DIRECTOS ---
# Estos enlaces permiten que Render descargue la imagen directamente de GitHub
URL_FONDO = "https://raw.githubusercontent.com/aizawauwunun/stardew-ia-web/main/fondo%20pagina%20web.png"
URL_CHICA = "https://raw.githubusercontent.com/aizawauwunun/stardew-ia-web/main/chica%20mandarina.png"

DISENO_MANTENIMIENTO = f'''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>stardew-ia-web</title>
    <style>
        * {{
            margin: 0; padding: 0; box-sizing: border-box;
            /* Mantiene los píxeles nítidos sin que se vean borrosos */
            image-rendering: pixelated;
        }}

        body, html {{
            width: 100%; height: 100%;
            display: flex; justify-content: center; align-items: center;
            /* Tu imagen de fondo */
            background: #4facfe url('{URL_FONDO}') no-repeat center center fixed;
            background-size: cover;
            font-family: 'Courier New', Courier, monospace;
            overflow: hidden;
        }}

        .main-container {{
            display: flex; flex-direction: column; align-items: center;
            z-index: 10;
            /* Animación de flotado suave */
            animation: float 4s infinite ease-in-out;
        }

        @keyframes float {{
            0%, 100% {{ transform: translateY(0); }}
            50% {{ transform: translateY(-15px); }}
        }}

        /* Tu imagen de la Chica Mandarina */
        .chica-img {{
            width: 180px; 
            height: auto;
            display: block;
            /* Evita que se vea borrosa al escalar */
            image-rendering: pixelated;
        }}

        /* Cuadro de diálogo estilo madera */
        .dialog-box {{
            background: #e5b061; 
            border: 6px solid #633524;
            padding: 25px;
            width: 380px;
            text-align: center;
            box-shadow: 10px 10px 0 rgba(0,0,0,0.3);
            margin-top: -5px; /* Para que la chica parezca estar encima */
        }}

        p {{
            color: #3c2015;
            font-weight: bold;
            font-size: 1.3em;
            margin: 5px 0;
            text-transform: uppercase;
            line-height: 1.2;
        }}

        .footer {{
            font-size: 0.8em;
            color: #633524;
            margin-top: 15px;
            display: block;
            opacity: 0.8;
        }}
    </style>
</head>
<body>
    <div class="main-container">
        <img src="{URL_CHICA}" class="chica-img" alt="Chica Mandarina">
        
        <div class="dialog-box">
            <p>¡BIENVENIDOS!</p>
            <p>Estamos trabajando en el valle.</p>
            <span class="footer">Aviso de la Chica Mandarina - stardew-ia-web</span>
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
