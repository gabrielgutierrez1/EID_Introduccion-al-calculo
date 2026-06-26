import tkinter as tk
from tkinter import ttk
import os
import sys


PROYECTO_RAIZ = os.path.dirname(os.path.dirname(__file__))
if PROYECTO_RAIZ not in sys.path:
    sys.path.insert(0, PROYECTO_RAIZ)

from src.rut import validar_rut, obtener_digitos
from src.conicas import analizar_conica
from src.funciones_por_tramos import analizar_funcion_por_tramos, formatear_numero
from .graficos import (
    graficar_conica,
    graficar_funcion_por_tramos,
    obtener_vista_conica,
    obtener_vista_tramos,
)


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


def formatear_resultado_tramos(resultado):
    lineas = []
    lineas.append("")
    lineas.append("-" * 40)
    lineas.append("Análisis de Función por Tramos")
    lineas.append("-" * 40)

    funcion = resultado["funcion"]
    caso = resultado["caso"]
    a = resultado["a"]

    lineas.append(f"Caso detectado: {caso['nombre']}")
    lineas.append(f"Punto crítico de análisis: a = {a}")
    lineas.append("")
    lineas.append("Tramos de la función:")
    for tramo in funcion["tramos"]:
        lineas.append(f"  • f(x) = {tramo['expresion']} si {tramo['condicion']}")

    if funcion["simplificada"]:
        lineas.append(f"Fórmula simplificada: {funcion['simplificada']}")

    lineas.append("")
    lineas.append("Memoria de cálculo:")
    for paso in resultado["pasos"]:
        lineas.append(f"  - {paso}")

    lineas.append("")
    lineas.append("Tabla de valores cerca de x = a:")
    lineas.append(f" {'Lado':<10} | {'x':<12} | {'f(x)':<12}")
    lineas.append("-" * 40)
    for fila in resultado["tabla"]:
        lineas.append(f" {fila['lado']:<10} | {fila['x_texto']:<12} | {fila['f_x_texto']:<12}")

    lineas.append("")
    lineas.append("Respuestas de la defensa:")
    lineas.append("-" * 40)

    lim = resultado["limites"]
    cont = resultado["continuidad"]

    def_izq = formatear_numero(lim["izquierda"])
    def_der = formatear_numero(lim["derecha"])
    def_ex = "Existe y vale " + formatear_numero(lim["valor"]) if lim["existe"] else "No existe"
    def_val = formatear_numero(cont["valor_en_a"])
    def_cont = "Continua" if cont["es_continua"] else "Discontinua"
    def_tipo = cont["tipo_discontinuidad"]
    def_just = cont["justificacion"]

    lineas.append(f"• Límite por la izquierda: {def_izq}")
    lineas.append(f"• Límite por la derecha: {def_der}")
    lineas.append(f"• Conclusión sobre el límite: {def_ex}")
    lineas.append(f"• Valor de la función en el punto: {def_val}")
    lineas.append(f"• Conclusión sobre continuidad: {def_cont}")
    lineas.append(f"• Tipo de discontinuidad: {def_tipo}")
    lineas.append(f"• Justificación: {def_just}")

    return lineas


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
    root.geometry("1100x670")
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
    style.configure(
        "Tool.TButton",
        background="#dbeafe",
        foreground=color_texto,
        bordercolor=color_borde,
        font=("Segoe UI", 10, "bold"),
        padding=(8, 4),
    )
    style.map(
        "Tool.TButton",
        background=[("active", "#bfdbfe"), ("pressed", "#93c5fd")],
        foreground=[("active", color_texto)],
    )

    # Estilos modernos para Notebook y Pestañas
    style.configure("TNotebook", background=color_fondo, borderwidth=0)
    style.configure("TNotebook.Tab", background=color_borde, foreground=color_texto, font=("Segoe UI", 11, "bold"), padding=(15, 5))
    style.map("TNotebook.Tab",
              background=[("selected", color_header), ("active", color_boton)],
              foreground=[("selected", "#ffffff"), ("active", "#ffffff")])
    
    # Header moderno
    header_frame = tk.Frame(root, bg=color_header, pady=15)
    header_frame.pack(fill="x")
    
    lbl_titulo = tk.Label(header_frame, text="Calculadora de Cónicas y Funciones por Tramo", font=("Segoe UI", 18, "bold"), bg=color_header, fg="white")
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

    # Notebook para organizar por pestañas
    notebook = ttk.Notebook(main_frame)
    notebook.pack(fill="both", expand=True)

    tab_conicas = ttk.Frame(notebook)
    tab_tramos = ttk.Frame(notebook)
    notebook.add(tab_conicas, text=" Cónicas ")
    notebook.add(tab_tramos, text=" Funciones por Tramo ")

    # Pestaña 1: Cónicas
    paneles_frame = ttk.Frame(tab_conicas)
    paneles_frame.pack(fill="both", expand=True)

    # Lado Izquierdo: Gráfico de Cónicas
    frame_grafico = tk.LabelFrame(paneles_frame, text=" Representación Gráfica (Cónicas) ", font=("Segoe UI", 12, "bold"), bg=color_grafico, fg=color_header, padx=10, pady=10, highlightbackground=color_borde, highlightcolor=color_borde)
    frame_grafico.pack(side="left", fill="both", expand=True, padx=(0, 15))

    barra_grafico = tk.Frame(frame_grafico, bg=color_grafico)
    barra_grafico.pack(fill="x", pady=(0, 8))
    lbl_ayuda_grafico = tk.Label(
        barra_grafico,
        text="Rueda: zoom | Arrastrar: mover | Doble clic: reiniciar",
        font=("Segoe UI", 9),
        bg=color_grafico,
        fg="#475569",
    )
    lbl_ayuda_grafico.pack(side="left")
    btn_reset_conica = ttk.Button(barra_grafico, text="Reiniciar vista", style="Tool.TButton")
    btn_reset_conica.pack(side="right")

    canvas_grafico = tk.Canvas(frame_grafico, bg=color_grafico, highlightthickness=1, highlightbackground=color_borde)
    canvas_grafico.pack(fill="both", expand=True)

    # Lado Derecho: Resultados (Cónicas)
    frame_resultados = tk.LabelFrame(paneles_frame, text=" Memoria de Cálculo ", font=("Segoe UI", 12, "bold"), bg=color_panel, fg=color_header_secundario, padx=10, pady=10, highlightbackground=color_borde, highlightcolor=color_borde)
    frame_resultados.pack(side="right", fill="y")

    txt_resultados = tk.Text(frame_resultados, wrap="word", state="disabled", font=("Consolas", 10), width=45, bg="#f8fbff", fg=color_texto, relief="flat", padx=10, pady=10, highlightthickness=1, highlightbackground=color_borde)
    txt_resultados.pack(fill="both", expand=True)

    # Pestaña 2: Funciones por Tramo
    paneles_tramos_frame = ttk.Frame(tab_tramos)
    paneles_tramos_frame.pack(fill="both", expand=True)

    # Lado Izquierdo: Gráfico de Tramos
    frame_grafico_tramos = tk.LabelFrame(paneles_tramos_frame, text=" Representación Gráfica (Por Tramo) ", font=("Segoe UI", 12, "bold"), bg=color_grafico, fg=color_header, padx=10, pady=10, highlightbackground=color_borde, highlightcolor=color_borde)
    frame_grafico_tramos.pack(side="left", fill="both", expand=True, padx=(0, 15))

    barra_grafico_tramos = tk.Frame(frame_grafico_tramos, bg=color_grafico)
    barra_grafico_tramos.pack(fill="x", pady=(0, 8))
    lbl_ayuda_tramos = tk.Label(
        barra_grafico_tramos,
        text="Rueda: zoom | Arrastrar: mover | Doble clic: reiniciar",
        font=("Segoe UI", 9),
        bg=color_grafico,
        fg="#475569",
    )
    lbl_ayuda_tramos.pack(side="left")
    btn_reset_tramos = ttk.Button(barra_grafico_tramos, text="Reiniciar vista", style="Tool.TButton")
    btn_reset_tramos.pack(side="right")

    canvas_tramos = tk.Canvas(frame_grafico_tramos, bg=color_grafico, highlightthickness=1, highlightbackground=color_borde)
    canvas_tramos.pack(fill="both", expand=True)

    # Lado Derecho: Resultados (Tramos)
    frame_resultados_tramos = tk.LabelFrame(paneles_tramos_frame, text=" Memoria de Cálculo y Defensa ", font=("Segoe UI", 12, "bold"), bg=color_panel, fg=color_header_secundario, padx=10, pady=10, highlightbackground=color_borde, highlightcolor=color_borde)
    frame_resultados_tramos.pack(side="right", fill="y")

    txt_resultados_tramos = tk.Text(frame_resultados_tramos, wrap="word", state="disabled", font=("Consolas", 10), width=45, bg="#f8fbff", fg=color_texto, relief="flat", padx=10, pady=10, highlightthickness=1, highlightbackground=color_borde)
    txt_resultados_tramos.pack(fill="both", expand=True)

    # Estados de gráficos para redibujo
    ultimo_grafico = {"coeficientes": None, "redibujo": None, "vista": None, "arrastre": None, "movio": False}
    ultimo_grafico_tramos = {"analisis": None, "redibujo": None, "vista": None, "arrastre": None, "movio": False}

    def redibujar_grafico():
        ultimo_grafico["redibujo"] = None
        if ultimo_grafico["coeficientes"] is not None:
            graficar_conica(canvas_grafico, ultimo_grafico["coeficientes"], ultimo_grafico["vista"])

    def preparar_redibujo(_evento):
        if ultimo_grafico["coeficientes"] is None:
            return
        if ultimo_grafico["redibujo"] is not None:
            canvas_grafico.after_cancel(ultimo_grafico["redibujo"])
        ultimo_grafico["redibujo"] = canvas_grafico.after(120, redibujar_grafico)

    def redibujar_grafico_tramos():
        ultimo_grafico_tramos["redibujo"] = None
        if ultimo_grafico_tramos["analisis"] is not None:
            graficar_funcion_por_tramos(canvas_tramos, ultimo_grafico_tramos["analisis"], ultimo_grafico_tramos["vista"])

    def preparar_redibujo_tramos(_evento):
        if ultimo_grafico_tramos["analisis"] is None:
            return
        if ultimo_grafico_tramos["redibujo"] is not None:
            canvas_tramos.after_cancel(ultimo_grafico_tramos["redibujo"])
        ultimo_grafico_tramos["redibujo"] = canvas_tramos.after(120, redibujar_grafico_tramos)

    def escala_canvas(canvas, vista):
        w = canvas.winfo_width()
        h = canvas.winfo_height()
        if w <= 1 or h <= 1:
            w, h = 600, 500
        return min(w, h) / (vista["rango"] * 2)

    def punto_mundo(canvas, vista, px, py):
        escala = escala_canvas(canvas, vista)
        w = canvas.winfo_width() if canvas.winfo_width() > 1 else 600
        h = canvas.winfo_height() if canvas.winfo_height() > 1 else 500
        x = vista["cx"] + (px - w / 2) / escala
        y = vista["cy"] - (py - h / 2) / escala
        return x, y

    def aplicar_zoom(canvas, estado, redibujar, evento):
        vista = estado["vista"]
        if vista is None:
            return

        delta = getattr(evento, "delta", 0)
        factor = 0.82 if delta > 0 or getattr(evento, "num", None) == 4 else 1.22
        rango_nuevo = max(0.25, min(250.0, vista["rango"] * factor))

        x_antes, y_antes = punto_mundo(canvas, vista, evento.x, evento.y)
        vista["rango"] = rango_nuevo
        x_despues, y_despues = punto_mundo(canvas, vista, evento.x, evento.y)
        vista["cx"] += x_antes - x_despues
        vista["cy"] += y_antes - y_despues
        redibujar()

    def iniciar_arrastre(estado, evento):
        estado["arrastre"] = {"x": evento.x, "y": evento.y}
        estado["movio"] = False

    def mover_vista(canvas, estado, evento):
        vista = estado["vista"]
        arrastre = estado["arrastre"]
        if vista is None or arrastre is None:
            return

        escala = escala_canvas(canvas, vista)
        dx = evento.x - arrastre["x"]
        dy = evento.y - arrastre["y"]
        vista["cx"] -= dx / escala
        vista["cy"] += dy / escala
        estado["arrastre"] = {"x": evento.x, "y": evento.y}
        estado["movio"] = True
        canvas.move("all", dx, dy)

    def terminar_arrastre(estado, redibujar, _evento):
        debe_redibujar = estado["movio"]
        estado["arrastre"] = None
        estado["movio"] = False
        if debe_redibujar:
            redibujar()

    def reiniciar_vista_conica():
        if ultimo_grafico["coeficientes"] is None:
            return
        ultimo_grafico["vista"] = obtener_vista_conica(ultimo_grafico["coeficientes"])
        redibujar_grafico()

    def reiniciar_vista_tramos():
        if ultimo_grafico_tramos["analisis"] is None:
            return
        ultimo_grafico_tramos["vista"] = obtener_vista_tramos(ultimo_grafico_tramos["analisis"])
        redibujar_grafico_tramos()

    def mostrar_rut():
        rut_ingresado = entry_rut.get()
        resultado = validar_rut(rut_ingresado)

        lineas_conicas = formatear_resultado_rut(resultado)
        lineas_tramos = formatear_resultado_rut(resultado)
        
        if resultado["valido"]:
            digitos = obtener_digitos(resultado["cuerpo"])
            
            # Cónicas
            resultado_conica = analizar_conica(digitos, resultado["dv_ingresado"])
            lineas_conicas.extend(formatear_resultado_conica(resultado_conica))
            ultimo_grafico["coeficientes"] = resultado_conica["coeficientes"]
            ultimo_grafico["vista"] = obtener_vista_conica(ultimo_grafico["coeficientes"])
            graficar_conica(canvas_grafico, ultimo_grafico["coeficientes"], ultimo_grafico["vista"])
            
            # Funciones por tramos
            resultado_tramos = analizar_funcion_por_tramos(digitos)
            lineas_tramos.extend(formatear_resultado_tramos(resultado_tramos))
            ultimo_grafico_tramos["analisis"] = resultado_tramos
            ultimo_grafico_tramos["vista"] = obtener_vista_tramos(ultimo_grafico_tramos["analisis"])
            graficar_funcion_por_tramos(canvas_tramos, ultimo_grafico_tramos["analisis"], ultimo_grafico_tramos["vista"])
        else:
            ultimo_grafico["coeficientes"] = None
            ultimo_grafico["vista"] = None
            ultimo_grafico["arrastre"] = None
            ultimo_grafico["movio"] = False
            canvas_grafico.delete("all")
            
            ultimo_grafico_tramos["analisis"] = None
            ultimo_grafico_tramos["vista"] = None
            ultimo_grafico_tramos["arrastre"] = None
            ultimo_grafico_tramos["movio"] = False
            canvas_tramos.delete("all")

        # Actualizar panel de Cónicas
        txt_resultados.configure(state="normal")
        txt_resultados.delete("1.0", tk.END)
        txt_resultados.insert(tk.END, "\n".join(lineas_conicas))
        txt_resultados.configure(state="disabled")

        # Actualizar panel de Tramos
        txt_resultados_tramos.configure(state="normal")
        txt_resultados_tramos.delete("1.0", tk.END)
        txt_resultados_tramos.insert(tk.END, "\n".join(lineas_tramos))
        txt_resultados_tramos.configure(state="disabled")

    btn_calcular.config(command=mostrar_rut)
    btn_reset_conica.config(command=reiniciar_vista_conica)
    btn_reset_tramos.config(command=reiniciar_vista_tramos)
    canvas_grafico.bind("<Configure>", preparar_redibujo)
    canvas_tramos.bind("<Configure>", preparar_redibujo_tramos)
    canvas_grafico.bind("<MouseWheel>", lambda e: aplicar_zoom(canvas_grafico, ultimo_grafico, redibujar_grafico, e))
    canvas_grafico.bind("<Button-4>", lambda e: aplicar_zoom(canvas_grafico, ultimo_grafico, redibujar_grafico, e))
    canvas_grafico.bind("<Button-5>", lambda e: aplicar_zoom(canvas_grafico, ultimo_grafico, redibujar_grafico, e))
    canvas_grafico.bind("<ButtonPress-1>", lambda e: iniciar_arrastre(ultimo_grafico, e))
    canvas_grafico.bind("<B1-Motion>", lambda e: mover_vista(canvas_grafico, ultimo_grafico, e))
    canvas_grafico.bind("<ButtonRelease-1>", lambda e: terminar_arrastre(ultimo_grafico, redibujar_grafico, e))
    canvas_grafico.bind("<Double-Button-1>", lambda _e: reiniciar_vista_conica())
    canvas_tramos.bind("<MouseWheel>", lambda e: aplicar_zoom(canvas_tramos, ultimo_grafico_tramos, redibujar_grafico_tramos, e))
    canvas_tramos.bind("<Button-4>", lambda e: aplicar_zoom(canvas_tramos, ultimo_grafico_tramos, redibujar_grafico_tramos, e))
    canvas_tramos.bind("<Button-5>", lambda e: aplicar_zoom(canvas_tramos, ultimo_grafico_tramos, redibujar_grafico_tramos, e))
    canvas_tramos.bind("<ButtonPress-1>", lambda e: iniciar_arrastre(ultimo_grafico_tramos, e))
    canvas_tramos.bind("<B1-Motion>", lambda e: mover_vista(canvas_tramos, ultimo_grafico_tramos, e))
    canvas_tramos.bind("<ButtonRelease-1>", lambda e: terminar_arrastre(ultimo_grafico_tramos, redibujar_grafico_tramos, e))
    canvas_tramos.bind("<Double-Button-1>", lambda _e: reiniciar_vista_tramos())
    entry_rut.focus_set()

    root.mainloop()

if __name__ == "__main__":
    iniciar_interfaz()
