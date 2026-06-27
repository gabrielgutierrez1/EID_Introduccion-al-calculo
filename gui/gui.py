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
from gui.graficos import (
    graficar_conica,
    graficar_funcion_por_tramos,
    obtener_vista_conica,
    obtener_vista_tramos,
)
import threading
import re
from src.buscar_ruts import buscar_casos_prueba
from src.elementos import calcular_elementos_geometricos
from src.solucionario import generar_solucionario



def formatear_resultado_rut(resultado):
    lineas = []

    if not resultado["valido"] and "error" in resultado:
        lineas.append(("RUT INVÁLIDO", "titulo"))
        lineas.append((resultado["error"], "subtitulo"))
        return lineas

    lineas.append(("VALIDACIÓN DEL RUT", "titulo"))
    lineas.append((f"RUT limpio: {resultado['rut_limpio']}", "subtitulo"))
    lineas.append((f"Cuerpo: {resultado['cuerpo']}", "calculo"))
    lineas.append((f"Dígito verificador: {resultado['dv_ingresado']}", "calculo"))

    lineas.append(("Procedimiento módulo 11", "subtitulo"))
    for paso in resultado["calculo"]["pasos"]:
        lineas.append((f"{paso['digito']} x {paso['multiplicador']} = {paso['producto']}", "calculo"))

    lineas.append((f"Suma de productos: {resultado['calculo']['suma']}", "calculo"))
    lineas.append((f"Resto de división por 11: {resultado['calculo']['resto']}", "calculo"))
    lineas.append((f"11 - resto = {resultado['calculo']['valor']}", "calculo"))
    lineas.append((f"DV esperado: {resultado['dv_esperado']}", "resultado"))

    if resultado["valido"]:
        lineas.append(("Conclusión: el RUT es válido.", "resultado"))
    else:
        lineas.append(("Conclusión: el RUT no es válido.", "subtitulo"))

    return lineas

def formatear_resultado_conica(resultado):
    lineas = []
    lineas.append(("CONSTRUCCIÓN DE LA CÓNICA", "titulo"))

    for paso in resultado["coeficientes"]["pasos"]:
        lineas.append((paso, "calculo"))

    lineas.append(("Ecuación general", "subtitulo"))
    lineas.append((resultado['ecuacion_general'], "formula"))
    
    lineas.append(("Clasificación", "subtitulo"))
    lineas.append((resultado['tipo'], "resultado"))

    if "forma_canonica" in resultado and resultado["forma_canonica"]:
        transform = resultado["forma_canonica"]
        if transform.get("pasos"):
            lineas.append(("Transformación a forma canónica", "subtitulo"))
            for paso in transform["pasos"]:
                lineas.append((paso, "calculo"))

        forma = transform.get("forma_canonica")
        if forma:
            lineas.append(("Forma canónica", "subtitulo"))
            lineas.append((forma, "formula"))

    if "canonica_a_general" in resultado and resultado["canonica_a_general"]:
        inversa = resultado["canonica_a_general"]
        if inversa.get("pasos"):
            lineas.append(("Transformación inversa", "subtitulo"))
            for paso in inversa["pasos"]:
                lineas.append((paso, "calculo"))

    return lineas


def formatear_resultado_tramos(resultado):
    lineas = []
    lineas.append(("ANÁLISIS DE FUNCIÓN POR TRAMOS", "titulo"))

    funcion = resultado["funcion"]
    caso = resultado["caso"]
    a = resultado["a"]

    lineas.append(("Caso detectado", "subtitulo"))
    lineas.append((caso['nombre'], "resultado"))
    
    lineas.append(("Punto crítico", "subtitulo"))
    lineas.append((f"a = {a}", "calculo"))

    lineas.append(("Tramos de la función", "subtitulo"))
    for tramo in funcion["tramos"]:
        lineas.append((f"f(x) = {tramo['expresion']} si {tramo['condicion']}", "formula"))

    if funcion["simplificada"]:
        lineas.append(("Fórmula simplificada", "subtitulo"))
        lineas.append((funcion['simplificada'], "formula"))

    lineas.append(("Memoria de cálculo", "subtitulo"))
    for paso in resultado["pasos"]:
        lineas.append((paso, "calculo"))

    lineas.append(("Tabla de valores cerca de x = a", "subtitulo"))
    lineas.append((f"{'Lado':<10} | {'x':<12} | {'f(x)':<12}", "calculo"))
    lineas.append(("-" * 40, "calculo"))
    for fila in resultado["tabla"]:
        lineas.append((f"{fila['lado']:<10} | {fila['x_texto']:<12} | {fila['f_x_texto']:<12}", "calculo"))

    lineas.append(("Respuestas de la defensa", "titulo"))

    lim = resultado["limites"]
    cont = resultado["continuidad"]

    def_izq = formatear_numero(lim["izquierda"])
    def_der = formatear_numero(lim["derecha"])
    def_ex = "Existe y vale " + formatear_numero(lim["valor"]) if lim["existe"] else "No existe"
    def_val = formatear_numero(cont["valor_en_a"])
    def_cont = "Continua" if cont["es_continua"] else "Discontinua"
    def_tipo = cont["tipo_discontinuidad"]
    def_just = cont["justificacion"]

    lineas.append(("Límite por la izquierda:", "subtitulo"))
    lineas.append((def_izq, "calculo"))
    lineas.append(("Límite por la derecha:", "subtitulo"))
    lineas.append((def_der, "calculo"))
    lineas.append(("Conclusión sobre el límite:", "subtitulo"))
    lineas.append((def_ex, "resultado"))
    
    lineas.append(("Valor de la función en el punto:", "subtitulo"))
    lineas.append((def_val, "calculo"))
    
    lineas.append(("Conclusión sobre continuidad:", "subtitulo"))
    lineas.append((def_cont, "resultado"))
    
    lineas.append(("Tipo de discontinuidad:", "subtitulo"))
    lineas.append((def_tipo, "calculo"))
    
    lineas.append(("Justificación:", "subtitulo"))
    lineas.append((def_just, "calculo"))

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
    tab_defensa = ttk.Frame(notebook)
    tab_tramos = ttk.Frame(notebook)
    tab_ruts = ttk.Frame(notebook)
    notebook.add(tab_conicas, text=" Cónicas ")
    notebook.add(tab_defensa, text=" Defensa Oral ")
    notebook.add(tab_tramos, text=" Funciones por Tramo ")
    notebook.add(tab_ruts, text=" Casos de Prueba ")

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

    # Lado Derecho: Contenedor para Resultados y Elementos Geométricos
    frame_derecha = ttk.Frame(paneles_frame)
    frame_derecha.pack(side="right", fill="y", padx=(10, 0))

    frame_resultados = tk.LabelFrame(frame_derecha, text=" Memoria de Cálculo ", font=("Segoe UI", 12, "bold"), bg=color_panel, fg=color_header_secundario, padx=10, pady=10, highlightbackground=color_borde, highlightcolor=color_borde)
    frame_resultados.pack(fill="both", expand=True, pady=(0, 10))

    txt_resultados = tk.Text(frame_resultados, wrap="word", state="disabled", font=("Consolas", 10), width=45, bg="#f8fbff", fg=color_texto, relief="flat", padx=15, pady=15, highlightthickness=1, highlightbackground=color_borde)
    txt_resultados.pack(fill="both", expand=True)
    
    txt_resultados.tag_configure("titulo", font=("Segoe UI", 13, "bold"), foreground="#1d4ed8", spacing1=5, spacing3=15, justify="center")
    txt_resultados.tag_configure("subtitulo", font=("Segoe UI", 11, "bold"), foreground="#334155", spacing1=15, spacing3=5)
    txt_resultados.tag_configure("formula", font=("Consolas", 10, "italic"), foreground="#64748b", lmargin1=20)
    txt_resultados.tag_configure("calculo", font=("Consolas", 10), foreground="#475569", lmargin1=20, spacing1=2)
    txt_resultados.tag_configure("resultado", font=("Consolas", 11, "bold"), foreground="#059669", lmargin1=20, spacing1=6, spacing3=5)

    # Pestaña 1B: Defensa Oral
    paneles_defensa_frame = ttk.Frame(tab_defensa)
    paneles_defensa_frame.pack(fill="both", expand=True)

    frame_grafico_def = tk.LabelFrame(paneles_defensa_frame, text=" Gráfico para Identificar Puntos ", font=("Segoe UI", 12, "bold"), bg=color_grafico, fg=color_header, padx=10, pady=10, highlightbackground=color_borde, highlightcolor=color_borde)
    frame_grafico_def.pack(side="left", fill="both", expand=True, padx=(0, 15))

    barra_grafico_def = tk.Frame(frame_grafico_def, bg=color_grafico)
    barra_grafico_def.pack(fill="x", pady=(0, 8))
    lbl_ayuda_def = tk.Label(barra_grafico_def, text="Rueda: zoom | Arrastrar: mover | Doble clic: reiniciar", font=("Segoe UI", 9), bg=color_grafico, fg="#475569")
    lbl_ayuda_def.pack(side="left")
    btn_reset_def = ttk.Button(barra_grafico_def, text="Reiniciar vista", style="Tool.TButton")
    btn_reset_def.pack(side="right")

    canvas_defensa = tk.Canvas(frame_grafico_def, bg=color_grafico, highlightthickness=1, highlightbackground=color_borde)
    canvas_defensa.pack(fill="both", expand=True)

    frame_derecha_def = ttk.Frame(paneles_defensa_frame)
    frame_derecha_def.pack(side="right", fill="y", padx=(10, 0))

    # Panel de Elementos Geométricos (Fase 4) - Movido
    frame_elementos = tk.LabelFrame(frame_derecha_def, text=" Defensa Oral: Elementos ", font=("Segoe UI", 12, "bold"), bg=color_panel, fg=color_header_secundario, padx=10, pady=10, highlightbackground=color_borde, highlightcolor=color_borde)
    frame_elementos.pack(fill="x")

    frame_solucionario = tk.LabelFrame(frame_derecha_def, text=" Solucionario ", font=("Segoe UI", 12, "bold"), bg=color_panel, fg=color_header_secundario, padx=10, pady=10, highlightbackground=color_borde, highlightcolor=color_borde)
    frame_solucionario.pack(fill="both", expand=True, pady=(10, 0))
    
    txt_solucionario = tk.Text(frame_solucionario, wrap="word", state="disabled", font=("Consolas", 10), width=45, bg="#f8fbff", fg=color_texto, relief="flat", padx=15, pady=15, highlightthickness=1, highlightbackground=color_borde)
    
    txt_solucionario.tag_configure("titulo", font=("Segoe UI", 13, "bold"), foreground="#1d4ed8", spacing1=5, spacing3=15, justify="center")
    txt_solucionario.tag_configure("subtitulo", font=("Segoe UI", 11, "bold"), foreground="#334155", spacing1=15, spacing3=5)
    txt_solucionario.tag_configure("formula", font=("Consolas", 10, "italic"), foreground="#64748b", lmargin1=20)
    txt_solucionario.tag_configure("calculo", font=("Consolas", 10), foreground="#475569", lmargin1=20, spacing1=2)
    txt_solucionario.tag_configure("resultado", font=("Consolas", 11, "bold"), foreground="#059669", lmargin1=20, spacing1=6, spacing3=5)
    
    def mostrar_soluciones():
        if ultimo_grafico_def["coeficientes"] is not None and ultimo_grafico_def["tipo"] is not None:
            lineas = generar_solucionario(ultimo_grafico_def["coeficientes"], ultimo_grafico_def["tipo"])
            txt_solucionario.configure(state="normal")
            txt_solucionario.delete("1.0", tk.END)
            for texto, tag in lineas:
                txt_solucionario.insert(tk.END, texto + "\n", tag)
            txt_solucionario.configure(state="disabled")
            txt_solucionario.pack(fill="both", expand=True)
            btn_mostrar_solucionario.pack_forget()

    btn_mostrar_solucionario = ttk.Button(frame_solucionario, text="📖 Mostrar Solucionario", style="Tool.TButton", command=mostrar_soluciones)
    btn_mostrar_solucionario.pack(pady=10)

    campos_elementos = {}
    nombres_campos = [
        ("centro", "Centro:"),
        ("vertices", "Vértice(s):"),
        ("focos", "Foco(s):"),
        ("eje_mayor", "Eje Mayor / Transverso:"),
        ("eje_menor", "Eje Menor / Conjugado:"),
        ("directriz", "Directriz:"),
    ]

    for i, (clave, texto) in enumerate(nombres_campos):
        lbl = ttk.Label(frame_elementos, text=texto, background=color_panel)
        lbl.grid(row=i, column=0, sticky="e", pady=3, padx=5)
        entry = ttk.Entry(frame_elementos, width=25)
        entry.grid(row=i, column=1, sticky="w", pady=3, padx=5)
        lbl_feedback = ttk.Label(frame_elementos, text="", background=color_panel, font=("Segoe UI", 10, "bold"))
        lbl_feedback.grid(row=i, column=2, sticky="w", pady=3, padx=5)
        campos_elementos[clave] = {"label": lbl, "entry": entry, "feedback": lbl_feedback}

    def parse_numbers(text):
        return [float(x) for x in re.findall(r'-?\d+\.?\d*', text)]

    def verificar_respuestas():
        if not ultimo_grafico.get("coeficientes") or not ultimo_grafico.get("tipo"):
            return
            
        valores_correctos = calcular_elementos_geometricos(ultimo_grafico["coeficientes"], ultimo_grafico["tipo"])
        
        for clave, valor_esperado in valores_correctos.items():
            if clave not in campos_elementos or not campos_elementos[clave]["entry"].winfo_ismapped():
                continue
                
            texto_ingresado = campos_elementos[clave]["entry"].get().strip()
            if not texto_ingresado:
                campos_elementos[clave]["feedback"].config(text="")
                continue
                
            nums_ingresados = parse_numbers(texto_ingresado)
            es_correcto = False
            
            def tolerante(a, b):
                # Aumentamos la tolerancia a 0.2 para permitir que recortes (ej. 3.3 en vez de 3.345) pasen como válidos
                return abs(a - b) <= 0.2

            if isinstance(valor_esperado, tuple) and len(valor_esperado) == 2:
                # Punto (x, y)
                if len(nums_ingresados) == 2 and tolerante(nums_ingresados[0], valor_esperado[0]) and tolerante(nums_ingresados[1], valor_esperado[1]):
                    es_correcto = True
            elif isinstance(valor_esperado, list):
                # Lista de puntos [(x1,y1), (x2,y2)]
                if len(nums_ingresados) == len(valor_esperado) * 2:
                    pares_ingresados = [(nums_ingresados[j], nums_ingresados[j+1]) for j in range(0, len(nums_ingresados), 2)]
                    matches = 0
                    for p_esp in valor_esperado:
                        for p_ing in pares_ingresados:
                            if tolerante(p_ing[0], p_esp[0]) and tolerante(p_ing[1], p_esp[1]):
                                matches += 1
                                pares_ingresados.remove(p_ing)
                                break
                    if matches == len(valor_esperado):
                        es_correcto = True
            elif isinstance(valor_esperado, (int, float)):
                # Valor unico
                if len(nums_ingresados) == 1 and tolerante(nums_ingresados[0], valor_esperado):
                    es_correcto = True
                    
            if es_correcto:
                campos_elementos[clave]["feedback"].config(text="✔ Correcto", foreground="#00aa00")
            else:
                campos_elementos[clave]["feedback"].config(text="✘ Incorrecto", foreground="#ff0000")

    btn_verificar = ttk.Button(frame_elementos, text="✔ Verificar Respuestas", style="Accent.TButton", command=verificar_respuestas)
    btn_verificar.grid(row=len(nombres_campos), column=0, columnspan=3, pady=(10, 5))

    def ocultar_campos():
        for clave in campos_elementos:
            campos_elementos[clave]["label"].grid_remove()
            campos_elementos[clave]["entry"].grid_remove()
            campos_elementos[clave]["feedback"].grid_remove()
            campos_elementos[clave]["entry"].delete(0, tk.END)
            campos_elementos[clave]["feedback"].config(text="")
        btn_verificar.grid_remove()

    def mostrar_campos(claves):
        ocultar_campos()
        for i, (clave, _texto) in enumerate(nombres_campos):
            if clave in claves:
                campos_elementos[clave]["label"].grid()
                campos_elementos[clave]["entry"].grid()
                campos_elementos[clave]["feedback"].grid()
        if claves:
            btn_verificar.grid()
    
    ocultar_campos()

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

    txt_resultados_tramos = tk.Text(frame_resultados_tramos, wrap="word", state="disabled", font=("Consolas", 10), width=45, bg="#f8fbff", fg=color_texto, relief="flat", padx=15, pady=15, highlightthickness=1, highlightbackground=color_borde)
    txt_resultados_tramos.pack(fill="both", expand=True)
    
    txt_resultados_tramos.tag_configure("titulo", font=("Segoe UI", 13, "bold"), foreground="#1d4ed8", spacing1=5, spacing3=15, justify="center")
    txt_resultados_tramos.tag_configure("subtitulo", font=("Segoe UI", 11, "bold"), foreground="#334155", spacing1=15, spacing3=5)
    txt_resultados_tramos.tag_configure("formula", font=("Consolas", 10, "italic"), foreground="#64748b", lmargin1=20)
    txt_resultados_tramos.tag_configure("calculo", font=("Consolas", 10), foreground="#475569", lmargin1=20, spacing1=2)
    txt_resultados_tramos.tag_configure("resultado", font=("Consolas", 11, "bold"), foreground="#059669", lmargin1=20, spacing1=6, spacing3=5)

    # Estados de gráficos para redibujo
    ultimo_grafico = {"coeficientes": None, "redibujo": None, "vista": None, "arrastre": None, "movio": False, "tipo": None}
    ultimo_grafico_def = {"coeficientes": None, "redibujo": None, "vista": None, "arrastre": None, "movio": False, "tipo": None}
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

    def redibujar_grafico_def():
        ultimo_grafico_def["redibujo"] = None
        if ultimo_grafico_def["coeficientes"] is not None:
            graficar_conica(canvas_defensa, ultimo_grafico_def["coeficientes"], ultimo_grafico_def["vista"], mostrar_nombres=False)

    def preparar_redibujo_def(_evento):
        if ultimo_grafico_def["coeficientes"] is None:
            return
        if ultimo_grafico_def["redibujo"] is not None:
            canvas_defensa.after_cancel(ultimo_grafico_def["redibujo"])
        ultimo_grafico_def["redibujo"] = canvas_defensa.after(120, redibujar_grafico_def)

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

    def reiniciar_vista_def():
        if ultimo_grafico_def["coeficientes"] is None:
            return
        ultimo_grafico_def["vista"] = obtener_vista_conica(ultimo_grafico_def["coeficientes"])
        redibujar_grafico_def()

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
            ultimo_grafico["tipo"] = resultado_conica.get("tipo", "")
            ultimo_grafico["vista"] = obtener_vista_conica(ultimo_grafico["coeficientes"])
            graficar_conica(canvas_grafico, ultimo_grafico["coeficientes"], ultimo_grafico["vista"])
            
            # Defensa
            ultimo_grafico_def["coeficientes"] = resultado_conica["coeficientes"]
            ultimo_grafico_def["tipo"] = resultado_conica.get("tipo", "")
            ultimo_grafico_def["vista"] = obtener_vista_conica(ultimo_grafico_def["coeficientes"])
            graficar_conica(canvas_defensa, ultimo_grafico_def["coeficientes"], ultimo_grafico_def["vista"], mostrar_nombres=False)
            
            txt_solucionario.pack_forget()
            btn_mostrar_solucionario.pack(pady=10)
            
            # Mostrar los inputs correspondientes a la cónica
            tipo_conica = resultado_conica.get("tipo", "").lower()
            if "circunferencia" in tipo_conica:
                mostrar_campos(["centro"])
            elif "parábola" in tipo_conica or "parabola" in tipo_conica:
                mostrar_campos(["vertices", "focos", "directriz"])
            elif "elipse" in tipo_conica or "hipérbola" in tipo_conica or "hiperbola" in tipo_conica:
                mostrar_campos(["centro", "vertices", "focos", "eje_mayor", "eje_menor"])
            else:
                ocultar_campos()
            
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
            
            ultimo_grafico_def["coeficientes"] = None
            ultimo_grafico_def["vista"] = None
            ultimo_grafico_def["arrastre"] = None
            ultimo_grafico_def["movio"] = False
            canvas_defensa.delete("all")
            
            ocultar_campos()
            txt_solucionario.pack_forget()
            btn_mostrar_solucionario.pack_forget()
            
            ultimo_grafico_tramos["analisis"] = None
            ultimo_grafico_tramos["vista"] = None
            ultimo_grafico_tramos["arrastre"] = None
            ultimo_grafico_tramos["movio"] = False
            canvas_tramos.delete("all")

        # Actualizar panel de Cónicas
        txt_resultados.configure(state="normal")
        txt_resultados.delete("1.0", tk.END)
        for texto, tag in lineas_conicas:
            txt_resultados.insert(tk.END, texto + "\n", tag)
        txt_resultados.configure(state="disabled")

        # Actualizar panel de Tramos
        txt_resultados_tramos.configure(state="normal")
        txt_resultados_tramos.delete("1.0", tk.END)
        for texto, tag in lineas_tramos:
            txt_resultados_tramos.insert(tk.END, texto + "\n", tag)
        txt_resultados_tramos.configure(state="disabled")

    btn_calcular.config(command=mostrar_rut)
    btn_reset_conica.config(command=reiniciar_vista_conica)
    btn_reset_def.config(command=reiniciar_vista_def)
    btn_reset_tramos.config(command=reiniciar_vista_tramos)
    
    canvas_grafico.bind("<Configure>", preparar_redibujo)
    canvas_defensa.bind("<Configure>", preparar_redibujo_def)
    canvas_tramos.bind("<Configure>", preparar_redibujo_tramos)
    
    canvas_grafico.bind("<MouseWheel>", lambda e: aplicar_zoom(canvas_grafico, ultimo_grafico, redibujar_grafico, e))
    canvas_grafico.bind("<Button-4>", lambda e: aplicar_zoom(canvas_grafico, ultimo_grafico, redibujar_grafico, e))
    canvas_grafico.bind("<Button-5>", lambda e: aplicar_zoom(canvas_grafico, ultimo_grafico, redibujar_grafico, e))
    canvas_grafico.bind("<ButtonPress-1>", lambda e: iniciar_arrastre(ultimo_grafico, e))
    canvas_grafico.bind("<B1-Motion>", lambda e: mover_vista(canvas_grafico, ultimo_grafico, e))
    canvas_grafico.bind("<ButtonRelease-1>", lambda e: terminar_arrastre(ultimo_grafico, redibujar_grafico, e))
    canvas_grafico.bind("<Double-Button-1>", lambda _e: reiniciar_vista_conica())
    
    canvas_defensa.bind("<MouseWheel>", lambda e: aplicar_zoom(canvas_defensa, ultimo_grafico_def, redibujar_grafico_def, e))
    canvas_defensa.bind("<Button-4>", lambda e: aplicar_zoom(canvas_defensa, ultimo_grafico_def, redibujar_grafico_def, e))
    canvas_defensa.bind("<Button-5>", lambda e: aplicar_zoom(canvas_defensa, ultimo_grafico_def, redibujar_grafico_def, e))
    canvas_defensa.bind("<ButtonPress-1>", lambda e: iniciar_arrastre(ultimo_grafico_def, e))
    canvas_defensa.bind("<B1-Motion>", lambda e: mover_vista(canvas_defensa, ultimo_grafico_def, e))
    canvas_defensa.bind("<ButtonRelease-1>", lambda e: terminar_arrastre(ultimo_grafico_def, redibujar_grafico_def, e))
    canvas_defensa.bind("<Double-Button-1>", lambda _e: reiniciar_vista_def())
    
    canvas_tramos.bind("<MouseWheel>", lambda e: aplicar_zoom(canvas_tramos, ultimo_grafico_tramos, redibujar_grafico_tramos, e))
    canvas_tramos.bind("<Button-4>", lambda e: aplicar_zoom(canvas_tramos, ultimo_grafico_tramos, redibujar_grafico_tramos, e))
    canvas_tramos.bind("<Button-5>", lambda e: aplicar_zoom(canvas_tramos, ultimo_grafico_tramos, redibujar_grafico_tramos, e))
    canvas_tramos.bind("<ButtonPress-1>", lambda e: iniciar_arrastre(ultimo_grafico_tramos, e))
    canvas_tramos.bind("<B1-Motion>", lambda e: mover_vista(canvas_tramos, ultimo_grafico_tramos, e))
    canvas_tramos.bind("<ButtonRelease-1>", lambda e: terminar_arrastre(ultimo_grafico_tramos, redibujar_grafico_tramos, e))
    canvas_tramos.bind("<Double-Button-1>", lambda _e: reiniciar_vista_tramos())
    
    # --- Pestaña 3: Casos de Prueba (RUTs) ---
    frame_ruts_main = ttk.Frame(tab_ruts, padding="20 20 20 20")
    frame_ruts_main.pack(fill="both", expand=True)
    
    lbl_ruts_info = ttk.Label(frame_ruts_main, text="Genera 4 RUTs válidos reales (con su DV correcto) para probar las 4 cónicas requeridas:", font=("Segoe UI", 12))
    lbl_ruts_info.pack(pady=(0, 15))
    
    btn_generar_ruts = ttk.Button(frame_ruts_main, text="▶ Generar RUTs de Prueba", style="Accent.TButton")
    btn_generar_ruts.pack(pady=(0, 20))
    
    txt_ruts_resultados = tk.Text(frame_ruts_main, wrap="word", state="disabled", font=("Consolas", 12), height=10, bg="#f8fbff", fg=color_texto, relief="flat", padx=20, pady=20, highlightthickness=1, highlightbackground=color_borde)
    txt_ruts_resultados.pack(fill="both", expand=True)
    
    def procesar_busqueda():
        btn_generar_ruts.config(text="Buscando... (puede tardar unos segundos)", state="disabled")
        txt_ruts_resultados.configure(state="normal")
        txt_ruts_resultados.delete("1.0", tk.END)
        txt_ruts_resultados.insert(tk.END, "Buscando casos de prueba en segundo plano... por favor espera.\n")
        txt_ruts_resultados.configure(state="disabled")
        
        def tarea_en_hilo():
            casos = buscar_casos_prueba()
            
            def actualizar_gui():
                txt_ruts_resultados.configure(state="normal")
                txt_ruts_resultados.delete("1.0", tk.END)
                if None in casos.values():
                    txt_ruts_resultados.insert(tk.END, "No se encontraron todos los casos en el límite de intentos.\n\n")
                else:
                    txt_ruts_resultados.insert(tk.END, "¡Búsqueda completada! Estos RUTs son matemáticamente válidos:\n\n")
                
                for tipo, rut in casos.items():
                    val = rut if rut else "No encontrado"
                    txt_ruts_resultados.insert(tk.END, f"  • {tipo}: {val}\n")
                
                txt_ruts_resultados.configure(state="disabled")
                btn_generar_ruts.config(text="▶ Generar RUTs de Prueba", state="normal")
            
            root.after(0, actualizar_gui)
            
        t = threading.Thread(target=tarea_en_hilo)
        t.daemon = True
        t.start()
        
    btn_generar_ruts.config(command=procesar_busqueda)
    
    entry_rut.focus_set()

    root.mainloop()

if __name__ == "__main__":
    iniciar_interfaz()
