from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

# --- BASE DE DATOS INTERNA DE HABITANTES ---
# Esta información no se muestra en la web, pero la IA la tiene lista para usar.
HABITANTES = {
    "Alex": "Deportista y egocéntrico.",
    "Elliott": "Escritor romántico.",
    "Harvey": "Médico miedoso.",
    "Sam": "Músico alegre.",
    "Sebastian": "Programador introvertido.",
    "Shane": "Rudo que ama gallinas.",
    "Abigail": "Aventurera mística.",
    "Emily": "Espiritual y costurera.",
    "Haley": "Fotógrafa de moda.",
    "Leah": "Artista del bosque.",
    "Maru": "Científica inventora.",
    "Penny": "Tímida y educada.",
    "Caroline": "Ama su té.",
    "Clint": "Herrero solitario.",
    "Demetrius": "Científico formal.",
    "Evelyn": "Abuela cariñosa.",
    "George": "Abuelo gruñón.",
    "Gus": "Cocinero del salón.", 
    "Jas": "Niña tímida.",
    "Jodi": "Madre dedicada.",
    "Kent": "Ex-militar serio.", 
    "Leo": "Niño de la selva.",
    "Lewis": "Alcalde del pueblo.",
    "Linus": "Ermitaño sabio.", 
    "Marnie": "Ganadera amable.",
    "Pam": "Conductora de bus.",
    "Pierre": "Tendero ambicioso.", 
    "Robin": "Carpintera alegre.",
    "Sandy": "Dueña del Oasis.",
    "Vincent": "Niño juguetón.",
    "Willy": "Pescador experto."
}

# --- ENLACES DE IMAGEN ---
URL_FONDO = "https://raw.githubusercontent.com/aizawauwunun/stardew-ia-web/main/fondo%20pagina%20web.png"
URL_CHICA = "https://raw.githubusercontent.com/aizawauwunun/stardew-ia-web/main/chica%20mandarina.png"

# --- DISEÑO DE LA PÁGINA DE ESPERA ---
DISENO_MANTENIMIENTO = f'''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>stardew-ia-web</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; image-rendering: pixelated; }}
        body {{
            height: 100vh; display: flex; justify-content: center; align-items: center;
            background: #4facfe url('{URL_FONDO}') no-repeat center center fixed;
            background-size: cover; font-family: 'Courier New', monospace;
            overflow: hidden;
        }}
        .container {{ text-align: center; animation: float 3s infinite ease-in-out; }}
        @keyframes float {{ 50% {{ transform: translateY(-15px); }} }}
        .chica-img {{ width: 220px; height: auto; }}
        .dialog-box {{
            background: #e5b061; border: 6px solid #633524;
            padding: 30px; width: 400px; margin-top: -10px;
            box-shadow: 10px 10px 0 rgba(0,0,0,0.3);
        }}
        h1 {{ color: #3c2015; font-size: 1.5em; text-transform: uppercase; margin-bottom: 10px; }}
        p {{ color: #633524; font-weight: bold; font-size: 1em; }}
    </style>
</head>
<body>
    <div class="container">
        <img src="{URL_CHICA}" class="chica-img">
        <div class="dialog-box">
            <h1>Próximamente</h1>
            <h1>Stardew IA Web</h1>
            <p>Atte: Chica Mandarina</p>
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
    # Aquí es donde la IA usará los datos de 'HABITANTES' en el futuro
    return "OK"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
