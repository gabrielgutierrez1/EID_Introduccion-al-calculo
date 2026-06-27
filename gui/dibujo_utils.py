def dibujar_punto_destacado(canvas, a_pixels, x, y, color, radio=5):
    px, py = a_pixels(x, y)
    canvas.create_oval(px - radio, py - radio, px + radio, py + radio, fill=color, outline="black")


def dibujar_linea(canvas, a_pixels, color, vertical=False, horizontal=False, val=0, dash=(4, 4)):
    if vertical:
        px_val, _ = a_pixels(val, 0)
        canvas.create_line(px_val, 0, px_val, canvas.winfo_height(), fill=color, dash=dash, width=2)
    elif horizontal:
        _, py_val = a_pixels(0, val)
        canvas.create_line(0, py_val, canvas.winfo_width(), py_val, fill=color, dash=dash, width=2)


def crear_caja_leyenda(canvas, width=165, height=130):
    x_base = 20
    y_base = 20
    canvas.create_rectangle(
        x_base, y_base, x_base + width, y_base + height, fill="white", outline="#ccc", width=1
    )
    return x_base, y_base


def dibujar_item_leyenda(canvas, x_base, y_base, offset_y, text, color, shape="oval", dash=(4, 4)):
    if shape == "oval":
        canvas.create_oval(
            x_base + 10, y_base + offset_y, x_base + 20, y_base + offset_y + 10, fill=color, outline="black"
        )
    elif shape == "line":
        canvas.create_line(
            x_base + 10, y_base + offset_y + 5, x_base + 20, y_base + offset_y + 5, fill=color, dash=dash, width=2
        )
    elif shape == "solid_line":
        canvas.create_line(
            x_base + 10, y_base + offset_y + 5, x_base + 20, y_base + offset_y + 5, fill=color, width=2
        )

    canvas.create_text(
        x_base + 30, y_base + offset_y + 5, text=text, fill="#172554", anchor="w", font=("Segoe UI", 9, "bold")
    )
