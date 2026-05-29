import tkinter as tk
from tkinter import ttk

def iniciar_interfaz():
    root = tk.Tk()
    root.title("EID N°1 - Introducción al Cálculo")
    root.geometry("500x450")
    
    # Configuración de estilos básicos
    root.configure(padx=20, pady=20)

    # Título principal
    lbl_titulo = tk.Label(root, text="Calculadora de Cónicas por RUT", font=("Helvetica", 16, "bold"))
    lbl_titulo.pack(pady=(0, 20))

    # Marco para la entrada de datos
    frame_entrada = tk.Frame(root)
    frame_entrada.pack(pady=10, fill="x")

    lbl_rut = tk.Label(frame_entrada, text="Ingrese RUT (Ej: 21.929.009-8):", font=("Helvetica", 11))
    lbl_rut.pack(side="left", padx=(0, 10))

    entry_rut = tk.Entry(frame_entrada, width=20, font=("Helvetica", 11))
    entry_rut.pack(side="left", expand=True, fill="x")

    # Botón de cálculo (sin funcionalidad aún, como solicitaste)
    btn_calcular = tk.Button(root, text="Analizar RUT y Cónica", font=("Helvetica", 11, "bold"), bg="#4CAF50", fg="white", relief="flat", pady=5)
    btn_calcular.pack(pady=20, fill="x")

    # Marco para mostrar resultados
    frame_resultados = tk.LabelFrame(root, text=" Resultados del Análisis ", font=("Helvetica", 11, "bold"), padx=10, pady=10)
    frame_resultados.pack(fill="both", expand=True)

    # Text box para mostrar los resultados detallados más adelante
    txt_resultados = tk.Text(frame_resultados, wrap="word", state="disabled", font=("Courier", 10))
    txt_resultados.pack(fill="both", expand=True)

    # Iniciar el bucle principal de la aplicación
    root.mainloop()

if __name__ == "__main__":
    iniciar_interfaz()
