def obtener_vista_conica(coeficientes):
    A = coeficientes["A"]
    B = coeficientes["B"]
    C = coeficientes["C"]
    D = coeficientes["D"]
    E = coeficientes["E"]

    if A != 0 and B == 0 and D != 0:
        cx = -C / (2 * A)
        cy = -(A * cx * cx + C * cx + E) / D
    elif A == 0 and B != 0 and C != 0:
        cy = -D / (2 * B)
        cx = -(B * cy * cy + D * cy + E) / C
    else:
        cx = -C / (2 * A) if A != 0 else 0
        cy = -D / (2 * B) if B != 0 else 0

    return {"cx": cx, "cy": cy, "rango": 15.0}


def obtener_vista_tramos(analisis):
    return {"cx": analisis["a"], "cy": 0.0, "rango": 10.0}


def _limites_visibles(w, h, vista):
    escala = min(w, h) / (vista["rango"] * 2)
    x_min = vista["cx"] - (w / 2) / escala
    x_max = vista["cx"] + (w / 2) / escala
    y_min = vista["cy"] - (h / 2) / escala
    y_max = vista["cy"] + (h / 2) / escala
    return escala, x_min, x_max, y_min, y_max


def _paso_cuadricula(rango):
    pasos = [0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 50, 100]
    objetivo = rango / 6
    for paso in pasos:
        if paso >= objetivo:
            return paso
    return pasos[-1]


def _dibujar_cuadricula_y_ejes(canvas, w, h, vista, a_pixels):
    escala, x_min, x_max, y_min, y_max = _limites_visibles(w, h, vista)
    paso = _paso_cuadricula(vista["rango"])

    i = int(x_min // paso) - 1
    while i * paso <= x_max + paso:
        x = i * paso
        px, _ = a_pixels(x, 0)
        canvas.create_line(px, 0, px, h, fill="#e6f2ff")
        i += 1

    i = int(y_min // paso) - 1
    while i * paso <= y_max + paso:
        y = i * paso
        _, py = a_pixels(0, y)
        canvas.create_line(0, py, w, py, fill="#e6f2ff")
        i += 1

    _, py_eje_x = a_pixels(0, 0)
    canvas.create_line(0, py_eje_x, w, py_eje_x, fill="#5b7cfa", width=2)

    px_eje_y, _ = a_pixels(0, 0)
    canvas.create_line(px_eje_y, 0, px_eje_y, h, fill="#5b7cfa", width=2)

    return escala, x_min, x_max, y_min, y_max, paso


def _formatear_tick(valor):
    if abs(valor) < 1e-9:
        valor = 0
    return f"{valor:.2f}".rstrip("0").rstrip(".")


def _dibujar_numeros_ejes(canvas, w, h, x_min, x_max, y_min, y_max, paso_tick, a_pixels):
    i = int(x_min // paso_tick) - 1
    while i * paso_tick <= x_max + paso_tick:
        val_x = i * paso_tick
        i += 1
        if abs(val_x) < 1e-9:
            continue

        px, py = a_pixels(val_x, 0)
        if 0 <= px <= w and 0 <= py <= h:
            canvas.create_line(px, py - 3, px, py + 3, fill="#5b7cfa", width=1.5)
            canvas.create_text(
                px,
                py + 12,
                text=_formatear_tick(val_x),
                fill="#172554",
                font=("Segoe UI", 8),
            )

    i = int(y_min // paso_tick) - 1
    while i * paso_tick <= y_max + paso_tick:
        val_y = i * paso_tick
        i += 1
        if abs(val_y) < 1e-9:
            continue

        px, py = a_pixels(0, val_y)
        if 0 <= px <= w and 0 <= py <= h:
            canvas.create_line(px - 3, py, px + 3, py, fill="#5b7cfa", width=1.5)
            canvas.create_text(
                px - 12,
                py,
                text=_formatear_tick(val_y),
                fill="#172554",
                font=("Segoe UI", 8),
                anchor="e",
            )


def graficar_conica(canvas, coeficientes, vista=None):
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

    if vista is None:
        vista = obtener_vista_conica(coeficientes)

    escala = min(w, h) / (vista["rango"] * 2)

    def a_pixels(x, y):
        px = w / 2 + (x - vista["cx"]) * escala
        py = h / 2 - (y - vista["cy"]) * escala
        return px, py

    _, x_min, x_max, y_min, y_max, paso_tick = _dibujar_cuadricula_y_ejes(canvas, w, h, vista, a_pixels)
    _dibujar_numeros_ejes(canvas, w, h, x_min, x_max, y_min, y_max, paso_tick, a_pixels)

    cx = -C / (2 * A) if A != 0 else 0
    cy = -D / (2 * B) if B != 0 else 0

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
        if x_min <= x <= x_max and y_min <= y <= y_max:
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

    paso_x = max((x_max - x_min) / 1400.0, 0.005)
    paso_y = max((y_max - y_min) / 1400.0, 0.005)

    x = x_min
    while x <= x_max:
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
        x += paso_x

    y = y_min
    while y <= y_max:
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
        y += paso_y

    if (A == 0 and B != 0) or (A != 0 and B == 0):
        try:
            import sys
            import os
            PROYECTO_RAIZ = os.path.dirname(os.path.dirname(__file__))
            if PROYECTO_RAIZ not in sys.path:
                sys.path.insert(0, PROYECTO_RAIZ)
            from elementos_conicas.elem_parabola import marcar_elementos_parabola
            marcar_elementos_parabola(canvas, coeficientes, a_pixels, (x_min, x_max, y_min, y_max))
        except Exception as e:
            print(f"No se pudo marcar elementos de la parabola: {e}")
    elif A == B and A != 0:
        try:
            import sys
            import os
            PROYECTO_RAIZ = os.path.dirname(os.path.dirname(__file__))
            if PROYECTO_RAIZ not in sys.path:
                sys.path.insert(0, PROYECTO_RAIZ)
            from elementos_conicas.elem_circunferencia import marcar_elementos_circunferencia
            marcar_elementos_circunferencia(canvas, coeficientes, a_pixels, (x_min, x_max, y_min, y_max))
        except Exception as e:
            print(f"No se pudo marcar elementos de la circunferencia: {e}")

    if puntos_graficados == 0:
        canvas.create_text(
            w / 2,
            h / 2 + 34,
            text="Sin puntos reales para graficar",
            fill="#7c3aed",
            font=("Segoe UI", 13, "bold"),
        )


def graficar_funcion_por_tramos(canvas, analisis, vista=None):
    canvas.delete("all")
    canvas.update_idletasks()
    w = canvas.winfo_width()
    h = canvas.winfo_height()

    if w <= 1 or h <= 1:
        w, h = 600, 500

    a = analisis["a"]
    if vista is None:
        vista = obtener_vista_tramos(analisis)

    escala = min(w, h) / (vista["rango"] * 2)

    def a_pixels(x, y):
        px = w / 2 + (x - vista["cx"]) * escala
        py = h / 2 - (y - vista["cy"]) * escala
        return px, py

    _, x_min, x_max, y_min, y_max, paso_tick = _dibujar_cuadricula_y_ejes(canvas, w, h, vista, a_pixels)
    _dibujar_numeros_ejes(canvas, w, h, x_min, x_max, y_min, y_max, paso_tick, a_pixels)

    # Línea de discontinuidad en x = a (roja segmentada)
    px_a, _ = a_pixels(a, 0)
    if -20 <= px_a <= w + 20:
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
