```markdown
# 📚 Conversor de PDF a Audiolibro (Python + Rust)

## 🐍 Versión Python con GUI

### 📋 Requisitos
```bash
sudo apt install ffmpeg python3-tk
pip install PyPDF2 gtts pydub ttkbootstrap
```

### 🚀 Ejecución
```bash
python3 main.py
```

## 🦀 Versión Rust (CLI)

### 📋 Requisitos para Linux Debian/Ubuntu
```bash
# Dependencias del sistema
sudo apt update
sudo apt install -y build-essential cmake pkg-config libssl-dev

# Instalar Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env

# Dependencias adicionales para PDF
sudo apt install -y libfontconfig1-dev libxcb-shape0-dev libxcb-xfixes0-dev
```

### 🚀 Instalación y Ejecución
```bash
git clone https://github.com/Diez111/PDF-AUDIO-GUI.git
cd PDF-AUDIO-GUI/rust_version

# Compilar el proyecto
cargo build --release

# Ejecutar (modo interactivo)
./target/release/pdf_to_speech

# Ejecutar con parámetros
./target/release/pdf_to_speech \
  --pdf_dir ../PDFs/ \
  --output_dir ../AUDIOS/ \
  --lang es
```

### 🛠️ Explicación del Código Rust

#### Estructura Principal
```rust
struct Args {
    pdf_dir: PathBuf,     // Directorio de entrada para PDFs
    output_dir: PathBuf,  // Directorio de salida para audios
    lang: Language,       // Idioma (es/en)
}
```
- Parámetros configurables via línea de comandos
- Soporte para español e inglés

#### Flujo de Trabajo
1. **Extracción de texto** (`extract_pdf_text`):
   - Usa la librería `lopdf` para leer PDFs
   - Limpia formato y guiones de división de palabras

2. **Procesamiento de texto** (`split_text`):
   - Divide el texto en chunks de 200 caracteres
   - Evita límites de tamaño de peticiones HTTP

3. **Síntesis de voz** (`generate_speech`):
   - Usa la API pública de Google Text-to-Speech
   - Descarga fragmentos de audio en formato MP3
   - Combina todos los fragmentos en un solo archivo

#### Consideraciones Importantes
- Requiere conexión a Internet para la síntesis de voz
- Los PDFs deben contener texto (no funciona con documentos escaneados)
- Límite práctico de ~200 páginas por PDF

### 📄 Opciones de Ejecución
```bash
# Mostrar ayuda
./pdf_to_speech --help

# Especificar directorios personalizados
./pdf_to_speech -p /ruta/pdfs -o /ruta/salida

# Generar en inglés
./pdf_to_speech --lang en
```

## 📂 Estructura del Proyecto (Actualizada)
```
.
├── python_gui/       # Versión Python con GUI
│   ├── main.py
│   └── ... 
├── rust_cli/         # Versión Rust CLI
│   ├── src/
│   ├── Cargo.toml
│   └── ...
├── PDFs/             # PDFs de entrada
├── AUDIOLIBROS/      # Audios generados
└── README.md         # Este archivo
```

## ⚠️ Notas Importantes
1. La versión Rust es más rápida pero requiere compilación
2. El uso de la API de Google TTS está sujeto a:
   - Límites de uso no documentados
   - Posibles cambios en la URL de la API
   - Consideraciones legales para uso comercial
3. Para producción considerar:
   - Usar un servicio TTS profesional
   - Implementar manejo de errores robusto
   - Añadir límites de tasa de solicitudes
```
