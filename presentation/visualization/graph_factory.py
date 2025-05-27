"""
Factory para crear gráficas mejoradas
"""

from matplotlib.figure import Figure
from typing import Optional
import numpy as np

# IMPORTACIÓN ABSOLUTA CORREGIDA
from infrastructure.genetic_operations.exercise_specific_functions import FunctionFactory


class GraphFactory:
    """Factory para crear gráficas"""
    
    def create_graph(self, graph_type: str, result) -> Optional[Figure]:
        """Crea gráfica del tipo especificado"""
        
        if graph_type == "objective_population":
            return self.create_objective_with_population(result)
        elif graph_type == "evolution_best":
            return self.create_evolution_best(result)
        elif graph_type == "evolution_all":
            return self.create_evolution_all(result)
        else:
            return None
    
    def create_objective_with_population(self, result) -> Figure:
        """Gráfica de función objetivo con población completa"""
        figure = Figure(figsize=(12, 8), dpi=100)
        ax = figure.add_subplot(111)
        
        # Obtener función objetivo
        objective_function = FunctionFactory.create_from_exercise_config(result.exercise_config)
        
        # Generar puntos para la función
        x_min = result.exercise_config.x_min
        x_max = result.exercise_config.x_max
        x_vals = np.linspace(x_min, x_max, 1000)
        
        # Evaluar función (valores originales)
        y_vals = [objective_function.evaluate_original(x) for x in x_vals]
        
        # Filtrar valores infinitos
        finite_mask = np.isfinite(y_vals)
        x_finite = x_vals[finite_mask]
        y_finite = np.array(y_vals)[finite_mask]
        
        # Plotear función
        ax.plot(x_finite, y_finite, 'b-', linewidth=2, alpha=0.7,
                label=f'f(x) = {objective_function.get_name()}')
        
        # Población final
        final_population = result.final_population
        population_x = []
        population_y = []
        population_fitness = []
        
        for individual in final_population.individuals:
            x_val = individual.to_decimal(x_min, x_max)
            y_val = objective_function.evaluate_original(x_val)
            
            population_x.append(x_val)
            population_y.append(y_val)
            population_fitness.append(individual.fitness)
        
        # Encontrar mejor y peor según el tipo de optimización
        if result.is_minimization:
            # Para minimización: mejor fitness es el más alto (menos negativo)
            # pero mejor valor real es el más bajo
            best_idx = np.argmax(population_fitness)  
            worst_idx = np.argmin(population_fitness)
        else:
            # Para maximización: mejor fitness es el más alto
            # y mejor valor real también es el más alto
            best_idx = np.argmax(population_fitness)
            worst_idx = np.argmin(population_fitness)
        
        # Verificar que los índices sean diferentes
        if best_idx == worst_idx and len(population_fitness) > 1:
            # Si son iguales, encontrar el segundo mejor/peor
            sorted_indices = np.argsort(population_fitness)
            if result.is_minimization:
                worst_idx = sorted_indices[0] if sorted_indices[0] != best_idx else sorted_indices[1]
            else:
                worst_idx = sorted_indices[0] if sorted_indices[0] != best_idx else sorted_indices[1]
        
        # Plotear población
        scatter = ax.scatter(population_x, population_y, 
                           c=population_fitness, cmap='viridis', 
                           s=80, alpha=0.8, edgecolors='black', linewidth=0.5,
                           label='Población final')
        
        # Colorbar
        cbar = figure.colorbar(scatter, ax=ax)
        cbar.set_label('Fitness (interno AG)', fontsize=12)
        
        # Resaltar mejor y peor
        best_x, best_y = population_x[best_idx], population_y[best_idx]
        worst_x, worst_y = population_x[worst_idx], population_y[worst_idx]
        
        ax.scatter([best_x], [best_y], color='red', s=200, marker='*', 
                  edgecolors='darkred', linewidth=2, zorder=10,
                  label=f'Mejor: x = {best_x:.4f}')
        
        ax.scatter([worst_x], [worst_y], color='orange', s=150, marker='v', 
                  edgecolors='darkorange', linewidth=2, zorder=10,
                  label=f'Peor: x = {worst_x:.4f}')
        
        # Configurar gráfica
        objective_word = "Minimización" if result.is_minimization else "Maximización"
        ax.set_xlabel('x', fontsize=14)
        ax.set_ylabel('f(x)', fontsize=14)
        ax.set_title(f'{objective_word} - Función Objetivo y Población Final', 
                    fontsize=16, fontweight='bold')
        ax.legend(fontsize=11, loc='best')
        ax.grid(True, alpha=0.3)
        
        # Estadísticas
        x_mean = np.mean(population_x)
        x_std = np.std(population_x)
        best_value = result.get_display_result()
        
        stats_text = f'{objective_word[0:3]} encontrado: {best_value:.6f}\n'
        stats_text += f'x̄ población: {x_mean:.4f} ± {x_std:.4f}\n'
        stats_text += f'Individuos: {len(population_x)}\n'
        stats_text += f'Diversidad: {x_std:.6f}'
        
        ax.text(0.02, 0.98, stats_text, 
               transform=ax.transAxes, fontsize=10, 
               verticalalignment='top', 
               bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
        
        figure.tight_layout()
        return figure
    
    def create_evolution_best(self, result) -> Figure:
        """Gráfica de evolución del mejor individuo"""
        figure = Figure(figsize=(12, 8), dpi=100)
        ax = figure.add_subplot(111)
        
        generations = range(len(result.best_fitness_history))
        
        # Valores reales para mostrar
        if result.is_minimization:
            display_values = [-x for x in result.best_fitness_history]
            objective_word = "Minimización"
        else:
            display_values = result.best_fitness_history
            objective_word = "Maximización"
        
        # Plotear evolución
        ax.plot(generations, display_values, 'g-', 
               linewidth=3, marker='o', markersize=4,
               label=f'Mejor Fitness ({objective_word})')
        
        # Resaltar mejoras
        threshold = abs(max(display_values) - min(display_values)) * 0.001
        
        for i in range(1, len(display_values)):
            if result.is_minimization:
                improvement = display_values[i-1] - display_values[i]
            else:
                improvement = display_values[i] - display_values[i-1]
            
            if improvement > threshold:
                ax.scatter(i, display_values[i], 
                          color='orange', s=80, zorder=5,
                          alpha=0.8)
        
        # Líneas de referencia
        ax.axhline(y=display_values[0], color='gray', 
                  linestyle=':', alpha=0.7, linewidth=2,
                  label=f'Inicial: {display_values[0]:.4f}')
        
        ax.axhline(y=display_values[-1], color='red', 
                  linestyle='--', alpha=0.7, linewidth=2,
                  label=f'Final: {display_values[-1]:.4f}')
        
        # Configurar
        ax.set_xlabel('Generación', fontsize=14)
        ax.set_ylabel('f(x)', fontsize=14)
        ax.set_title(f'Evolución del Mejor Individuo - {objective_word}', 
                    fontsize=16, fontweight='bold')
        ax.legend(fontsize=11)
        ax.grid(True, alpha=0.3)
        
        # Estadísticas
        total_improvement = abs(display_values[-1] - display_values[0])
        
        stats_text = f'Mejora total: {total_improvement:.6f}\n'
        stats_text += f'Resultado final: {result.get_display_result():.6f}'
        
        y_pos = 0.98 if result.is_minimization else 0.02
        ax.text(0.02, y_pos, stats_text, 
               transform=ax.transAxes, fontsize=11, 
               verticalalignment='top' if result.is_minimization else 'bottom',
               bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))
        
        figure.tight_layout()
        return figure
    
    def create_evolution_all(self, result) -> Figure:
        """Gráfica de evolución de toda la población"""
        figure = Figure(figsize=(12, 8), dpi=100)
        ax = figure.add_subplot(111)
        
        # Preparar datos
        all_x_values = []
        generation_numbers = []
        all_fitness_values = []
        
        for gen_idx, (population, fitness_scores) in enumerate(
            zip(result.population_history, result.fitness_history)
        ):
            for individual, fitness in zip(population.individuals, fitness_scores):
                x_val = individual.to_decimal(
                    result.parameters.x_min, 
                    result.parameters.x_max
                )
                all_x_values.append(x_val)
                generation_numbers.append(gen_idx)
                all_fitness_values.append(fitness)
        
        # Scatter plot
        scatter = ax.scatter(
            all_x_values, generation_numbers, 
            c=all_fitness_values, cmap='viridis', 
            alpha=0.6, s=30
        )
        
        # Colorbar
        cbar = figure.colorbar(scatter, ax=ax)
        cbar.set_label('Fitness', fontsize=12)
        
        # Trayectoria del mejor
        best_x_history = []
        for population, fitness_scores in zip(result.population_history, result.fitness_history):
            best_idx = fitness_scores.index(max(fitness_scores))
            best_individual = population.individuals[best_idx]
            best_x = best_individual.to_decimal(
                result.parameters.x_min, 
                result.parameters.x_max
            )
            best_x_history.append(best_x)
        
        ax.plot(best_x_history, range(len(best_x_history)), 
               'r-', linewidth=3, alpha=0.8, label='Trayectoria del mejor')
        
        # Marcar resultado final
        ax.scatter([result.best_x], [len(best_x_history) - 1],
                  color='red', s=150, marker='*', zorder=10,
                  label=f'Mejor final: x={result.best_x:.3f}')
        
        # Configurar
        ax.set_xlabel('x', fontsize=14)
        ax.set_ylabel('Generación', fontsize=14)
        ax.set_title('Evolución de Toda la Población', fontsize=16, fontweight='bold')
        ax.legend(fontsize=11)
        ax.grid(True, alpha=0.3)
        ax.invert_yaxis()
        
        figure.tight_layout()
        return figure