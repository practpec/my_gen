"""
Ventana principal corregida - División en 3 secciones sin redundancias
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from typing import Optional
import os

# IMPORTACIONES ABSOLUTAS
from presentation.components.parameter_input import ParameterInputPanel
from presentation.components.progress_dialog import ProgressDialog
from presentation.visualization.graph_factory import GraphFactory
# from presentation.utils.video_generator import VideoGenerator


class MainWindowSimplified:
    """Ventana principal con diseño corregido de 3 secciones"""
    
    def __init__(self, controller):
        self.controller = controller
        self.root = tk.Tk()
        self.setup_window()
        
        # Referencias
        self.parameter_panel = None
        self.graph_factory = GraphFactory()
        # self.video_generator = VideoGenerator()
        self.current_canvas = None
        self.current_figure = None
        self.graph_buttons = []
        
        # Labels de información
        self.result_labels = {}
        self.population_text = None
        
        self.create_interface()
    
    def setup_window(self):
        """Configura ventana principal"""
        self.root.title("Algoritmo Genético - Optimización con Estrategias Específicas")
        self.root.geometry("1600x900")
        self.root.configure(bg='#f0f0f0')
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
    
    def create_interface(self):
        """Crea interfaz de SOLO 3 secciones"""
        
        # SECCIÓN SUPERIOR (25% altura) - Solo parámetros
        top_section = tk.Frame(self.root, bg='white', relief='raised', bd=2, height=225)
        top_section.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        top_section.grid_propagate(False)
        
        # SECCIÓN INFERIOR (75% altura) - Dividida en 2 columnas
        bottom_section = tk.Frame(self.root, bg='#f0f0f0')
        bottom_section.grid(row=1, column=0, sticky="nsew", padx=10, pady=(5, 10))
        bottom_section.grid_columnconfigure(0, weight=1)  # Izquierda: resultados
        bottom_section.grid_columnconfigure(1, weight=2)  # Derecha: gráficas (más ancho)
        bottom_section.grid_rowconfigure(0, weight=1)
        
        self.create_top_section(top_section)
        self.create_bottom_left_section(bottom_section)
        self.create_bottom_right_section(bottom_section)
    
    def create_top_section(self, parent):
        """Sección superior - SOLO parámetros y configuración"""
        # Título principal
        title_label = tk.Label(parent, text="Configuración del Algoritmo Genético", 
                              font=("Arial", 16, "bold"), bg='white')
        title_label.pack(pady=(10, 5))
        
        # Subtítulo con función
        function_info = self.controller.get_function_info()
        subtitle = f"Función: {function_info['expression']} | Intervalo: {function_info['interval']}"
        subtitle_label = tk.Label(parent, text=subtitle, 
                                 font=("Arial", 10), bg='white', fg='#666666')
        subtitle_label.pack(pady=(0, 10))
        
        # Panel de parámetros mejorado
        self.parameter_panel = ParameterInputPanel(
            parent, 
            self.controller,
            self.on_execute_algorithm
        )
    
    def create_bottom_left_section(self, parent):
        """Sección inferior izquierda - Resultados y análisis"""
        results_panel = tk.Frame(parent, bg='white', relief='raised', bd=2)
        results_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        
        # Título
        title_label = tk.Label(results_panel, text="Resultados y Análisis", 
                              font=("Arial", 14, "bold"), bg='white')
        title_label.pack(pady=(10, 5))
        
        self.create_results_section(results_panel)
        self.create_population_analysis_section(results_panel)
        self.create_action_buttons(results_panel)
    
    def create_results_section(self, parent):
        """Sección de resultados principales"""
        results_frame = tk.LabelFrame(parent, text="Resultados Principales", 
                                     font=("Arial", 11, "bold"), bg='white')
        results_frame.pack(fill="x", padx=10, pady=5)
        
        result_items = [
            ("Mejor x:", "best_x"),
            ("Valor f(x):", "best_fitness"),
            ("Generación:", "best_generation"),
            ("Evaluaciones:", "total_evaluations"),
            ("Mejora total:", "improvement"),
            ("Estado:", "status")
        ]
        
        self.result_labels = {}
        for i, (label_text, key) in enumerate(result_items):
            row = i // 2
            col = (i % 2) * 2
            
            tk.Label(results_frame, text=label_text, bg='white', 
                    font=("Arial", 9, "bold")).grid(row=row, column=col, sticky="w", padx=5, pady=3)
            
            value_label = tk.Label(results_frame, text="--", bg='white', 
                                 font=("Arial", 9), fg='#333333')
            value_label.grid(row=row, column=col+1, sticky="w", padx=5, pady=3)
            
            self.result_labels[key] = value_label
    
    def create_population_analysis_section(self, parent):
        """Sección de análisis de población"""
        analysis_frame = tk.LabelFrame(parent, text="Análisis de Población", 
                                      font=("Arial", 11, "bold"), bg='white')
        analysis_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Text widget con scrollbar
        text_frame = tk.Frame(analysis_frame, bg='white')
        text_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.population_text = tk.Text(text_frame, height=15, width=50, 
                                     bg='#f8f8f8', font=("Arial", 8),
                                     state='disabled', wrap=tk.WORD)
        
        scrollbar = tk.Scrollbar(text_frame, orient="vertical", command=self.population_text.yview)
        self.population_text.configure(yscrollcommand=scrollbar.set)
        
        self.population_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Mensaje inicial
        self.population_text.config(state='normal')
        self.population_text.insert(1.0, "Ejecute el algoritmo para ver el análisis detallado...")
        self.population_text.config(state='disabled')
    
    def create_action_buttons(self, parent):
        """Botones de acciones"""
        actions_frame = tk.Frame(parent, bg='white')
        actions_frame.pack(fill="x", padx=10, pady=10)
        
        # Botón ejecutar (prominente)
        self.execute_btn = tk.Button(actions_frame, text="🚀 EJECUTAR ALGORITMO", 
                                    command=self.execute_from_button,
                                    bg='#4CAF50', fg='white', 
                                    font=("Arial", 12, "bold"),
                                    height=2)
        self.execute_btn.pack(fill="x", pady=(0, 5))
        
        # Botón generar reporte
        self.report_btn = tk.Button(actions_frame, text="📄 Generar Reporte", 
                                   command=self.generate_report,
                                   bg='#FF9800', fg='white', 
                                   font=("Arial", 10, "bold"),
                                   height=1, state="disabled")
        self.report_btn.pack(fill="x", pady=2)
        
        # Botón generar video
        self.video_btn = tk.Button(actions_frame, text="🎬 Generar Video", 
                                  command=self.generate_video,
                                  bg='#9C27B0', fg='white', 
                                  font=("Arial", 10, "bold"),
                                  height=1, state="disabled")
        self.video_btn.pack(fill="x", pady=2)
        
        # Botón limpiar
        clear_btn = tk.Button(actions_frame, text="🗑️ Limpiar", 
                             command=self.clear_results,
                             bg='#f44336', fg='white', 
                             font=("Arial", 10, "bold"),
                             height=1)
        clear_btn.pack(fill="x", pady=2)
    
    def create_bottom_right_section(self, parent):
        """Sección inferior derecha - Gráficas"""
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
        
        tk.Label(controls_frame, text="📊 Visualizaciones", 
                font=("Arial", 14, "bold"), bg='white').pack()
        
        buttons_frame = tk.Frame(controls_frame, bg='white')
        buttons_frame.pack(pady=10)
        
        graph_types = [
            ("Función y Población", "objective_population"),
            ("Evolución Mejor", "evolution_best"),
            ("Evolución Completa", "evolution_all")
        ]
        
        for text, value in graph_types:
            btn = tk.Button(buttons_frame, text=text, 
                           command=lambda v=value: self.show_graph(v),
                           bg='white', relief='raised', bd=2,
                           font=("Arial", 10), width=16,
                           state="disabled")
            btn.pack(side="left", padx=3)
            self.graph_buttons.append(btn)
    
    def create_welcome_graph_message(self):
        """Mensaje de bienvenida en gráficas"""
        welcome_frame = tk.Frame(self.graph_container, bg='white')
        welcome_frame.pack(expand=True)
        
        welcome_text = """
        📊 Visualizaciones del Algoritmo Genético
        
        Configure los parámetros y ejecute el algoritmo
        para ver las visualizaciones disponibles:
        
        🎯 Función objetivo con población final
        📈 Evolución del mejor individuo  
        🌊 Evolución de toda la población
        🎬 Video de evolución (generación automática)
        """
        
        tk.Label(welcome_frame, text=welcome_text, 
                font=("Arial", 12), bg='white',
                justify="center", fg='#666666').pack(expand=True)
    
    def execute_from_button(self):
        """Ejecuta desde el botón principal"""
        if hasattr(self.parameter_panel, 'execute_algorithm'):
            self.parameter_panel.execute_algorithm()
    
    def on_execute_algorithm(self, params_dict: dict) -> bool:
        """Callback para ejecutar algoritmo"""
        progress_dialog = ProgressDialog(self.root, params_dict['num_generations'])
        
        def progress_callback(generation, total_generations, best_fitness, strategy_info):
            progress_dialog.update_progress(generation, total_generations, best_fitness)
        
        try:
            # Deshabilitar botón durante ejecución
            self.execute_btn.config(state="disabled", text="⏳ Ejecutando...")
            self.root.update()
            
            success = self.controller.execute_genetic_algorithm(
                params_dict, 
                progress_callback
            )
            
            progress_dialog.close()
            
            if success:
                self.update_results_display()
                self.graph_buttons_enabled(True)
                self.report_btn.config(state="normal")
                self.video_btn.config(state="normal")
                
                # Mostrar automáticamente la primera gráfica
                self.show_graph("objective_population")
            
            # Rehabilitar botón
            self.execute_btn.config(state="normal", text="🚀 EJECUTAR ALGORITMO")
            
            return success
            
        except Exception as e:
            progress_dialog.close()
            self.execute_btn.config(state="normal", text="🚀 EJECUTAR ALGORITMO")
            messagebox.showerror("Error", f"Error ejecutando algoritmo: {str(e)}")
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
            self.result_labels['status'].config(text=f"✅ {objective_type} encontrado", fg='green')
            
            self.update_population_analysis(result)
            
        except Exception as e:
            print(f"Error actualizando resultados: {e}")
    
    def update_population_analysis(self, result):
        """Actualiza análisis detallado de población"""
        try:
            self.population_text.config(state='normal')
            self.population_text.delete(1.0, tk.END)
            
            final_pop = result.final_population
            config = result.exercise_config
            
            final_x_values = [ind.to_decimal(config.x_min, config.x_max) 
                            for ind in final_pop.individuals]
            
            import numpy as np
            
            analysis_text = "🔍 ANÁLISIS DETALLADO DE RESULTADOS\n"
            analysis_text += "=" * 50 + "\n\n"
            
            # Información del mejor resultado
            objective_type = "MINIMIZACIÓN" if result.is_minimization else "MAXIMIZACIÓN"
            analysis_text += f"📊 OBJETIVO: {objective_type}\n"
            analysis_text += f"🎯 Mejor x encontrado: {result.best_x:.8f}\n"
            analysis_text += f"📈 Valor función f(x): {result.get_display_result():.8f}\n"
            analysis_text += f"🏆 Encontrado en generación: {self.find_best_generation(result)}\n"
            analysis_text += f"🔄 Total evaluaciones: {result.total_evaluations}\n"
            analysis_text += f"📈 Mejora total: {abs(result.improvement):.8f}\n\n"
            
            # Análisis de población final
            analysis_text += "👥 POBLACIÓN FINAL:\n"
            analysis_text += f"• Tamaño: {len(final_pop.individuals)} individuos\n"
            analysis_text += f"• Diversidad (σ): {np.std(final_x_values):.6f}\n"
            analysis_text += f"• Rango x: [{min(final_x_values):.4f}, {max(final_x_values):.4f}]\n"
            analysis_text += f"• Media x̄: {np.mean(final_x_values):.6f}\n\n"
            
            # Top 5 mejores individuos
            sorted_individuals = sorted(
                final_pop.individuals,
                key=lambda ind: ind.fitness,
                reverse=True  # Siempre descendente porque fitness ya está ajustado
            )
            
            analysis_text += "🏅 TOP 5 MEJORES INDIVIDUOS:\n"
            for i, ind in enumerate(sorted_individuals[:5]):
                x_val = ind.to_decimal(config.x_min, config.x_max)
                fitness_val = result.exercise_config.objective_type == "minimize" and -ind.fitness or ind.fitness
                analysis_text += f"{i+1}. x = {x_val:.6f} → f(x) = {fitness_val:.6f}\n"
            
            analysis_text += "\n"
            
            # Análisis de precisión
            required_precision = config.precision
            actual_precision = result.parameters.calculate_actual_precision()
            precision_ok = actual_precision <= required_precision
            
            analysis_text += "⚡ ANÁLISIS DE PRECISIÓN:\n"
            analysis_text += f"• Precisión requerida: {required_precision}\n"
            analysis_text += f"• Precisión alcanzada: {actual_precision:.8f}\n"
            analysis_text += f"• Estado: {'✅ CUMPLIDA' if precision_ok else '❌ NO CUMPLIDA'}\n"
            analysis_text += f"• Factor de cumplimiento: {required_precision/actual_precision:.2f}x\n\n"
            
            # Información de estrategias
            analysis_text += "🛠️ ESTRATEGIAS UTILIZADAS:\n"
            strategies = self.controller.get_strategy_summary()
            analysis_text += f"• Emparejamiento: {strategies['emparejamiento']}\n"
            analysis_text += f"• Cruzamiento: {strategies['cruzamiento']}\n"
            analysis_text += f"• Mutación: {strategies['mutacion']}\n"
            analysis_text += f"• Selección: {strategies['seleccion']}\n\n"
            
            analysis_text += "📋 PARÁMETROS DE ESTRATEGIAS:\n"
            for param, value in strategies['parametros'].items():
                analysis_text += f"• {param}: {value}\n"
            
            self.population_text.insert(1.0, analysis_text)
            self.population_text.config(state='disabled')
            
        except Exception as e:
            print(f"Error actualizando análisis: {e}")
    
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
    
    def generate_video(self):
        """Genera video de la evolución del algoritmo"""
        if not self.controller.has_results():
            messagebox.showwarning("Advertencia", "No hay resultados para generar video.")
            return
        
        # Seleccionar carpeta de salida
        output_dir = filedialog.askdirectory(
            title="Seleccionar carpeta para guardar el video"
        )
        
        if not output_dir:
            return
        
        try:
            result = self.controller.get_algorithm_result()
            
            # Mostrar progreso de generación de video
            progress_window = tk.Toplevel(self.root)
            progress_window.title("Generando Video")
            progress_window.geometry("450x120")
            progress_window.configure(bg='#f0f0f0')
            progress_window.resizable(False, False)
            
            # Centrar ventana
            progress_window.transient(self.root)
            progress_window.grab_set()
            
            tk.Label(progress_window, text="🎬 Generando video de evolución...", 
                    font=("Arial", 12, "bold"), bg='#f0f0f0').pack(pady=15)
            
            progress_bar = ttk.Progressbar(progress_window, mode='indeterminate', length=350)
            progress_bar.pack(pady=10, padx=20)
            progress_bar.start()
            
            status_label = tk.Label(progress_window, text="Preparando frames...", 
                                   font=("Arial", 10), bg='#f0f0f0', fg='#666666')
            status_label.pack(pady=5)
            
            progress_window.update()
            
            # Generar video
            def update_status(message):
                status_label.config(text=message)
                progress_window.update()
            
            video_path = self.video_generator.create_evolution_video(
                result, output_dir, progress_callback=update_status
            )
            
            # Cerrar ventana de progreso
            progress_bar.stop()
            progress_window.grab_release()
            progress_window.destroy()
            
            if video_path and os.path.exists(video_path):
                messagebox.showinfo("✅ Video Generado", 
                                  f"Video generado exitosamente:\n\n{os.path.basename(video_path)}\n\n"
                                  f"Ubicación: {output_dir}")
                
                # Preguntar si quiere abrir la carpeta
                if messagebox.askyesno("📁 Abrir Carpeta", "¿Desea abrir la carpeta donde se guardó el video?"):
                    self.open_folder(output_dir)
            else:
                messagebox.showerror("❌ Error", "No se pudo generar el video.")
                
        except Exception as e:
            # Cerrar ventana de progreso si hay error
            try:
                progress_window.grab_release()
                progress_window.destroy()
            except:
                pass
            messagebox.showerror("Error", f"Error al generar video:\n{str(e)}")
    
    def open_folder(self, folder_path: str):
        """Abre una carpeta en el explorador"""
        try:
            if os.name == 'nt':  # Windows
                os.startfile(folder_path)
            elif os.name == 'posix':  # Linux/Mac
                if os.uname().sysname == 'Darwin':  # macOS
                    os.system(f'open "{folder_path}"')
                else:  # Linux
                    os.system(f'xdg-open "{folder_path}"')
        except Exception as e:
            print(f"No se pudo abrir la carpeta: {e}")
    
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
        self.population_text.insert(1.0, "Ejecute el algoritmo para ver el análisis detallado...")
        self.population_text.config(state='disabled')
        
        self.graph_buttons_enabled(False)
        self.report_btn.config(state="disabled")
        self.video_btn.config(state="disabled")
        
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
                self.result_labels['status'].config(text="📄 Reporte generado", fg='blue')
    
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