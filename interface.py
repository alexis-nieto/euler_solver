"""
Módulo: interface.py
Descripción: Centraliza toda la lógica de presentación y menús de la aplicación.
Reemplaza a output_formatter.py y absorbe la lógica visual de main.py.
"""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from typing import Dict, Any, Optional
import math
import sys

# Instancia global de consola
console = Console()

def show_header():
    """Muestra el banner principal."""
    console.rule()
    console.print(Panel.fit(
        "[bold]Solucionador Numérico de EDOs[/bold]\n"
        "Métodos de Euler y Heun",
        border_style="white"
    ))

def show_function_panel(func_str: str):
    """Muestra el panel con la EDO original."""
    console.print("")
    console.print(Panel(
        f"[bold]{func_str}[/bold]",
        title="[bold]Función EDO Original[/bold]",
        border_style="white",
        expand=False
    ))

def show_exact_solution_success(expr_str: str):
    """Muestra el panel verde cuando se encuentra solución exacta."""
    console.print("")
    console.print(Panel(
        f"[bold]y(x) = {expr_str}[/bold]",
        title="[bold green]Solución Analítica Encontrada[/bold green]",
        border_style="green",
        expand=False
    ))

def show_error(message: str):
    """Muestra un mensaje de error estandarizado."""
    console.print(f"[bold red]Error:[/bold red] {message}")

def show_info(message: str):
    """Muestra un mensaje de información/warning estandarizado."""
    console.print(f"[dim]{message}[/dim]")

def display_summary(x0: float, y0: float, x_final: float, h: float, func_str: str):
    """Muestra resumen de parámetros."""
    console.print("\n[bold underline]Resumen de Parámetros:[/bold underline]")
    console.print(f" • EDO: [bold]y' = {func_str}[/bold]")
    console.print(f" • Condición Inicial: y({x0}) = {y0}")
    console.print(f" • Intervalo: [{x0}, {x_final}]")
    console.print(f" • Paso (h): {h}")
    console.print(f" • Pasos estimados: {int((x_final - x0)/h)}")
    console.print("")

def display_results(sim_data: Dict[str, Any], h: float, decimals: int = 8):
    """
    Genera la tabla de resultados basada en los datos de simulation.py.
    """
    error = sim_data.get('error')
    if error:
        show_error(f"Error en simulación: {error}")
        return

    euler_points = sim_data.get('euler_points')
    heun_points = sim_data.get('heun_points')
    real_values = sim_data.get('exact_points')
    
    # Determinar título dinámico
    modes = []
    if euler_points: modes.append("Euler")
    if heun_points: modes.append("Heun")
    title = f"Resultados: {' & '.join(modes)} (h={h})"

    table = Table(title=title, show_header=True, header_style="bold", title_style="bold")
    
    # Columnas base
    table.add_column("Iter", justify="right", style="dim", no_wrap=True)
    table.add_column("x_i", justify="right")
    
    # Base list para iterar
    base_list = euler_points if euler_points else heun_points
    if not base_list:
        show_error("No hay datos generados.")
        return
        
    num_steps = len(base_list)

    # Columnas condicionales
    if real_values:
        table.add_column("Verdadero y(x)", justify="right", style="bold")

    if euler_points:
        table.add_column("Euler y_i", justify="right")
    if heun_points:
        table.add_column("Heun y_i", justify="right")
    
    if real_values:
        table.add_column("% Error", justify="right", style="red")

    # Llenado de filas
    for i in range(num_steps):
        x_val = base_list[i][0]
        row_data = [str(i), f"{x_val:.4f}"]
        
        approx_data = [] # Buffer para datos numéricos
        y_approx_for_error = 0.0 # Para calcular error (usa Euler si no hay Heun, o Heun si hay)

        # Exacta
        val_real = float('nan')
        if real_values:
            val_real = real_values[i]
            if math.isnan(val_real):
                row_data.append("N/A")
            else:
                row_data.append(f"{val_real:.{decimals}f}")

        # Euler
        if euler_points:
            y_eu = euler_points[i][1]
            approx_data.append(f"{y_eu:.{decimals}f}")
            if not heun_points: y_approx_for_error = y_eu

        # Heun
        if heun_points:
            y_imp = heun_points[i][1]
            approx_data.append(f"{y_imp:.{decimals}f}")
            y_approx_for_error = y_imp

        row_data.extend(approx_data)

        # Error Relativo
        if real_values:
            if not math.isnan(val_real):
                if abs(val_real) < 1e-12:
                    row_data.append("undef")
                else:
                    err = abs((val_real - y_approx_for_error) / val_real) * 100.0
                    row_data.append(f"{err:.4f}%")
            else:
                row_data.append("N/A")
        
        table.add_row(*row_data)
        
    console.print(table)

def get_main_menu_choice() -> str:
    """Muestra y captura opción del menú principal."""
    console.print("\n[bold]Seleccione el Método Numérico:[/bold]")
    console.print("1. Método de Euler")
    console.print("2. Euler Mejorado (Heun)")
    console.print("3. [red]Salir[/red]")
    return input("\nSeleccione una opción (1-3): ").strip()

def get_post_calc_choice() -> str:
    """Muestra y captura menú post-cálculo."""
    console.print("\n[bold]¿Qué desea hacer?[/bold]")
    console.print("1. Reintentar por Euler (Misma función, nuevos parámetros)")
    console.print("2. Reintentar por Heun (Misma función, nuevos parámetros)")
    console.print("3. Regresar al Menú Principal")
    console.print("4. [red]Salir de la Aplicación[/red]")
    return input("\nOpción: ").strip()

def print_separator():
    console.rule()

def show_status(message: str):
    return console.status(message)

def wait_for_enter():
    console.input("\n[dim]Presione <Enter> para continuar...[/dim]")
