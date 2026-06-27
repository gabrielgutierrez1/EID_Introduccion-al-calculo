from src.elementos import calcular_elementos_geometricos
from gui.dibujo_utils import dibujar_punto_destacado, crear_caja_leyenda, dibujar_item_leyenda, dibujar_linea

def marcar_elementos_parabola(canvas, coeficientes, a_pixels, limites_visibles, mostrar_nombres=True):
    elementos = calcular_elementos_geometricos(coeficientes, "Parabola")
    if not elementos:
        return
        
    h, k = elementos["h"], elementos["k"]
    es_vertical = elementos["es_vertical"]
    
    # Vértice
    dibujar_punto_destacado(canvas, a_pixels, h, k, "#ff0000")

    # Foco
    foco = elementos["focos"][0]
    dibujar_punto_destacado(canvas, a_pixels, foco[0], foco[1], "#00aa00")

    # Directriz y Eje
    directriz = elementos["directriz"]
    eje = elementos["eje"]
    if es_vertical:
        dibujar_linea(canvas, a_pixels, "#64748b", horizontal=True, val=directriz, dash=(4, 4))
        dibujar_linea(canvas, a_pixels, "#f59e0b", vertical=True, val=eje, dash=(2, 3))
    else:
        dibujar_linea(canvas, a_pixels, "#64748b", vertical=True, val=directriz, dash=(4, 4))
        dibujar_linea(canvas, a_pixels, "#f59e0b", horizontal=True, val=eje, dash=(2, 3))

    if mostrar_nombres:
        x_base, y_base = crear_caja_leyenda(canvas, width=165, height=95)
        dibujar_item_leyenda(canvas, x_base, y_base, -3, "Vértice", "#ff0000")
        dibujar_item_leyenda(canvas, x_base, y_base, 19, "Foco", "#00aa00")
        dibujar_item_leyenda(canvas, x_base, y_base, 41, "Directriz", "#64748b", shape="line")
        dibujar_item_leyenda(canvas, x_base, y_base, 63, "Eje Simetría", "#f59e0b", shape="line", dash=(2, 3))
