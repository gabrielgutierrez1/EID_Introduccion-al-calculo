def marcar_elementos_circunferencia(canvas, coeficientes, a_pixels, limites_visibles, mostrar_nombres=True):
    A = coeficientes["A"]
    B = coeficientes["B"]
    C = coeficientes["C"]
    D = coeficientes["D"]
    E = coeficientes["E"]
    
    if A == 0 or A != B:
        return
        
    h = -C / (2 * A)
    k = -D / (2 * A)
    
    discriminante = C**2 + D**2 - 4 * A * E
    if discriminante <= 0:
        return # No es un circulo real o es solo un punto
        
    r = (discriminante ** 0.5) / (2 * abs(A))
    
    def dibujar_punto_destacado(x, y, color, radio=5):
        px, py = a_pixels(x, y)
        canvas.create_oval(px - radio, py - radio, px + radio, py + radio, fill=color, outline="black")
            
    def dibujar_radio(h, k, r, color):
        px1, py1 = a_pixels(h, k)
        px2, py2 = a_pixels(h + r, k)
        canvas.create_line(px1, py1, px2, py2, fill=color, width=2)
        
    def dibujar_leyenda():
        # Fondo y borde de la leyenda
        x_base = 20
        y_base = 20
        canvas.create_rectangle(x_base, y_base, x_base + 100, y_base + 65, fill="white", outline="#ccc", width=1)
        
        # Centro
        canvas.create_oval(x_base + 10, y_base + 15, x_base + 20, y_base + 25, fill="#ff0000", outline="black")
        canvas.create_text(x_base + 30, y_base + 20, text="Centro", fill="#172554", anchor="w", font=("Segoe UI", 10, "bold"))
        
        # Radio
        canvas.create_line(x_base + 10, y_base + 45, x_base + 20, y_base + 45, fill="#0000ff", width=2)
        canvas.create_text(x_base + 30, y_base + 45, text="Radio", fill="#172554", anchor="w", font=("Segoe UI", 10, "bold"))
        
    dibujar_radio(h, k, r, "#0000ff")
    dibujar_punto_destacado(h, k, "#ff0000")
    if mostrar_nombres:
        dibujar_leyenda()
