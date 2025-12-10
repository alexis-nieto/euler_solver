"""
Módulo: output_formatter.py
Descripción: Se encarga de la presentación de resultados utilizando tablas de la librería 'rich'.
Genera tablas comparativas entre los métodos de Euler y Euler Mejorado.
"""

from rich.console import Console
from rich.table import Table
from typing import List, Tuple

from typing import List, Tuple, Optional
import math

console = Console()

def display_results_table(h: float,
                          euler_points: Optional[List[Tuple[float, float]]] = None, 
                          improved_euler_points: Optional[List[Tuple[float, float]]] = None,
                          real_values: Optional[List[float]] = None):
    """
    Genera y muestra una tabla comparativa dinámica.
    Dependiendo de qué listas se pasen (euler o improved o ambas), la tabla se adapta.

    Args:
        h: Tamaño de paso.
        euler_points: Lista (x, y) Euler (Opcional).
        improved_euler_points: Lista (x, y) Euler Mejorado (Opcional).
        real_values: Lista opcional con valores exactos y(x).
    """
    if not euler_points and not improved_euler_points:
        console.print("[red]Error: No data to display[/red]")
        return

    # Título dinámico
    modes = []
    if euler_points: modes.append("Euler")
    if improved_euler_points: modes.append("Heun")
    title = f"Resultados: {' & '.join(modes)} (h={h})"

    table = Table(title=title, show_header=True, header_style="bold magenta")
    
    # Definir columnas base
    table.add_column("Iter", justify="right", style="cyan", no_wrap=True)
    table.add_column("x_i", justify="right", style="green")
    
    # Calcular num_steps basándose en la lista que exista
    base_list = euler_points if euler_points else improved_euler_points
    num_steps = len(base_list)

    if euler_points:
        table.add_column("Euler y_i", justify="right", style="yellow")
    if improved_euler_points:
        table.add_column("Heun y_i", justify="right", style="blue")
    
    if real_values:
        table.add_column("Verdadero y(x)", justify="right", style="white")
        table.add_column("% Error", justify="right", style="red")

    for i in range(num_steps):
        # Obtenemos x del que esté disponible (serán iguales si hay ambos)
        x_val = base_list[i][0]
        f_x = f"{x_val:.4f}"
        
        row_data = [str(i), f_x]
        
        # Valor aproximado para calcular error (priorizamos Heun si existe, sino Euler)
        y_approx = 0.0
        
        if euler_points:
            y_eu = euler_points[i][1]
            row_data.append(f"{y_eu:.8g}")
            if not improved_euler_points: y_approx = y_eu # Si solo es Euler, el error es de Euler

        if improved_euler_points:
            y_imp = improved_euler_points[i][1]
            row_data.append(f"{y_imp:.8g}")
            y_approx = y_imp # Prioridad para error

        if real_values:
            val_real = real_values[i]
            
            if math.isnan(val_real):
                f_real = "N/A"
                f_error = "N/A"
            else:
                f_real = f"{val_real:.8g}"
                if abs(val_real) < 1e-12:
                    f_error = "undef"
                else:
                    err = abs((val_real - y_approx) / val_real) * 100.0
                    f_error = f"{err:.4g}%"
            
            row_data.append(f_real)
            row_data.append(f_error)
        
        table.add_row(*row_data)
        
    console.print(table)

def display_summary(x0: float, y0: float, x_final: float, h: float, func_str: str):
    """Muestra un resumen de los parámetros de la simulación."""
    console.print("\n[bold underline]Resumen de Parámetros:[/bold underline]")
    console.print(f" • EDO: [bold]y' = {func_str}[/bold]")
    console.print(f" • Condición Inicial: y({x0}) = {y0}")
    console.print(f" • Intervalo: [{x0}, {x_final}]")
    console.print(f" • Paso (h): {h}")
    console.print(f" • Pasos estimados: {int((x_final - x0)/h)}")
    console.print("")
