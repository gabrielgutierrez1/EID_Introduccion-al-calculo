from .conicas import ecuacion_general, formatear_numero


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
