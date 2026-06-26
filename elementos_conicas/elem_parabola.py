def marcar_elementos_parabola(canvas, coeficientes, a_pixels, limites_visibles):
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

    def dibujar_leyenda():
        # Fondo y borde de la leyenda
        x_base = 20
        y_base = 20
        canvas.create_rectangle(x_base, y_base, x_base + 100, y_base + 90, fill="white", outline="#ccc", width=1)
        
        # Vértice
        canvas.create_oval(x_base + 10, y_base + 15, x_base + 20, y_base + 25, fill="#ff0000", outline="black")
        canvas.create_text(x_base + 30, y_base + 20, text="Vértice", fill="#172554", anchor="w", font=("Segoe UI", 10, "bold"))
        
        # Foco
        canvas.create_oval(x_base + 10, y_base + 40, x_base + 20, y_base + 50, fill="#00aa00", outline="black")
        canvas.create_text(x_base + 30, y_base + 45, text="Foco", fill="#172554", anchor="w", font=("Segoe UI", 10, "bold"))
        
        # Directriz
        canvas.create_line(x_base + 10, y_base + 70, x_base + 20, y_base + 70, fill="#ff8800", dash=(4, 4), width=2)
        canvas.create_text(x_base + 30, y_base + 70, text="Directriz", fill="#172554", anchor="w", font=("Segoe UI", 10, "bold"))

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
        
        dibujar_linea("#ff8800", horizontal=True, val=directrix_y)
        dibujar_punto_destacado(h, k, "#ff0000")
        dibujar_punto_destacado(foco_x, foco_y, "#00aa00")
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
        
        dibujar_linea("#ff8800", vertical=True, val=directrix_x)
        dibujar_punto_destacado(h, k, "#ff0000")
        dibujar_punto_destacado(foco_x, foco_y, "#00aa00")
        dibujar_leyenda()
