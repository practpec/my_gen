"""
Panel para entrada de parámetros del algoritmo genético
"""

import tkinter as tk
from tkinter import ttk
from typing import Callable, Dict, Any


class ParameterInputPanel:
    """Panel para configurar parámetros del algoritmo"""
    
    def __init__(self, parent, controller, execute_callback: Callable[[Dict[str, Any]], bool]):
        self.parent = parent
        self.controller = controller
        self.execute_callback = execute_callback
        
        # Variables de configuración
        self.interval_a = tk.DoubleVar(value=-5.0)
        self.interval_b = tk.DoubleVar(value=5.0)
        self.delta_x = tk.DoubleVar(value=0.0705)
        self.pop_size = tk.IntVar(value=25)
        self.num_generations = tk.IntVar(value=150)
        self.prob_crossover = tk.DoubleVar(value=0.75)
        self.prob_mutation_x = tk.DoubleVar(value=0.20)
        self.prob_mutation_g = tk.DoubleVar(value=0.20)
        
        # Variables calculadas
        self.num_points = tk.StringVar(value="...")
        self.num_bits = tk.StringVar(value="...")
        self.max_decimal = tk.StringVar(value="...")
        
        self.create_panel()
        self.setup_auto_update()
        self.update_calculated_values()
    
    def create_panel(self):
        """Crea el panel de parámetros"""
        # Título
        title_label = tk.Label(self.parent, text="Parámetros del Algoritmo", 
                              font=("Arial", 14, "bold"), bg='white')
        title_label.pack(pady=10)
        
        # Frame para parámetros
        params_frame = tk.LabelFrame(self.parent, text="Configuración", 
                                    font=("Arial", 11, "bold"), bg='white')
        params_frame.pack(fill="x", padx=10, pady=5)
        
        # Crear entradas
        self.create_labeled_entry(params_frame, "Intervalo A:", self.interval_a)
        self.create_labeled_entry(params_frame, "Intervalo B:", self.interval_b)
        self.create_labeled_entry(params_frame, "Δx:", self.delta_x)
        self.create_labeled_entry(params_frame, "Población:", self.pop_size)
        self.create_labeled_entry(params_frame, "Generaciones:", self.num_generations)
        self.create_labeled_entry(params_frame, "Prob. Cruzamiento:", self.prob_crossover)
        self.create_labeled_entry(params_frame, "Prob. Mutación X:", self.prob_mutation_x)
        self.create_labeled_entry(params_frame, "Prob. Mutación G:", self.prob_mutation_g)
        
        # Información calculada
        info_frame = tk.LabelFrame(params_frame, text="Parámetros Calculados", 
                                  font=("Arial", 10, "bold"), bg='white')
        info_frame.pack(fill="x", pady=10)
        
        self.create_info_display(info_frame, "# Puntos:", self.num_points)
        self.create_info_display(info_frame, "# Bits:", self.num_bits)
        self.create_info_display(info_frame, "Máx. Decimal:", self.max_decimal)
        
        # Botón ejecutar
        execute_btn = tk.Button(params_frame, text="EJECUTAR ALGORITMO", 
                               command=self.execute_algorithm,
                               bg='#4CAF50', fg='white', 
                               font=("Arial", 12, "bold"),
                               height=2)
        execute_btn.pack(fill="x", pady=20)
    
    def create_labeled_entry(self, parent, label: str, variable):
        """Crea entrada con etiqueta"""
        frame = tk.Frame(parent, bg='white')
        frame.pack(fill="x", pady=2)
        
        tk.Label(frame, text=label, bg='white', width=18, anchor="w").pack(side="left")
        tk.Entry(frame, textvariable=variable, width=12).pack(side="right")
    
    def create_info_display(self, parent, label: str, variable):
        """Crea display de información"""
        frame = tk.Frame(parent, bg='white')
        frame.pack(fill="x", pady=1)
        
        tk.Label(frame, text=label, bg='white', width=12, anchor="w").pack(side="left")
        info_label = tk.Label(frame, textvariable=variable, bg='#f0f0f0', 
                             relief="sunken", bd=1, width=12)
        info_label.pack(side="right")
    
    def setup_auto_update(self):
        """Configura actualización automática"""
        for var in [self.interval_a, self.interval_b, self.delta_x]:
            var.trace('w', lambda *args: self.update_calculated_values())
    
    def update_calculated_values(self):
        """Actualiza valores calculados"""
        try:
            x_min = self.interval_a.get()
            x_max = self.interval_b.get()
            delta_x = self.delta_x.get()
            
            derived = self.controller.calculate_derived_parameters(x_min, x_max, delta_x)
            
            self.num_points.set(str(derived['num_points']))
            self.num_bits.set(str(derived['num_bits']))
            self.max_decimal.set(str(derived['max_decimal']))
            
        except Exception:
            self.num_points.set("...")
            self.num_bits.set("...")
            self.max_decimal.set("...")
    
    def execute_algorithm(self):
        """Ejecuta el algoritmo genético"""
        try:
            params = {
                'x_min': self.interval_a.get(),
                'x_max': self.interval_b.get(),
                'delta_x': self.delta_x.get(),
                'population_size': self.pop_size.get(),
                'num_generations': self.num_generations.get(),
                'crossover_probability': self.prob_crossover.get(),
                'mutation_x_probability': self.prob_mutation_x.get(),
                'mutation_g_probability': self.prob_mutation_g.get()
            }
            
            self.execute_callback(params)
            
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Error", f"Error al obtener parámetros: {str(e)}")