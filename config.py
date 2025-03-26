import os

# Carpeta de descargas
DOWNLOAD_FOLDER = 'static/downloads'  # Ruta donde se almacenan los archivos descargados
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# Ruta de FFmpeg (ajústala según tu sistema)
FFMPEG_PATH = r"C:\ffmpeg\bin"
