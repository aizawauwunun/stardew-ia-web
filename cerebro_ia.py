import torch
import torch.nn as nn
import os
import sqlite3

# 1. PREPARACIÓN DE DATOS (Historia del Jardín)
with open('datos.txt', 'r', encoding='utf-8') as f:
    texto = f.read()

caracteres = sorted(list(set(texto)))
vocab_size = len(caracteres)
stoi = { ch:i for i,ch in enumerate(caracteres) }
itos = { i:ch for i,ch in enumerate(caracteres) }
datos = torch.tensor([stoi[c] for c in texto], dtype=torch.long)

# 2. EL CEREBRO PRO (LSTM con Memoria)
class MiIA_Pro(nn.Module):
    def __init__(self, vocab_size):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, 128)
        # LSTM es el motor de memoria (2 capas para más inteligencia)
        self.lstm = nn.LSTM(128, 256, num_layers=2, batch_first=True)
        self.linear = nn.Linear(256, vocab_size)
        
    def forward(self, x, h=None):
        x = self.embedding(x)
        # x puede ser una letra o una frase entera
        out, h = self.lstm(x, h)
        out = self.linear(out)
        return out, h

modelo = MiIA_Pro(vocab_size)

# 3. CARGAR O ENTRENAR
if os.path.exists('cerebro_ia.pth'):
    # Intentamos cargar, si falla por el cambio de modelo, avisamos
    try:
        modelo.load_state_dict(torch.load('cerebro_ia.pth', weights_only=True))
        print("--- CEREBRO PRO CARGADO ---")
    except:
        print("--- MODELO ANTIGUO DETECTADO. POR FAVOR BORRA 'cerebro_ia.pth' ---")
else:
    print("\n--- ENTRENANDO CEREBRO PRO (ESTO SERÁ MEJOR) ---")
    optimizador = torch.optim.Adam(modelo.parameters(), lr=0.001) # Más rápido
    for paso in range(10000): # Con 10k ya será muy lista
        # Seleccionamos un trozo de la historia al azar
        idx = torch.randint(0, len(datos) - 64, (1,))
        x = datos[idx:idx+64].unsqueeze(0)
        y = datos[idx+1:idx+65].unsqueeze(0)
        
        logits, _ = modelo(x)
        loss = nn.CrossEntropyLoss()(logits.view(-1, vocab_size), y.view(-1))
        
        optimizador.zero_grad()
        loss.backward()
        optimizador.step()

        if paso % 500 == 0:
            print(f"Paso: {paso} | Inteligencia: {100 - (loss.item()*20):.1f}%")
            torch.save(modelo.state_dict(), 'cerebro_ia.pth')

    torch.save(modelo.state_dict(), 'cerebro_ia.pth')

# 4. MOTOR PARA LA WEB (CONEXIÓN CON FLASK Y SQL)
modelo.eval()
DB_PATH = r"C:\Users\pizar\Stardew_IA_Project\stardew_saas.db"

def generar_respuesta_stardew(mensaje_usuario, nombre_npc):
    # BUSCAMOS SI ES UN HIJO EN LA DB
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT personalidad FROM hijos_custom WHERE nombre = ?", (nombre_npc,))
    resultado = cursor.fetchone()
    conn.close()

    # Si es hijo, inyectamos su personalidad al modelo
    if resultado:
        personalidad = resultado[0]
        contexto = f"{nombre_npc} ({personalidad}): {mensaje_usuario}\nIA: "
    else:
        contexto = f"{nombre_npc}: {mensaje_usuario}\nIA: "

    # Convertimos el texto a números para tu LSTM
    entrada = torch.tensor([stoi.get(c, 0) for c in contexto], dtype=torch.long).unsqueeze(0)
    h = None
    respuesta_ia = ""

    with torch.no_grad():
        logits, h = modelo(entrada, h)
        
        for _ in range(200): # Límite de letras
            v, _ = torch.topk(logits[:, -1, :], 5)
            logits_f = logits[:, -1, :].clone()
            logits_f[logits_f < v[:, [-1]]] = -float('Inf')
            
            probs = torch.softmax(logits_f / 1.1, dim=-1)
            proximo = torch.multinomial(probs, 1)
            
            letra = itos[proximo.item()]
            if letra == "\n": break
            respuesta_ia += letra
            
            logits, h = modelo(proximo, h)

    return respuesta_ia