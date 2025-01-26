import re

def limpiar_texto(texto):
    """Limpia y normaliza el texto extraído"""
    sustituciones = {
        'Ã¡': 'á', 'Ã©': 'é', 'Ã­': 'í', 'Ã³': 'ó', 'Ãº': 'ú',
        'Ã±': 'ñ', 'Ã¼': 'ü', 'Â¡': '¡', 'Â¿': '¿',
        '\ufeff': '', '\xad': '', '\u200b': ''
    }
    
    for incorrecto, correcto in sustituciones.items():
        texto = texto.replace(incorrecto, correcto)
    
    patrones = [
        (r'(\w+)-\n(\w+)', r'\1\2'),        # Unir palabras divididas
        (r'(?<!\n)\n(?!\n)', ' '),          # Reemplazar saltos simples
        (r'\n{2,}', '\n\n'),                # Normalizar saltos múltiples
        (r'[^\S\n]+', ' '),                 # Eliminar espacios extraños
        (r'\s*([,.:;!?])\s*', r'\1 '),      # Espaciado después de puntuación
        (r'([a-zñáéíóú])([A-ZÁÉÍÓÚ])', r'\1. \2'),  # Puntos entre oraciones
        (r'\s+', ' '),                      # Espacios múltiples a uno
        (r'^[ \t]+|[ \t]+$', '')            # Eliminar espacios al inicio/final
    ]
    
    for patron, reemplazo in patrones:
        texto = re.sub(patron, reemplazo, texto, flags=re.MULTILINE)
    
    return texto.strip()