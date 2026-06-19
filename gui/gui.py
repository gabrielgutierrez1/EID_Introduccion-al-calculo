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

    def mostrar_rut():
        rut_ingresado = entry_rut.get()
        resultado = validar_rut(rut_ingresado)

        lineas_mostrar = formatear_resultado_rut(resultado)
        
        if resultado["valido"]:
            digitos = obtener_digitos(resultado["cuerpo"])
            resultado_conica = analizar_conica(digitos, resultado["dv_ingresado"])
            lineas_mostrar.extend(formatear_resultado_conica(resultado_conica))

        txt_resultados.configure(state="normal")
        txt_resultados.delete("1.0", tk.END)
        txt_resultados.insert(tk.END, "\n".join(lineas_mostrar))
        txt_resultados.configure(state="disabled")

    # Botón conectado al campo de entrada y al panel de resultados
    btn_calcular = tk.Button(root, text="Validar y mostrar RUT", font=("Helvetica", 11, "bold"), bg="#4CAF50", fg="white", relief="flat", pady=5, command=mostrar_rut)
    btn_calcular.pack(pady=20, fill="x")

    # Marco para mostrar resultados
    frame_resultados = tk.LabelFrame(root, text=" Resultados del Análisis ", font=("Helvetica", 11, "bold"), padx=10, pady=10)
    frame_resultados.pack(fill="both", expand=True)

    # Text box para mostrar los resultados detallados más adelante
    txt_resultados = tk.Text(frame_resultados, wrap="word", state="disabled", font=("Courier", 10))
    txt_resultados.pack(fill="both", expand=True)

    entry_rut.focus_set()

    # Iniciar el bucle principal de la aplicación
    root.mainloop()

if __name__ == "__main__":
    iniciar_interfaz()
