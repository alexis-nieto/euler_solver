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
                          real_values: Optional[List[float]] = None,
                          decimals: int = 8):
    """
    Genera y muestra una tabla comparativa dinámica.
    Dependiendo de qué listas se pasen (euler o improved o ambas), la tabla se adapta.

    Args:
        h: Tamaño de paso.
        euler_points: Lista (x, y) Euler (Opcional).
        improved_euler_points: Lista (x, y) Euler Mejorado (Opcional).
        real_values: Lista opcional con valores exactos y(x).
        decimals: Número de decimales para mostrar (default: 8).
    """
    if not euler_points and not improved_euler_points:
        console.print("[red]Error: No data to display[/red]")
        return

    # Título dinámico
    modes = []
    if euler_points: modes.append("Euler")
    if improved_euler_points: modes.append("Heun")
    title = f"Resultados: {' & '.join(modes)} (h={h})"

    table = Table(title=title, show_header=True, header_style="bold", title_style="bold")
    
    # Definir columnas base (Iteración y X)
    table.add_column("Iter", justify="right", style="dim", no_wrap=True)
    table.add_column("x_i", justify="right")
    
    # Calcular num_steps basándose en la lista que exista
    base_list = euler_points if euler_points else improved_euler_points
    num_steps = len(base_list)

    # Orden solicitado: Exacta antes que aproximaciones
    if real_values:
        # Valor verdadero destacado (Bold)
        table.add_column("Verdadero y(x)", justify="right", style="bold")

    if euler_points:
        table.add_column("Euler y_i", justify="right")
    if improved_euler_points:
        table.add_column("Heun y_i", justify="right")
    
    if real_values:
        table.add_column("% Error", justify="right", style="red")

    for i in range(num_steps):
        # Obtenemos x del que esté disponible
        x_val = base_list[i][0]
        f_x = f"{x_val:.4f}" # x suele ser limpio con 4
        
        row_data = [str(i), f_x]
        
        # Buffer para datos aproximados para añadirlos después de la exacta
        approx_data = []

        # Valor aproximado para calcular error
        y_approx = 0.0
        
        # Procesar exacta para añadirla primero si existe
        val_real = float('nan')
        f_real = "N/A"
        f_error = "N/A"

        if real_values:
            val_real = real_values[i]
            if math.isnan(val_real):
                f_real = "N/A"
            else:
                # Decimales dinámicos
                f_real = f"{val_real:.{decimals}f}"
            
            row_data.append(f_real)

        if euler_points:
            y_eu = euler_points[i][1]
            approx_data.append(f"{y_eu:.{decimals}f}")
            if not improved_euler_points: y_approx = y_eu

        if improved_euler_points:
            y_imp = improved_euler_points[i][1]
            approx_data.append(f"{y_imp:.{decimals}f}")
            y_approx = y_imp 

        row_data.extend(approx_data)

        if real_values:
            if not math.isnan(val_real):
                if abs(val_real) < 1e-12:
                    f_error = "undef"
                else:
                    err = abs((val_real - y_approx) / val_real) * 100.0
                    f_error = f"{err:.4f}%" # Error también con formato fijo limpio
            
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
