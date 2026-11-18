# Sistema de registro de eventos y errores

from datetime import datetime

def registrar_log(tipo, mensaje):
    """
    Registra un evento o error en el archivo logs.txt
    tipo: "ERROR", "INFO", "WARNING"
    """
    try:
        with open("logs.txt", "a", encoding="utf-8") as archivo:
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            archivo.write(f"[{fecha}] [{tipo}] {mensaje}\n")
    except Exception as e:
        print(f"Error al registrar el log: {e}")
