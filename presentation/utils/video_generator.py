"""
Generador de videos de evolución del algoritmo genético
"""

import os
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from typing import Callable, Optional

# IMPORTACIÓN ABSOLUTA
from infrastructure.genetic_operations.exercise_specific_functions import FunctionFactory


class VideoGenerator:
    """Generador de videos de evolución"""
    
    def __init__(self):
        self.figure = None
        self.ax = None
        
    def create_evolution_video(
        self, 
        result, 
        output_dir: str, 
        progress_callback: Optional[Callable[[str], None]] = None,
        fps: int = 2
    ) -> str:
        """Crea video de la evolución del algoritmo genético"""
        
        try:
            if progress_callback:
                progress_callback("Inicializando generación de video...")
            
            # Configurar figura
            self.figure, self.ax = plt.subplots(figsize=(12, 8))
            
            # Obtener función objetivo
            objective_function = FunctionFactory.create_from_exercise_config(result.exercise_config)
            
            # Generar puntos para la función
            x_min = result.exercise_config.x_min
            x_max = result.exercise_config.x_max
            x_vals = np.linspace(x_min, x_max, 1000)
            y_vals = [objective_function.evaluate_original(x) for x in x_vals]
            
            # Filtrar valores infinitos
            finite_mask = np.isfinite(y_vals)
            x_finite = x_vals[finite_mask]
            y_finite = np.array(y_vals)[finite_mask]
            
            # Configurar límites del gráfico
            self.ax.set_xlim(x_min, x_max)
            self.ax.set_ylim(min(y_finite) * 1.1, max(y_finite) * 1.1)
            
            if progress_callback:
                progress_callback("Preparando frames de animación...")
            
            # Crear animación
            def animate(frame):
                self.ax.clear()
                
                # Plotear función objetivo
                self.ax.plot(x_finite, y_finite, 'b-', linewidth=2, alpha=0.7,
                           label=f'f(x) = {objective_function.get_name()}')
                
                # Obtener población de esta generación
                if frame < len(result.population_history):
                    population = result.population_history[frame]
                    
                    # Calcular posiciones x y valores y
                    population_x = []
                    population_y = []
                    population_fitness = []
                    
                    for individual in population.individuals:
                        x_val = individual.to_decimal(x_min, x_max)
                        y_val = objective_function.evaluate_original(x_val)
                        
                        population_x.append(x_val)
                        population_y.append(y_val)
                        population_fitness.append(individual.fitness)
                    
                    # Plotear población
                    scatter = self.ax.scatter(population_x, population_y, 
                                            c=population_fitness, cmap='viridis', 
                                            s=80, alpha=0.8, edgecolors='black', linewidth=0.5)
                    
                    # Resaltar mejor individuo
                    if result.is_minimization:
                        best_idx = np.argmax(population_fitness)
                    else:
                        best_idx = np.argmax(population_fitness)
                    
                    best_x, best_y = population_x[best_idx], population_y[best_idx]
                    self.ax.scatter([best_x], [best_y], color='red', s=200, marker='*', 
                                  edgecolors='darkred', linewidth=2, zorder=10)
                
                # Configurar gráfico
                objective_word = "Minimización" if result.is_minimization else "Maximización"
                self.ax.set_xlabel('x', fontsize=14)
                self.ax.set_ylabel('f(x)', fontsize=14)
                self.ax.set_title(f'{objective_word} - Generación {frame}', 
                                fontsize=16, fontweight='bold')
                self.ax.legend()
                self.ax.grid(True, alpha=0.3)
                
                return []
            
            # Crear animación
            num_frames = len(result.population_history)
            anim = animation.FuncAnimation(
                self.figure, animate, frames=num_frames,
                interval=1000//fps, blit=False, repeat=True
            )
            
            if progress_callback:
                progress_callback("Guardando video...")
            
            # Guardar video
            student_name = result.exercise_config.student_name.replace(" ", "_")
            video_filename = f"evolution_{student_name}.mp4"
            video_path = os.path.join(output_dir, video_filename)
            
            # Usar writer disponible
            try:
                writer = animation.FFMpegWriter(fps=fps, metadata=dict(artist='GA-App'), bitrate=1800)
                anim.save(video_path, writer=writer)
            except Exception:
                # Fallback a pillow
                try:
                    writer = animation.PillowWriter(fps=fps)
                    gif_path = os.path.join(output_dir, f"evolution_{student_name}.gif")
                    anim.save(gif_path, writer=writer)
                    video_path = gif_path
                except Exception as e:
                    print(f"Error guardando animación: {e}")
                    return None
            
            if progress_callback:
                progress_callback("¡Video generado exitosamente!")
            
            # Limpiar
            plt.close(self.figure)
            
            return video_path
            
        except Exception as e:
            print(f"Error generando video: {e}")
            if self.figure:
                plt.close(self.figure)
            return None