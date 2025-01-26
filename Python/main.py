import sys
import os
import threading
import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as ttk
from pdf_utils import listar_pdfs, extraer_texto
from text_processing import limpiar_texto
from audio_generation import generar_audio_comprimido, CHUNK_SIZE

# Configuración de tema oscuro
THEME = 'darkly'
ICON_PATH = os.path.join(os.path.dirname(__file__), 'icon.ico')

class ModernConverter(ttk.Window):
    def __init__(self):
        super().__init__(themename=THEME)
        self.title("PDF a Audiolibro")
        self.geometry("800x600")
        self.create_widgets()
        self.running = False
        self.progress_value = 0
        
        if os.path.exists(ICON_PATH):
            self.iconbitmap(ICON_PATH)
        
        # Cargar PDFs al iniciar
        self.load_pdfs()

    def create_widgets(self):
        """Crea los componentes de la interfaz"""
        # Frame principal
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Cabecera
        header = ttk.Frame(main_frame)
        header.pack(fill=tk.X, pady=10)
        
        ttk.Label(header, 
                text="📚 PDF a Audiolibro", 
                font=('Helvetica', 20, 'bold'),
                bootstyle="light").pack(side=tk.LEFT)

        # Lista de PDFs
        self.pdf_list = ttk.Treeview(main_frame,
                                   columns=('size',),
                                   show='tree headings',
                                   selectmode='browse',
                                   bootstyle="dark")
        self.pdf_list.heading('#0', text='Archivo PDF', anchor=tk.W)
        self.pdf_list.heading('size', text='Tamaño')
        self.pdf_list.column('#0', width=400, stretch=tk.YES)
        self.pdf_list.column('size', width=150, anchor=tk.E)
        self.pdf_list.pack(fill=tk.BOTH, expand=True, pady=10)

        # Barra de progreso
        self.progress = ttk.Progressbar(main_frame,
                                      bootstyle="success-striped",
                                      maximum=100,
                                      mode='determinate')
        self.progress.pack(fill=tk.X, pady=20)

        # Botones
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        self.btn_convert = ttk.Button(btn_frame,
                                    text="Convertir a Audio",
                                    bootstyle="success",
                                    command=self.start_conversion)
        self.btn_convert.pack(side=tk.RIGHT, ipadx=20, ipady=5)

        # Etiqueta de estado
        self.lbl_status = ttk.Label(main_frame,
                                  text="Listo para convertir",
                                  bootstyle="light")
        self.lbl_status.pack(side=tk.BOTTOM, fill=tk.X)

    def load_pdfs(self):
        """Carga los PDFs en la lista"""
        try:
            pdfs = listar_pdfs()
            self.pdf_list.delete(*self.pdf_list.get_children())
            
            for pdf in pdfs:
                name = os.path.basename(pdf)
                size = f"{os.path.getsize(pdf)/1024/1024:.1f} MB"
                self.pdf_list.insert('', tk.END, text=name, values=(size,), iid=pdf)
                
            if not pdfs:
                self.lbl_status.config(text="No se encontraron PDFs en la carpeta 'PDFs'")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error cargando PDFs:\n{str(e)}")

    def update_progress(self, value, total):
        """Actualiza la barra de progreso"""
        self.progress_value = int((value / total) * 100)
        self.progress['value'] = self.progress_value
        self.lbl_status.config(text=f"Procesando: {self.progress_value}%")
        self.update()

    def start_conversion(self):
        """Inicia el proceso de conversión"""
        if not self.running:
            selected = self.pdf_list.selection()
            if not selected:
                messagebox.showwarning("Selección requerida", "Por favor selecciona un PDF")
                return
                
            self.running = True
            self.btn_convert.config(state=tk.DISABLED)
            
            thread = threading.Thread(target=self.conversion_process, args=(selected[0],), daemon=True)
            thread.start()

    def conversion_process(self, pdf_path):
        """Proceso de conversión en segundo plano"""
        try:
            # Paso 1: Extraer texto
            self.lbl_status.config(text="Extrayendo texto...")
            texto = extraer_texto(pdf_path)
            
            if not texto:
                messagebox.showerror("Error", "No se pudo extraer texto del PDF")
                return
                
            # Paso 2: Limpiar texto
            self.lbl_status.config(text="Limpiando texto...")
            texto_limpio = limpiar_texto(texto)
            
            # Paso 3: Generar audio
            output_dir = "AUDIOLIBROS"
            os.makedirs(output_dir, exist_ok=True)
            nombre_base = os.path.splitext(os.path.basename(pdf_path))[0]
            archivo_salida = os.path.join(output_dir, f"{nombre_base}_audio.mp3")
            
            def progress_callback(current, total):
                self.update_progress(current, total)
                
            generar_audio_comprimido(texto_limpio, archivo_salida, progress_callback)
            
            # Finalización
            self.lbl_status.config(text="¡Conversión completada!")
            messagebox.showinfo("Éxito", f"Audio generado en:\n{archivo_salida}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en la conversión:\n{str(e)}")
        finally:
            self.running = False
            self.btn_convert.config(state=tk.NORMAL)
            self.progress['value'] = 0
            self.load_pdfs()

if __name__ == "__main__":
    app = ModernConverter()
    app.mainloop()