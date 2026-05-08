def mostrar_validacion(resultado):
    if not resultado["valido"] and "error" in resultado:
        print("RUT invalido")
        print(resultado["error"])
        return

    print("Validacion del RUT")
    print(f"RUT limpio: {resultado['rut_limpio']}")
    print(f"Cuerpo: {resultado['cuerpo']}")
    print(f"Digito verificador ingresado: {resultado['dv_ingresado']}")
    print()
    print("Procedimiento modulo 11:")

    for paso in resultado["calculo"]["pasos"]:
        print(
            f"{paso['digito']} x {paso['multiplicador']} = {paso['producto']}"
        )

    print(f"Suma de productos: {resultado['calculo']['suma']}")
    print(f"Resto de la division por 11: {resultado['calculo']['resto']}")
    print(f"11 - resto = {resultado['calculo']['valor']}")
    print(f"Digito verificador esperado: {resultado['dv_esperado']}")

    if resultado["valido"]:
        print("Conclusion: el RUT es valido.")
    else:
        print("Conclusion: el RUT no es valido.")


def mostrar_conica(resultado):
    print()
    print("Construccion de la conica")

    for paso in resultado["coeficientes"]["pasos"]:
        print(paso)

    print()
    print(f"Ecuacion general: {resultado['ecuacion_general']}")
    print(f"Clasificacion: {resultado['tipo']}")
