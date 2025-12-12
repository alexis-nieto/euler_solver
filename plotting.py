"""
Módulo: plotting.py
Descripción: Visualización de resultados numéricos mediante gráficos.
Genera gráficas comparativas de métodos numéricos vs solución exacta.
"""

import matplotlib.pyplot as plt
import numpy as np
from typing import Callable, List, Tuple, Optional, Dict, Any
from rich.console import Console

console = Console()


def plot_results(sim_data: Dict[str, Any], 
                func: Callable[[float, float], float],
                x0: float,
                y0: float,
                x_end: float,
                func_str: str) -> None:
    """
    Genera un gráfico comparativo de los resultados numéricos.
    
    Args:
        sim_data: Diccionario con resultados de la simulación
        func: Función f(x, y) de la EDO
        x0: Valor inicial de x
        y0: Valor inicial de y
        x_end: Valor final de x
        func_str: String representando la función EDO
    """
    euler_points = sim_data.get('euler_points')
    heun_points = sim_data.get('heun_points')
    heun_points_iterated = sim_data.get('heun_points_iterated')
    exact_points = sim_data.get('exact_points')
    exact_func_str = sim_data.get('exact_func_str')
    
    # Verificar que hay datos para graficar
    if not euler_points and not heun_points:
        console.print("[bold red]Error:[/bold red] No hay datos para graficar")
        return
    
    # Crear figura
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Obtener puntos base para x
    base_points = euler_points if euler_points else heun_points
    x_vals = [p[0] for p in base_points]
    
    # Graficar Euler si existe
    if euler_points:
        y_euler = [p[1] for p in euler_points]
        ax.plot(x_vals, y_euler, 'o-', label='Euler', linewidth=2, markersize=5, alpha=0.7)
    
    # Graficar Heun si existe
    if heun_points:
        y_heun = [p[1] for p in heun_points]
        ax.plot(x_vals, y_heun, 's-', label='Heun (1 iteración)', linewidth=2, markersize=5, alpha=0.7)
    
    # Graficar Heun iterado si existe
    if heun_points_iterated:
        y_heun_iter = [p[1] for p in heun_points_iterated]
        ax.plot(x_vals, y_heun_iter, '^-', label='Heun Iterado', linewidth=2, markersize=5, alpha=0.7)
    
    # Graficar solución exacta si existe
    if exact_points and exact_func_str:
        # Crear array denso de puntos x para gráfica suave de la exacta
        x_dense = np.linspace(x0, x_end, 500)
        try:
            from function_parser import solve_exact_ode
            exact_res = solve_exact_ode(func_str, x0, y0)
            if exact_res:
                real_func, _ = exact_res
                y_exact = [real_func(x) for x in x_dense]
                ax.plot(x_dense, y_exact, 'r-', label=f'Exacta: {exact_func_str}', linewidth=2.5, alpha=0.8)
        except Exception as e:
            console.print(f"[dim]Nota: No se pudo graficar solución exacta ({e})[/dim]")
    
    # Configuración de la gráfica
    ax.set_xlabel('x', fontsize=12, fontweight='bold')
    ax.set_ylabel('y(x)', fontsize=12, fontweight='bold')
    ax.set_title(f'Solución de EDO: y\' = {func_str}', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend(fontsize=10, loc='best')
    
    # Ajustar layout
    plt.tight_layout()
    
    # Mostrar gráfica
    try:
        plt.show()
    except Exception as e:
        console.print(f"[bold red]Error al mostrar gráfica:[/bold red] {e}")
        console.print("[dim]Intenta ejecutar desde un entorno con soporte gráfico[/dim]")


def plot_error_comparison(sim_data: Dict[str, Any],
                         x0: float,
                         func_str: str) -> None:
    """
    Genera un gráfico comparativo de errores relativos porcentuales.
    Solo funciona cuando existe solución exacta.
    
    Args:
        sim_data: Diccionario con resultados de la simulación
        x0: Valor inicial de x
        func_str: String representando la función EDO
    """
    euler_points = sim_data.get('euler_points')
    heun_points = sim_data.get('heun_points')
    heun_points_iterated = sim_data.get('heun_points_iterated')
    exact_points = sim_data.get('exact_points')
    
    # Verificar que hay datos y solución exacta
    if not exact_points:
        console.print("[dim]No se puede graficar errores: solución exacta no disponible[/dim]")
        return
    
    base_points = euler_points if euler_points else heun_points
    if not base_points:
        return
    
    x_vals = [p[0] for p in base_points]
    
    # Crear figura
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Calcular errores relativos porcentuales
    if euler_points:
        errors_euler = []
        for i, (x, y_euler) in enumerate(euler_points):
            y_exact = exact_points[i]
            if abs(y_exact) > 1e-12:
                err = abs((y_exact - y_euler) / y_exact) * 100.0
                errors_euler.append(err)
            else:
                errors_euler.append(0)
        ax.semilogy(x_vals, errors_euler, 'o-', label='Error Euler', linewidth=2, markersize=5)
    
    if heun_points:
        errors_heun = []
        for i, (x, y_heun) in enumerate(heun_points):
            y_exact = exact_points[i]
            if abs(y_exact) > 1e-12:
                err = abs((y_exact - y_heun) / y_exact) * 100.0
                errors_heun.append(err)
            else:
                errors_heun.append(0)
        ax.semilogy(x_vals, errors_heun, 's-', label='Error Heun', linewidth=2, markersize=5)
    
    if heun_points_iterated:
        errors_heun_iter = []
        for i, (x, y_iter) in enumerate(heun_points_iterated):
            y_exact = exact_points[i]
            if abs(y_exact) > 1e-12:
                err = abs((y_exact - y_iter) / y_exact) * 100.0
                errors_heun_iter.append(err)
            else:
                errors_heun_iter.append(0)
        ax.semilogy(x_vals, errors_heun_iter, '^-', label='Error Heun Iterado', linewidth=2, markersize=5)
    
    # Configuración
    ax.set_xlabel('x', fontsize=12, fontweight='bold')
    ax.set_ylabel('Error Relativo (%)', fontsize=12, fontweight='bold')
    ax.set_title(f'Errores Relativos: y\' = {func_str}', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3, linestyle='--', which='both')
    ax.legend(fontsize=10, loc='best')
    
    # Ajustar layout
    plt.tight_layout()
    
    # Mostrar gráfica
    try:
        plt.show()
    except Exception as e:
        console.print(f"[bold red]Error al mostrar gráfica:[/bold red] {e}")
        console.print("[dim]Intenta ejecutar desde un entorno con soporte gráfico[/dim]")
