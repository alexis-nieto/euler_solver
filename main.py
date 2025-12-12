"""
Módulo: main.py
Descripción: Controlador principal de la aplicación.
Orquesta la interacción entre Interface, InputHandler y Simulation.
"""

import sys
from input_handler import get_float, get_int, get_function_input
import interface
import simulation
import plotting
from rich.console import Console
console = Console()

def run_solver_flow(initial_method: str):
    """Flujo de resolución de EDO: Input -> Simulación -> Resultados."""
    current_method = initial_method
    
    interface.print_separator()
    console.print("")
    interface.show_info("### Nueva Función ###")
    console.print("")
    
    # 1. Obtener Función
    print("Ingrese la función f(x, y) para la EDO y' = f(x, y)")
    f_func, f_str = get_function_input("f(x, y) = ")
    
    while True:
        # 2. Configurar Parámetros
        interface.show_info(f"\nConfiguración para: {current_method}")
        
        t0 = get_float("Ingrese valor inicial x_0")
        y0 = get_float("Ingrese valor inicial y_0")
        tf = get_float("Ingrese valor final x_final", greater_than=t0)
        h = get_float("Ingrese tamaño de paso h", min_val=0.000001)
        corrector_iterations = 1
        if current_method == 'HEUN':
            corrector_iterations = get_int("Número de iteraciones del corrector (Heun), default -> ", min_val=1, max_val=100, default=1)
        decimals = get_int("Cifras significativas, default -> ", min_val=0, max_val=20, default=8)

        console.print("")
        interface.print_separator()

        # 3. Mostrar Resumen Previo
        interface.show_function_panel(f_str)
        
        # 4. Ejecutar Simulación
        with interface.show_status(f"[bold]Calculando ({current_method})...[/bold]"):
            results = simulation.run_simulation(current_method, f_func, f_str, t0, y0, h, tf, corrector_iterations)
        
        # 5. Mostrar Resultados
        if results.get('exact_func_str'):
            interface.show_exact_solution_success(results['exact_func_str'])
        elif not results.get('error'):
             interface.show_info("Sin solución analítica simple (omitendo errores).")

        interface.display_results(results, h, decimals)
        interface.display_summary(t0, y0, tf, h, f_str)
        
        interface.print_separator()

        # 6. Menú Post-Cálculo
        while True:
            choice = interface.get_post_calc_choice()
            
            if choice == "1":
                current_method = 'EULER'
                break
            elif choice == "2":
                current_method = 'HEUN'
                break
            elif choice == "3":
                try:
                    plotting.plot_results(results, f_func, t0, y0, tf, f_str)
                except Exception as e:
                    interface.show_error(f"Error al graficar: {e}")
                interface.wait_for_enter()
            elif choice == "4":
                try:
                    plotting.plot_error_comparison(results, t0, f_str)
                except Exception as e:
                    interface.show_error(f"Error al graficar errores: {e}")
                interface.wait_for_enter()
            elif choice == "5":
                return # Volver al menú principal
            elif choice == "6":
                interface.show_info("Saliendo...")
                sys.exit(0)
            else:
                interface.show_error("Opción no válida.")

def main():
    """Bucle principal de la aplicación."""
    while True:
        interface.show_header()
        choice = interface.get_main_menu_choice()
        
        if choice == "1":
            run_solver_flow('EULER')
        elif choice == "2":
            run_solver_flow('HEUN')
        elif choice == "3":
            interface.show_info("Saliendo... ¡Hasta luego!")
            sys.exit(0)
        else:
            interface.show_error("Opción no válida.")
            interface.wait_for_enter()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n")
        interface.show_info("Interrupción de usuario detectada. Saliendo...")
        sys.exit(0)
    except Exception as e:
        print(f"Error crítico: {e}")
        sys.exit(1)
