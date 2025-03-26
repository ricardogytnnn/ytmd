import yt_dlp
import requests
from mutagen.id3 import ID3, TIT2, TPE1, APIC
from mutagen.mp3 import MP3
import os
from config import DOWNLOAD_FOLDER, FFMPEG_PATH

def descargar_audio(url):
    """ Descarga el audio en MP3 y devuelve la información de la canción. Si el archivo ya existe, no lo descarga nuevamente. """
    opciones = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
        'ffmpeg_location': FFMPEG_PATH,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with yt_dlp.YoutubeDL(opciones) as ydl:
        # Extraer la información de la canción sin descargarla todavía
        info = ydl.extract_info(url, download=False)
        
        archivo_mp3 = f"{info['title']}.mp3"  # Nombre del archivo basado en el título
        archivo_mp3_ruta = os.path.join(DOWNLOAD_FOLDER, archivo_mp3)

        # Verificar si el archivo ya existe
        if os.path.exists(archivo_mp3_ruta):
            print(f"✅ El archivo '{archivo_mp3}' ya existe. Usando el archivo existente.")
            return archivo_mp3, info.get("title", "Desconocido"), info.get("uploader", "Desconocido"), info.get("duration", 0), info.get("thumbnail", "")

        # Si el archivo no existe, descargarlo
        ydl.download([url])

        # Obtener metadatos y agregar portada
        titulo = info.get("title", "Desconocido")
        canal = info.get("uploader", "Desconocido")
        duracion = info.get("duration", 0)  # Duración en segundos
        miniatura = info.get("thumbnail", "")  # URL de la miniatura
        
        # Agregar metadatos al archivo descargado
        agregar_metadatos(archivo_mp3_ruta, titulo, canal, miniatura)

    return archivo_mp3, titulo, canal, duracion, miniatura

def agregar_metadatos(archivo_mp3, titulo, canal, portada_url):
    """ Agrega metadatos y la portada al MP3. """
    try:
        audio = MP3(archivo_mp3, ID3=ID3)
        if audio.tags is None:
            audio.add_tags()

        audio.tags["TIT2"] = TIT2(encoding=3, text=titulo)
        audio.tags["TPE1"] = TPE1(encoding=3, text=canal)

        if portada_url:
            portada_data = requests.get(portada_url).content
            audio.tags.add(APIC(
                encoding=3,
                mime="image/jpeg",
                type=3,
                desc="Cover",
                data=portada_data
            ))

        audio.save()
    
    except Exception as e:
        print(f"❌ Error al agregar metadatos: {e}")
