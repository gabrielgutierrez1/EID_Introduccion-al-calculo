def marcar_elementos_hiperbola(canvas, coeficientes, a_pixels, limites_visibles):
    A = coeficientes["A"]
    B = coeficientes["B"]
    C = coeficientes["C"]
    D = coeficientes["D"]
    E = coeficientes["E"]
    
    x_min, x_max, y_min, y_max = limites_visibles

    if A == 0 or B == 0 or A * B >= 0:
        return # No es una hipérbola válida

    h = -C / (2 * A)
    k = -D / (2 * B)

    # Lado derecho trasplantado a la forma trasladada: A(x-h)^2 + B(y-k)^2 = rhs
    rhs = (C * C) / (4 * A) + (D * D) / (4 * B) - E

    if abs(rhs) < 1e-9:
        return # Caso degenerado (dos rectas que se cruzan)

    if A / rhs > 0:
        # Hipérbola horizontal: (x-h)^2 / a^2 - (y-k)^2 / b^2 = 1
        a2 = rhs / A
        b2 = -rhs / B
        es_horizontal = True
    else:
        # Hipérbola vertical: (y-k)^2 / a^2 - (x-h)^2 / b^2 = 1
        a2 = rhs / B
        b2 = -rhs / A
        es_horizontal = False

    a = a2 ** 0.5
    b = b2 ** 0.5
    c = (a2 + b2) ** 0.5

    def dibujar_punto_destacado(x, y, color, radio=5):
        px, py = a_pixels(x, y)
        canvas.create_oval(px - radio, py - radio, px + radio, py + radio, fill=color, outline="black")

    def dibujar_asintotas():
        # Pendiente m de las asíntotas
        m = (b / a) if es_horizontal else (a / b)
        
        # Asíntota 1: y = k + m * (x - h)
        y1_min = k + m * (x_min - h)
        y1_max = k + m * (x_max - h)
        px1_min, py1_min = a_pixels(x_min, y1_min)
        px1_max, py1_max = a_pixels(x_max, y1_max)
        canvas.create_line(px1_min, py1_min, px1_max, py1_max, fill="#64748b", dash=(4, 4), width=1.5)

        # Asíntota 2: y = k - m * (x - h)
        y2_min = k - m * (x_min - h)
        y2_max = k - m * (x_max - h)
        px2_min, py2_min = a_pixels(x_min, y2_min)
        px2_max, py2_max = a_pixels(x_max, y2_max)
        canvas.create_line(px2_min, py2_min, px2_max, py2_max, fill="#64748b", dash=(4, 4), width=1.5)

    def dibujar_leyenda():
        # Fondo y borde de la leyenda
        x_base = 20
        y_base = 20
        canvas.create_rectangle(x_base, y_base, x_base + 165, y_base + 130, fill="white", outline="#ccc", width=1)
        
        # Centro
        canvas.create_oval(x_base + 10, y_base + 12, x_base + 20, y_base + 22, fill="#38bdf8", outline="black")
        canvas.create_text(x_base + 30, y_base + 17, text="Centro", fill="#172554", anchor="w", font=("Segoe UI", 9, "bold"))
        
        # Vértices
        canvas.create_oval(x_base + 10, y_base + 34, x_base + 20, y_base + 44, fill="#ff0000", outline="black")
        canvas.create_text(x_base + 30, y_base + 39, text="Vértices", fill="#172554", anchor="w", font=("Segoe UI", 9, "bold"))
        
        # Vértices Sec
        canvas.create_oval(x_base + 10, y_base + 56, x_base + 20, y_base + 66, fill="#d946ef", outline="black")
        canvas.create_text(x_base + 30, y_base + 61, text="Vértices Secundarios", fill="#172554", anchor="w", font=("Segoe UI", 9, "bold"))
        
        # Focos
        canvas.create_oval(x_base + 10, y_base + 78, x_base + 20, y_base + 88, fill="#00aa00", outline="black")
        canvas.create_text(x_base + 30, y_base + 83, text="Focos", fill="#172554", anchor="w", font=("Segoe UI", 9, "bold"))

        # Asíntotas
        canvas.create_line(x_base + 10, y_base + 105, x_base + 20, y_base + 105, fill="#64748b", dash=(4, 4), width=1.5)
        canvas.create_text(x_base + 30, y_base + 105, text="Asíntotas", fill="#172554", anchor="w", font=("Segoe UI", 9, "bold"))

    # 1. Dibujar asíntotas
    dibujar_asintotas()

    # 2. Dibujar vértices
    if es_horizontal:
        dibujar_punto_destacado(h - a, k, "#ff0000")
        dibujar_punto_destacado(h + a, k, "#ff0000")
    else:
        dibujar_punto_destacado(h, k - a, "#ff0000")
        dibujar_punto_destacado(h, k + a, "#ff0000")

    # 3. Dibujar vértices secundarios 
    if es_horizontal:
        dibujar_punto_destacado(h, k + b, "#d946ef")
        dibujar_punto_destacado(h, k - b, "#d946ef")
    else:
        dibujar_punto_destacado(h + b, k, "#d946ef")
        dibujar_punto_destacado(h - b, k, "#d946ef")

    # 4. Dibujar focos
    if es_horizontal:
        dibujar_punto_destacado(h - c, k, "#00aa00")
        dibujar_punto_destacado(h + c, k, "#00aa00")
    else:
        dibujar_punto_destacado(h, k - c, "#00aa00")
        dibujar_punto_destacado(h, k + c, "#00aa00")

    # 5. Dibujar centro
    dibujar_punto_destacado(h, k, "#38bdf8")

    # 6. Dibujar leyenda
    dibujar_leyenda()
