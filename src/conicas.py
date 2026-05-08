def valor_v(dv):
    if dv == "K":
        return 10
    if dv == "0":
        return 11
    return int(dv)


def dividir(numerador, denominador):
    return numerador / denominador


def formatear_numero(numero):
    if numero == int(numero):
        return str(int(numero))
    return f"{numero:.4f}".rstrip("0").rstrip(".")


def construir_coeficientes(digitos, dv):
    d1, d2, d3, d4, d5, d6, d7, d8 = digitos
    v = valor_v(dv)
    pasos = []

    a_original = dividir(d1 + d2, v)
    b_original = dividir(d3 + d4, v)
    c = -(d5 + d6)
    d = -(d7 + d8)
    e = d1 + d3 + d5 + d7

    a = a_original
    b = b_original

    pasos.append(f"v = {v}, porque DV = {dv}")
    pasos.append(f"A = (d1 + d2) / v = ({d1} + {d2}) / {v} = {formatear_numero(a)}")
    pasos.append(f"B = (d3 + d4) / v = ({d3} + {d4}) / {v} = {formatear_numero(b)}")
    pasos.append(f"C = -(d5 + d6) = -({d5} + {d6}) = {c}")
    pasos.append(f"D = -(d7 + d8) = -({d7} + {d8}) = {d}")
    pasos.append(f"E = d1 + d3 + d5 + d7 = {d1} + {d3} + {d5} + {d7} = {e}")

    if d8 % 2 != 0:
        b = -b
        pasos.append(f"Como d8 = {d8} es impar, se reemplaza B por -B: B = {formatear_numero(b)}")

    if d1 == d2:
        b = a
        pasos.append(f"Como d1 = d2 = {d1}, se impone B = A: B = {formatear_numero(b)}")

    if (d5 + d6) % 3 == 0:
        if d7 % 2 == 0:
            b = 0
            pasos.append(
                f"Como d5 + d6 = {d5 + d6} es multiplo de 3 y d7 = {d7} es par, se define B = 0."
            )
        else:
            a = 0
            pasos.append(
                f"Como d5 + d6 = {d5 + d6} es multiplo de 3 y d7 = {d7} es impar, se define A = 0."
            )

    return {
        "A": a,
        "B": b,
        "C": c,
        "D": d,
        "E": e,
        "v": v,
        "pasos": pasos,
        "originales": {
            "A": a_original,
            "B": b_original,
        },
    }


def clasificar_conica(coeficientes):
    a = coeficientes["A"]
    b = coeficientes["B"]

    if a == 0 and b == 0:
        return "No corresponde a una conica del proyecto"

    if a == b and a != 0:
        return "Circunferencia"

    if (a == 0 and b != 0) or (a != 0 and b == 0):
        return "Parabola"

    if (a > 0 and b > 0) or (a < 0 and b < 0):
        return "Elipse"

    if (a > 0 and b < 0) or (a < 0 and b > 0):
        return "Hiperbola"

    return "No clasificada"


def ecuacion_general(coeficientes):
    terminos = [
        (coeficientes["A"], "x^2"),
        (coeficientes["B"], "y^2"),
        (coeficientes["C"], "x"),
        (coeficientes["D"], "y"),
        (coeficientes["E"], ""),
    ]

    partes = []

    for coeficiente, variable in terminos:
        if coeficiente == 0:
            continue

        signo = "-" if coeficiente < 0 else "+"
        valor = formatear_numero(abs(coeficiente))
        termino = f"{valor}{variable}"

        if not partes:
            partes.append(termino if signo == "+" else f"-{termino}")
        else:
            partes.append(f"{signo} {termino}")

    if not partes:
        return "0 = 0"

    return " ".join(partes) + " = 0"


def analizar_conica(digitos, dv):
    coeficientes = construir_coeficientes(digitos, dv)
    tipo = clasificar_conica(coeficientes)

    return {
        "coeficientes": coeficientes,
        "tipo": tipo,
        "ecuacion_general": ecuacion_general(coeficientes),
    }
