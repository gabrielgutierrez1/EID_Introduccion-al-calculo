def marcar_elementos_parabola(canvas, coeficientes, a_pixels, limites_visibles, mostrar_nombres=True):
    A = coeficientes["A"]
    B = coeficientes["B"]
    C = coeficientes["C"]
    D = coeficientes["D"]
    E = coeficientes["E"]
    
    x_min, x_max, y_min, y_max = limites_visibles

    def dibujar_punto_destacado(x, y, color, radio=5):
        px, py = a_pixels(x, y)
        # Dibujar punto
        canvas.create_oval(px - radio, py - radio, px + radio, py + radio, fill=color, outline="black")
            
    def dibujar_linea(color, vertical=False, horizontal=False, val=0):
        # Para directrices
        if vertical:
            px_val, _ = a_pixels(val, 0)
            canvas.create_line(px_val, 0, px_val, canvas.winfo_height(), fill=color, dash=(4, 4), width=2)
        elif horizontal:
            _, py_val = a_pixels(0, val)
            canvas.create_line(0, py_val, canvas.winfo_width(), py_val, fill=color, dash=(4, 4), width=2)

    def dibujar_segmento_p(x1, y1, x2, y2, texto):
        px1, py1 = a_pixels(x1, y1)
        px2, py2 = a_pixels(x2, y2)
        canvas.create_line(px1, py1, px2, py2, fill="#2563eb", width=2, arrow="last")
        if mostrar_nombres:
            canvas.create_text(
                (px1 + px2) / 2 + 10,
                (py1 + py2) / 2,
                text=texto,
                fill="#2563eb",
                anchor="w",
                font=("Segoe UI", 9, "bold"),
            )

    def dibujar_leyenda():
        # Fondo y borde de la leyenda
        x_base = 20
        y_base = 20
        canvas.create_rectangle(x_base, y_base, x_base + 145, y_base + 140, fill="white", outline="#ccc", width=1)
        
        # Vértice
        canvas.create_oval(x_base + 10, y_base + 15, x_base + 20, y_base + 25, fill="#ff0000", outline="black")
        canvas.create_text(x_base + 30, y_base + 20, text="Vértice", fill="#172554", anchor="w", font=("Segoe UI", 10, "bold"))
        
        # Foco
        canvas.create_oval(x_base + 10, y_base + 40, x_base + 20, y_base + 50, fill="#00aa00", outline="black")
        canvas.create_text(x_base + 30, y_base + 45, text="Foco", fill="#172554", anchor="w", font=("Segoe UI", 10, "bold"))
        
        # Directriz
        canvas.create_line(x_base + 10, y_base + 70, x_base + 20, y_base + 70, fill="#ff8800", dash=(4, 4), width=2)
        canvas.create_text(x_base + 30, y_base + 70, text="Directriz", fill="#172554", anchor="w", font=("Segoe UI", 10, "bold"))

        # Eje de simetría
        canvas.create_line(x_base + 10, y_base + 95, x_base + 20, y_base + 95, fill="#64748b", dash=(2, 3), width=2)
        canvas.create_text(x_base + 30, y_base + 95, text="Eje", fill="#172554", anchor="w", font=("Segoe UI", 10, "bold"))

        # Lado recto
        canvas.create_oval(x_base + 10, y_base + 115, x_base + 20, y_base + 125, fill="#d946ef", outline="black")
        canvas.create_text(x_base + 30, y_base + 120, text="Lado recto", fill="#172554", anchor="w", font=("Segoe UI", 10, "bold"))

    if A != 0 and B == 0:
        # Parábola vertical: A x^2 + C x + D y + E = 0
        if D == 0:
            return # Degenerada
        
        h = -C / (2 * A)
        k = -(A * h**2 + C * h + E) / D
        p = -D / (4 * A)
        
        foco_x = h
        foco_y = k + p
        directrix_y = k - p
        lado_recto_1 = (h - 2 * abs(p), foco_y)
        lado_recto_2 = (h + 2 * abs(p), foco_y)
        
        dibujar_linea("#ff8800", horizontal=True, val=directrix_y)
        dibujar_linea("#64748b", vertical=True, val=h)
        dibujar_segmento_p(h, k, foco_x, foco_y, f"p = {p:.4g}")
        dibujar_punto_destacado(h, k, "#ff0000")
        dibujar_punto_destacado(foco_x, foco_y, "#00aa00")
        dibujar_punto_destacado(lado_recto_1[0], lado_recto_1[1], "#d946ef", radio=4)
        dibujar_punto_destacado(lado_recto_2[0], lado_recto_2[1], "#d946ef", radio=4)
        if mostrar_nombres:
            dibujar_leyenda()
        
    elif A == 0 and B != 0:
        # Parábola horizontal: B y^2 + C x + D y + E = 0
        if C == 0:
            return # Degenerada
            
        k = -D / (2 * B)
        h = -(B * k**2 + D * k + E) / C
        p = -C / (4 * B)
        
        foco_x = h + p
        foco_y = k
        directrix_x = h - p
        lado_recto_1 = (foco_x, k - 2 * abs(p))
        lado_recto_2 = (foco_x, k + 2 * abs(p))
        
        dibujar_linea("#ff8800", vertical=True, val=directrix_x)
        dibujar_linea("#64748b", horizontal=True, val=k)
        dibujar_segmento_p(h, k, foco_x, foco_y, f"p = {p:.4g}")
        dibujar_punto_destacado(h, k, "#ff0000")
        dibujar_punto_destacado(foco_x, foco_y, "#00aa00")
        dibujar_punto_destacado(lado_recto_1[0], lado_recto_1[1], "#d946ef", radio=4)
        dibujar_punto_destacado(lado_recto_2[0], lado_recto_2[1], "#d946ef", radio=4)
        if mostrar_nombres:
            dibujar_leyenda()
