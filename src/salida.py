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
    # Mostrar transformacion a forma canonica si existe
    if "forma_canonica" in resultado and resultado["forma_canonica"]:
        transform = resultado["forma_canonica"]
        if transform.get("pasos"):
            print()
            print("Transformacion a forma canonica:")
            for paso in transform["pasos"]:
                print(paso)

        forma = transform.get("forma_canonica")
        if forma:
            print()
            print(f"Forma canonica: {forma}")

    if "canonica_a_general" in resultado and resultado["canonica_a_general"]:
        inversa = resultado["canonica_a_general"]
        if inversa.get("pasos"):
            print()
            print("Transformacion inversa: forma canonica a general:")
            for paso in inversa["pasos"]:
                print(paso)
