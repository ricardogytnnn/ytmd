import os
import time

def eliminar_archivo(archivo_path):
    """ Función para eliminar el archivo después de un tiempo. """
    print(f"[INFO] Esperando 20 segundos antes de eliminar el archivo: {archivo_path}")
    time.sleep(20)  # Esperamos 20 segundos
    try:
        os.remove(archivo_path)
        print(f"[INFO] Archivo {archivo_path} eliminado exitosamente.")
    except Exception as e:
        print(f"[ERROR] No se pudo eliminar el archivo: {e}")
