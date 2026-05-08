# Proyecto EID - Introduccion al Calculo

Aplicacion en Python para la Evaluacion Integrada de Desempeno N°1 del curso MAT1186.

El proyecto valida un RUT chileno, extrae sus digitos y construye una ecuacion general de segundo grado para clasificar una seccion conica. Mas adelante incorporara el analisis de funciones por tramos generado desde el mismo RUT.

## Requisitos actuales

- Python 3.
- No usar librerias matematicas externas como `numpy`, `math`, `sympy`, `scipy` o `pandas`.
- Todos los calculos matematicos deben implementarse manualmente.

## Como ejecutar

Desde la carpeta raiz del proyecto:

```powershell
python main.py
```

Luego ingresar un RUT chileno con cuerpo de 8 digitos, por ejemplo:

```text
21.929.009-8
```

## Estructura del proyecto

```text
calculo_eid/
├─ main.py
├─ eid_calculo.py
├─ src/
│  ├─ __init__.py
│  ├─ rut.py
│  ├─ conicas.py
│  └─ salida.py
└─ README.md
```

## Modulos

### `main.py`

Archivo principal. Controla el flujo del programa:

1. Pide el RUT al usuario.
2. Valida el RUT.
3. Extrae los digitos.
4. Construye y clasifica la conica.
5. Muestra los resultados en consola.

### `src/rut.py`

Contiene la logica relacionada con el RUT:

- Limpieza del formato.
- Separacion entre cuerpo y digito verificador.
- Validacion mediante modulo 11.
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

### `src/salida.py`

Contiene funciones para mostrar el procedimiento paso a paso en consola.

### `eid_calculo.py`

Archivo puente para ejecutar el mismo programa desde el nombre inicial del proyecto.

## Funcionalidades implementadas

- Validacion de RUT chileno mediante modulo 11.
- Procedimiento paso a paso de validacion.
- Extraccion de digitos `d1` a `d8`.
- Calculo de coeficientes `A`, `B`, `C`, `D`, `E`.
- Aplicacion de reglas especiales para obtener distintas conicas.
- Clasificacion automatica de la conica.
- Impresion ordenada de la ecuacion general.

## Funcionalidades pendientes

- Transformacion paso a paso desde forma general a forma canonica.
- Procedimiento inverso desde forma canonica a forma general.
- Grafica de la conica.
- Modulo de funciones por tramos.
- Analisis de limites laterales, continuidad y discontinuidades.
- Interfaz grafica o web.
- Campos vacios para completar durante la defensa oral.

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

## Integrantes

- Integrante 1:
- Integrante 2:
- Integrante 3:

## Lider del grupo

- Lider:

## Codigo de etica

Pendiente de completar por el grupo.
