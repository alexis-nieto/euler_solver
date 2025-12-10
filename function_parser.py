"""
Módulo: function_parser.py
Descripción: Este módulo se encarga del análisis y conversión segura de funciones matemáticas
ingresadas por el usuario en formato string a expresiones ejecutables de Python/SymPy.
"""

import sympy as sp
from typing import Callable, Tuple, Any, Optional

class FunctionParserError(Exception):
    """Excepción personalizada para errores en el análisis de funciones."""
    pass

def parse_function(expression_str: str) -> Callable[[float, float], float]:
    """
    Convierte una cadena de texto representando una función matemática f(x, y)
    en un objeto llamable de Python.

    Utiliza SymPy para 'sympify' la expresión de manera segura, permitiendo funciones
    como sin, cos, exp, etc.

    Args:
        expression_str (str): La función ingresada por el usuario (ej. "x + y", "sin(x)*y").
    
    Returns:
        Callable[[float, float], float]: Una función lambda que toma x e y como argumentos
                                         y devuelve el valor evaluado.
    
    Raises:
        FunctionParserError: Si la expresión es inválida o contiene símbolos no permitidos.
    """
    try:
        # Definir los símbolos permitidos.
        # x: variable independiente
        # y: variable dependiente
        x, y = sp.symbols('x y')
        
        # Diccionario de contexto local para sympify.
        # Esto restringe qué se puede interpretar, mejorando la seguridad,
        # aunque 'sympify' sigue siendo potente.
        allowed_locals = {
            'x': x,
            'y': y,
            'sin': sp.sin,
            'cos': sp.cos,
            'tan': sp.tan,
            'exp': sp.exp,
            'log': sp.log,
            'sqrt': sp.sqrt,
            'pi': sp.pi,
            'e': sp.E
        }

        # Convertir el string a una expresión simbólica de SymPy.
        # Se usa evaluate=False para simplemente parsear primero, aunque para lambdify no es estricto.
        expr = sp.sympify(expression_str, locals=allowed_locals)

        # Verificar que no haya símbolos extraños que no sean x, y o constantes.
        # free_symbols devuelve el conjunto de símbolos en la expresión.
        free_syms = expr.free_symbols
        for sym in free_syms:
            if str(sym) not in ['x', 'y']:
                 # Nota: sympy.pi es constante, no free symbol en este contexto usualmente,
                 # pero si el usuario mete 'z', aquí lo detectamos.
                 raise FunctionParserError(f"Símbolo desconocido detectado: '{sym}'. Solo se permiten 'x' e 'y'.")

        # Convertir la expresión simbólica a una función rápida de Python (usando numpy/math backend por defecto).
        # "modules='math'" asegura que use math.sin, etc., para rendimiento y compatibilidad con floats estándar.
        f_lambda = sp.lambdify((x, y), expr, modules='math')

        def safe_wrapper(val_x: float, val_y: float) -> float:
            """Wrapper para capturar errores de dominio matemático (ej. div por cero) durante la ejecución."""
            try:
                # sp.lambdify a veces puede devolver tipos complejos o numpy, forzamos float nativo si es necesario
                # y manejamos excepciones.
                return float(f_lambda(val_x, val_y))
            except ZeroDivisionError:
                raise FunctionParserError(f"División por cero evaluando f({val_x}, {val_y})")
            except ValueError as e:
                # Errores como sqrt(-1) en dominio real
                raise FunctionParserError(f"Error matemático evaluando f({val_x}, {val_y}): {e}")
            except Exception as e:
                raise FunctionParserError(f"Error inesperado evaluando función: {e}")

        return safe_wrapper

    except sp.SympifyError as e:
        raise FunctionParserError(f"La expresión no es válida: {e}")
    except FunctionParserError:
        raise
    except Exception as e:
        raise FunctionParserError(f"Error al procesar la función: {e}")

import signal

def solve_exact_ode(expression_str: str, x0: float, y0: float) -> Optional[Tuple[Callable[[float], float], str]]:
    """
    Intenta encontrar la solución analítica exacta para y' = f(x, y) con y(x0) = y0.
    INCLUYE TIMEOUT DE 3 SEGUNDOS para evitar bloqueos en EDOs complejas.
    
    Args:
        expression_str: String de f(x, y)
        x0, y0: Condiciones iniciales
        
    Returns:
        (Callable, str): Tupla con (función lambda, representación string) si tiene éxito.
        None: Si falla/timeout.
    """
    
    # Identificar si podemos usar señales (Unix-only) para timeout
    has_alarm = hasattr(signal, 'SIGALRM')
    
    # Manejador para el timeout
    def handler(signum, frame):
        raise TimeoutError("Cálculo excedió el tiempo límite.")

    try:
        # Configurar alarma de 3 segundos solo si existe SIGALRM
        if has_alarm:
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(3)
        
        try:
            x = sp.symbols('x')
            y = sp.Function('y')(x)
            
            # Parsear sympy expression
            local_dict = {'x': x, 'y': y, 'e': sp.E, 'pi': sp.pi}
            f_sym = sp.sympify(expression_str, locals={'x': x, 'y': sp.symbols('y'), 'e': sp.E})
            ode_eq = sp.Eq(y.diff(x), f_sym.subs(sp.symbols('y'), y))
            
            # Resolver
            sol = sp.dsolve(ode_eq, y, ics={y.subs(x, x0): y0})
            
            if isinstance(sol, list):
                sol = sol[0]
                
            rhs = sol.rhs
            real_lambda = sp.lambdify(x, rhs, modules='math')
            
            def safe_real_y(val_x: float) -> float:
                try:
                    return float(real_lambda(val_x))
                except Exception:
                    return float('nan')
                    
            return safe_real_y, str(rhs)
            
        finally:
            # Desactivar alarma pase lo que pase si se usó
            if has_alarm:
                signal.alarm(0)

    except TimeoutError:
        # El llamador manejará el None mostrando un mensaje de advertencia si desea
        return None
        
    except Exception:
        return None
