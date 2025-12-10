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

def display_results_table(euler_points: List[Tuple[float, float]], 
                          improved_euler_points: List[Tuple[float, float]],
                          h: float,
                          real_values: Optional[List[float]] = None):
    """
    Genera y muestra una tabla comparativa de los resultados.
    Ahora incluye opción para mostrar valor real y error relativo.

    Args:
        euler_points: Lista (x, y) Euler.
        improved_euler_points: Lista (x, y) Euler Mejorado.
        h: Tamaño de paso.
        real_values: Lista opcional con valores exactos y(x) para cada punto.
    """
    table = Table(title=f"Comparación de Métodos (h={h})", show_header=True, header_style="bold magenta")
    
    # Definir columnas
    table.add_column("Iter", justify="right", style="cyan", no_wrap=True)
    table.add_column("x_i", justify="right", style="green")
    table.add_column("Euler y_i", justify="right", style="yellow")
    table.add_column("Heun y_i", justify="right", style="blue")
    
    if real_values:
        table.add_column("Exacta y(x)", justify="right", style="white")
        table.add_column("% Error (Heun)", justify="right", style="red")

    num_steps = len(euler_points)
    
    for i in range(num_steps):
        x_eu, y_eu = euler_points[i]
        _, y_imp = improved_euler_points[i]
        
        # Formatear números para legibilidad (8 cifras significativas como solicitado)
        # ".8g" usa notación científica si es necesario o decimal compacto.
        f_x = f"{x_eu:.4f}"
        f_yeu = f"{y_eu:.8g}"
        f_yimp = f"{y_imp:.8g}"
        
        row_data = [str(i), f_x, f_yeu, f_yimp]
        
        if real_values:
            val_real = real_values[i]
            
            # Formatear valor real
            if math.isnan(val_real):
                f_real = "N/A"
                f_error = "N/A"
            else:
                f_real = f"{val_real:.8g}"
                
                # Calcular error relativo: |(Real - Aprox) / Real| * 100
                # Usamos la aproximación de Heun para el error
                if abs(val_real) < 1e-12: # Evitar división por cero si real es 0
                    f_error = "undef"
                else:
                    err = abs((val_real - y_imp) / val_real) * 100.0
                    f_error = f"{err:.4g}%" # 4 cifras para el error es suficiente usualmente
            
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
