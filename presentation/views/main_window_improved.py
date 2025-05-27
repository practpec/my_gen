"""
Ventana principal mejorada con diseño de tres secciones
"""

import tkinter as tk
from tkinter import filedialog
from typing import Optional

# IMPORTACIONES ABSOLUTAS (SIN ... ni ..)
from presentation.components.parameter_input import ParameterInputPanel
from presentation.components.progress_dialog import ProgressDialog
from presentation.components.excercise_selector import ExerciseSelector
from presentation.visualization.graph_factory import GraphFactory


class MainWindowImproved:
    """Ventana principal con diseño de tres secciones"""
    
    def __init__(self, controller):
        self.controller = controller
        self.root = tk.Tk()
        self.setup_window()
        
        # Referencias
        self.parameter_panel = None
        self.exercise_selector = None
        self.graph_factory = GraphFactory()
        self.current_canvas = None
        self.current_figure = None
        self.graph_buttons = []
        
        # Labels de información
        self.info_labels = {}
        self.result_labels = {}
        self.strategy_text = None
        self.population_text = None
        
        self.create_interface()
        self.update_exercise_display()
    
    def setup_window(self):
        """Configura ventana principal"""
        self.root.title("Algoritmo Genético - Julio César Pérez Ortiz")
        self.root.geometry("1600x900")
        self.root.configure(bg='#f0f0f0')
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
    
    def create_interface(self):
        """Crea interfaz de tres secciones"""
        
        # SECCIÓN SUPERIOR (30% altura)
        top_section = tk.Frame(self.root, bg='#f0f0f0', height=270)
        top_section.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        top_section.grid_propagate(False)
        
        # SECCIÓN INFERIOR (70% altura)
        bottom_section = tk.Frame(self.root, bg='#f0f0f0')
        bottom_section.grid(row=1, column=0, sticky="nsew", padx=10, pady=(5, 10))
        bottom_section.grid_columnconfigure(1, weight=2)
        bottom_section.grid_rowconfigure(0, weight=1)
        
        self.create_top_section(top_section)
        self.create_bottom_left_section(bottom_section)
        self.create_bottom_right_section(bottom_section)
    
    def create_top_section(self, parent):
        """Sección superior con controles"""
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=1)
        
        # Izquierda: Selector de ejercicio
        left_frame = tk.Frame(parent, bg='white', relief='raised', bd=2)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        
        # Derecha: Parámetros
        right_frame = tk.Frame(parent, bg='white', relief='raised', bd=2)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        
        self.create_exercise_section(left_frame)
        self.create_parameters_section(right_frame)
    
    def create_exercise_section(self, parent):
        """Sección de ejercicio"""
        # Título
        title_label = tk.Label(parent, text="Ejercicio Configurado", 
                              font=("Arial", 14, "bold"), bg='white')
        title_label.pack(pady=10)
        
        # Selector de ejercicio
        self.exercise_selector = ExerciseSelector(
            parent, 
            self.controller, 
            self.on_exercise_changed
        )
        
        # Información actual
        self.create_current_exercise_info(parent)
    
    def create_current_exercise_info(self, parent):
        """Información del ejercicio actual"""
        info_frame = tk.LabelFrame(parent, text="Ejercicio Actual", 
                                  font=("Arial", 11, "bold"), bg='white')
        info_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        info_items = [
            ("Estudiante:", "student"),
            ("Función:", "function"),
            ("Intervalo:", "interval"),
            ("Objetivo:", "objective")
        ]
        
        for i, (label_text, key) in enumerate(info_items):
            tk.Label(info_frame, text=label_text, bg='white', 
                    font=("Arial", 9, "bold")).grid(row=i, column=0, sticky="w", padx=5, pady=2)
            
            value_label = tk.Label(info_frame, text="...", bg='white', 
                                 font=("Arial", 9), wraplength=180, justify="left")
            value_label.grid(row=i, column=1, sticky="w", padx=5, pady=2)
            
            self.info_labels[key] = value_label
    
    def create_parameters_section(self, parent):
        """Sección de parámetros"""
        self.parameter_panel = ParameterInputPanel(
            parent, 
            self.controller,
            self.on_execute_algorithm
        )
    
    def create_bottom_left_section(self, parent):
        """Sección inferior izquierda - información"""
        info_panel = tk.Frame(parent, bg='white', relief='raised', bd=2, width=500)
        info_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        info_panel.grid_propagate(False)
        
        # Título
        title_label = tk.Label(info_panel, text="Información y Resultados", 
                              font=("Arial", 14, "bold"), bg='white')
        title_label.pack(pady=10)
        
        self.create_results_section(info_panel)
        self.create_strategies_section(info_panel)
        self.create_population_section(info_panel)
        self.create_action_buttons(info_panel)
    
    def create_results_section(self, parent):
        """Sección de resultados principales"""
        results_frame = tk.LabelFrame(parent, text="Resultados Principales", 
                                     font=("Arial", 11, "bold"), bg='white')
        results_frame.pack(fill="x", padx=10, pady=5)
        
        result_items = [
            ("Mejor x:", "best_x"),
            ("Mejor f(x):", "best_fitness"),
            ("Generación:", "best_generation"),
            ("Evaluaciones:", "total_evaluations"),
            ("Mejora:", "improvement"),
            ("Estado:", "status")
        ]
        
        self.result_labels = {}
        for i, (label_text, key) in enumerate(result_items):
            row = i // 2
            col = (i % 2) * 2
            
            tk.Label(results_frame, text=label_text, bg='white', 
                    font=("Arial", 9, "bold")).grid(row=row, column=col, sticky="w", padx=5, pady=2)
            
            value_label = tk.Label(results_frame, text="--", bg='white', 
                                 font=("Arial", 9), fg='#333333')
            value_label.grid(row=row, column=col+1, sticky="w", padx=5, pady=2)
            
            self.result_labels[key] = value_label
    
    def create_strategies_section(self, parent):
        """Sección de estrategias"""
        strategy_frame = tk.LabelFrame(parent, text="Estrategias Utilizadas", 
                                      font=("Arial", 11, "bold"), bg='white')
        strategy_frame.pack(fill="x", padx=10, pady=5)
        
        self.strategy_text = tk.Text(strategy_frame, height=6, width=50, 
                                   bg='#f8f8f8', font=("Arial", 8),
                                   state='disabled')
        self.strategy_text.pack(pady=5, padx=5, fill="x")
    
    def create_population_section(self, parent):
        """Sección de análisis de población"""
        pop_frame = tk.LabelFrame(parent, text="Análisis de Población", 
                                 font=("Arial", 11, "bold"), bg='white')
        pop_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.population_text = tk.Text(pop_frame, height=8, width=50, 
                                     bg='#f8f8f8', font=("Arial", 8),
                                     state='disabled')
        self.population_text.pack(pady=5, padx=5, fill="both", expand=True)
    
    def create_action_buttons(self, parent):
        """Botones de acciones"""
        actions_frame = tk.Frame(parent, bg='white')
        actions_frame.pack(fill="x", padx=10, pady=10)
        
        self.report_btn = tk.Button(actions_frame, text="Generar Reporte", 
                                   command=self.generate_report,
                                   bg='#FF9800', fg='white', 
                                   font=("Arial", 10, "bold"),
                                   height=1, state="disabled")
        self.report_btn.pack(fill="x", pady=2)
        
        clear_btn = tk.Button(actions_frame, text="Limpiar Resultados", 
                             command=self.clear_results,
                             bg='#f44336', fg='white', 
                             font=("Arial", 10, "bold"),
                             height=1)
        clear_btn.pack(fill="x", pady=2)
    
    def create_bottom_right_section(self, parent):
        """Sección inferior derecha - gráficas"""
        graph_panel = tk.Frame(parent, bg='white', relief='raised', bd=2)
        graph_panel.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        graph_panel.grid_rowconfigure(1, weight=1)
        graph_panel.grid_columnconfigure(0, weight=1)
        
        self.create_graph_controls(graph_panel)
        
        # Área de gráficas
        self.graph_container = tk.Frame(graph_panel, bg='white', relief='sunken', bd=2)
        self.graph_container.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        self.create_welcome_graph_message()
    
    def create_graph_controls(self, parent):
        """Controles de gráficas"""
        controls_frame = tk.Frame(parent, bg='white')
        controls_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        
        tk.Label(controls_frame, text="Visualizaciones", 
                font=("Arial", 14, "bold"), bg='white').pack()
        
        buttons_frame = tk.Frame(controls_frame, bg='white')
        buttons_frame.pack(pady=10)
        
        graph_types = [
            ("Función y Población", "objective_population"),
            ("Evolución Mejor", "evolution_best"),
            ("Evolución Población", "evolution_all")
        ]
        
        for text, value in graph_types:
            btn = tk.Button(buttons_frame, text=text, 
                           command=lambda v=value: self.show_graph(v),
                           bg='white', relief='raised', bd=2,
                           font=("Arial", 10), width=15,
                           state="disabled")
            btn.pack(side="left", padx=5)
            self.graph_buttons.append(btn)
    
    def create_welcome_graph_message(self):
        """Mensaje de bienvenida en gráficas"""
        welcome_frame = tk.Frame(self.graph_container, bg='white')
        welcome_frame.pack(expand=True)
        
        welcome_text = """
        Visualizaciones del Algoritmo Genético
        
        1. Configure los parámetros
        2. Ejecute el algoritmo
        3. Seleccione una visualización
        
        Las gráficas mostrarán:
        • Función objetivo con población final
        • Evolución del mejor individuo
        • Evolución de toda la población
        """
        
        tk.Label(welcome_frame, text=welcome_text, 
                font=("Arial", 12), bg='white',
                justify="center", fg='#666666').pack(expand=True)
    
    def on_exercise_changed(self, exercise_key: str) -> bool:
        """Callback al cambiar ejercicio"""
        success = self.controller.change_exercise(exercise_key)
        if success:
            self.update_exercise_display()
            self.clear_results_display()
            self.update_parameters_from_exercise()
        return success
    
    def update_exercise_display(self):
        """Actualiza información del ejercicio"""
        try:
            info = self.controller.get_current_exercise_info()
            
            self.info_labels['student'].config(text=f"{info['student_name']} ({info['student_id']})")
            self.info_labels['function'].config(text=info['function'])
            self.info_labels['interval'].config(text=info['interval'])
            self.info_labels['objective'].config(text=info['objective'].upper())
            
            self.update_strategies_display()
            
        except Exception as e:
            print(f"Error actualizando display: {e}")
    
    def update_strategies_display(self):
        """Actualiza información de estrategias"""
        try:
            strategies = self.controller.get_strategy_summary()
            
            self.strategy_text.config(state='normal')
            self.strategy_text.delete(1.0, tk.END)
            
            strategy_text = "ESTRATEGIAS CONFIGURADAS:\n\n"
            strategy_text += f"• Emparejamiento: {strategies['emparejamiento']}\n"
            strategy_text += f"• Cruzamiento: {strategies['cruzamiento']}\n"
            strategy_text += f"• Mutación: {strategies['mutacion']}\n"
            strategy_text += f"• Selección: {strategies['seleccion']}\n\n"
            
            strategy_text += "PARÁMETROS:\n"
            for param, value in strategies['parametros'].items():
                strategy_text += f"• {param}: {value}\n"
            
            self.strategy_text.insert(1.0, strategy_text)
            self.strategy_text.config(state='disabled')
            
        except Exception as e:
            print(f"Error actualizando estrategias: {e}")
    
    def update_parameters_from_exercise(self):
        """Actualiza parámetros desde ejercicio"""
        try:
            defaults = self.controller.get_default_parameters()
            
            if self.parameter_panel:
                self.parameter_panel.interval_a.set(defaults['x_min'])
                self.parameter_panel.interval_b.set(defaults['x_max'])
                self.parameter_panel.delta_x.set(defaults['delta_x'])
                self.parameter_panel.pop_size.set(defaults['population_size'])
                self.parameter_panel.num_generations.set(defaults['num_generations'])
                self.parameter_panel.prob_crossover.set(defaults['crossover_probability'])
                self.parameter_panel.prob_mutation_x.set(defaults['mutation_x_probability'])
                self.parameter_panel.prob_mutation_g.set(defaults['mutation_g_probability'])
                
                self.parameter_panel.update_calculated_values()
        
        except Exception as e:
            print(f"Error actualizando parámetros: {e}")
    
    def on_execute_algorithm(self, params_dict: dict) -> bool:
        """Callback para ejecutar algoritmo"""
        progress_dialog = ProgressDialog(self.root, params_dict['num_generations'])
        
        def progress_callback(generation, total_generations, best_fitness, strategy_info):
            progress_dialog.update_progress(generation, total_generations, best_fitness)
        
        try:
            success = self.controller.execute_genetic_algorithm(
                params_dict, 
                progress_callback
            )
            
            progress_dialog.close()
            
            if success:
                self.update_results_display()
                self.graph_buttons_enabled(True)
                self.report_btn.config(state="normal")
            
            return success
            
        except Exception as e:
            progress_dialog.close()
            print(f"Error ejecutando: {e}")
            return False
    
    def update_results_display(self):
        """Actualiza resultados"""
        try:
            result = self.controller.get_algorithm_result()
            if not result:
                return
            
            display_value = result.get_display_result()
            objective_type = "Mínimo" if result.is_minimization else "Máximo"
            
            self.result_labels['best_x'].config(text=f"{result.best_x:.6f}")
            self.result_labels['best_fitness'].config(text=f"{display_value:.6f}")
            self.result_labels['best_generation'].config(text=f"{self.find_best_generation(result)}")
            self.result_labels['total_evaluations'].config(text=f"{result.total_evaluations}")
            self.result_labels['improvement'].config(text=f"{abs(result.improvement):.6f}")
            self.result_labels['status'].config(text=f"{objective_type} encontrado", fg='green')
            
            self.update_population_analysis(result)
            
        except Exception as e:
            print(f"Error actualizando resultados: {e}")
    
    def update_population_analysis(self, result):
        """Actualiza análisis de población"""
        try:
            self.population_text.config(state='normal')
            self.population_text.delete(1.0, tk.END)
            
            final_pop = result.final_population
            config = result.exercise_config
            
            final_x_values = [ind.to_decimal(config.x_min, config.x_max) 
                            for ind in final_pop.individuals]
            
            import numpy as np
            
            analysis_text = "ANÁLISIS DE POBLACIÓN FINAL:\n\n"
            analysis_text += f"Tamaño: {len(final_pop.individuals)} individuos\n"
            analysis_text += f"Diversidad: {np.std(final_x_values):.6f}\n"
            analysis_text += f"Rango: [{min(final_x_values):.4f}, {max(final_x_values):.4f}]\n\n"
            
            # Mejores individuos
            sorted_individuals = sorted(
                final_pop.individuals,
                key=lambda ind: ind.fitness,
                reverse=not result.is_minimization
            )
            
            analysis_text += "MEJORES INDIVIDUOS:\n"
            for i, ind in enumerate(sorted_individuals[:3]):
                x_val = ind.to_decimal(config.x_min, config.x_max)
                fitness_val = -ind.fitness if result.is_minimization else ind.fitness
                analysis_text += f"{i+1}. x={x_val:.6f}, f(x)={fitness_val:.6f}\n"
            
            # Precisión
            required_precision = config.precision
            actual_precision = result.parameters.calculate_actual_precision()
            precision_ok = actual_precision <= required_precision
            
            analysis_text += f"\nPrecisión requerida: {required_precision}\n"
            analysis_text += f"Precisión alcanzada: {actual_precision:.6f}\n"
            analysis_text += f"Estado: {'✅ CUMPLIDA' if precision_ok else '⚠️ No cumplida'}\n"
            
            self.population_text.insert(1.0, analysis_text)
            self.population_text.config(state='disabled')
            
        except Exception as e:
            print(f"Error actualizando población: {e}")
    
    def show_graph(self, graph_type: str):
        """Muestra gráfica seleccionada"""
        if not self.controller.has_results():
            return
        
        self.clear_graph_area()
        self.update_button_selection(graph_type)
        
        result = self.controller.get_algorithm_result()
        self.current_figure = self.graph_factory.create_graph(graph_type, result)
        
        if self.current_figure:
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
            self.current_canvas = FigureCanvasTkAgg(self.current_figure, 
                                                   master=self.graph_container)
            self.current_canvas.draw()
            self.current_canvas.get_tk_widget().pack(fill="both", expand=True)
    
    def update_button_selection(self, selected_type: str):
        """Actualiza selección de botones"""
        button_mapping = {
            "objective_population": 0,
            "evolution_best": 1,
            "evolution_all": 2
        }
        
        for i, btn in enumerate(self.graph_buttons):
            if i == button_mapping.get(selected_type, -1):
                btn.config(bg='#cce0ff', relief='sunken')
            else:
                btn.config(bg='white', relief='raised')
    
    def graph_buttons_enabled(self, enabled: bool):
        """Habilita/deshabilita botones de gráficas"""
        state = "normal" if enabled else "disabled"
        for btn in self.graph_buttons:
            btn.config(state=state)
    
    def clear_graph_area(self):
        """Limpia área de gráficas"""
        if self.current_canvas:
            self.current_canvas.get_tk_widget().destroy()
            self.current_canvas = None
        
        if self.current_figure:
            import matplotlib.pyplot as plt
            plt.close(self.current_figure)
            self.current_figure = None
        
        for widget in self.graph_container.winfo_children():
            widget.destroy()
    
    def clear_results_display(self):
        """Limpia información de resultados"""
        for label in self.result_labels.values():
            label.config(text="--", fg='#333333')
        
        self.population_text.config(state='normal')
        self.population_text.delete(1.0, tk.END)
        self.population_text.insert(1.0, "Ejecute el algoritmo para ver el análisis...")
        self.population_text.config(state='disabled')
        
        self.graph_buttons_enabled(False)
        self.report_btn.config(state="disabled")
        
        self.clear_graph_area()
        self.create_welcome_graph_message()
    
    def generate_report(self):
        """Genera reporte de resultados"""
        if not self.controller.has_results():
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Guardar Reporte del Ejercicio"
        )
        
        if filename:
            success = self.controller.generate_report(filename)
            if success:
                self.result_labels['status'].config(text="Reporte generado", fg='blue')
    
    def clear_results(self):
        """Limpia todos los resultados"""
        self.controller.clear_results()
        self.clear_results_display()
    
    def clear_visualization(self):
        """Limpia visualización (llamado desde controlador)"""
        self.clear_graph_area()
        self.create_welcome_graph_message()
    
    def find_best_generation(self, result) -> int:
        """Encuentra generación del mejor resultado"""
        target_fitness = result.best_fitness
        for i, fitness in enumerate(result.best_fitness_history):
            if abs(fitness - target_fitness) < 1e-10:
                return i
        return len(result.best_fitness_history) - 1
    
    def run(self):
        """Ejecuta la aplicación"""
        self.root.mainloop()