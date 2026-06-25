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
