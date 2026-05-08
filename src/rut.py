def limpiar_rut(rut):
    """Elimina puntos, guion y espacios; deja el DV en mayuscula."""
    rut_limpio = ""

    for caracter in rut.strip().upper():
        if caracter not in ".- ":
            rut_limpio += caracter

    return rut_limpio


def separar_rut(rut):
    rut_limpio = limpiar_rut(rut)

    if len(rut_limpio) < 2:
        return None, None, "El RUT debe incluir cuerpo y digito verificador."

    cuerpo = rut_limpio[:-1]
    dv = rut_limpio[-1]

    if not cuerpo.isdigit():
        return None, None, "El cuerpo del RUT debe contener solo numeros."

    if not (dv.isdigit() or dv == "K"):
        return None, None, "El digito verificador debe ser un numero o K."

    if len(cuerpo) != 8:
        return None, None, "Para este proyecto el cuerpo del RUT debe tener exactamente 8 digitos."

    return cuerpo, dv, None


def calcular_dv(cuerpo):
    multiplicador = 2
    suma = 0
    pasos = []

    for digito_texto in reversed(cuerpo):
        digito = int(digito_texto)
        producto = digito * multiplicador
        suma += producto

        pasos.append({
            "digito": digito,
            "multiplicador": multiplicador,
            "producto": producto,
        })

        multiplicador += 1
        if multiplicador > 7:
            multiplicador = 2

    resto = suma % 11
    valor = 11 - resto

    if valor == 11:
        dv_esperado = "0"
    elif valor == 10:
        dv_esperado = "K"
    else:
        dv_esperado = str(valor)

    return {
        "pasos": pasos,
        "suma": suma,
        "resto": resto,
        "valor": valor,
        "dv_esperado": dv_esperado,
    }


def validar_rut(rut):
    cuerpo, dv_ingresado, error = separar_rut(rut)

    if error:
        return {
            "valido": False,
            "error": error,
            "rut_limpio": limpiar_rut(rut),
        }

    calculo = calcular_dv(cuerpo)

    return {
        "valido": dv_ingresado == calculo["dv_esperado"],
        "rut_limpio": cuerpo + dv_ingresado,
        "cuerpo": cuerpo,
        "dv_ingresado": dv_ingresado,
        "dv_esperado": calculo["dv_esperado"],
        "calculo": calculo,
    }


def obtener_digitos(cuerpo):
    return [int(digito) for digito in cuerpo]
