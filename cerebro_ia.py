import torch
import torch.nn as nn
import os

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

# 4. MOTOR DE DIÁLOGO STARDEW (MEMORIA Y REACCIÓN)
modelo.eval()
historial = "" # Memoria para que entienda el contexto del chat
print("\n" + "="*30 + "\n¡IA DE PUEBLO PELÍCANO LISTA PARA MODS!\n" + "="*30)

while True:
    usuario = input("\nTú: ")
    if usuario.lower() == "salir": break
    
    # Añadimos tu mensaje al historial para que la IA sepa de qué están hablando
    historial += f"Tú: {usuario}\nIA: "
    
    # Tomamos los últimos 600 caracteres para no saturar la memoria
    contexto_reciente = historial[-600:]
    
    # Convertimos a tensor y aseguramos la dimensión correcta para el LSTM
    entrada = torch.tensor([stoi.get(c, 0) for c in contexto_reciente], dtype=torch.long).unsqueeze(0)
    print("IA: ", end="")
    
    h = None
    respuesta_ia = ""
    
    with torch.no_grad():
        # Procesamos el contexto inicial
        logits, h = modelo(entrada, h)
        
        # Generamos la respuesta letra por letra
        for _ in range(350):
            # Filtro Top-K para mantener la coherencia
            v, _ = torch.topk(logits[:, -1, :], 5)
            logits_f = logits[:, -1, :].clone()
            logits_f[logits_f < v[:, [-1]]] = -float('Inf')
            
            # Temperatura 1.1: El balance entre naturalidad y orden
            probs = torch.softmax(logits_f / 1.1, dim=-1)
            proximo = torch.multinomial(probs, 1)
            
            letra = itos[proximo.item()]
            print(letra, end="", flush=True)
            respuesta_ia += letra
            
            # Si la IA hace un salto de línea, termina su turno
            if letra == "\n": break
            
            # Pasamos la letra generada al modelo (CORRECCIÓN DE DIMENSIÓN)
            logits, h = modelo(proximo, h)
            
    # Guardamos la respuesta en el historial para el siguiente turno
    historial += respuesta_ia + "\n"
    print("\n" + "-"*30)