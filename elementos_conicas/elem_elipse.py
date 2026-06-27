from src.elementos import calcular_elementos_geometricos
from gui.dibujo_utils import dibujar_punto_destacado, crear_caja_leyenda, dibujar_item_leyenda

def marcar_elementos_elipse(canvas, coeficientes, a_pixels, limites_visibles, mostrar_nombres=True):
    elementos = calcular_elementos_geometricos(coeficientes, "Elipse")
    if not elementos:
        return
        
    h, k = elementos["h"], elementos["k"]
    a, b = elementos["a"], elementos["b"]
    es_horizontal = elementos["es_horizontal"]
    
    # 1. Dibujar vértices principales (reales)
    v1, v2 = elementos["vertices"]
    dibujar_punto_destacado(canvas, a_pixels, v1[0], v1[1], "#ff0000")
    dibujar_punto_destacado(canvas, a_pixels, v2[0], v2[1], "#ff0000")
    
    # 2. Dibujar vértices secundarios en el eje menor
    if es_horizontal:
        dibujar_punto_destacado(canvas, a_pixels, h, k + b, "#d946ef")
        dibujar_punto_destacado(canvas, a_pixels, h, k - b, "#d946ef")
    else:
        dibujar_punto_destacado(canvas, a_pixels, h + b, k, "#d946ef")
        dibujar_punto_destacado(canvas, a_pixels, h - b, k, "#d946ef")

    # 3. Dibujar focos
    f1, f2 = elementos["focos"]
    dibujar_punto_destacado(canvas, a_pixels, f1[0], f1[1], "#00aa00")
    dibujar_punto_destacado(canvas, a_pixels, f2[0], f2[1], "#00aa00")

    # 4. Dibujar centro
    dibujar_punto_destacado(canvas, a_pixels, h, k, "#38bdf8")

    # 5. Dibujar leyenda
    if mostrar_nombres:
        x_base, y_base = crear_caja_leyenda(canvas, width=165, height=95)
        dibujar_item_leyenda(canvas, x_base, y_base, -3, "Centro", "#38bdf8")
        dibujar_item_leyenda(canvas, x_base, y_base, 19, "Vértices Reales", "#ff0000")
        dibujar_item_leyenda(canvas, x_base, y_base, 41, "Vértices Secundarios", "#d946ef")
        dibujar_item_leyenda(canvas, x_base, y_base, 63, "Focos", "#00aa00")
