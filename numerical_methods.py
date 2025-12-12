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
                          x_end: float,
                          corrector_iterations: int = 1) -> List[Tuple[float, float, float]]:
    """
    Resuelve una EDO y' = f(x, y) utilizando el método de Euler Mejorado (Método de Heun).
    Es un método Predictor-Corrector con corrector iterado.

    Fórmulas:
        Predictor: y_{i+1}^* = y_i + h * f(x_i, y_i)
        Corrector (iterado): y_{i+1}^(k) = y_i + (h/2) * [ f(x_i, y_i) + f(x_{i+1}, y_{i+1}^(k-1)) ]

    Args:
        f (Callable): La función derivada f(x, y).
        x0 (float): Valor inicial de x.
        y0 (float): Valor inicial de y (condición inicial).
        h (float): Tamaño del paso.
        x_end (float): Valor final de x.
        corrector_iterations (int): Número de iteraciones del corrector (default 1).

    Returns:
        List[Tuple[float, float, float]]: Lista de tuplas (x_i, y_i_single, y_i_iterated) con los resultados.
                                          y_i_single: resultado con 1 corrección
                                          y_i_iterated: resultado con iteraciones completas
    """
    points = [(x0, y0, y0)]  # Punto inicial: iteración 0
    curr_x = x0
    curr_y_single = y0  # Para seguimiento de Heun simple
    curr_y_iter = y0    # Para seguimiento de Heun iterado

    while curr_x < x_end - 1e-9:
        # Paso 1: Calcular la pendiente en el punto actual (común con Euler)
        # k1 = f(x_i, y_i) - usamos el valor de una iteración como base
        k1 = f(curr_x, curr_y_single)
        
        # Paso 2: Predecir el siguiente punto usando Euler simple
        # y_predict = y_i + h * k1
        # x_next = x_i + h
        x_next = curr_x + h
        y_predict = curr_y_single + h * k1
        
        # Paso 3: Calcular la pendiente en el punto predicho
        # k2 = f(x_{i+1}, y_{i+1}^*)
        k2 = f(x_next, y_predict)
        
        # Paso 4: Corrección simple (una iteración)
        # y_{i+1}^(1) = y_i + (h/2) * (k1 + k2)
        y_single_correction = curr_y_single + (h / 2.0) * (k1 + k2)
        
        # Paso 5: Correcciones iteradas si corrector_iterations > 1
        # Partimos de la versión simple para las iteraciones adicionales
        y_iterated = y_single_correction
        if corrector_iterations > 1:
            for _ in range(corrector_iterations - 1):
                # y_{i+1}^(k) = y_i + (h/2) * [ f(x_i, y_i) + f(x_{i+1}, y_{i+1}^(k-1)) ]
                k2_new = f(x_next, y_iterated)
                y_iterated = curr_y_single + (h / 2.0) * (k1 + k2_new)
        
        # Actualizar x y guardar tanto la versión simple como la iterada
        curr_x = x_next
        curr_y_single = y_single_correction  # Seguir con versión simple para próximo paso
        curr_y_iter = y_iterated              # Seguir con versión iterada para próximo paso
        points.append((curr_x, y_single_correction, y_iterated))
        
    return points
