import io
from gtts import gTTS
from pydub import AudioSegment

CHUNK_SIZE = 2000

def generar_audio_comprimido(texto, archivo_salida, callback_progreso=None):
    """Genera audio con compresión optimizada"""
    try:
        chunks = [texto[i:i+CHUNK_SIZE] for i in range(0, len(texto), CHUNK_SIZE)]
        audio_final = AudioSegment.empty()
        
        for i, chunk in enumerate(chunks):
            try:
                # Generar audio del fragmento
                tts = gTTS(text=chunk, lang='es', slow=False, lang_check=False)
                buffer = io.BytesIO()
                tts.write_to_fp(buffer)
                buffer.seek(0)
                
                # Procesamiento de audio con compresión
                audio = AudioSegment.from_file(buffer, format="mp3")
                audio = audio.speedup(playback_speed=1.03)
                audio = audio.fade_in(50).fade_out(50)
                
                # Aplicar compresión de dinámica
                compressed_audio = audio.compress_dynamic_range()
                
                audio_final += compressed_audio
                if callback_progreso:
                    callback_progreso(i + 1, len(chunks))
                    
            except Exception as e:
                raise RuntimeError(f"Error en fragmento {i+1}: {str(e)}")
        
        # Exportar con máxima compresión
        try:
            audio_final.export(
                archivo_salida,
                format="mp3",
                bitrate="48k",  # Reducir bitrate
                parameters=[
                    "-q:a", "2",  # Calidad de compresión (0-9, 0=max)
                    "-ac", "1"    # Mono en vez de estéreo
                ]
            )
        except Exception as e:
            raise RuntimeError(f"Error al exportar audio: {str(e)}")
            
    except Exception as e:
        raise RuntimeError(f"Error general en generación de audio: {str(e)}")