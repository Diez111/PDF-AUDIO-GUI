import os
import zipfile

def comprimir_audio(mp3_path):
    try:
        if not os.path.exists(mp3_path):
            raise FileNotFoundError(f"Archivo no encontrado: {mp3_path}")
        
        zip_path = os.path.splitext(mp3_path)[0] + ".zip"
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(mp3_path, arcname=os.path.basename(mp3_path))
        
        os.remove(mp3_path)
        return zip_path
    
    except Exception as e:
        if 'zip_path' in locals() and os.path.exists(zip_path):
            os.remove(zip_path)
        raise RuntimeError(f"Error en compresión: {str(e)}")