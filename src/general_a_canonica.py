def transformar_a_canonica(coeficientes, tipo=None, ecuacion_general_fn=None, formatear_numero_fn=None):
    if ecuacion_general_fn is None:
        raise ValueError("Se requiere ecuacion_general_fn para transformar a forma canonica.")

    if formatear_numero_fn is None:
        raise ValueError("Se requiere formatear_numero_fn para transformar a forma canonica.")

    A = coeficientes["A"]
    B = coeficientes["B"]
    C = coeficientes["C"]
    D = coeficientes["D"]
    E = coeficientes["E"]

    pasos = []
    pasos.append(f"Partimos de la ecuacion general: {ecuacion_general_fn(coeficientes)}")

    if (A == 0) and (B == 0):
        pasos.append("No hay terminos cuadraticos A = 0 y B = 0: no es una conica de segundo grado.")
        return {"pasos": pasos, "forma_canonica": None}

    hx = None
    ky = None
    if A != 0:
        rx = C / (2 * A)
        const_x = (C * C) / (4 * A)
        pasos.append(
            f"Completar el cuadrado en x: A(x^2 + (C/A) x) => A[(x + {formatear_numero_fn(rx)})^2 - ({formatear_numero_fn(rx)})^2] = A(x + {formatear_numero_fn(rx)})^2 - {formatear_numero_fn(const_x)}"
        )
        hx = -C / (2 * A)

    if B != 0:
        ry = D / (2 * B)
        const_y = (D * D) / (4 * B)
        pasos.append(
            f"Completar el cuadrado en y: B(y^2 + (D/B) y) => B[(y + {formatear_numero_fn(ry)})^2 - ({formatear_numero_fn(ry)})^2] = B(y + {formatear_numero_fn(ry)})^2 - {formatear_numero_fn(const_y)}"
        )
        ky = -D / (2 * B)

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
                f"Traslacion: x0 = {formatear_numero_fn(hx)}, y0 = {formatear_numero_fn(ky)}"
            )
            pasos.append(
                f"La ecuacion se convierte en: {formatear_numero_fn(A)}(x + {formatear_numero_fn(C/(2*A))})^2 + {formatear_numero_fn(B)}(y + {formatear_numero_fn(D/(2*B))})^2 = {formatear_numero_fn(rhs)}"
            )

            if A * B > 0:
                denom_x = rhs / A if A != 0 else None
                denom_y = rhs / B if B != 0 else None
                pasos.append(
                    f"Dividimos entre {formatear_numero_fn(rhs)} para obtener 1 en el lado derecho y obtenemos la forma con denominadores:"
                )
                if rhs == 0:
                    pasos.append("El lado derecho queda 0, por lo que no se puede dividir para obtener una forma canonica estandar igual a 1.")
                    forma = None
                elif denom_x is None or denom_y is None:
                    forma = None
                else:
                    forma = (
                        f"(x + {formatear_numero_fn(C/(2*A))})^2 / {formatear_numero_fn(denom_x)} + "
                        f"(y + {formatear_numero_fn(D/(2*B))})^2 / {formatear_numero_fn(denom_y)} = 1"
                    )
                    pasos.append(f"Forma canonica: {forma}")

            else:
                pasos.append("Como A y B tienen signos opuestos se obtiene una hipérbola.")
                if rhs == 0:
                    pasos.append("El lado derecho queda 0, por lo que no se puede dividir para obtener una forma canonica estandar igual a 1.")
                    forma = None
                elif A / rhs > 0:
                    a2 = rhs / A
                    b2 = -rhs / B
                    forma = (
                        f"(x + {formatear_numero_fn(C/(2*A))})^2 / {formatear_numero_fn(a2)} - "
                        f"(y + {formatear_numero_fn(D/(2*B))})^2 / {formatear_numero_fn(b2)} = 1"
                    )
                else:
                    a2 = rhs / B
                    b2 = -rhs / A
                    forma = (
                        f"(y + {formatear_numero_fn(D/(2*B))})^2 / {formatear_numero_fn(a2)} - "
                        f"(x + {formatear_numero_fn(C/(2*A))})^2 / {formatear_numero_fn(b2)} = 1"
                    )
                if forma:
                    pasos.append(f"Forma canonica: {forma}")

        else:
            pasos.append("Al menos uno de los coeficientes cuadraticos es cero: cónica tipo parábola potencial.")
            if A == 0 and B != 0:
                if C == 0:
                    pasos.append("No hay termino lineal en x (C = 0): la ecuacion no permite aislar x -> degenerada o no estandar.")
                    forma = None
                else:
                    k = D / (2 * B)
                    beta = (D * D) / (4 * B) - E
                    h = beta / C
                    pasos.append(
                        f"Completar el cuadrado en y da B(y + {formatear_numero_fn(D/(2*B))})^2 - {formatear_numero_fn((D*D)/(4*B))}; reordenando se obtiene:"
                    )
                    pasos.append(
                        f"x = {formatear_numero_fn(-B/C)}(y + {formatear_numero_fn(k)})^2 + {formatear_numero_fn(h)}"
                    )
                    pasos.append(
                        f"Reescribiendo como forma canónica: (y + {formatear_numero_fn(k)})^2 = {formatear_numero_fn(-C/B)} (x - {formatear_numero_fn(h)})"
                    )
                    forma = (
                        f"(y + {formatear_numero_fn(k)})^2 = {formatear_numero_fn(-C/B)} (x - {formatear_numero_fn(h)})"
                    )

            elif B == 0 and A != 0:
                if D == 0:
                    pasos.append("No hay termino lineal en y (D = 0): la ecuacion no permite aislar y -> degenerada o no estandar.")
                    forma = None
                else:
                    h = C / (2 * A)
                    beta = (C * C) / (4 * A) - E
                    k = beta / D
                    pasos.append(
                        f"Completar el cuadrado en x da A(x + {formatear_numero_fn(C/(2*A))})^2 - {formatear_numero_fn((C*C)/(4*A))}; reordenando se obtiene:"
                    )
                    pasos.append(
                        f"y = {formatear_numero_fn(-A/D)}(x + {formatear_numero_fn(h)})^2 + {formatear_numero_fn(k)}"
                    )
                    pasos.append(
                        f"Reescribiendo como forma canónica: (x + {formatear_numero_fn(h)})^2 = {formatear_numero_fn(-D/A)} (y - {formatear_numero_fn(k)})"
                    )
                    forma = (
                        f"(x + {formatear_numero_fn(h)})^2 = {formatear_numero_fn(-D/A)} (y - {formatear_numero_fn(k)})"
                    )

    except Exception:
        pasos.append("No fue posible completar la transformacion debido a un error numerico (division por cero u otra condicion).")
        forma = None

    return {"pasos": pasos, "forma_canonica": forma}