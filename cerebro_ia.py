import torch
import torch.nn as nn
import os
import sqlite3

memoria_conversacion = {}

# ----------------------------
# PREPARACIÓN DE DATOS
# ----------------------------
with open("datos.txt", "r", encoding="utf-8") as f:
    texto = f.read()

caracteres = sorted(list(set(texto)))
vocab_size = len(caracteres)
stoi = {ch:i for i,ch in enumerate(caracteres)}
itos = {i:ch for i,ch in enumerate(caracteres)}
datos = torch.tensor([stoi[c] for c in texto], dtype=torch.long)

# ----------------------------
# MODELO
# ----------------------------
class MiIA_Pro(nn.Module):
    def __init__(self, vocab_size):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, 128)
        self.lstm = nn.LSTM(128, 256, num_layers=2, batch_first=True)
        self.linear = nn.Linear(256, vocab_size)

    def forward(self, x, h=None):
        x = self.embedding(x)
        out, h = self.lstm(x, h)
        out = self.linear(out)
        return out, h

modelo = MiIA_Pro(vocab_size)

# ----------------------------
# CARGAR O ENTRENAR
# ----------------------------
if os.path.exists('cerebro_ia.pth'):
    try:
        modelo.load_state_dict(torch.load('cerebro_ia.pth'))
        print("--- CEREBRO PRO CARGADO ---")
    except:
        print("BORRA cerebro_ia.pth Y EJECUTA DE NUEVO")
else:
    print("ENTRENANDO IA...")
    optimizador = torch.optim.Adam(modelo.parameters(), lr=0.001)
    for paso in range(10000):
        idx = torch.randint(0, len(datos) - 64, (1,))
        x = datos[idx:idx+64].unsqueeze(0)
        y = datos[idx+1:idx+65].unsqueeze(0)
        logits, _ = modelo(x)
        loss = nn.CrossEntropyLoss()(logits.view(-1, vocab_size), y.view(-1))
        optimizador.zero_grad()
        loss.backward()
        optimizador.step()
        if paso % 500 == 0:
            print("Paso:", paso)
            torch.save(modelo.state_dict(), "cerebro_ia.pth")
    torch.save(modelo.state_dict(), "cerebro_ia.pth")

modelo.eval()

# ----------------------------
# BASE DE DATOS
# ----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "stardew_saas.db")

def generar_respuesta_stardew(mensaje_usuario, nombre_npc):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT personalidad FROM hijos_custom WHERE nombre = ?",
        (nombre_npc,)
    )
    resultado = cursor.fetchone()
    conn.close()

    if nombre_npc not in memoria_conversacion:
        memoria_conversacion[nombre_npc] = ""

    historial = memoria_conversacion[nombre_npc]

    if resultado:
        personalidad = resultado[0]
        contexto = f"{historial}\nJugador: {mensaje_usuario}\n{nombre_npc} ({personalidad}): "
    else:
        contexto = f"{historial}\nJugador: {mensaje_usuario}\n{nombre_npc}: "

    entrada = torch.tensor([stoi.get(c, 0) for c in contexto], dtype=torch.long).unsqueeze(0)
    h = None
    respuesta_ia = ""

    with torch.no_grad():
        logits, h = modelo(entrada, h)
        for _ in range(120):
            v, _ = torch.topk(logits[:, -1, :], 5)
            logits_f = logits[:, -1, :].clone()
            logits_f[logits_f < v[:, [-1]]] = -float("Inf")
            probs = torch.softmax(logits_f / 1.1, dim=-1)
            proximo = torch.multinomial(probs, 1)
            letra = itos[proximo.item()]
            if letra == "\n": break
            respuesta_ia += letra
            logits, h = modelo(proximo, h)

    memoria_conversacion[nombre_npc] += f"\nJugador: {mensaje_usuario}\n{nombre_npc}: {respuesta_ia}"
    return respuesta_ia