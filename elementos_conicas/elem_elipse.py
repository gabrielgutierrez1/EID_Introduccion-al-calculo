def marcar_elementos_elipse(canvas, coeficientes, a_pixels, limites_visibles):
    A = coeficientes["A"]
    B = coeficientes["B"]
    C = coeficientes["C"]
    D = coeficientes["D"]
    E = coeficientes["E"]
    
    x_min, x_max, y_min, y_max = limites_visibles

    if A == 0 or B == 0 or A * B <= 0 or A == B:
        return # No es una elipse válida (o es circunferencia)

    h = -C / (2 * A)
    k = -D / (2 * B)

    # Lado derecho trasplantado a la forma trasladada: A(x-h)^2 + B(y-k)^2 = rhs
    rhs = (C * C) / (4 * A) + (D * D) / (4 * B) - E

    if rhs <= 0:
        return # Elipse imaginaria o punto único

    # Denominadores en la forma (x-h)^2 / ax2 + (y-k)^2 / by2 = 1
    ax2 = rhs / A
    by2 = rhs / B

    if ax2 > by2:
        # Elipse horizontal: semieje mayor en eje X
        a = ax2 ** 0.5
        b = by2 ** 0.5
        c = (ax2 - by2) ** 0.5
        es_horizontal = True
    else:
        # Elipse vertical: semieje mayor en eje Y
        a = by2 ** 0.5
        b = ax2 ** 0.5
        c = (by2 - ax2) ** 0.5
        es_horizontal = False

    def dibujar_punto_destacado(x, y, color, radio=5):
        px, py = a_pixels(x, y)
        canvas.create_oval(px - radio, py - radio, px + radio, py + radio, fill=color, outline="black")

    def dibujar_leyenda():
        # Fondo y borde de la leyenda
        x_base = 20
        y_base = 20
        canvas.create_rectangle(x_base, y_base, x_base + 165, y_base + 110, fill="white", outline="#ccc", width=1)
        
        # Centro
        canvas.create_oval(x_base + 10, y_base + 12, x_base + 20, y_base + 22, fill="#38bdf8", outline="black")
        canvas.create_text(x_base + 30, y_base + 17, text="Centro", fill="#172554", anchor="w", font=("Segoe UI", 9, "bold"))
        
        # Vértices Reales
        canvas.create_oval(x_base + 10, y_base + 34, x_base + 20, y_base + 44, fill="#ff0000", outline="black")
        canvas.create_text(x_base + 30, y_base + 39, text="Vértices Reales", fill="#172554", anchor="w", font=("Segoe UI", 9, "bold"))
        
        # Vértices Secundarios
        canvas.create_oval(x_base + 10, y_base + 56, x_base + 20, y_base + 66, fill="#d946ef", outline="black")
        canvas.create_text(x_base + 30, y_base + 61, text="Vértices Secundarios", fill="#172554", anchor="w", font=("Segoe UI", 9, "bold"))
        
        # Focos
        canvas.create_oval(x_base + 10, y_base + 78, x_base + 20, y_base + 88, fill="#00aa00", outline="black")
        canvas.create_text(x_base + 30, y_base + 83, text="Focos", fill="#172554", anchor="w", font=("Segoe UI", 9, "bold"))

    # 1. Dibujar vértices principales (reales) en el eje mayor
    if es_horizontal:
        dibujar_punto_destacado(h - a, k, "#ff0000")
        dibujar_punto_destacado(h + a, k, "#ff0000")
    else:
        dibujar_punto_destacado(h, k - a, "#ff0000")
        dibujar_punto_destacado(h, k + a, "#ff0000")

    # 2. Dibujar vértices secundarios en el eje menor
    if es_horizontal:
        dibujar_punto_destacado(h, k + b, "#d946ef")
        dibujar_punto_destacado(h, k - b, "#d946ef")
    else:
        dibujar_punto_destacado(h + b, k, "#d946ef")
        dibujar_punto_destacado(h - b, k, "#d946ef")

    # 3. Dibujar focos
    if es_horizontal:
        dibujar_punto_destacado(h - c, k, "#00aa00")
        dibujar_punto_destacado(h + c, k, "#00aa00")
    else:
        dibujar_punto_destacado(h, k - c, "#00aa00")
        dibujar_punto_destacado(h, k + c, "#00aa00")

    # 4. Dibujar centro
    dibujar_punto_destacado(h, k, "#38bdf8")

    # 5. Dibujar leyenda
    dibujar_leyenda()
