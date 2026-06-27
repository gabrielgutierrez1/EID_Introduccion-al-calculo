def formatear_numero(numero, precision=4):
    if numero is None:
        return "no definida"

    if isinstance(numero, str):
        return numero

    if abs(numero) < 1e-9:
        numero = 0

    if abs(numero - round(numero)) < 1e-9:
        return str(int(round(numero)))

    formato = f"{{:.{precision}f}}"
    return formato.format(numero).rstrip("0").rstrip(".")


def son_iguales(valor_1, valor_2):
    if isinstance(valor_1, str) or isinstance(valor_2, str):
        return valor_1 == valor_2

    return abs(valor_1 - valor_2) < 1e-9
