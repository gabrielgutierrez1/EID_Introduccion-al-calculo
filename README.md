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

La version por consola sigue disponible desde la funcion `main_consola`:

```powershell
python3 -c "from main import main_consola; main_consola()"
```

## Estructura del proyecto

```text
EID_Introduccion-al-calculo/
├─ main.py
├─ gui/
│  ├─ __init__.py
│  └─ gui.py
├─ src/
│  ├─ __init__.py
│  ├─ rut.py
│  ├─ conicas.py
│  ├─ canonica_a_general.py
│  ├─ general_a_canonica.py
│  └─ salida.py
├─ .gitignore
└─ README.md
```

## Modulos

### `main.py`

Archivo principal del programa. Por defecto abre la interfaz grafica con `main()`. Tambien conserva `main_consola()` para ejecutar el flujo completo por terminal:

1. Muestra el formato de RUT permitido.
2. Pide el RUT al usuario.
3. Valida el RUT.
4. Muestra el procedimiento de validacion modulo 11.
5. Extrae los digitos del cuerpo del RUT.
6. Construye y clasifica la conica.
7. Muestra la ecuacion general, la forma canonica y el procedimiento inverso.

### `gui/gui.py`

Interfaz grafica hecha con `tkinter`.

Incluye:

- Ventana principal.
- Campo para ingresar RUT.
- Boton de analisis.
- Area de resultados.
- Grafico de la conica.
- Conexion con la validacion de RUT y el analisis de conicas.

### `src/rut.py`

Contiene la logica relacionada con el RUT:

- Limpieza del formato.
- Validacion de formatos aceptados.
- Separacion entre cuerpo y digito verificador.
- Validacion mediante modulo 11.
- Registro paso a paso del calculo del digito verificador.
- Extraccion de los digitos del cuerpo.

### `src/conicas.py`

Construye la ecuacion:

```text
Ax^2 + By^2 + Cx + Dy + E = 0
```

Tambien aplica las reglas especiales del enunciado y clasifica la conica como:

- Circunferencia.
- Elipse.
- Hiperbola.
- Parabola.

Ademas contiene funciones para:

- Formatear numeros para la salida.
- Construir la ecuacion general.
- Coordinar el analisis completo de la conica.

### `src/canonica_a_general.py`

Contiene el procedimiento inverso para transformar la forma canonica de una conica a su ecuacion general.

### `src/general_a_canonica.py`

Contiene el procedimiento para transformar la ecuacion general de una conica a forma canonica completando cuadrados.

### `src/salida.py`

Contiene funciones para mostrar en consola:

- Resultado de la validacion del RUT.
- Procedimiento modulo 11.
- Construccion de coeficientes de la conica.
- Ecuacion general.
- Clasificacion.
- Transformacion a forma canonica.
- Transformacion inversa de forma canonica a general.

## Funcionalidades implementadas

- Validacion de RUT chileno mediante modulo 11.
- Aceptacion de RUT con puntos y guion, solo guion o sin separadores.
- Procedimiento paso a paso de validacion.
- Extraccion de digitos `d1` a `d8`.
- Calculo de coeficientes `A`, `B`, `C`, `D`, `E`.
- Conversion del digito verificador a valor `v`, considerando `K = 10` y `0 = 11`.
- Aplicacion de reglas especiales para obtener distintas conicas.
- Clasificacion automatica de la conica.
- Impresion ordenada de la ecuacion general.
- Transformacion paso a paso desde forma general a forma canonica.
- Procedimiento inverso desde forma canonica a forma general.
- Interfaz grafica conectada con validacion, analisis y grafica de la conica.

## Funcionalidades pendientes

- Modulo de funciones por tramos.
- Analisis de limites laterales, continuidad y discontinuidades.
- Mejorar la interfaz grafica o evaluar una version web.

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
