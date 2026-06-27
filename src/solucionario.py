from src.elementos import calcular_elementos_geometricos
from src.utils import formatear_numero

def generar_solucionario(coeficientes, tipo):
    A = coeficientes["A"]
    B = coeficientes["B"]
    C = coeficientes["C"]
    D = coeficientes["D"]
    E = coeficientes["E"]
    
    elementos = calcular_elementos_geometricos(coeficientes, tipo)
    if not elementos:
        return [("No se pudieron calcular los elementos geométricos.", "calculo")]
        
    lineas = []
    lineas.append((f"{tipo.upper()}", "titulo"))
    lineas.append((f"Ecuación general: {formatear_numero(A)}x² + {formatear_numero(B)}y² + {formatear_numero(C)}x + {formatear_numero(D)}y + {formatear_numero(E)} = 0", "subtitulo"))
    
    if tipo == "Circunferencia":
        h, k = elementos["h"], elementos["k"]
        r = elementos["radio"]
        
        lineas.append(("Centro (h, k)", "subtitulo"))
        lineas.append(("h = -C / (2A)   |   k = -D / (2A)", "formula"))
        lineas.append((f"h = -({formatear_numero(C)}) / (2*{formatear_numero(A)})  ->  {formatear_numero(h)}", "calculo"))
        lineas.append((f"k = -({formatear_numero(D)}) / (2*{formatear_numero(A)})  ->  {formatear_numero(k)}", "calculo"))
        lineas.append((f"C({formatear_numero(h)}, {formatear_numero(k)})", "resultado"))
        
        lineas.append(("Radio (r)", "subtitulo"))
        lineas.append(("r = √(C² + D² - 4AE) / |2A|", "formula"))
        disc = elementos["discriminante"]
        lineas.append((f"Δ = ({formatear_numero(C)})² + ({formatear_numero(D)})² - 4({formatear_numero(A)})({formatear_numero(E)}) = {formatear_numero(disc)}", "calculo"))
        lineas.append((f"r = √{formatear_numero(disc)} / {formatear_numero(abs(2*A))}", "calculo"))
        lineas.append((f"r = {formatear_numero(r)}", "resultado"))
        
    elif tipo == "Parabola" or tipo == "Parábola":
        es_vertical = elementos["es_vertical"]
        h, k = elementos["h"], elementos["k"]
        p_val = elementos["p"]
        f_x, f_y = elementos["focos"][0]
        
        lineas.append(("Orientación", "subtitulo"))
        lineas.append((("Vertical" if es_vertical else "Horizontal"), "resultado"))
        
        lineas.append(("Vértice V(h, k)", "subtitulo"))
        if es_vertical:
            lineas.append(("h = -C / (2A)", "formula"))
            lineas.append((f"h = -({formatear_numero(C)}) / (2*{formatear_numero(A)})  ->  {formatear_numero(h)}", "calculo"))
            lineas.append((f"k = -({formatear_numero(A)}*{formatear_numero(h)}² + {formatear_numero(C)}*{formatear_numero(h)} + {formatear_numero(E)}) / {formatear_numero(D)}  ->  {formatear_numero(k)}", "calculo"))
        else:
            lineas.append(("k = -D / (2B)", "formula"))
            lineas.append((f"k = -({formatear_numero(D)}) / (2*{formatear_numero(B)})  ->  {formatear_numero(k)}", "calculo"))
            lineas.append((f"h = -({formatear_numero(B)}*{formatear_numero(k)}² + {formatear_numero(D)}*{formatear_numero(k)} + {formatear_numero(E)}) / {formatear_numero(C)}  ->  {formatear_numero(h)}", "calculo"))
        lineas.append((f"V({formatear_numero(h)}, {formatear_numero(k)})", "resultado"))
        
        lineas.append(("Parámetro (p)", "subtitulo"))
        if es_vertical:
            lineas.append(("p = -D / (4A)", "formula"))
            lineas.append((f"p = -({formatear_numero(D)}) / (4*{formatear_numero(A)})", "calculo"))
        else:
            lineas.append(("p = -C / (4B)", "formula"))
            lineas.append((f"p = -({formatear_numero(C)}) / (4*{formatear_numero(B)})", "calculo"))
        lineas.append((f"p = {formatear_numero(p_val)}", "resultado"))
        
        lineas.append(("Foco (F)", "subtitulo"))
        if es_vertical:
            lineas.append(("F(h, k + p)", "formula"))
        else:
            lineas.append(("F(h + p, k)", "formula"))
        lineas.append((f"F({formatear_numero(f_x)}, {formatear_numero(f_y)})", "resultado"))
        
        lineas.append(("Directriz y Eje", "subtitulo"))
        if es_vertical:
            lineas.append((f"Directriz: y = {formatear_numero(elementos['directriz'])}", "calculo"))
            lineas.append((f"Eje de simetría: x = {formatear_numero(elementos['eje'])}", "calculo"))
        else:
            lineas.append((f"Directriz: x = {formatear_numero(elementos['directriz'])}", "calculo"))
            lineas.append((f"Eje de simetría: y = {formatear_numero(elementos['eje'])}", "calculo"))
            
    elif tipo == "Elipse":
        h, k = elementos["h"], elementos["k"]
        a, b, c = elementos["a"], elementos["b"], elementos["c"]
        rhs = elementos["rhs"]
        ax2, by2 = elementos["ax2"], elementos["by2"]
        es_horizontal = elementos["es_horizontal"]
        
        lineas.append(("Centro (h, k)", "subtitulo"))
        lineas.append(("h = -C / (2A)   |   k = -D / (2B)", "formula"))
        lineas.append((f"h = -({formatear_numero(C)}) / (2*{formatear_numero(A)})  ->  {formatear_numero(h)}", "calculo"))
        lineas.append((f"k = -({formatear_numero(D)}) / (2*{formatear_numero(B)})  ->  {formatear_numero(k)}", "calculo"))
        lineas.append((f"C({formatear_numero(h)}, {formatear_numero(k)})", "resultado"))
        
        lineas.append(("Parámetros (a, b, c)", "subtitulo"))
        lineas.append((f"Término independiente (rhs) = {formatear_numero(rhs)}", "calculo"))
        lineas.append((f"rx² = rhs/A = {formatear_numero(ax2)}  |  ry² = rhs/B = {formatear_numero(by2)}", "calculo"))
        lineas.append((("Horizontal" if es_horizontal else "Vertical"), "resultado"))
        lineas.append((f"a = √max(rx², ry²) = {formatear_numero(a)}", "calculo"))
        lineas.append((f"b = √min(rx², ry²) = {formatear_numero(b)}", "calculo"))
        lineas.append((f"c = √(a² - b²) = {formatear_numero(c)}", "calculo"))
        
        lineas.append(("Longitud de Ejes", "subtitulo"))
        lineas.append((f"Eje mayor = 2a = 2({formatear_numero(a)}) = {formatear_numero(elementos['eje_mayor'])}", "resultado"))
        lineas.append((f"Eje menor = 2b = 2({formatear_numero(b)}) = {formatear_numero(elementos['eje_menor'])}", "resultado"))
        
        lineas.append(("Vértices Reales", "subtitulo"))
        v1, v2 = elementos["vertices"]
        lineas.append((f"V1({formatear_numero(v1[0])}, {formatear_numero(v1[1])})   V2({formatear_numero(v2[0])}, {formatear_numero(v2[1])})", "resultado"))
        
        lineas.append(("Focos", "subtitulo"))
        f1, f2 = elementos["focos"]
        lineas.append((f"F1({formatear_numero(f1[0])}, {formatear_numero(f1[1])})   F2({formatear_numero(f2[0])}, {formatear_numero(f2[1])})", "resultado"))

    elif tipo == "Hiperbola" or tipo == "Hipérbola":
        h, k = elementos["h"], elementos["k"]
        a, b, c = elementos["a"], elementos["b"], elementos["c"]
        rhs = elementos["rhs"]
        es_horizontal = elementos["es_horizontal"]
        
        lineas.append(("Centro (h, k)", "subtitulo"))
        lineas.append(("h = -C / (2A)   |   k = -D / (2B)", "formula"))
        lineas.append((f"h = -({formatear_numero(C)}) / (2*{formatear_numero(A)})  ->  {formatear_numero(h)}", "calculo"))
        lineas.append((f"k = -({formatear_numero(D)}) / (2*{formatear_numero(B)})  ->  {formatear_numero(k)}", "calculo"))
        lineas.append((f"C({formatear_numero(h)}, {formatear_numero(k)})", "resultado"))
        
        lineas.append(("Parámetros (a, b, c)", "subtitulo"))
        lineas.append((f"rhs = {formatear_numero(rhs)}", "calculo"))
        lineas.append((("Horizontal" if es_horizontal else "Vertical"), "resultado"))
        lineas.append((f"a = {formatear_numero(a)}", "calculo"))
        lineas.append((f"b = {formatear_numero(b)}", "calculo"))
        lineas.append((f"c = √(a² + b²) = {formatear_numero(c)}", "calculo"))
        
        lineas.append(("Longitud de Ejes", "subtitulo"))
        lineas.append((f"Eje mayor (transverso) = 2a = 2({formatear_numero(a)}) = {formatear_numero(elementos['eje_mayor'])}", "resultado"))
        lineas.append((f"Eje menor (conjugado) = 2b = 2({formatear_numero(b)}) = {formatear_numero(elementos['eje_menor'])}", "resultado"))
        
        lineas.append(("Vértices Reales", "subtitulo"))
        v1, v2 = elementos["vertices"]
        lineas.append((f"V1({formatear_numero(v1[0])}, {formatear_numero(v1[1])})   V2({formatear_numero(v2[0])}, {formatear_numero(v2[1])})", "resultado"))
        
        lineas.append(("Focos", "subtitulo"))
        f1, f2 = elementos["focos"]
        lineas.append((f"F1({formatear_numero(f1[0])}, {formatear_numero(f1[1])})   F2({formatear_numero(f2[0])}, {formatear_numero(f2[1])})", "resultado"))

    return lineas

