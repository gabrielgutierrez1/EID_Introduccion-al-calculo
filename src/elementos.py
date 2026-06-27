def calcular_elementos_geometricos(coeficientes, tipo):
    A = coeficientes["A"]
    B = coeficientes["B"]
    C = coeficientes["C"]
    D = coeficientes["D"]
    E = coeficientes["E"]
    
    elementos = {}
    
    if tipo == "Circunferencia":
        if A == 0: return elementos
        h = -C / (2 * A)
        k = -D / (2 * A)
        discriminante = C**2 + D**2 - 4 * A * E
        if discriminante > 0:
            r = (discriminante ** 0.5) / (2 * abs(A))
            elementos["centro"] = (h, k)
            elementos["radio"] = r
            elementos["h"] = h
            elementos["k"] = k
            elementos["discriminante"] = discriminante
            
    elif tipo == "Parabola" or tipo == "Parábola":
        if A != 0 and B == 0 and D != 0:
            # Parábola vertical
            h = -C / (2 * A)
            k = -(A * h**2 + C * h + E) / D
            p = -D / (4 * A)
            foco_x = h
            foco_y = k + p
            directrix_y = k - p
            elementos["vertices"] = [(h, k)]
            elementos["focos"] = [(foco_x, foco_y)]
            elementos["directriz"] = directrix_y
            elementos["eje"] = h
            elementos["h"] = h
            elementos["k"] = k
            elementos["p"] = p
            elementos["es_vertical"] = True
            
        elif A == 0 and B != 0 and C != 0:
            # Parábola horizontal
            k = -D / (2 * B)
            h = -(B * k**2 + D * k + E) / C
            p = -C / (4 * B)
            foco_x = h + p
            foco_y = k
            directrix_x = h - p
            elementos["vertices"] = [(h, k)]
            elementos["focos"] = [(foco_x, foco_y)]
            elementos["directriz"] = directrix_x
            elementos["eje"] = k
            elementos["h"] = h
            elementos["k"] = k
            elementos["p"] = p
            elementos["es_vertical"] = False
            
    elif tipo == "Elipse":
        if A == 0 or B == 0 or A == B: return elementos
        h = -C / (2 * A)
        k = -D / (2 * B)
        rhs = (C * C) / (4 * A) + (D * D) / (4 * B) - E
        if rhs > 0:
            ax2 = rhs / A
            by2 = rhs / B
            if ax2 > by2:
                a = ax2 ** 0.5
                b = by2 ** 0.5
                c = (ax2 - by2) ** 0.5
                v1, v2 = (h - a, k), (h + a, k)
                f1, f2 = (h - c, k), (h + c, k)
                es_horizontal = True
            else:
                a = by2 ** 0.5
                b = ax2 ** 0.5
                c = (by2 - ax2) ** 0.5
                v1, v2 = (h, k - a), (h, k + a)
                f1, f2 = (h, k - c), (h, k + c)
                es_horizontal = False
            elementos["centro"] = (h, k)
            elementos["vertices"] = [v1, v2]
            elementos["focos"] = [f1, f2]
            elementos["eje_mayor"] = 2 * a
            elementos["eje_menor"] = 2 * b
            elementos["h"] = h
            elementos["k"] = k
            elementos["a"] = a
            elementos["b"] = b
            elementos["c"] = c
            elementos["rhs"] = rhs
            elementos["ax2"] = ax2
            elementos["by2"] = by2
            elementos["es_horizontal"] = es_horizontal
            
    elif tipo == "Hiperbola" or tipo == "Hipérbola":
        if A == 0 or B == 0: return elementos
        h = -C / (2 * A)
        k = -D / (2 * B)
        rhs = (C * C) / (4 * A) + (D * D) / (4 * B) - E
        if abs(rhs) > 1e-9:
            if A / rhs > 0:
                a2 = rhs / A
                b2 = -rhs / B
                a = a2 ** 0.5
                b = b2 ** 0.5
                c = (a2 + b2) ** 0.5
                v1, v2 = (h - a, k), (h + a, k)
                f1, f2 = (h - c, k), (h + c, k)
                es_horizontal = True
            else:
                a2 = rhs / B
                b2 = -rhs / A
                a = a2 ** 0.5
                b = b2 ** 0.5
                c = (a2 + b2) ** 0.5
                v1, v2 = (h, k - a), (h, k + a)
                f1, f2 = (h, k - c), (h, k + c)
                es_horizontal = False
            elementos["centro"] = (h, k)
            elementos["vertices"] = [v1, v2]
            elementos["focos"] = [f1, f2]
            elementos["eje_mayor"] = 2 * a
            elementos["eje_menor"] = 2 * b
            elementos["h"] = h
            elementos["k"] = k
            elementos["a"] = a
            elementos["b"] = b
            elementos["c"] = c
            elementos["rhs"] = rhs
            elementos["a2"] = a2
            elementos["b2"] = b2
            elementos["es_horizontal"] = es_horizontal
            
    return elementos

