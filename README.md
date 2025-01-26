# PDF-AUDIO-GUI
```markdown
# 📚 Conversor de PDF a Audiolibro

Convierte archivos PDF a audiolibros en formato MP3 con una interfaz gráfica moderna.

![Captura de la Interfaz](gui_screenshot.png) <!-- Reemplaza con tu imagen -->

## 📋 Requisitos

### Dependencias
- **Python 3.10+**
- **FFmpeg** (requerido por pydub)
```bash
# Para Linux (Debian/Ubuntu):
sudo apt install ffmpeg python3-tk
```

### Librerías Python
```bash
pip install PyPDF2 gtts pydub ttkbootstrap
```

## 🚀 Cómo Usar

1. **Clona el repositorio:**
```bash
git clone https://github.com/tu-usuario/pdf-a-audiolibro.git
cd pdf-a-audiolibro
```

2. **Coloca tus PDFs:**
   - Crea una carpeta `PDFs` en el directorio principal
   - Copia tus archivos PDF a esta carpeta

3. **Ejecuta la aplicación:**
```bash
python3 main.py
```

4. **Interfaz Gráfica:**
   - Selecciona un PDF de la lista
   - Haz clic en "Convertir a Audio"
   - El audiolibro se guardará en `AUDIOLIBROS/`

## 🖥️ Características de la GUI
- Interfaz moderna con modo oscuro
- Listado interactivo de PDFs con tamaños
- Barra de progreso animada
- Notificaciones integradas
- Botones con efectos hover
- Diseño responsive

## 📂 Estructura del Proyecto
```
.
├── PDFs/                 # PDFs de entrada
├── AUDIOLIBROS/          # Audios generados
├── main.py               # Programa principal
├── pdf_utils.py          # Manejo de PDFs
├── text_processing.py    # Procesamiento de texto
├── audio_generation.py   # Generación de audio
├── README.md             # Este archivo
└── requirements.txt      # Dependencias
```

## 📸 Captura de la Interfaz
<!-- Reemplaza 'gui_screenshot.png' con tu propia captura -->
![Interfaz Gráfica Moderna](![image](https://github.com/user-attachments/assets/c6181d29-2ae8-44e1-80fa-60d128a2a6c1)
)

## 📄 Licencia
MIT License © 2024 [Tu Nombre]

```

Para usar este README:
1. Reemplaza `tu-usuario` en el URL del clone
2. Agrega tu propia captura de pantalla como `gui_screenshot.png`
3. Personaliza la sección de licencia con tu nombre
4. Si agregas más características, actualiza las secciones correspondientes

El README incluye:
- Instrucciones claras de instalación
- Demo visual con imagen
- Estructura de archivos
- Descripción de funcionalidades
- Compatibilidad con temas oscuros
- Formato amigable con emojis
- Sección para créditos/licencia
