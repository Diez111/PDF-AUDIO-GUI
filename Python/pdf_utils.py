import os
from PyPDF2 import PdfReader

def listar_pdfs():
    """Lista todos los PDFs en la carpeta PDFs"""
    pdf_dir = "PDFs"
    if not os.path.exists(pdf_dir):
        raise FileNotFoundError(f"No existe la carpeta '{pdf_dir}'")
    if not os.path.isdir(pdf_dir):
        raise NotADirectoryError(f"'{pdf_dir}' no es una carpeta válida")
    
    return [
        os.path.join(pdf_dir, archivo)
        for archivo in os.listdir(pdf_dir)
        if archivo.lower().endswith('.pdf') and os.path.isfile(os.path.join(pdf_dir, archivo))
    ]

def seleccionar_pdf_cli(pdfs):
    """Versión CLI para selección de PDF (usada en la GUI)"""
    print("\n📚 PDFs encontrados en carpeta PDFs:")
    for i, pdf in enumerate(pdfs, 1):
        print(f" [{i}] {os.path.basename(pdf)}")
    
    while True:
        try:
            seleccion = int(input("\n🔢 Ingrese el número del PDF a convertir: "))
            if 1 <= seleccion <= len(pdfs):
                return pdfs[seleccion - 1]
            print("❌ Número fuera de rango")
        except ValueError:
            print("❌ Ingrese solo números")

def extraer_texto(ruta_pdf):
    """Extrae texto de un archivo PDF"""
    texto = ""
    try:
        with open(ruta_pdf, 'rb') as archivo:
            lector = PdfReader(archivo)
            for pagina in lector.pages:
                texto_pagina = pagina.extract_text()
                if texto_pagina:
                    texto += f"{texto_pagina}\n"
        return texto.strip() if texto.strip() else None
    except Exception as e:
        raise RuntimeError(f"Error al leer PDF: {str(e)}")