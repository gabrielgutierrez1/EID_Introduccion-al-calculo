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
    pasos.append(f"• Ecuación general original:")
    pasos.append(f"  {ecuacion_general_fn(coeficientes)}")

    if (A == 0) and (B == 0):
        pasos.append("• No hay términos cuadráticos, no es una cónica.")
        return {"pasos": pasos, "forma_canonica": None}

    hx = None
    ky = None
    if A != 0:
        rx = C / (2 * A)
        const_x = (C * C) / (4 * A)
        pasos.append(f"• Completando cuadrado en x:")
        pasos.append(f"  {formatear_numero_fn(A)}(x + {formatear_numero_fn(rx)})² - {formatear_numero_fn(const_x)}")
        hx = -C / (2 * A)

    if B != 0:
        ry = D / (2 * B)
        const_y = (D * D) / (4 * B)
        pasos.append(f"• Completando cuadrado en y:")
        pasos.append(f"  {formatear_numero_fn(B)}(y + {formatear_numero_fn(ry)})² - {formatear_numero_fn(const_y)}")
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
            pasos.append(f"• Agrupando términos independientes a la derecha (rhs):")
            pasos.append(f"  rhs = {formatear_numero_fn(rhs)}")
            pasos.append(f"• Ecuación agrupada:")
            pasos.append(f"  {formatear_numero_fn(A)}(x + {formatear_numero_fn(C/(2*A))})² + {formatear_numero_fn(B)}(y + {formatear_numero_fn(D/(2*B))})² = {formatear_numero_fn(rhs)}")

            if A * B > 0:
                denom_x = rhs / A if A != 0 else None
                denom_y = rhs / B if B != 0 else None
                pasos.append(f"• Dividimos por rhs ({formatear_numero_fn(rhs)}) para igualar a 1:")
                if rhs == 0:
                    pasos.append("  (Lado derecho es 0, no se puede dividir)")
                    forma = None
                elif denom_x is None or denom_y is None:
                    forma = None
                else:
                    forma = (
                        f"(x + {formatear_numero_fn(C/(2*A))})² / {formatear_numero_fn(denom_x)} + "
                        f"(y + {formatear_numero_fn(D/(2*B))})² / {formatear_numero_fn(denom_y)} = 1"
                    )
                    pasos.append(f"• Forma canónica final:")
                    pasos.append(f"  {forma}")

            else:
                pasos.append("• Signos opuestos en cuadráticos (Hipérbola)")
                if rhs == 0:
                    pasos.append("  (Lado derecho es 0, degenerada)")
                    forma = None
                elif A / rhs > 0:
                    a2 = rhs / A
                    b2 = -rhs / B
                    forma = (
                        f"(x + {formatear_numero_fn(C/(2*A))})² / {formatear_numero_fn(a2)} - "
                        f"(y + {formatear_numero_fn(D/(2*B))})² / {formatear_numero_fn(b2)} = 1"
                    )
                else:
                    a2 = rhs / B
                    b2 = -rhs / A
                    forma = (
                        f"(y + {formatear_numero_fn(D/(2*B))})² / {formatear_numero_fn(a2)} - "
                        f"(x + {formatear_numero_fn(C/(2*A))})² / {formatear_numero_fn(b2)} = 1"
                    )
                if forma:
                    pasos.append(f"• Forma canónica final:")
                    pasos.append(f"  {forma}")

        else:
            if A == 0 and B != 0:
                if C == 0:
                    pasos.append("• No hay x (Degenerada)")
                    forma = None
                else:
                    k = D / (2 * B)
                    beta = (D * D) / (4 * B) - E
                    h = beta / C
                    pasos.append(f"• Reordenando aislando x:")
                    pasos.append(f"  x = {formatear_numero_fn(-B/C)}(y + {formatear_numero_fn(k)})² + {formatear_numero_fn(h)}")
                    forma = f"(y + {formatear_numero_fn(k)})² = {formatear_numero_fn(-C/B)} (x - {formatear_numero_fn(h)})"
                    pasos.append(f"• Forma canónica final:")
                    pasos.append(f"  {forma}")

            elif B == 0 and A != 0:
                if D == 0:
                    pasos.append("• No hay y (Degenerada)")
                    forma = None
                else:
                    h = C / (2 * A)
                    beta = (C * C) / (4 * A) - E
                    k = beta / D
                    pasos.append(f"• Reordenando aislando y:")
                    pasos.append(f"  y = {formatear_numero_fn(-A/D)}(x + {formatear_numero_fn(h)})² + {formatear_numero_fn(k)}")
                    forma = f"(x + {formatear_numero_fn(h)})² = {formatear_numero_fn(-D/A)} (y - {formatear_numero_fn(k)})"
                    pasos.append(f"• Forma canónica final:")
                    pasos.append(f"  {forma}")

    except Exception:
        pasos.append("• Error numérico al calcular (división por cero).")
        forma = None

    return {"pasos": pasos, "forma_canonica": forma}