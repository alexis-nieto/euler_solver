"""
Módulo: simulation.py
Descripción: Encapsula la lógica de orquestación de la simulación.
Coordina la ejecución de métodos numéricos y la búsqueda de soluciones exactas.
"""

from typing import Callable, Optional, Dict, Any, List, Tuple
from numerical_methods import euler_method, improved_euler_method
from function_parser import solve_exact_ode

def run_simulation(method_type: str, 
                   func: Callable[[float, float], float], 
                   func_str: str, 
                   x0: float, 
                   y0: float, 
                   h: float, 
                   tf: float) -> Dict[str, Any]:
    """
    Ejecuta la simulación completa bajo los parámetros dados.

    Args:
        method_type: 'EULER' o 'HEUN'.
        func: La función f(x, y) compilada.
        func_str: La representación string de la función.
        x0, y0: Condiciones iniciales.
        h: Paso.
        tf: x final.

    Returns:
        Un diccionario con los resultados:
        {
            'method': str,
            'euler_points': List or None,
            'heun_points': List or None,
            'exact_points': List or None,
            'exact_func_str': str or None,
            'error': str (si hubo excepción)
        }
    """
    results = {
        'method': method_type,
        'euler_points': None,
        'heun_points': None,
        'exact_points': None,
        'exact_func_str': None,
        'error': None
    }

    try:
        # 1. Ejecutar Método Numérico
        if method_type == 'EULER':
            results['euler_points'] = euler_method(func, x0, y0, h, tf)
        elif method_type == 'HEUN':
            results['heun_points'] = improved_euler_method(func, x0, y0, h, tf)

        # 2. Intentar Solución Exacta
        # Solo calculamos si tenemos puntos de referencia (que deberíamos tener)
        ref_points = results['euler_points'] if results['euler_points'] else results['heun_points']
        
        if ref_points:
            exact_res = solve_exact_ode(func_str, x0, y0)
            if exact_res:
                real_func, expr_str = exact_res
                results['exact_func_str'] = expr_str
                # Evaluar solución exacta en los mismos puntos x
                results['exact_points'] = [real_func(p[0]) for p in ref_points]

    except Exception as e:
        results['error'] = str(e)
    
    return results
