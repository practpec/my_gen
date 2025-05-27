"""
Controlador para manejar ejercicios configurables
"""

from typing import Optional, Callable, Dict, Any
from tkinter import messagebox

# Importaciones absolutas
from config.exercises import ExerciseManager, ExerciseConfig
from application.use_cases.run_exercise_genetic_algorithm import RunExerciseGeneticAlgorithm, ExerciseResult
from domain.entities.ga_parameters import GAParameters


class ExerciseController:
    """Controlador para ejercicios de algoritmos genéticos"""
    
    def __init__(self, initial_exercise: str = 'julio_cesar'):
        self.current_exercise_key = initial_exercise
        self.exercise_use_case = RunExerciseGeneticAlgorithm(initial_exercise)
        self.current_result: Optional[ExerciseResult] = None
        self.view = None
    
    def set_view(self, view):
        """Establece referencia a la vista"""
        self.view = view
    
    def get_available_exercises(self) -> Dict[str, str]:
        """Ejercicios disponibles"""
        return ExerciseManager.list_exercises()
    
    def get_current_exercise_info(self) -> dict:
        """Información del ejercicio actual"""
        return self.exercise_use_case.get_exercise_info()
    
    def change_exercise(self, exercise_key: str) -> bool:
        """Cambia a un ejercicio diferente"""
        try:
            self.current_exercise_key = exercise_key
            self.exercise_use_case.change_exercise(exercise_key)
            self.current_result = None
            if self.view:
                self.view.clear_visualization()
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Error al cambiar ejercicio: {str(e)}")
            return False
    
    def get_default_parameters(self) -> dict:
        """Parámetros por defecto del ejercicio"""
        config = self.exercise_use_case.exercise_config
        return {
            'x_min': config.x_min,
            'x_max': config.x_max,
            'delta_x': config.precision,
            'population_size': config.default_population_size,
            'num_generations': config.default_generations,
            'crossover_probability': config.default_crossover_prob,
            'mutation_x_probability': config.default_mutation_prob,
            'mutation_g_probability': config.default_mutation_prob
        }
    
    def validate_parameters(self, params_dict: dict) -> Optional[GAParameters]:
        """Valida y crea parámetros"""
        try:
            parameters = GAParameters(
                x_min=params_dict['x_min'],
                x_max=params_dict['x_max'],
                delta_x=params_dict['delta_x'],
                population_size=params_dict['population_size'],
                num_generations=params_dict['num_generations'],
                crossover_probability=params_dict['crossover_probability'],
                mutation_x_probability=params_dict['mutation_x_probability'],
                mutation_g_probability=params_dict['mutation_g_probability']
            )
            return parameters
        except ValueError as e:
            messagebox.showerror("Error de Validación", str(e))
            return None
    
    def calculate_derived_parameters(self, x_min: float, x_max: float, delta_x: float) -> dict:
        """Calcula parámetros derivados"""
        try:
            temp_params = GAParameters(
                x_min=x_min, x_max=x_max, delta_x=delta_x,
                population_size=10, num_generations=10,
                crossover_probability=0.9, mutation_x_probability=0.1, mutation_g_probability=0.1
            )
            
            return {
                'num_bits': temp_params.calculate_num_bits(),
                'max_decimal': temp_params.calculate_max_decimal(),
                'num_points': temp_params.calculate_num_points(),
                'actual_precision': temp_params.calculate_actual_precision()
            }
        except:
            return {
                'num_bits': '...',
                'max_decimal': '...',
                'num_points': '...',
                'actual_precision': '...'
            }
    
    def execute_genetic_algorithm(
        self, 
        params_dict: dict, 
        progress_callback: Optional[Callable] = None
    ) -> bool:
        """Ejecuta el algoritmo genético"""
        
        parameters = self.validate_parameters(params_dict)
        if not parameters:
            return False
        
        try:
            self.current_result = self.exercise_use_case.execute(
                custom_parameters=parameters,
                progress_callback=progress_callback
            )
            return True
            
        except Exception as e:
            messagebox.showerror("Error", f"Error durante la ejecución: {str(e)}")
            return False
    
    def get_algorithm_result(self) -> Optional[ExerciseResult]:
        """Resultado actual"""
        return self.current_result
    
    def has_results(self) -> bool:
        """Verifica si hay resultados"""
        return self.current_result is not None
    
    def generate_report(self, filename: str) -> bool:
        """Genera reporte"""
        if not self.current_result:
            messagebox.showwarning("Advertencia", "No hay resultados para generar el reporte.")
            return False
        
        try:
            # Aquí iría la generación del reporte
            # Por ahora solo simulamos
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("REPORTE DEL EJERCICIO\n")
                f.write("=" * 50 + "\n")
                f.write(f"Estudiante: {self.current_result.exercise_config.student_name}\n")
                f.write(f"Función: {self.current_result.exercise_config.function_expression}\n")
                f.write(f"Mejor resultado: x = {self.current_result.best_x:.6f}\n")
                f.write(f"Valor objetivo: {self.current_result.get_display_result():.6f}\n")
            
            messagebox.showinfo("Éxito", f"Reporte generado: {filename}")
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar reporte: {str(e)}")
            return False
    
    def clear_results(self):
        """Limpia resultados"""
        self.current_result = None
        if self.view:
            self.view.clear_visualization()
        messagebox.showinfo("Completado", "Resultados limpiados.")
    
    def get_strategy_summary(self) -> dict:
        """Resumen de estrategias"""
        config = self.exercise_use_case.exercise_config
        return {
            'emparejamiento': config.pairing_strategy,
            'cruzamiento': config.crossover_strategy,
            'mutacion': config.mutation_strategy,
            'seleccion': config.selection_strategy,
            'parametros': config.strategy_params
        }
    
    def get_function_info(self) -> dict:
        """Información de función objetivo"""
        config = self.exercise_use_case.exercise_config
        return {
            'expression': config.function_expression,
            'description': config.function_description,
            'objective_type': config.objective_type,
            'interval': f"[{config.x_min}, {config.x_max}]",
            'precision': config.precision
        }