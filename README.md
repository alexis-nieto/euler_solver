# Solucionador Numérico de EDOs

Aplicación interactiva en Python para resolver Ecuaciones Diferenciales Ordinarias (EDOs) utilizando métodos numéricos clásicos.

## Características

- **Método de Euler**: Método simple de primer orden
- **Método de Heun (Euler Mejorado)**: Método predictor-corrector de segundo orden
  - Soporte para iteraciones múltiples del corrector
  - Comparación entre versión simple e iterada
- **Solución Exacta**: Búsqueda automática de soluciones analíticas cuando existen
- **Análisis de Errores**: Cálculo de errores relativos porcentuales
- **Interfaz Interactiva**: Menú intuitivo con Rich console

## Requisitos

- Python 3.8+
- Dependencias (ver `pyproject.toml`):
  - `rich`: Para interfaz de consola
  - `sympy`: Para parsing y resolución simbólica de EDOs

## Instalación

```bash
# Clonar o descargar el repositorio
cd euler_solver

# Instalar dependencias
pip install -r requirements.txt
# O si usa pyproject.toml:
pip install -e .
```

## Uso

```bash
python main.py
```

### Flujo de la Aplicación

1. **Seleccionar Método**: Elige entre Euler o Heun
2. **Ingresar EDO**: Define la función f(x, y) en formato Python/SymPy
   - Ejemplos: `x + y`, `sin(y)`, `x**2 - y`, etc.
3. **Configurar Parámetros**:
   - Valor inicial x₀
   - Valor inicial y₀
   - Valor final x_final
   - Tamaño de paso h
   - (Solo Heun) Número de iteraciones del corrector
   - Cifras significativas para mostrar
4. **Visualizar Resultados**: Tabla con:
   - Puntos calculados (x, y)
   - Solución exacta (si existe)
   - Errores relativos porcentuales
   - Para Heun: comparación simple vs iterado
5. **Continuar o Cambiar**: Reintentar con nuevos parámetros o cambiar método

## Métodos Numéricos

### Euler
Método de primer orden:
$$y_{i+1} = y_i + h \cdot f(x_i, y_i)$$

### Heun (Euler Mejorado)
Método predictor-corrector de segundo orden:
- **Predictor**: $y_{i+1}^* = y_i + h \cdot f(x_i, y_i)$
- **Corrector**: $y_{i+1} = y_i + \frac{h}{2}[f(x_i, y_i) + f(x_{i+1}, y_{i+1}^*)]$
- **Corrector Iterado** (opcional): Refina el valor repetiendo el paso corrector

## Estructura del Proyecto

```
eurler_solver/
├── main.py                 # Punto de entrada principal
├── interface.py            # Lógica de presentación y menús
├── input_handler.py        # Validación y captura de entrada del usuario
├── numerical_methods.py    # Implementación de métodos numéricos
├── simulation.py           # Orquestación de simulaciones
├── function_parser.py      # Parser y compilador de funciones
├── pyproject.toml          # Configuración de dependencias
└── README.md              # Este archivo
```

## Ejemplo de Uso

**EDO**: y' = -2xy

**Condiciones**:
- x₀ = 0, y₀ = 1
- x_final = 1
- h = 0.1
- Método: Heun (1 iteración)

**Resultado**: Tabla mostrando la evolución de y(x) con errores vs solución exacta (y = e^(-x²))

## Validación de Parámetros

La aplicación valida automáticamente:
- ✓ h > 0
- ✓ x_end > x₀
- ✓ corrector_iterations ≥ 1
- ✓ Sintaxis de función EDO
- ✓ División por cero en cálculo de errores

## Error Handling

- Captura de excepciones en funciones numéricas
- Visualización clara de errores al usuario
- Manejo de soluciones exactas no encontradas
- Tratamiento de valores cercanos a cero ("~0")

## Notas Técnicas

- Los métodos mantienen trayectorias independientes para simple vs iterado
- El número de pasos se calcula con ceil para precisión
- Se incluye el punto inicial (iteración 0) en resultados
- El epsilon 1e-9 previene errores de redondeo en condición de parada

## Autores

Desarrollado como herramienta educativa para análisis numérico.

## Licencia

Abierto para uso educativo.
