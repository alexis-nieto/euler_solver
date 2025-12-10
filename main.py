"""
Módulo: main.py
Descripción: Punto de entrada principal de la aplicación.
Controla el flujo del programa, el menú principal y la orquestación de la resolución de EDOs.
"""

import sys
from rich.console import Console
from rich.panel import Panel

# Importación de módulos locales
# Asegura que el path sea correcto si se ejecuta desde el directorio
try:
    from function_parser import FunctionParserError, solve_exact_ode
    from numerical_methods import euler_method, improved_euler_method
    from input_handler import get_float, get_function_input, wait_for_enter
    from output_formatter import display_results_table, display_summary
except ImportError as e:
    print(f"Error crítico importando módulos: {e}")
    sys.exit(1)

console = Console()

def show_header():
    """Muestra el banner principal de la aplicación."""
    console.clear()
    console.print(Panel.fit(
        "[bold magenta]Solucionador Numérico de EDOs[/bold magenta]\n"
        "[dim]Métodos de Euler y Heun[/dim]",
        border_style="cyan"
    ))

def solve_single_method(initial_method: str):
    """
    Flujo de trabajo con capacidad de reintentos y cambio de método.
    initial_method: 'EULER' o 'HEUN'
    """
    current_method = initial_method
    
    console.print(f"\n[bold green]-- Nueva Resolución --[/bold green]")
    
    console.print("Ingrese la función f(x, y) para la EDO [bold]y' = f(x, y)[/bold]")
    f_func, f_str = get_function_input("f(x, y) = ")
    
    while True:
        # Mostrar qué método se está configurando
        method_name = "Método de Euler" if current_method == 'EULER' else "Euler Mejorado (Heun)"
        console.print(f"\n[bold magenta]Configuración para: {method_name}[/bold magenta]")
        
        # Bucle de parámetros
        t0 = get_float("Ingrese valor inicial x0: ")
        y0 = get_float("Ingrese valor inicial y0: ")
        tf = get_float("Ingrese valor final x_final: ", greater_than=t0)
        h = get_float("Ingrese tamaño de paso h: ", min_val=0.000001)
        
        display_summary(t0, y0, tf, h, f_str)
        
        try:
            euler_pts = None
            improved_pts = None
            
            with console.status(f"[bold green]Calculando ({current_method})...[/bold green]"):
                if current_method == 'EULER':
                    euler_pts = euler_method(f_func, t0, y0, h, tf)
                elif current_method == 'HEUN':
                    improved_pts = improved_euler_method(f_func, t0, y0, h, tf)
            
            # Intentar exacta
            real_values = None
            try:
                with console.status("[bold cyan]Buscando solución analítica...[/bold cyan]"):
                    result_exact = solve_exact_ode(f_str, t0, y0)
                    
                    if result_exact:
                        real_func, expr_str = result_exact
                        
                        # Mostrar la función estilizada en un Panel Verde
                        console.print(Panel(
                            f"[bold]y(x) = {expr_str}[/bold]",
                            title="[green]✔ Solución Analítica Encontrada[/green]",
                            border_style="green",
                            expand=False
                        ))

                        ref_pts = euler_pts if euler_pts else improved_pts
                        real_values = [real_func(p[0]) for p in ref_pts]
                    else:
                        console.print("[yellow]⚠ Sin solución analítica simple (omitendo errores).[/yellow]")
            except Exception:
                pass 
            # Mostrar tabla adaptada
            display_results_table(h, euler_points=euler_pts, improved_euler_points=improved_pts, real_values=real_values)
            
        except Exception as e:
            console.print(f"[bold red]Error de cálculo:[/bold red] {e}")
            
        # Menú Post-Cálculo Avanzado
        console.print("\n[bold]¿Qué desea hacer?[/bold]")
        console.print("1. [cyan]Reintentar por Euler[/cyan] (Misma función, nuevos parámetros)")
        console.print("2. [blue]Reintentar por Heun[/blue] (Misma función, nuevos parámetros)")
        console.print("3. [yellow]Regresar al Menú Principal[/yellow]")
        console.print("4. [red]Salir de la Aplicación[/red]")
        
        choice = input("\nOpción: ").strip()
        
        if choice == "1":
            current_method = 'EULER'
            continue 
        elif choice == "2":
            current_method = 'HEUN'
            continue
        elif choice == "3":
            break 
        elif choice == "4":
            console.print("[yellow]Saliendo...[/yellow]")
            sys.exit(0)
        else:
            console.print("[red]Opción no válida, regresando al menú principal por seguridad.[/red]")
            break

def main_menu():
    """Bucle del menú principal."""
    while True:
        show_header()
        console.print("\n[bold]Seleccione el Método Numérico:[/bold]")
        console.print("1. [green]Método de Euler[/green]")
        console.print("2. [blue]Euler Mejorado (Heun)[/blue]")
        console.print("3. [red]Salir[/red]")
        
        choice = input("\nSeleccione una opción (1-3): ").strip()
        
        if choice == "1":
            solve_single_method('EULER')
        elif choice == "2":
            solve_single_method('HEUN')
        elif choice == "3":
            console.print("[yellow]Saliendo... ¡Hasta luego![/yellow]")
            sys.exit(0)
        else:
            console.print("[bold red]Opción no válida.[/bold red]")
            wait_for_enter()

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupción de usuario detectada. Saliendo...[/yellow]")
        sys.exit(0)
