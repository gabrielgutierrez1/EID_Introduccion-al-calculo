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
    w, h = 400, 400
    
    A = coeficientes["A"]
    B = coeficientes["B"]
    C = coeficientes["C"]
    D = coeficientes["D"]
    E = coeficientes["E"]
    
    # Calcular centro aproximado para enfocar la vista
    cx = -C / (2 * A) if A != 0 else 0
    cy = -D / (2 * B) if B != 0 else 0
    
    rango = 15.0 # Unidades hacia cada lado desde el centro
    escala = (w / 2) / rango
    
    def a_pixels(x, y):
        px = w / 2 + (x - cx) * escala
        py = h / 2 - (y - cy) * escala
        return px, py

    # Dibujar ejes cartesianos (x=0, y=0)
    px1, py1 = a_pixels(cx - rango, 0)
    px2, py2 = a_pixels(cx + rango, 0)
    canvas.create_line(px1, py1, px2, py2, fill="lightgray", dash=(4, 4))
    
    px1, py1 = a_pixels(0, cy - rango)
    px2, py2 = a_pixels(0, cy + rango)
    canvas.create_line(px1, py1, px2, py2, fill="lightgray", dash=(4, 4))
    
    # Dibujar centro
    px_c, py_c = a_pixels(cx, cy)
    canvas.create_oval(px_c-3, py_c-3, px_c+3, py_c+3, fill="blue", outline="blue")
    
    def dibujar_punto(x, y):
        if cx - rango <= x <= cx + rango and cy - rango <= y <= cy + rango:
            px, py = a_pixels(x, y)
            # Dibujar un rectangulo pequeno es mas rapido que oval
            canvas.create_rectangle(px, py, px+1, py+1, fill="red", outline="red")
            
    # Escaneo para graficar evaluando manualmente la ecuacion
    paso = (rango * 2) / 1000.0
    
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
    root = tk.Tk()
    root.title("EID N°1 - Introducción al Cálculo")
    root.geometry("1000x600")
    
    # Configuración de estilos básicos
    root.configure(padx=20, pady=20)

    # Título principal
    lbl_titulo = tk.Label(root, text="Calculadora de Cónicas por RUT", font=("Helvetica", 16, "bold"))
    lbl_titulo.pack(pady=(0, 10))

    # Marco para la entrada de datos
    frame_entrada = tk.Frame(root)
    frame_entrada.pack(pady=5, fill="x")

    lbl_rut = tk.Label(frame_entrada, text="Ingrese RUT (Ej: 21.929.009-8):", font=("Helvetica", 11))
    lbl_rut.pack(side="left", padx=(0, 10))

    entry_rut = tk.Entry(frame_entrada, width=20, font=("Helvetica", 11))
    entry_rut.pack(side="left", expand=True, fill="x")

    # Botón conectado al campo de entrada y al panel de resultados
    btn_calcular = tk.Button(root, text="Validar y mostrar RUT", font=("Helvetica", 11, "bold"), bg="#4CAF50", fg="white", relief="flat", pady=5)
    btn_calcular.pack(pady=10, fill="x")

    # Contenedor principal para resultados y gráfico
    frame_contenido = tk.Frame(root)
    frame_contenido.pack(fill="both", expand=True, pady=10)

    # Lado izquierdo: resultados
    frame_resultados = tk.LabelFrame(frame_contenido, text=" Resultados del Análisis ", font=("Helvetica", 11, "bold"), padx=10, pady=10)
    frame_resultados.pack(side="left", fill="both", expand=True, padx=(0, 10))

    txt_resultados = tk.Text(frame_resultados, wrap="word", state="disabled", font=("Courier", 10), width=40)
    txt_resultados.pack(fill="both", expand=True)

    # Lado derecho: grafico
    frame_grafico = tk.LabelFrame(frame_contenido, text=" Gráfica de la Cónica ", font=("Helvetica", 11, "bold"), padx=10, pady=10)
    frame_grafico.pack(side="right", fill="both")

    canvas_grafico = tk.Canvas(frame_grafico, width=400, height=400, bg="white")
    canvas_grafico.pack(padx=10, pady=10)

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

    # Iniciar el bucle principal de la aplicación
    root.mainloop()

if __name__ == "__main__":
    iniciar_interfaz()
