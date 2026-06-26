def graficar_conica(canvas, coeficientes):
    canvas.delete("all")
    canvas.update_idletasks()
    w = canvas.winfo_width()
    h = canvas.winfo_height()

    if w <= 1 or h <= 1:
        w, h = 600, 500

    A = coeficientes["A"]
    B = coeficientes["B"]
    C = coeficientes["C"]
    D = coeficientes["D"]
    E = coeficientes["E"]

    cx = -C / (2 * A) if A != 0 else 0
    cy = -D / (2 * B) if B != 0 else 0

    rango = 15.0
    escala = min(w, h) / (rango * 2)

    def a_pixels(x, y):
        px = w / 2 + (x - cx) * escala
        py = h / 2 - (y - cy) * escala
        return px, py

    for i in range(-int(rango), int(rango) + 1):
        px, _ = a_pixels(cx + i, 0)
        canvas.create_line(px, 0, px, h, fill="#e6f2ff")
        _, py = a_pixels(0, cy + i)
        canvas.create_line(0, py, w, py, fill="#e6f2ff")

    _, py_eje_x = a_pixels(0, 0)
    canvas.create_line(0, py_eje_x, w, py_eje_x, fill="#5b7cfa", width=2)

    px_eje_y, _ = a_pixels(0, 0)
    canvas.create_line(px_eje_y, 0, px_eje_y, h, fill="#5b7cfa", width=2)

    px_c, py_c = a_pixels(cx, cy)
    canvas.create_oval(
        px_c - 4,
        py_c - 4,
        px_c + 4,
        py_c + 4,
        fill="#38bdf8",
        outline="#2563eb",
    )

    puntos_graficados = 0

    def dibujar_punto(x, y):
        nonlocal puntos_graficados
        if cx - rango <= x <= cx + rango and cy - rango <= y <= cy + rango:
            px, py = a_pixels(x, y)
            canvas.create_rectangle(
                px - 1,
                py - 1,
                px + 1,
                py + 1,
                fill="#7c3aed",
                outline="#7c3aed",
            )
            puntos_graficados += 1

    paso = (rango * 2) / 1200.0

    x = cx - rango
    while x <= cx + rango:
        c_eq = A * x * x + C * x + E
        if B == 0:
            if D != 0:
                dibujar_punto(x, -c_eq / D)
        else:
            delta = D * D - 4 * B * c_eq
            if delta >= 0:
                raiz = delta ** 0.5
                dibujar_punto(x, (-D + raiz) / (2 * B))
                dibujar_punto(x, (-D - raiz) / (2 * B))
        x += paso

    y = cy - rango
    while y <= cy + rango:
        c_eq = B * y * y + D * y + E
        if A == 0:
            if C != 0:
                dibujar_punto(-c_eq / C, y)
        else:
            delta = C * C - 4 * A * c_eq
            if delta >= 0:
                raiz = delta ** 0.5
                dibujar_punto((-C + raiz) / (2 * A), y)
                dibujar_punto((-C - raiz) / (2 * A), y)
        y += paso

    if puntos_graficados == 0:
        canvas.create_text(
            w / 2,
            h / 2 + 34,
            text="Sin puntos reales para graficar",
            fill="#7c3aed",
            font=("Segoe UI", 13, "bold"),
        )


def graficar_funcion_por_tramos(canvas, analisis):
    canvas.delete("all")
    canvas.update_idletasks()
    w = canvas.winfo_width()
    h = canvas.winfo_height()

    if w <= 1 or h <= 1:
        w, h = 600, 500

    a = analisis["a"]
    cx = a
    cy = 0.0

    rango = 10.0
    escala = min(w, h) / (rango * 2)

    def a_pixels(x, y):
        px = w / 2 + (x - cx) * escala
        py = h / 2 - (y - cy) * escala
        return px, py

    # Dibujar cuadrícula
    for i in range(-int(rango), int(rango) + 1):
        # vertical grid line
        px, _ = a_pixels(cx + i, 0)
        canvas.create_line(px, 0, px, h, fill="#e6f2ff")
        # horizontal grid line
        _, py = a_pixels(0, cy + i)
        canvas.create_line(0, py, w, py, fill="#e6f2ff")

    # Eje X (y = 0)
    _, py_eje_x = a_pixels(0, 0)
    canvas.create_line(0, py_eje_x, w, py_eje_x, fill="#5b7cfa", width=2)

    # Eje Y (x = 0)
    px_eje_y, _ = a_pixels(0, 0)
    canvas.create_line(px_eje_y, 0, px_eje_y, h, fill="#5b7cfa", width=2)

    # Ticks y etiquetas del Eje X
    for i in range(-int(rango), int(rango) + 1):
        if i == 0:
            continue
        val_x = cx + i
        px, py = a_pixels(val_x, 0)
        if 0 <= px <= w:
            canvas.create_line(px, py - 3, px, py + 3, fill="#5b7cfa", width=1.5)
            val_str = f"{val_x:.1f}".rstrip("0").rstrip(".")
            canvas.create_text(px, py + 12, text=val_str, fill="#172554", font=("Segoe UI", 8))

    # Ticks y etiquetas del Eje Y
    for i in range(-int(rango), int(rango) + 1):
        if i == 0:
            continue
        val_y = cy + i
        px, py = a_pixels(0, val_y)
        if 0 <= py <= h:
            canvas.create_line(px - 3, py, px + 3, py, fill="#5b7cfa", width=1.5)
            val_str = f"{val_y:.1f}".rstrip("0").rstrip(".")
            canvas.create_text(px - 12, py, text=val_str, fill="#172554", font=("Segoe UI", 8), anchor="e")

    # Línea de discontinuidad en x = a (roja segmentada)
    px_a, _ = a_pixels(a, 0)
    canvas.create_line(px_a, 0, px_a, h, fill="#ef4444", dash=(4, 4), width=1.5)
    canvas.create_text(px_a + 12, 10, text=f"x = {a}", fill="#ef4444", anchor="nw", font=("Segoe UI", 9, "bold"))

    # Dibujar segmentos
    segmentos = analisis.get("puntos_grafico", [])
    puntos_graficados = 0

    for segment in segmentos:
        if len(segment) < 2:
            continue
        
        coords = []
        for p in segment:
            px, py = a_pixels(p["x"], p["y"])
            if -w <= px <= w * 2 and -h <= py <= h * 2:
                coords.append(px)
                coords.append(py)
        
        if len(coords) >= 4:
            canvas.create_line(*coords, fill="#7c3aed", width=3.0)
            puntos_graficados += len(segment)

    # Dibujar puntos críticos / discontinuidades
    clave_caso = analisis["caso"]["clave"]
    limites = analisis["limites"]
    
    if clave_caso == "removible":
        L = limites.get("valor")
        if L is not None and isinstance(L, (int, float)):
            px, py = a_pixels(a, L)
            canvas.create_oval(px - 5, py - 5, px + 5, py + 5, fill="white", outline="#7c3aed", width=2)
            
    elif clave_caso == "salto":
        L_izq = limites.get("izquierda")
        L_der = limites.get("derecha")
        if L_izq is not None and isinstance(L_izq, (int, float)):
            px_izq, py_izq = a_pixels(a, L_izq)
            canvas.create_oval(px_izq - 5, py_izq - 5, px_izq + 5, py_izq + 5, fill="white", outline="#7c3aed", width=2)
        if L_der is not None and isinstance(L_der, (int, float)):
            px_der, py_der = a_pixels(a, L_der)
            canvas.create_oval(px_der - 5, py_der - 5, px_der + 5, py_der + 5, fill="#7c3aed", outline="#7c3aed", width=2)

    if puntos_graficados == 0:
        canvas.create_text(
            w / 2,
            h / 2 + 34,
            text="Sin puntos para graficar",
            fill="#7c3aed",
            font=("Segoe UI", 13, "bold"),
        )

