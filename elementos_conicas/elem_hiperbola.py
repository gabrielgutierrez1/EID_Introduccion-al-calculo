from src.elementos import calcular_elementos_geometricos
from gui.dibujo_utils import dibujar_punto_destacado, crear_caja_leyenda, dibujar_item_leyenda

def marcar_elementos_hiperbola(canvas, coeficientes, a_pixels, limites_visibles, mostrar_nombres=True):
    elementos = calcular_elementos_geometricos(coeficientes, "Hiperbola")
    if not elementos:
        return
        
    h, k = elementos["h"], elementos["k"]
    a, b = elementos["a"], elementos["b"]
    es_horizontal = elementos["es_horizontal"]
    x_min, x_max, y_min, y_max = limites_visibles
    
    def dibujar_asintotas():
        m = (b / a) if es_horizontal else (a / b)
        y1_min, y1_max = k + m * (x_min - h), k + m * (x_max - h)
        px1_min, py1_min = a_pixels(x_min, y1_min)
        px1_max, py1_max = a_pixels(x_max, y1_max)
        canvas.create_line(px1_min, py1_min, px1_max, py1_max, fill="#64748b", dash=(4, 4), width=1.5)

        y2_min, y2_max = k - m * (x_min - h), k - m * (x_max - h)
        px2_min, py2_min = a_pixels(x_min, y2_min)
        px2_max, py2_max = a_pixels(x_max, y2_max)
        canvas.create_line(px2_min, py2_min, px2_max, py2_max, fill="#64748b", dash=(4, 4), width=1.5)

    dibujar_asintotas()

    # 2. Dibujar vértices
    v1, v2 = elementos["vertices"]
    dibujar_punto_destacado(canvas, a_pixels, v1[0], v1[1], "#ff0000")
    dibujar_punto_destacado(canvas, a_pixels, v2[0], v2[1], "#ff0000")

    # 3. Dibujar extremos del eje conjugado
    if es_horizontal:
        dibujar_punto_destacado(canvas, a_pixels, h, k + b, "#d946ef")
        dibujar_punto_destacado(canvas, a_pixels, h, k - b, "#d946ef")
    else:
        dibujar_punto_destacado(canvas, a_pixels, h + b, k, "#d946ef")
        dibujar_punto_destacado(canvas, a_pixels, h - b, k, "#d946ef")

    # 4. Dibujar focos
    f1, f2 = elementos["focos"]
    dibujar_punto_destacado(canvas, a_pixels, f1[0], f1[1], "#00aa00")
    dibujar_punto_destacado(canvas, a_pixels, f2[0], f2[1], "#00aa00")

    # 5. Dibujar centro
    dibujar_punto_destacado(canvas, a_pixels, h, k, "#38bdf8")

    # 6. Dibujar leyenda
    if mostrar_nombres:
        x_base, y_base = crear_caja_leyenda(canvas, width=165, height=115)
        dibujar_item_leyenda(canvas, x_base, y_base, -3, "Centro", "#38bdf8")
        dibujar_item_leyenda(canvas, x_base, y_base, 19, "Vértices", "#ff0000")
        dibujar_item_leyenda(canvas, x_base, y_base, 41, "Eje conjugado", "#d946ef")
        dibujar_item_leyenda(canvas, x_base, y_base, 63, "Focos", "#00aa00")
        dibujar_item_leyenda(canvas, x_base, y_base, 85, "Asíntotas", "#64748b", shape="line")
