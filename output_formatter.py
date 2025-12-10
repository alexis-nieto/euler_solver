"""
Módulo: output_formatter.py
Descripción: Se encarga de la presentación de resultados utilizando tablas de la librería 'rich'.
Genera tablas comparativas entre los métodos de Euler y Euler Mejorado.
"""

from rich.console import Console
from rich.table import Table
from typing import List, Tuple

console = Console()

def display_results_table(euler_points: List[Tuple[float, float]], 
                          improved_euler_points: List[Tuple[float, float]],
                          h: float):
    """
    Genera y muestra una tabla comparativa de los resultados.

    Args:
        euler_points (List[Tuple]): Puntos (x, y) calculados por Euler.
        improved_euler_points (List[Tuple]): Puntos (x, y) calculados por Euler Mejorado.
        h (float): Tamaño del paso utilizado.
    """
    table = Table(title=f"Comparación de Métodos (h={h})", show_header=True, header_style="bold magenta")
    
    # Definir columnas
    table.add_column("Iter (i)", justify="right", style="cyan", no_wrap=True)
    table.add_column("x_i", justify="right", style="green")
    table.add_column("y_i (Euler)", justify="right", style="yellow")
    table.add_column("y_i (Euler Mejorado)", justify="right", style="blue")
    
    # Asumimos que ambas listas tienen la misma longitud y corresponden a los mismos x.
    # Usamos zip para iterar ambas.
    num_steps = len(euler_points)
    
    for i in range(num_steps):
        x_eu, y_eu = euler_points[i]
        x_imp, y_imp = improved_euler_points[i]
        
        # Formatear números para legibilidad (4 decimales)
        f_x = f"{x_eu:.4f}"
        f_yeu = f"{y_eu:.6f}"
        f_yimp = f"{y_imp:.6f}"
        
        table.add_row(str(i), f_x, f_yeu, f_yimp)
        
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
