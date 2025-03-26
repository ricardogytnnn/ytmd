import os
import threading
from flask import Flask, render_template, request, send_from_directory
from config import DOWNLOAD_FOLDER
from descargador import descargar_audio
from file_manager import eliminar_archivo  # Usamos la nueva función

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    """ Página principal para ingresar la URL de YouTube y mostrar los datos de la canción. """
    if request.method == 'POST':
        url = request.form['url']
        if url:
            # Llamada a la función para descargar y obtener los metadatos
            archivo_mp3, titulo, canal, duracion, miniatura = descargar_audio(url)
            
            # Pasar los datos a la plantilla
            return render_template('index.html', 
                                   archivo=archivo_mp3, 
                                   titulo=titulo, 
                                   canal=canal, 
                                   duracion=duracion, 
                                   miniatura=miniatura)

    return render_template('index.html')

@app.route('/downloads/<filename>')
def download(filename):
    """ Ruta para descargar los archivos MP3. """
    archivo_path = os.path.join(DOWNLOAD_FOLDER, filename)
    
    # Iniciar el proceso de eliminación del archivo en un hilo separado
    threading.Thread(target=eliminar_archivo, args=(archivo_path,)).start()
    
    return send_from_directory(DOWNLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
