"""
Módulo: numerical_methods.py
Descripción: Implementación de los algoritmos numéricos para la resolución de EDOs.
Contiene las funciones para el método de Euler y el método de Euler Mejorado (Heun).
"""

from typing import Callable, List, Tuple

def euler_method(f: Callable[[float, float], float], 
                 x0: float, 
                 y0: float, 
                 h: float, 
                 x_end: float) -> List[Tuple[float, float]]:
    """
    Resuelve una EDO y' = f(x, y) utilizando el método de Euler.

    Fórmula: y_{i+1} = y_i + h * f(x_i, y_i)

    Args:
        f (Callable): La función derivada f(x, y).
        x0 (float): Valor inicial de x.
        y0 (float): Valor inicial de y (condición inicial).
        h (float): Tamaño del paso.
        x_end (float): Valor final de x hasta donde integrar.

    Returns:
        List[Tuple[float, float]]: Lista de tuplas (x_i, y_i) con los resultados.
    """
    points = [(x0, y0)]
    curr_x = x0
    curr_y = y0

    # Iterar mientras no superemos x_end.
    # Usamos un pequeño epsilon para manejo de errores de punto flotante en la parada.
    # O simplemente número de pasos calculados si quisiéramos ser más exactos con steps enteros.
    # Aquí iremos acumulando x.
    while curr_x < x_end - 1e-9: # 1e-9 evita un último paso extra por error de redondeo
        slope = f(curr_x, curr_y)
        curr_y = curr_y + h * slope
        curr_x = curr_x + h
        points.append((curr_x, curr_y))
    
    return points


def improved_euler_method(f: Callable[[float, float], float], 
                          x0: float, 
                          y0: float, 
                          h: float, 
                          x_end: float) -> List[Tuple[float, float]]:
    """
    Resuelve una EDO y' = f(x, y) utilizando el método de Euler Mejorado (Método de Heun).
    Es un método Predictor-Corrector.

    Fórmulas:
        Predictor: y_{i+1}^* = y_i + h * f(x_i, y_i)
        Corrector: y_{i+1} = y_i + (h/2) * [ f(x_i, y_i) + f(x_{i+1}, y_{i+1}^*) ]

    Args:
        f (Callable): La función derivada f(x, y).
        x0 (float): Valor inicial de x.
        y0 (float): Valor inicial de y (condición inicial).
        h (float): Tamaño del paso.
        x_end (float): Valor final de x.

    Returns:
        List[Tuple[float, float]]: Lista de tuplas (x_i, y_i) con los resultados.
    """
    points = [(x0, y0)]
    curr_x = x0
    curr_y = y0

    while curr_x < x_end - 1e-9:
        # Paso 1: Calcular la pendiente en el punto actual (común con Euler)
        # k1 = f(x_i, y_i)
        k1 = f(curr_x, curr_y)
        
        # Paso 2: Predecir el siguiente punto usando Euler simple
        # y_predict = y_i + h * k1
        # x_next = x_i + h
        x_next = curr_x + h
        y_predict = curr_y + h * k1
        
        # Paso 3: Calcular la pendiente en el punto predicho
        # k2 = f(x_{i+1}, y_{i+1}^*)
        k2 = f(x_next, y_predict)
        
        # Paso 4: Corregir el valor de y promediando las pendientes
        # y_{i+1} = y_i + (h/2) * (k1 + k2)
        curr_y = curr_y + (h / 2.0) * (k1 + k2)
        
        # Actualizar x y guardar
        curr_x = x_next
        points.append((curr_x, curr_y))
        
    return points
