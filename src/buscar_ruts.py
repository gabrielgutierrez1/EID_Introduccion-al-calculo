import sys
import os

PROYECTO_RAIZ = os.path.dirname(os.path.dirname(__file__))
if PROYECTO_RAIZ not in sys.path:
    sys.path.insert(0, PROYECTO_RAIZ)

from src.rut import obtener_digitos, calcular_dv
from src.conicas import analizar_conica

def buscar_casos_prueba():
    casos_encontrados = {
        "Circunferencia": None,
        "Parábola": None,
        "Elipse": None,
        "Hipérbola": None
    }
    
    # Vamos a buscar RUTs probando cuerpos aleatorios o incrementales
    import random
    
    intentos = 0
    while None in casos_encontrados.values() and intentos < 20000:
        cuerpo = str(random.randint(10000000, 29999999))
        dv = calcular_dv(cuerpo)["dv_esperado"]
        
        # Omitimos 'K' para que sea más facil ingresarlo, o lo tomamos igual.
        # En este caso, busquemos los que tengan un dígito normal
        digitos = obtener_digitos(str(cuerpo))
        resultado_conica = analizar_conica(digitos, str(dv))
        
        tipo = resultado_conica["tipo"]
        
        if "Circunferencia" in tipo and casos_encontrados["Circunferencia"] is None:
            casos_encontrados["Circunferencia"] = f"{cuerpo}-{dv}"
        elif "Parabola" in tipo and casos_encontrados["Parábola"] is None:
            casos_encontrados["Parábola"] = f"{cuerpo}-{dv}"
        elif "Elipse" in tipo and casos_encontrados["Elipse"] is None:
            casos_encontrados["Elipse"] = f"{cuerpo}-{dv}"
        elif "Hiperbola" in tipo and casos_encontrados["Hipérbola"] is None:
            casos_encontrados["Hipérbola"] = f"{cuerpo}-{dv}"
            
        intentos += 1
        
        # Seguridad para evitar loops infinitos si hay un bug en el clasificador
        if intentos >= 20000:
            print("No se encontraron todos los casos en los primeros 20000 intentos.")
            break
            
    return casos_encontrados

if __name__ == "__main__":
    casos = buscar_casos_prueba()
    print("Casos de Prueba (RUTs válidos):")
    for tipo, rut in casos.items():
        print(f"{tipo}: {rut}")
