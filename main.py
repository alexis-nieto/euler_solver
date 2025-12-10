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
    from function_parser import FunctionParserError
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
        "[dim]Métodos de Euler y Euler Mejorado[/dim]",
        border_style="cyan"
    ))

def solve_ode_workflow():
    """Flujo de trabajo para solicitar datos y resolver una EDO."""
    console.print("\n[bold green]-- Nueva Resolución --[/bold green]")
    
    # 1. Obtener la función EDO
    console.print("Ingrese la función f(x, y) para la EDO [bold]y' = f(x, y)[/bold]")
    f_func, f_str = get_function_input("f(x, y) = ")
    
    # 2. Obtener condiciones iniciales y rangos
    t0 = get_float("Ingrese valor inicial x0: ")
    y0 = get_float("Ingrese valor inicial y0: ")
    tf = get_float("Ingrese valor final x_final: ", greater_than=t0)
    h = get_float("Ingrese tamaño de paso h: ", min_val=0.000001) # Evitar h=0 o negativo
    
    # 3. Mostrar resumen
    display_summary(t0, y0, tf, h, f_str)
    
    # 4. Calcular soluciones
    try:
        with console.status("[bold green]Calculando soluciones...[/bold green]"):
            euler_pts = euler_method(f_func, t0, y0, h, tf)
            improved_pts = improved_euler_method(f_func, t0, y0, h, tf)
            
        # 5. Mostrar resultados
        display_results_table(euler_pts, improved_pts, h)
        
    except Exception as e:
        console.print(f"[bold red]Error durante el cálculo:[/bold red] {e}")
    
    wait_for_enter()

def main_menu():
    """Bucle del menú principal."""
    while True:
        show_header()
        console.print("\n[bold]Opciones:[/bold]")
        console.print("1. [green]Resolver EDO[/green]")
        console.print("2. [red]Salir[/red]")
        
        choice = input("\nSeleccione una opción (1-2): ").strip()
        
        if choice == "1":
            solve_ode_workflow()
        elif choice == "2":
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
