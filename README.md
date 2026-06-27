# Proyecto EID - Introduccion al Calculo

Aplicacion en Python para la Evaluacion Integrada de Desempeno N°1 del curso MAT1186.

El proyecto valida un RUT chileno, extrae sus digitos y construye una ecuacion general de segundo grado para clasificar una seccion conica. Tambien muestra el procedimiento de transformacion desde la forma general a la forma canonica, el proceso inverso desde la forma canonica a la forma general y una interfaz grafica para visualizar los resultados.

## Requisitos actuales

- Python 3.
- No usar librerias matematicas externas como `numpy`, `math`, `sympy`, `scipy` o `pandas`.
- Todos los calculos matematicos deben implementarse manualmente.
- Para ejecutar la prueba grafica se usa `tkinter`, que viene incluido normalmente con Python.

## Como ejecutar

Desde la carpeta raiz del proyecto, ejecutar la version principal con interfaz grafica:

```powershell
python3 main.py
```

Luego ingresar un RUT chileno con cuerpo de 8 digitos. Formatos aceptados:

```text
21.929.009-8
21929009-8
219290098
```

## Estructura del proyecto

```text
EID_Introduccion-al-calculo/
├─ main.py
├─ gui/
│  ├─ __init__.py
│  ├─ dibujo_utils.py
│  ├─ formatters.py
│  ├─ graficos.py
│  └─ gui.py
├─ src/
│  ├─ __init__.py
│  ├─ buscar_ruts.py
│  ├─ canonica_a_general.py
│  ├─ conicas.py
│  ├─ elementos.py
│  ├─ funciones_por_tramos.py
│  ├─ general_a_canonica.py
│  ├─ rut.py
│  ├─ salida.py
│  ├─ solucionario.py
│  └─ utils.py
├─ elementos_conicas/
│  ├─ elem_circunferencia.py
│  ├─ elem_elipse.py
│  ├─ elem_hiperbola.py
│  └─ elem_parabola.py
├─ .gitignore
└─ README.md
```

## Modulos

### `main.py`

Archivo principal del programa. Ejecuta la funcion `main()` que inicia la interfaz grafica de la aplicacion.

### `gui/` (Interfaz grafica)

- `gui.py`: Interfaz grafica principal (ventanas, botones, eventos).
- `formatters.py`: Logica de formato de texto y memoria de calculo para mostrar en la interfaz.
- `graficos.py`: Renderizador grafico para las conicas.
- `dibujo_utils.py`: Primitivas y configuraciones para dibujar en el lienzo.

### `src/` (Logica principal)

- `rut.py`: Limpieza, validacion y extraccion de digitos del RUT mediante modulo 11.
- `conicas.py`: Construccion de la ecuacion general de la conica y clasificacion.
- `elementos.py`: Centralizacion de calculos matematicos de los elementos de las conicas (centro, focos, vertices).
- `utils.py`: Funciones utilitarias generales, como el formateo numerico.
- `canonica_a_general.py`: Procedimiento inverso (forma canonica a general).
- `general_a_canonica.py`: Procedimiento directo (forma general a canonica completando cuadrados).
- `salida.py`: Funciones para mostrar los resultados y calculos detallados en consola.
- `funciones_por_tramos.py`: Modulo para el analisis de funciones por tramos, limites y continuidad.
- `solucionario.py`: Generador de solucionarios automatizados.
- `buscar_ruts.py`: Utilidad para buscar RUTs que generen conicas especificas.

### `elementos_conicas/`

Modulos especificos para calcular las propiedades matematicas de cada tipo de conica:
- `elem_circunferencia.py`
- `elem_elipse.py`
- `elem_hiperbola.py`
- `elem_parabola.py`

## Funcionalidades implementadas

- Validacion de RUT chileno mediante modulo 11.
- Aceptacion de multiples formatos de RUT.
- Procedimiento paso a paso de validacion y extraccion de digitos.
- Construccion y clasificacion automatica de ecuaciones generales de conicas.
- Calculo de elementos matematicos de las conicas (centro, focos, vertices, etc.).
- Transformacion bidireccional entre forma general y canonica paso a paso.
- Interfaz grafica completa con renderizado interactivo de la conica y memoria de calculo.
- Analisis de funciones por tramos, limites laterales, continuidad y discontinuidades.
- Generador de solucionarios y utilidades de busqueda de RUTs.
- Arquitectura limpia con clara separacion entre logica matematica, formateo de texto y renderizado de interfaz.

## Funcionalidades pendientes

- Evaluar una version web de la aplicacion.
## Ejemplo

Entrada:

```text
21.929.009-8
```

Salida esperada para la conica:

```text
0.375x^2 - 9x - 9y + 20 = 0
Clasificacion: Parabola
```

El programa tambien imprime los pasos de validacion del RUT, la construccion de coeficientes, la transformacion a forma canonica y la transformacion inversa.

## Integrantes

- Integrante 1: David Fernandez
- Integrante 2: Gabriel Gutiérrez
- Integrante 3: Ailyn Melillan

## Lider del grupo

- Lider: Gabriel Gutiérrez
