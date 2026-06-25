from src.conicas import analizar_conica
from gui.gui import iniciar_interfaz
from src.rut import FORMATO_RUT, obtener_digitos, validar_rut
from src.salida import mostrar_conica, mostrar_validacion


def main_consola():
    print(FORMATO_RUT)
    rut_usuario = input("Ingresa un RUT chileno: ")
    resultado_validacion = validar_rut(rut_usuario)
    mostrar_validacion(resultado_validacion)

    if not resultado_validacion["valido"]:
        return

    digitos = obtener_digitos(resultado_validacion["cuerpo"])
    resultado_conica = analizar_conica(digitos, resultado_validacion["dv_ingresado"])
    mostrar_conica(resultado_conica)


def main():
    iniciar_interfaz()


if __name__ == "__main__":
    main()
