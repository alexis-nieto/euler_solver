"""
Módulo: input_handler.py
Descripción: Maneja la entrada de datos del usuario, validando tipos, rangos y consistencia lógica.
Utiliza 'rich' para prompts estéticos cuando sea posible, aunque input() estándar es la base para captura.
"""

from typing import Callable, Optional, Tuple
from rich.console import Console
from rich.prompt import Prompt, FloatPrompt
from function_parser import parse_function, FunctionParserError

console = Console()

def get_float(prompt_text: str, min_val: Optional[float] = None, greater_than: Optional[float] = None) -> float:
    """
    Solicita al usuario un número flotante con validación de rango.

    Args:
        prompt_text (str): El mensaje a mostrar.
        min_val (Optional[float]): Valor mínimo permitido (inclusivo).
        greater_than (Optional[float]): Valor que el input debe superar estrictamente (exclusivo).

    Returns:
        float: El número válido ingresado por el usuario.
    """
    while True:
        try:
            # Usamos FloatPrompt de Rich para una experiencia input robusta
            val = FloatPrompt.ask(f"[cyan]{prompt_text}[/cyan]")
            
            if min_val is not None and val < min_val:
                console.print(f"[bold red]Error:[/bold red] El valor debe ser mayor o igual a {min_val}.")
                continue
            
            if greater_than is not None and val <= greater_than:
                console.print(f"[bold red]Error:[/bold red] El valor debe ser mayor estricto a {greater_than}.")
                continue
                
            return val
        except ValueError:
            console.print("[bold red]Error:[/bold red] Entrada no válida. Por favor ingrese un número.")

def get_function_input(prompt_text: str) -> Tuple[Callable[[float, float], float], str]:
    """
    Solicita al usuario una función EDO en formato string y la valida.

    Args:
        prompt_text (str): Mensaje a mostrar.

    Returns:
        Tuple[Callable, str]: Retorna la función 'compilada' y el string original.
    """
    while True:
        func_str = Prompt.ask(f"[cyan]{prompt_text}[/cyan]")
        try:
            func = parse_function(func_str)
            
            # Prueba rápida para verificar que no explota inmediatamente con valores simples (0,0) o (1,1)
            # Esto es solo un 'smoke test' opcional, pero ayuda a detectar typos graves.
            try:
                func(1.0, 1.0)
            except Exception:
                # Si falla al evaluar en 1,1 no necesariamente es error (ej. 1/log(1)), así que no bloqueamos,
                # pero confiamos en que parse_function ya hizo validación sintáctica.
                pass
                
            return func, func_str
        except FunctionParserError as e:
            console.print(f"[bold red]Error de Función:[/bold red] {e}")
            console.print("[yellow]Asegúrese de usar sintaxis Python/SymPy (ej: x + sin(y), x**2, etc.)[/yellow]")

def wait_for_enter():
    """Pausa la ejecución hasta que el usuario presione Enter."""
    console.input("\n[dim]Presione <Enter> para continuar...[/dim]")
