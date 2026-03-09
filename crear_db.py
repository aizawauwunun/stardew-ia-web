import sqlite3
import os

RUTA_BASE = r"C:\Users\pizar\Stardew_IA_Project"
DB_PATH = os.path.join(RUTA_BASE, "stardew_saas.db")

def inicializar_saas_limites():
    conexion = sqlite3.connect(DB_PATH)
    cursor = conexion.cursor()

    print("--- Configurando SaaS con Límites: 15/min y 100/día ---")

    # TABLA DE USUARIOS
    # ultima_conexion: Para resetear el contador diario
    # mensajes_hoy: Contador para el límite de 100
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id TEXT PRIMARY KEY,
            password_hash TEXT NOT NULL,
            plan TEXT DEFAULT 'free',
            mensajes_hoy INTEGER DEFAULT 0,
            ultima_conexion DATE,
            fecha_vencimiento DATE
        )
    ''')

    # TABLA DE MEMORIA DE CHAT
    # Usaremos la columna 'fecha' para contar los mensajes en el último minuto
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS memoria_chat (
            id_mensaje INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT,
            npc TEXT,
            mensaje TEXT,
            respuesta_ia TEXT,
            fecha TIMESTAMP DEFAULT (datetime('now', 'localtime'))
        )
    ''')

    conexion.commit()
    conexion.close()
    print(f"--- Base de datos lista en: {DB_PATH} ---")

if __name__ == "__main__":
    inicializar_saas_limites()