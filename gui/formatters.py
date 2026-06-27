from src.solucionario import generar_solucionario
from src.utils import formatear_numero

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

    # Agregar el resumen de elementos geométricos
    lineas_elementos = generar_solucionario(resultado["coeficientes"], resultado["tipo"])
    
    # Si pudo generar los elementos (longitud > 1), los añadimos omitiendo el primer título repetitivo
    if len(lineas_elementos) > 1:
        lineas.append(("ELEMENTOS GEOMÉTRICOS", "titulo"))
        # Nos saltamos el índice 0 que es el nombre de la cónica en grande y el índice 1 que es la ecuación general de nuevo
        lineas.extend(lineas_elementos[2:])

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
