from src.elementos import calcular_elementos_geometricos

def formatear_num(num):
    if abs(num) < 1e-9:
        return "0"
    if abs(num - round(num)) < 1e-9:
        return str(int(round(num)))
    return f"{num:.4f}".rstrip("0").rstrip(".")

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
    lineas.append((f"Ecuación general: {formatear_num(A)}x² + {formatear_num(B)}y² + {formatear_num(C)}x + {formatear_num(D)}y + {formatear_num(E)} = 0", "subtitulo"))
    
    if tipo == "Circunferencia":
        h, k = elementos["centro"]
        r = elementos["radio"]
        
        lineas.append(("Centro (h, k)", "subtitulo"))
        lineas.append(("h = -C / (2A)   |   k = -D / (2A)", "formula"))
        lineas.append((f"h = -({formatear_num(C)}) / (2*{formatear_num(A)})  ->  {formatear_num(h)}", "calculo"))
        lineas.append((f"k = -({formatear_num(D)}) / (2*{formatear_num(A)})  ->  {formatear_num(k)}", "calculo"))
        lineas.append((f"C({formatear_num(h)}, {formatear_num(k)})", "resultado"))
        
        lineas.append(("Radio (r)", "subtitulo"))
        lineas.append(("r = √(C² + D² - 4AE) / |2A|", "formula"))
        disc = C**2 + D**2 - 4*A*E
        lineas.append((f"Δ = ({formatear_num(C)})² + ({formatear_num(D)})² - 4({formatear_num(A)})({formatear_num(E)}) = {formatear_num(disc)}", "calculo"))
        lineas.append((f"r = √{formatear_num(disc)} / {formatear_num(abs(2*A))}", "calculo"))
        lineas.append((f"r = {formatear_num(r)}", "resultado"))
        
    elif tipo == "Parabola" or tipo == "Parábola":
        es_vertical = (A != 0 and B == 0)
        h, k = elementos["vertices"][0]
        f_x, f_y = elementos["focos"][0]
        p_val = f_y - k if es_vertical else f_x - h
        
        lineas.append(("Orientación", "subtitulo"))
        lineas.append((("Vertical" if es_vertical else "Horizontal"), "resultado"))
        
        lineas.append(("Vértice V(h, k)", "subtitulo"))
        if es_vertical:
            lineas.append(("h = -C / (2A)", "formula"))
            lineas.append((f"h = -({formatear_num(C)}) / (2*{formatear_num(A)})  ->  {formatear_num(h)}", "calculo"))
            lineas.append((f"k = -({formatear_num(A)}*{formatear_num(h)}² + {formatear_num(C)}*{formatear_num(h)} + {formatear_num(E)}) / {formatear_num(D)}  ->  {formatear_num(k)}", "calculo"))
        else:
            lineas.append(("k = -D / (2B)", "formula"))
            lineas.append((f"k = -({formatear_num(D)}) / (2*{formatear_num(B)})  ->  {formatear_num(k)}", "calculo"))
            lineas.append((f"h = -({formatear_num(B)}*{formatear_num(k)}² + {formatear_num(D)}*{formatear_num(k)} + {formatear_num(E)}) / {formatear_num(C)}  ->  {formatear_num(h)}", "calculo"))
        lineas.append((f"V({formatear_num(h)}, {formatear_num(k)})", "resultado"))
        
        lineas.append(("Parámetro (p)", "subtitulo"))
        if es_vertical:
            lineas.append(("p = -D / (4A)", "formula"))
            lineas.append((f"p = -({formatear_num(D)}) / (4*{formatear_num(A)})", "calculo"))
        else:
            lineas.append(("p = -C / (4B)", "formula"))
            lineas.append((f"p = -({formatear_num(C)}) / (4*{formatear_num(B)})", "calculo"))
        lineas.append((f"p = {formatear_num(p_val)}", "resultado"))
        
        lineas.append(("Foco (F)", "subtitulo"))
        if es_vertical:
            lineas.append(("F(h, k + p)", "formula"))
        else:
            lineas.append(("F(h + p, k)", "formula"))
        lineas.append((f"F({formatear_num(f_x)}, {formatear_num(f_y)})", "resultado"))
        
        lineas.append(("Directriz y Eje", "subtitulo"))
        if es_vertical:
            lineas.append((f"Directriz: y = {formatear_num(elementos['directriz'])}", "calculo"))
            lineas.append((f"Eje de simetría: x = {formatear_num(elementos['eje'])}", "calculo"))
        else:
            lineas.append((f"Directriz: x = {formatear_num(elementos['directriz'])}", "calculo"))
            lineas.append((f"Eje de simetría: y = {formatear_num(elementos['eje'])}", "calculo"))
            
    elif tipo == "Elipse":
        h, k = elementos["centro"]
        a = elementos["eje_mayor"] / 2
        b = elementos["eje_menor"] / 2
        c = (a**2 - b**2)**0.5 if a > b else (b**2 - a**2)**0.5
        
        rhs = (C * C) / (4 * A) + (D * D) / (4 * B) - E
        ax2 = rhs / A
        by2 = rhs / B
        es_horizontal = ax2 > by2
        
        lineas.append(("Centro (h, k)", "subtitulo"))
        lineas.append(("h = -C / (2A)   |   k = -D / (2B)", "formula"))
        lineas.append((f"h = -({formatear_num(C)}) / (2*{formatear_num(A)})  ->  {formatear_num(h)}", "calculo"))
        lineas.append((f"k = -({formatear_num(D)}) / (2*{formatear_num(B)})  ->  {formatear_num(k)}", "calculo"))
        lineas.append((f"C({formatear_num(h)}, {formatear_num(k)})", "resultado"))
        
        lineas.append(("Parámetros (a, b, c)", "subtitulo"))
        lineas.append((f"Término independiente (rhs) = {formatear_num(rhs)}", "calculo"))
        lineas.append((f"rx² = rhs/A = {formatear_num(ax2)}  |  ry² = rhs/B = {formatear_num(by2)}", "calculo"))
        lineas.append((("Horizontal" if es_horizontal else "Vertical"), "resultado"))
        lineas.append((f"a = √max(rx², ry²) = {formatear_num(a)}", "calculo"))
        lineas.append((f"b = √min(rx², ry²) = {formatear_num(b)}", "calculo"))
        lineas.append((f"c = √(a² - b²) = {formatear_num(c)}", "calculo"))
        
        lineas.append(("Longitud de Ejes", "subtitulo"))
        lineas.append((f"Eje mayor = 2a = 2({formatear_num(a)}) = {formatear_num(elementos['eje_mayor'])}", "resultado"))
        lineas.append((f"Eje menor = 2b = 2({formatear_num(b)}) = {formatear_num(elementos['eje_menor'])}", "resultado"))
        
        lineas.append(("Vértices Reales", "subtitulo"))
        v1, v2 = elementos["vertices"]
        lineas.append((f"V1({formatear_num(v1[0])}, {formatear_num(v1[1])})   V2({formatear_num(v2[0])}, {formatear_num(v2[1])})", "resultado"))
        
        lineas.append(("Focos", "subtitulo"))
        f1, f2 = elementos["focos"]
        lineas.append((f"F1({formatear_num(f1[0])}, {formatear_num(f1[1])})   F2({formatear_num(f2[0])}, {formatear_num(f2[1])})", "resultado"))

    elif tipo == "Hiperbola" or tipo == "Hipérbola":
        h, k = elementos["centro"]
        a = elementos["eje_mayor"] / 2
        b = elementos["eje_menor"] / 2
        c = (a**2 + b**2)**0.5
        
        rhs = (C * C) / (4 * A) + (D * D) / (4 * B) - E
        es_horizontal = A / rhs > 0
        
        lineas.append(("Centro (h, k)", "subtitulo"))
        lineas.append(("h = -C / (2A)   |   k = -D / (2B)", "formula"))
        lineas.append((f"h = -({formatear_num(C)}) / (2*{formatear_num(A)})  ->  {formatear_num(h)}", "calculo"))
        lineas.append((f"k = -({formatear_num(D)}) / (2*{formatear_num(B)})  ->  {formatear_num(k)}", "calculo"))
        lineas.append((f"C({formatear_num(h)}, {formatear_num(k)})", "resultado"))
        
        lineas.append(("Parámetros (a, b, c)", "subtitulo"))
        lineas.append((f"rhs = {formatear_num(rhs)}", "calculo"))
        lineas.append((("Horizontal" if es_horizontal else "Vertical"), "resultado"))
        lineas.append((f"a = {formatear_num(a)}", "calculo"))
        lineas.append((f"b = {formatear_num(b)}", "calculo"))
        lineas.append((f"c = √(a² + b²) = {formatear_num(c)}", "calculo"))
        
        lineas.append(("Longitud de Ejes", "subtitulo"))
        lineas.append((f"Eje mayor (transverso) = 2a = 2({formatear_num(a)}) = {formatear_num(elementos['eje_mayor'])}", "resultado"))
        lineas.append((f"Eje menor (conjugado) = 2b = 2({formatear_num(b)}) = {formatear_num(elementos['eje_menor'])}", "resultado"))
        
        lineas.append(("Vértices Reales", "subtitulo"))
        v1, v2 = elementos["vertices"]
        lineas.append((f"V1({formatear_num(v1[0])}, {formatear_num(v1[1])})   V2({formatear_num(v2[0])}, {formatear_num(v2[1])})", "resultado"))
        
        lineas.append(("Focos", "subtitulo"))
        f1, f2 = elementos["focos"]
        lineas.append((f"F1({formatear_num(f1[0])}, {formatear_num(f1[1])})   F2({formatear_num(f2[0])}, {formatear_num(f2[1])})", "resultado"))

    return lineas
