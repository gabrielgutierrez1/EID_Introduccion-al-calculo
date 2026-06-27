from src.elementos import calcular_elementos_geometricos
from gui.dibujo_utils import dibujar_punto_destacado, crear_caja_leyenda, dibujar_item_leyenda

def marcar_elementos_circunferencia(canvas, coeficientes, a_pixels, limites_visibles, mostrar_nombres=True):
    elementos = calcular_elementos_geometricos(coeficientes, "Circunferencia")
    if not elementos:
        return
        
    h, k = elementos["h"], elementos["k"]
    r = elementos["radio"]
    
    def dibujar_radio(h, k, r, color):
        px1, py1 = a_pixels(h, k)
        px2, py2 = a_pixels(h + r, k)
        canvas.create_line(px1, py1, px2, py2, fill=color, width=2)
        
    dibujar_radio(h, k, r, "#0000ff")
    dibujar_punto_destacado(canvas, a_pixels, h, k, "#ff0000")
    
    if mostrar_nombres:
        x_base, y_base = crear_caja_leyenda(canvas, width=100, height=55)
        dibujar_item_leyenda(canvas, x_base, y_base, 2, "Centro", "#ff0000")
        dibujar_item_leyenda(canvas, x_base, y_base, 27, "Radio", "#0000ff", shape="solid_line")
