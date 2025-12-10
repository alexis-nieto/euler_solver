# Euler Solver TUI

Este proyecto implementa una aplicación de consola en Python para solucionar Ecuaciones Diferenciales Ordinarias (EDOs) numéricamente utilizando los métodos de Euler y Euler Mejorado.

## Requisitos previos

El proyecto utiliza `uv` como gestor de paquetes (aunque `pip` también funcionaría si instalas las dependencias manualmente).

## Instalación

1.  Asegúrate de estar en el directorio del proyecto:
    ```bash
    cd /home/arkanvs-pop/Desktop/euler_solver
    ```

2.  Instala las dependencias necesarias (`rich` y `sympy`) usando `uv`:
    ```bash
    uv add rich sympy
    ```
    *Nota: `uv` creará automáticamente un entorno virtual y agregará las librerías.*

## Ejecución

Para iniciar la aplicación:

```bash
uv run main.py
```

## Uso

1.  Menú Principal: Selecciona **1** para resolver una EDO.
2.  Ingresa la función $f(x, y)$:
    -   Ejemplo 1: `x + y`
    -   Ejemplo 2: `sin(x) * y`
    -   Ejemplo 3: `y - x**2 + 1`
3.  Ingresa las condiciones iniciales:
    -   $x_0$: Valor inicial de x (ej. 0).
    -   $y_0$: Valor inicial de y (ej. 1).
    -   $x_{final}$: Hasta dónde integrar (ej. 2).
    -   $h$: Tamaño del paso (ej. 0.1).
4.  Revisa la tabla comparativa con los resultados.

## Estructura del Código

-   `main.py`: Archivo principal.
-   `numerical_methods.py`: Contiene los algoritmos de Euler y Heun.
-   `function_parser.py`: Parsea strings a funciones de forma segura.
-   `input_handler.py`: Maneja inputs con Rich.
-   `output_formatter.py`: Genera tablas con Rich.
