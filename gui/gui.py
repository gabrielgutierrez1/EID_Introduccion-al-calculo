import tkinter as tk
from tkinter import ttk
import os
import sys


PROYECTO_RAIZ = os.path.dirname(os.path.dirname(__file__))
if PROYECTO_RAIZ not in sys.path:
    sys.path.insert(0, PROYECTO_RAIZ)

from src.rut import validar_rut, obtener_digitos
from src.conicas import analizar_conica


def formatear_resultado_rut(resultado):
    lineas = []

    if not resultado["valido"] and "error" in resultado:
        lineas.append("RUT invalido")
        lineas.append(resultado["error"])
        return lineas

    lineas.append("Validacion del RUT")
    lineas.append(f"RUT limpio: {resultado['rut_limpio']}")
    lineas.append(f"Cuerpo: {resultado['cuerpo']}")
    lineas.append(f"Digito verificador ingresado: {resultado['dv_ingresado']}")
    lineas.append("")
    lineas.append("Procedimiento modulo 11:")

    for paso in resultado["calculo"]["pasos"]:
        lineas.append(
            f"{paso['digito']} x {paso['multiplicador']} = {paso['producto']}"
        )

    lineas.append(f"Suma de productos: {resultado['calculo']['suma']}")
    lineas.append(f"Resto de la division por 11: {resultado['calculo']['resto']}")
    lineas.append(f"11 - resto = {resultado['calculo']['valor']}")
    lineas.append(f"Digito verificador esperado: {resultado['dv_esperado']}")

    if resultado["valido"]:
        lineas.append("Conclusion: el RUT es valido.")
    else:
        lineas.append("Conclusion: el RUT no es valido.")

    return lineas

def formatear_resultado_conica(resultado):
    lineas = []
    lineas.append("")
    lineas.append("-" * 40)
    lineas.append("Construcción de la Cónica")
    lineas.append("-" * 40)

    for paso in resultado["coeficientes"]["pasos"]:
        lineas.append(paso)

    lineas.append("")
    lineas.append(f"Ecuación general: {resultado['ecuacion_general']}")
    lineas.append(f"Clasificación: {resultado['tipo']}")

    if "forma_canonica" in resultado and resultado["forma_canonica"]:
        transform = resultado["forma_canonica"]
        if transform.get("pasos"):
            lineas.append("")
            lineas.append("Transformación a forma canónica:")
            for paso in transform["pasos"]:
                lineas.append(paso)

        forma = transform.get("forma_canonica")
        if forma:
            lineas.append("")
            lineas.append(f"Forma canónica: {forma}")

    if "canonica_a_general" in resultado and resultado["canonica_a_general"]:
        inversa = resultado["canonica_a_general"]
        if inversa.get("pasos"):
            lineas.append("")
            lineas.append("Transformación inversa: forma canónica a general:")
            for paso in inversa["pasos"]:
                lineas.append(paso)

    return lineas

def graficar_conica(canvas, coeficientes):
    canvas.delete("all")
    canvas.update_idletasks()
    w = canvas.winfo_width()
    h = canvas.winfo_height()
    
    if w <= 1 or h <= 1:
        w, h = 600, 500 # Dimensiones por defecto
        
    A = coeficientes["A"]
    B = coeficientes["B"]
    C = coeficientes["C"]
    D = coeficientes["D"]
    E = coeficientes["E"]
    
    # Calcular centro aproximado para enfocar la vista
    cx = -C / (2 * A) if A != 0 else 0
    cy = -D / (2 * B) if B != 0 else 0
    
    rango = 15.0 # Unidades hacia cada lado desde el centro
    escala = min(w, h) / (rango * 2)
    
    def a_pixels(x, y):
        px = w / 2 + (x - cx) * escala
        py = h / 2 - (y - cy) * escala
        return px, py

    # Dibujar cuadrícula tenue (grid)
    for i in range(-int(rango), int(rango)+1):
        px, _ = a_pixels(cx + i, 0)
        canvas.create_line(px, 0, px, h, fill="#e6f2ff")
        _, py = a_pixels(0, cy + i)
        canvas.create_line(0, py, w, py, fill="#e6f2ff")

    # Dibujar ejes cartesianos (x=0, y=0)
    px1, py1 = a_pixels(cx - rango, 0)
    px2, py2 = a_pixels(cx + rango, 0)
    canvas.create_line(0, py1, w, py2, fill="#5b7cfa", width=2) # Eje X
    
    px1, py1 = a_pixels(0, cy - rango)
    px2, py2 = a_pixels(0, cy + rango)
    canvas.create_line(px1, 0, px2, h, fill="#5b7cfa", width=2) # Eje Y
    
    # Dibujar centro
    px_c, py_c = a_pixels(cx, cy)
    canvas.create_oval(px_c-4, py_c-4, px_c+4, py_c+4, fill="#38bdf8", outline="#2563eb")
    
    def dibujar_punto(x, y):
        if cx - rango <= x <= cx + rango and cy - rango <= y <= cy + rango:
            px, py = a_pixels(x, y)
            canvas.create_rectangle(px-1, py-1, px+1, py+1, fill="#7c3aed", outline="#7c3aed")
            
    # Escaneo detallado
    paso = (rango * 2) / 1200.0
    
    # Escaneo en X
    x = cx - rango
    while x <= cx + rango:
        c_eq = A*x*x + C*x + E
        if B == 0:
            if D != 0:
                dibujar_punto(x, -c_eq / D)
        else:
            delta = D*D - 4*B*c_eq
            if delta >= 0:
                raiz = delta ** 0.5
                dibujar_punto(x, (-D + raiz) / (2*B))
                dibujar_punto(x, (-D - raiz) / (2*B))
        x += paso

    # Escaneo en Y
    y = cy - rango
    while y <= cy + rango:
        c_eq = B*y*y + D*y + E
        if A == 0:
            if C != 0:
                dibujar_punto(-c_eq / C, y)
        else:
            delta = C*C - 4*A*c_eq
            if delta >= 0:
                raiz = delta ** 0.5
                dibujar_punto((-C + raiz) / (2*A), y)
                dibujar_punto((-C - raiz) / (2*A), y)
        y += paso


def iniciar_interfaz():
    color_fondo = "#eaf6ff"
    color_panel = "#f5f9ff"
    color_grafico = "#ffffff"
    color_texto = "#172554"
    color_header = "#1d4ed8"
    color_header_secundario = "#6d28d9"
    color_borde = "#bfdbfe"
    color_boton = "#7c3aed"
    color_boton_activo = "#2563eb"

    root = tk.Tk()
    root.title("EID N°1 - Introducción al Cálculo")
    root.geometry("1100x650")
    root.configure(bg=color_fondo)
    
    # Configuración de estilos ttk modernos
    style = ttk.Style()
    if 'clam' in style.theme_names():
        style.theme_use('clam')
        
    style.configure("TFrame", background=color_fondo)
    style.configure("TLabel", background=color_fondo, foreground=color_texto, font=("Segoe UI", 11))
    style.configure("TEntry", fieldbackground="#ffffff", foreground=color_texto, bordercolor=color_borde)
    style.configure(
        "Accent.TButton",
        background=color_boton,
        foreground="#ffffff",
        bordercolor=color_boton,
        focusthickness=2,
        focuscolor=color_borde,
        font=("Segoe UI", 11, "bold"),
        padding=7,
    )
    style.map(
        "Accent.TButton",
        background=[("active", color_boton_activo), ("pressed", color_header_secundario)],
        bordercolor=[("active", color_boton_activo), ("pressed", color_header_secundario)],
        foreground=[("disabled", "#dbeafe"), ("active", "#ffffff")],
    )
    
    # Header moderno
    header_frame = tk.Frame(root, bg=color_header, pady=15)
    header_frame.pack(fill="x")
    
    lbl_titulo = tk.Label(header_frame, text="Calculadora Analítica de Cónicas", font=("Segoe UI", 18, "bold"), bg=color_header, fg="white")
    lbl_titulo.pack()
    barra_acento = tk.Frame(root, bg=color_header_secundario, height=4)
    barra_acento.pack(fill="x")

    # Contenedor principal con padding
    main_frame = ttk.Frame(root, padding="20 20 20 20")
    main_frame.pack(fill="both", expand=True)

    # Barra superior para el input
    input_frame = ttk.Frame(main_frame)
    input_frame.pack(fill="x", pady=(0, 15))

    lbl_rut = ttk.Label(input_frame, text="RUT Chileno (Ej: 12.345.678-8):", font=("Segoe UI", 12))
    lbl_rut.pack(side="left", padx=(0, 10))

    entry_rut = ttk.Entry(input_frame, width=20, font=("Segoe UI", 12))
    entry_rut.pack(side="left", padx=(0, 15))

    btn_calcular = ttk.Button(input_frame, text="▶ Analizar y Graficar", style="Accent.TButton")
    btn_calcular.pack(side="left")

    # Contenedor dividido: Gráfico (Grande) y Resultados (Chico)
    paneles_frame = ttk.Frame(main_frame)
    paneles_frame.pack(fill="both", expand=True)

    # Lado Izquierdo: Gráfico (Se expande)
    frame_grafico = tk.LabelFrame(paneles_frame, text=" Representación Gráfica ", font=("Segoe UI", 12, "bold"), bg=color_grafico, fg=color_header, padx=10, pady=10, highlightbackground=color_borde, highlightcolor=color_borde)
    frame_grafico.pack(side="left", fill="both", expand=True, padx=(0, 15))

    canvas_grafico = tk.Canvas(frame_grafico, bg=color_grafico, highlightthickness=1, highlightbackground=color_borde)
    canvas_grafico.pack(fill="both", expand=True)

    # Lado Derecho: Resultados (Ancho fijo)
    frame_resultados = tk.LabelFrame(paneles_frame, text=" Memoria de Cálculo ", font=("Segoe UI", 12, "bold"), bg=color_panel, fg=color_header_secundario, padx=10, pady=10, highlightbackground=color_borde, highlightcolor=color_borde)
    frame_resultados.pack(side="right", fill="y")

    # Usamos un ancho menor (width=45) para darle prioridad al gráfico
    txt_resultados = tk.Text(frame_resultados, wrap="word", state="disabled", font=("Consolas", 10), width=45, bg="#f8fbff", fg=color_texto, relief="flat", padx=10, pady=10, highlightthickness=1, highlightbackground=color_borde)
    txt_resultados.pack(fill="both", expand=True)

    def mostrar_rut():
        rut_ingresado = entry_rut.get()
        resultado = validar_rut(rut_ingresado)

        lineas_mostrar = formatear_resultado_rut(resultado)
        
        if resultado["valido"]:
            digitos = obtener_digitos(resultado["cuerpo"])
            resultado_conica = analizar_conica(digitos, resultado["dv_ingresado"])
            lineas_mostrar.extend(formatear_resultado_conica(resultado_conica))
            graficar_conica(canvas_grafico, resultado_conica["coeficientes"])
        else:
            canvas_grafico.delete("all")

        txt_resultados.configure(state="normal")
        txt_resultados.delete("1.0", tk.END)
        txt_resultados.insert(tk.END, "\n".join(lineas_mostrar))
        txt_resultados.configure(state="disabled")

    btn_calcular.config(command=mostrar_rut)
    entry_rut.focus_set()

    # Redibujar la gráfica si la ventana cambia de tamaño
    # Guardamos los últimos coeficientes para redibujar
    root.mainloop()

if __name__ == "__main__":
    iniciar_interfaz()