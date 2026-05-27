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


def multiplicar_coeficientes(coeficientes, factor):
    return {
        "A": coeficientes["A"] * factor,
        "B": coeficientes["B"] * factor,
        "C": coeficientes["C"] * factor,
        "D": coeficientes["D"] * factor,
        "E": coeficientes["E"] * factor,
    }


def factor_para_general_original(coeficientes_originales, coeficientes_expandidos):
    for clave in ["A", "B", "C", "D", "E"]:
        if coeficientes_expandidos[clave] != 0:
            return coeficientes_originales[clave] / coeficientes_expandidos[clave]

    return 1


def transformar_a_canonica(coeficientes, tipo=None):
    A = coeficientes["A"]
    B = coeficientes["B"]
    C = coeficientes["C"]
    D = coeficientes["D"]
    E = coeficientes["E"]

    pasos = []
    pasos.append(f"Partimos de la ecuacion general: {ecuacion_general(coeficientes)}")

    # Caso degenerate: sin terminos cuadraticos
    if (A == 0) and (B == 0):
        pasos.append("No hay terminos cuadraticos A = 0 y B = 0: no es una conica de segundo grado.")
        return {"pasos": pasos, "forma_canonica": None}

    # Completar cuadrados cuando A y B no son cero
    hx = None
    ky = None
    if A != 0:
        rx = C / (2 * A)
        const_x = (C * C) / (4 * A)
        pasos.append(
            f"Completar el cuadrado en x: A(x^2 + (C/A) x) => A[(x + {formatear_numero(rx)})^2 - ({formatear_numero(rx)})^2] = A(x + {formatear_numero(rx)})^2 - {formatear_numero(const_x)}"
        )
        hx = -C / (2 * A)

    if B != 0:
        ry = D / (2 * B)
        const_y = (D * D) / (4 * B)
        pasos.append(
            f"Completar el cuadrado en y: B(y^2 + (D/B) y) => B[(y + {formatear_numero(ry)})^2 - ({formatear_numero(ry)})^2] = B(y + {formatear_numero(ry)})^2 - {formatear_numero(const_y)}"
        )
        ky = -D / (2 * B)

    # Si ambos cuadrados fueron completados, construir RHS
    forma = None
    try:
        rhs = 0.0
        if A != 0:
            rhs += (C * C) / (4 * A)
        if B != 0:
            rhs += (D * D) / (4 * B)
        rhs -= E

        if (A != 0) and (B != 0):
            pasos.append(
                f"Traslacion: x0 = {formatear_numero(hx)}, y0 = {formatear_numero(ky)}"
            )
            pasos.append(
                f"La ecuacion se convierte en: {formatear_numero(A)}(x + {formatear_numero(C/(2*A))})^2 + {formatear_numero(B)}(y + {formatear_numero(D/(2*B))})^2 = {formatear_numero(rhs)}"
            )

            # Clasificar y escribir forma canonica segun signos
            if A * B > 0:
                # Elipse o circunferencia (mismo signo)
                denom_x = rhs / A if A != 0 else None
                denom_y = rhs / B if B != 0 else None
                pasos.append(
                    f"Dividimos entre {formatear_numero(rhs)} para obtener 1 en el lado derecho y obtenemos la forma con denominadores:"
                )
                if rhs == 0:
                    pasos.append("El lado derecho queda 0, por lo que no se puede dividir para obtener una forma canonica estandar igual a 1.")
                    forma = None
                elif denom_x is None or denom_y is None:
                    forma = None
                else:
                    forma = (
                        f"(x + {formatear_numero(C/(2*A))})^2 / {formatear_numero(denom_x)} + "
                        f"(y + {formatear_numero(D/(2*B))})^2 / {formatear_numero(denom_y)} = 1"
                    )
                    pasos.append(f"Forma canonica: {forma}")

            else:
                # Hiperbola (signos opuestos)
                pasos.append("Como A y B tienen signos opuestos se obtiene una hipérbola.")
                # Determinar termino positivo primero
                if rhs == 0:
                    pasos.append("El lado derecho queda 0, por lo que no se puede dividir para obtener una forma canonica estandar igual a 1.")
                    forma = None
                elif A / rhs > 0:
                    a2 = rhs / A
                    b2 = -rhs / B
                    forma = (
                        f"(x + {formatear_numero(C/(2*A))})^2 / {formatear_numero(a2)} - "
                        f"(y + {formatear_numero(D/(2*B))})^2 / {formatear_numero(b2)} = 1"
                    )
                else:
                    a2 = rhs / B
                    b2 = -rhs / A
                    forma = (
                        f"(y + {formatear_numero(D/(2*B))})^2 / {formatear_numero(a2)} - "
                        f"(x + {formatear_numero(C/(2*A))})^2 / {formatear_numero(b2)} = 1"
                    )
                if forma:
                    pasos.append(f"Forma canonica: {forma}")

        else:
            # Caso parabola: uno de A o B es cero
            pasos.append("Al menos uno de los coeficientes cuadraticos es cero: cónica tipo parábola potencial.")
            if A == 0 and B != 0:
                # Resolver para x en funcion de y
                if C == 0:
                    pasos.append("No hay termino lineal en x (C = 0): la ecuacion no permite aislar x -> degenerada o no estandar.")
                    forma = None
                else:
                    k = D / (2 * B)
                    beta = (D * D) / (4 * B) - E
                    h = beta / C
                    pasos.append(
                        f"Completar el cuadrado en y da B(y + {formatear_numero(D/(2*B))})^2 - {formatear_numero((D*D)/(4*B))}; reordenando se obtiene:"
                    )
                    pasos.append(
                        f"x = {formatear_numero(-B/C)}(y + {formatear_numero(k)})^2 + {formatear_numero(h)}"
                    )
                    pasos.append(
                        f"Reescribiendo como forma canónica: (y + {formatear_numero(k)})^2 = {formatear_numero(-C/B)} (x - {formatear_numero(h)})"
                    )
                    forma = (
                        f"(y + {formatear_numero(k)})^2 = {formatear_numero(-C/B)} (x - {formatear_numero(h)})"
                    )

            elif B == 0 and A != 0:
                # Resolver para y en funcion de x
                if D == 0:
                    pasos.append("No hay termino lineal en y (D = 0): la ecuacion no permite aislar y -> degenerada o no estandar.")
                    forma = None
                else:
                    h = C / (2 * A)
                    beta = (C * C) / (4 * A) - E
                    k = beta / D
                    pasos.append(
                        f"Completar el cuadrado en x da A(x + {formatear_numero(C/(2*A))})^2 - {formatear_numero((C*C)/(4*A))}; reordenando se obtiene:"
                    )
                    pasos.append(
                        f"y = {formatear_numero(-A/D)}(x + {formatear_numero(h)})^2 + {formatear_numero(k)}"
                    )
                    pasos.append(
                        f"Reescribiendo como forma canónica: (x + {formatear_numero(h)})^2 = {formatear_numero(-D/A)} (y - {formatear_numero(k)})"
                    )
                    forma = (
                        f"(x + {formatear_numero(h)})^2 = {formatear_numero(-D/A)} (y - {formatear_numero(k)})"
                    )

    except Exception:
        pasos.append("No fue posible completar la transformacion debido a un error numerico (division por cero u otra condicion).")
        forma = None

    return {"pasos": pasos, "forma_canonica": forma}


def transformar_canonica_a_general(coeficientes, transformacion):
    A = coeficientes["A"]
    B = coeficientes["B"]
    C = coeficientes["C"]
    D = coeficientes["D"]
    E = coeficientes["E"]

    pasos = []
    forma_canonica = transformacion.get("forma_canonica")

    if not forma_canonica:
        pasos.append("No hay forma canonica disponible para aplicar el procedimiento inverso.")
        return {"pasos": pasos, "ecuacion_general": None}

    pasos.append(f"Partimos desde la forma canonica: {forma_canonica}")

    if A == 0 and B == 0:
        pasos.append("No es posible volver desde una forma canonica porque no hay terminos cuadraticos.")
        return {"pasos": pasos, "ecuacion_general": None}

    if A != 0 and B != 0:
        p = C / (2 * A)
        q = D / (2 * B)
        rhs = (C * C) / (4 * A) + (D * D) / (4 * B) - E

        if A * B > 0:
            a2 = rhs / A
            b2 = rhs / B
            coef_x2 = 1 / a2
            coef_y2 = 1 / b2
            coef_x = 2 * p / a2
            coef_y = 2 * q / b2
            constante = (p * p / a2) + (q * q / b2) - 1

            pasos.append(
                f"Leemos desde la canonica: (x + {formatear_numero(p)})^2 / {formatear_numero(a2)} + (y + {formatear_numero(q)})^2 / {formatear_numero(b2)} = 1"
            )
            pasos.append(
                f"Expandimos cuadrados: (x^2 + {formatear_numero(2 * p)}x + {formatear_numero(p * p)}) / {formatear_numero(a2)} + (y^2 + {formatear_numero(2 * q)}y + {formatear_numero(q * q)}) / {formatear_numero(b2)} = 1"
            )
            pasos.append(
                f"Distribuimos denominadores: {formatear_numero(coef_x2)}x^2 + {formatear_numero(coef_x)}x + {formatear_numero(p * p / a2)} + {formatear_numero(coef_y2)}y^2 + {formatear_numero(coef_y)}y + {formatear_numero(q * q / b2)} = 1"
            )
        else:
            if A > 0:
                a2 = rhs / A
                b2 = -rhs / B
                coef_x2 = 1 / a2
                coef_y2 = -1 / b2
                coef_x = 2 * p / a2
                coef_y = -2 * q / b2
                constante = (p * p / a2) - (q * q / b2) - 1
                pasos.append(
                    f"Leemos desde la canonica: (x + {formatear_numero(p)})^2 / {formatear_numero(a2)} - (y + {formatear_numero(q)})^2 / {formatear_numero(b2)} = 1"
                )
            else:
                a2 = rhs / B
                b2 = -rhs / A
                coef_x2 = -1 / b2
                coef_y2 = 1 / a2
                coef_x = -2 * p / b2
                coef_y = 2 * q / a2
                constante = (q * q / a2) - (p * p / b2) - 1
                pasos.append(
                    f"Leemos desde la canonica: (y + {formatear_numero(q)})^2 / {formatear_numero(a2)} - (x + {formatear_numero(p)})^2 / {formatear_numero(b2)} = 1"
                )

            pasos.append("Expandimos los cuadrados y distribuimos los denominadores.")

        coeficientes_expandidos = {
            "A": coef_x2,
            "B": coef_y2,
            "C": coef_x,
            "D": coef_y,
            "E": constante,
        }
        general = ecuacion_general(coeficientes_expandidos)
        pasos.append(
            f"Pasamos el 1 al lado izquierdo y ordenamos: {general}"
        )
        factor = factor_para_general_original(coeficientes, coeficientes_expandidos)
        coeficientes_finales = multiplicar_coeficientes(coeficientes_expandidos, factor)
        pasos.append(
            f"Multiplicamos toda la ecuacion por {formatear_numero(factor)} para dejarla con los coeficientes del ejercicio."
        )
        pasos.append(f"Ecuacion general final: {ecuacion_general(coeficientes_finales)}")
        return {"pasos": pasos, "ecuacion_general": ecuacion_general(coeficientes_finales)}

    elif A == 0 and B != 0:
        k = D / (2 * B)
        beta = (D * D) / (4 * B) - E
        h = beta / C
        m = -C / B
        constante = k * k + m * h

        pasos.append(
            f"Usamos la forma parabolica: (y + {formatear_numero(k)})^2 = {formatear_numero(m)}(x - {formatear_numero(h)})"
        )
        pasos.append(
            f"Expandimos: y^2 + {formatear_numero(2 * k)}y + {formatear_numero(k * k)} = {formatear_numero(m)}x - {formatear_numero(m * h)}"
        )
        coeficientes_expandidos = {
            "A": 0,
            "B": 1,
            "C": -m,
            "D": 2 * k,
            "E": constante,
        }
        general = ecuacion_general(coeficientes_expandidos)
        pasos.append(
            f"Pasamos todo al lado izquierdo y ordenamos: {general}"
        )
        factor = factor_para_general_original(coeficientes, coeficientes_expandidos)
        coeficientes_finales = multiplicar_coeficientes(coeficientes_expandidos, factor)
        pasos.append(
            f"Multiplicamos toda la ecuacion por {formatear_numero(factor)} para dejarla con los coeficientes del ejercicio."
        )
        pasos.append(f"Ecuacion general final: {ecuacion_general(coeficientes_finales)}")
        return {"pasos": pasos, "ecuacion_general": ecuacion_general(coeficientes_finales)}

    elif B == 0 and A != 0:
        h = C / (2 * A)
        beta = (C * C) / (4 * A) - E
        k = beta / D
        m = -D / A
        constante = h * h + m * k

        pasos.append(
            f"Usamos la forma parabolica: (x + {formatear_numero(h)})^2 = {formatear_numero(m)}(y - {formatear_numero(k)})"
        )
        pasos.append(
            f"Expandimos: x^2 + {formatear_numero(2 * h)}x + {formatear_numero(h * h)} = {formatear_numero(m)}y - {formatear_numero(m * k)}"
        )
        coeficientes_expandidos = {
            "A": 1,
            "B": 0,
            "C": 2 * h,
            "D": -m,
            "E": constante,
        }
        general = ecuacion_general(coeficientes_expandidos)
        pasos.append(
            f"Pasamos todo al lado izquierdo y ordenamos: {general}"
        )
        factor = factor_para_general_original(coeficientes, coeficientes_expandidos)
        coeficientes_finales = multiplicar_coeficientes(coeficientes_expandidos, factor)
        pasos.append(
            f"Multiplicamos toda la ecuacion por {formatear_numero(factor)} para dejarla con los coeficientes del ejercicio."
        )
        pasos.append(f"Ecuacion general final: {ecuacion_general(coeficientes_finales)}")
        return {"pasos": pasos, "ecuacion_general": ecuacion_general(coeficientes_finales)}

    return {"pasos": pasos, "ecuacion_general": None}


def analizar_conica(digitos, dv):
    coeficientes = construir_coeficientes(digitos, dv)
    tipo = clasificar_conica(coeficientes)

    # Transformacion a forma canonica (paso a paso)
    transformacion = transformar_a_canonica(coeficientes, tipo)
    inversa = transformar_canonica_a_general(coeficientes, transformacion)

    return {
        "coeficientes": coeficientes,
        "tipo": tipo,
        "ecuacion_general": ecuacion_general(coeficientes),
        "forma_canonica": transformacion,
        "canonica_a_general": inversa,
    }
