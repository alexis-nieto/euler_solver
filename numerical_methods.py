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
        h (float): Tamaño del paso (debe ser > 0).
        x_end (float): Valor final de x hasta donde integrar (debe ser > x0).

    Raises:
        ValueError: Si los parámetros son inválidos.

    Returns:
        List[Tuple[float, float]]: Lista de tuplas (x_i, y_i) con los resultados.
    """
    # Validación de parámetros
    if h <= 0:
        raise ValueError(f"El tamaño de paso h debe ser positivo, se recibió: {h}")
    if x_end <= x0:
        raise ValueError(f"x_end ({x_end}) debe ser mayor que x0 ({x0})")
    
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
        h (float): Tamaño del paso (debe ser > 0).
        x_end (float): Valor final de x (debe ser > x0).
        corrector_iterations (int): Número de iteraciones del corrector (default 1, debe ser >= 1).

    Raises:
        ValueError: Si los parámetros son inválidos.

    Returns:
        List[Tuple[float, float, float]]: Lista de tuplas (x_i, y_i_single, y_i_iterated) con los resultados.
                                          y_i_single: resultado con 1 corrección
                                          y_i_iterated: resultado con iteraciones completas
    """
    # Validación de parámetros
    if h <= 0:
        raise ValueError(f"El tamaño de paso h debe ser positivo, se recibió: {h}")
    if x_end <= x0:
        raise ValueError(f"x_end ({x_end}) debe ser mayor que x0 ({x0})")
    if corrector_iterations < 1:
        raise ValueError(f"El número de iteraciones del corrector debe ser >= 1, se recibió: {corrector_iterations}")
    
    points = [(x0, y0, y0)]  # Punto inicial: iteración 0
    curr_x = x0
    curr_y_single = y0  # Para seguimiento de Heun simple
    curr_y_iter = y0    # Para seguimiento de Heun iterado

    while curr_x < x_end - 1e-9:
        # Paso 1: Calcular la pendiente en el punto actual para versión simple
        # k1 = f(x_i, y_i)
        k1_single = f(curr_x, curr_y_single)
        
        # Paso 2: Predecir el siguiente punto usando Euler simple
        x_next = curr_x + h
        y_predict_single = curr_y_single + h * k1_single
        
        # Paso 3: Calcular la pendiente en el punto predicho
        k2_single = f(x_next, y_predict_single)
        
        # Paso 4: Corrección simple (una iteración)
        y_single_correction = curr_y_single + (h / 2.0) * (k1_single + k2_single)
        
        # Ahora para la versión iterada, usar su propia trayectoria
        k1_iter = f(curr_x, curr_y_iter)
        y_predict_iter = curr_y_iter + h * k1_iter
        k2_iter = f(x_next, y_predict_iter)
        
        # Corrección simple (una iteración) para versión iterada
        y_iterated = curr_y_iter + (h / 2.0) * (k1_iter + k2_iter)
        
        # Paso 5: Correcciones iteradas si corrector_iterations > 1
        if corrector_iterations > 1:
            for _ in range(corrector_iterations - 1):
                # y_{i+1}^(k) = y_i + (h/2) * [ f(x_i, y_i) + f(x_{i+1}, y_{i+1}^(k-1)) ]
                k2_iter_new = f(x_next, y_iterated)
                y_iterated = curr_y_iter + (h / 2.0) * (k1_iter + k2_iter_new)
        
        # Actualizar x y guardar tanto la versión simple como la iterada
        curr_x = x_next
        curr_y_single = y_single_correction  # Seguir con versión simple para próximo paso
        curr_y_iter = y_iterated              # Seguir con versión iterada para próximo paso
        points.append((curr_x, y_single_correction, y_iterated))
        
    return points
