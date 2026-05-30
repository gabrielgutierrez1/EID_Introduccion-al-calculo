import tkinter as tk
from tkinter import ttk

class AplicacionCalculo:
    def __init__(self, root):
        self.root = root
        self.root.title("EID N°1 - Calculadora de Cónicas")
        self.root.geometry("650x550")
        
        # Paleta de colores claros
        self.color_fondo = "#f4f6f9"
        self.color_texto = "#2c3e50"
        self.color_titulo = "#2980b9"
        self.color_subtitulo = "#7f8c8d"
        self.color_boton = "#3498db"
        self.color_boton_hover = "#2980b9"
        
        self.root.configure(bg=self.color_fondo)
        self.root.resizable(False, False)

        self.configurar_estilos()
        self.crear_widgets()

    def configurar_estilos(self):
        style = ttk.Style()
        style.theme_use("clam")

        # Estilo para frames
        style.configure("TFrame", background=self.color_fondo)
        
        # Estilo para etiquetas
        style.configure("TLabel", background=self.color_fondo, foreground=self.color_texto, font=("Segoe UI", 11))
        style.configure("Titulo.TLabel", foreground=self.color_titulo, font=("Segoe UI", 18, "bold"))
        style.configure("Subtitulo.TLabel", foreground=self.color_subtitulo, font=("Segoe UI", 10, "italic"))

        # Estilo para el Entry
        style.configure("TEntry", fieldbackground="#ffffff", foreground=self.color_texto, font=("Courier", 12))

        # Estilo para botones
        style.configure("TButton", font=("Segoe UI", 11, "bold"), background=self.color_boton, foreground="#ffffff", padding=6)
        style.map("TButton", background=[("active", self.color_boton_hover)])
        
        # Estilo para LabelFrame
        style.configure("TLabelframe", background=self.color_fondo)
        style.configure("TLabelframe.Label", background=self.color_fondo, foreground=self.color_titulo, font=("Segoe UI", 11, "bold"))

    def crear_widgets(self):
        # --- HEADER ---
        frame_header = ttk.Frame(self.root)
        frame_header.pack(pady=(20, 10), fill="x")

        lbl_titulo = ttk.Label(frame_header, text="Análisis de Cónicas por RUT", style="Titulo.TLabel")
        lbl_titulo.pack()

        lbl_sub = ttk.Label(frame_header, text="Evaluación Integrada de Desempeño N°1 - MAT1186", style="Subtitulo.TLabel")
        lbl_sub.pack(pady=(5, 0))

        # --- SECCIÓN DE ENTRADA ---
        frame_input = ttk.Frame(self.root)
        frame_input.pack(pady=15)

        lbl_instruccion = ttk.Label(frame_input, text="RUT Chileno:")
        lbl_instruccion.grid(row=0, column=0, padx=10, pady=10)

        self.entry_rut = ttk.Entry(frame_input, width=18, justify="center")
        self.entry_rut.grid(row=0, column=1, padx=10, pady=10)
        self.entry_rut.insert(0, "Ej: 21.929.009-8")
        
        # Efecto placeholder
        self.entry_rut.bind("<FocusIn>", self.limpiar_placeholder)
        self.entry_rut.bind("<FocusOut>", self.poner_placeholder)

        self.btn_analizar = ttk.Button(frame_input, text="Analizar Cónica", command=self.simular_analisis)
        self.btn_analizar.grid(row=0, column=2, padx=10, pady=10)

        # --- SECCIÓN DE RESULTADOS ---
        frame_resultados = ttk.LabelFrame(self.root, text=" Hoja de Resultados ")
        frame_resultados.pack(pady=10, padx=25, fill="both", expand=True)

        # Text area similar a una hoja de papel (blanco)
        self.txt_pizarra = tk.Text(
            frame_resultados, 
            bg="#ffffff", 
            fg="#333333", 
            font=("Consolas", 11), 
            wrap="word",
            state="disabled",
            padx=10, 
            pady=10,
            relief="solid",
            borderwidth=1
        )
        self.txt_pizarra.pack(fill="both", expand=True, padx=5, pady=5)

    def limpiar_placeholder(self, event):
        if self.entry_rut.get() == "Ej: 21.929.009-8":
            self.entry_rut.delete(0, tk.END)

    def poner_placeholder(self, event):
        if not self.entry_rut.get():
            self.entry_rut.insert(0, "Ej: 21.929.009-8")

    def escribir_en_pizarra(self, texto):
        self.txt_pizarra.config(state="normal")
        self.txt_pizarra.insert(tk.END, texto + "\n")
        self.txt_pizarra.see(tk.END)
        self.txt_pizarra.config(state="disabled")

    def limpiar_pizarra(self):
        self.txt_pizarra.config(state="normal")
        self.txt_pizarra.delete(1.0, tk.END)
        self.txt_pizarra.config(state="disabled")

    def simular_analisis(self):
        # Esta función es solo visual, luego se conectará con el código real
        self.limpiar_pizarra()
        rut = self.entry_rut.get()
        if rut == "Ej: 21.929.009-8" or not rut:
            self.escribir_en_pizarra("⚠️ Por favor, ingrese un RUT válido.")
            return

        self.escribir_en_pizarra(f"> Procesando RUT: {rut}")
        self.escribir_en_pizarra("...")
        self.escribir_en_pizarra("[+] Validando RUT (Módulo 11) ... [OK]")
        self.escribir_en_pizarra("[+] Extrayendo dígitos: d1, d2, d3... d8")
        self.escribir_en_pizarra("\n> Construyendo ecuación general:")
        self.escribir_en_pizarra("  Ax² + By² + Cx + Dy + E = 0")
        self.escribir_en_pizarra("\n> Clasificando cónica...")
        self.escribir_en_pizarra("\n[RESULTADO PENDIENTE DE CONECTAR]")


def iniciar_interfaz():
    root = tk.Tk()
    app = AplicacionCalculo(root)
    root.mainloop()

if __name__ == "__main__":
    iniciar_interfaz()
