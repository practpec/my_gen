#!/usr/bin/env python3
"""
Punto de entrada principal - Algoritmo Genético Configurable
"""

import sys
import os

# Agregar el directorio actual al path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Importaciones absolutas
from presentation.controllers.exercise_controller import ExerciseController
from presentation.views.main_window_simplified import MainWindowSimplified


def main():
    """Función principal"""
    try:
        # Crear controlador con ejercicio de Julio César por defecto
        controller = ExerciseController(initial_exercise='julio_cesar')
        
        # Crear ventana principal
        main_window = MainWindowSimplified(controller)
        controller.set_view(main_window)
        
        # Ejecutar aplicación
        main_window.run()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()