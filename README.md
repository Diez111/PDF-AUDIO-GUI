# PDF-AUDIO-GUI
```markdown
# 📚 Conversor de PDF a Audiolibro

Convierte archivos PDF a audiolibros en formato MP3 con una interfaz gráfica moderna.

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
[git clone https://github.com/tu-usuario/pdf-a-audiolibro.git](https://github.com/Diez111/PDF-AUDIO-GUI.git)
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
GPL3 License © 2025 [Lautaro Agustin Diez]

```
