"""
Panel mejorado para entrada de parámetros con combobox de objetivo
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, Dict, Any


class ParameterInputPanel:
    """Panel mejorado para configurar parámetros del algoritmo"""
    
    def __init__(self, parent, controller, execute_callback: Callable[[Dict[str, Any]], bool]):
        self.parent = parent
        self.controller = controller
        self.execute_callback = execute_callback
        
        # Variables de configuración
        self.interval_a = tk.DoubleVar()
        self.interval_b = tk.DoubleVar()
        self.delta_x = tk.DoubleVar()
        self.pop_size = tk.IntVar()
        self.num_generations = tk.IntVar()
        self.prob_crossover = tk.DoubleVar()
        self.prob_mutation_x = tk.DoubleVar()
        self.prob_mutation_g = tk.DoubleVar()
        self.objective_type = tk.StringVar()
        
        # Variables calculadas
        self.num_points = tk.StringVar(value="...")
        self.num_bits = tk.StringVar(value="...")
        self.max_decimal = tk.StringVar(value="...")
        
        self.create_panel()
        self.load_default_values()
        self.setup_auto_update()
        self.update_calculated_values()
    
    def load_default_values(self):
        """Carga valores por defecto del ejercicio"""
        try:
            defaults = self.controller.get_default_parameters()
            function_info = self.controller.get_function_info()
            
            self.interval_a.set(defaults['x_min'])
            self.interval_b.set(defaults['x_max'])
            self.delta_x.set(defaults['delta_x'])
            self.pop_size.set(defaults['population_size'])
            self.num_generations.set(defaults['num_generations'])
            self.prob_crossover.set(defaults['crossover_probability'])
            self.prob_mutation_x.set(defaults['mutation_x_probability'])
            self.prob_mutation_g.set(defaults['mutation_g_probability'])
            self.objective_type.set(function_info['objective_type'])
            
        except Exception as e:
            print(f"Error cargando valores por defecto: {e}")
    
    def create_panel(self):
        """Crea el panel de parámetros mejorado"""
        # Frame principal con diseño horizontal
        main_frame = tk.Frame(self.parent, bg='white')
        main_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Dividir en dos columnas
        left_frame = tk.Frame(main_frame, bg='white')
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        right_frame = tk.Frame(main_frame, bg='white')
        right_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        self.create_basic_parameters(left_frame)
        self.create_advanced_parameters(right_frame)
    
    def create_basic_parameters(self, parent):
        """Parámetros básicos"""
        basic_frame = tk.LabelFrame(parent, text="⚙️ Parámetros Básicos", 
                                   font=("Arial", 11, "bold"), bg='white')
        basic_frame.pack(fill="both", expand=True)
        
        # Objetivo (Combobox)
        self.create_objective_selector(basic_frame)
        
        # Intervalo
        self.create_labeled_entry(basic_frame, "🎯 Intervalo A:", self.interval_a, width=10)
        self.create_labeled_entry(basic_frame, "🎯 Intervalo B:", self.interval_b, width=10)
        self.create_labeled_entry(basic_frame, "📏 Precisión Δx:", self.delta_x, width=10)
        
        # Población y generaciones
        self.create_labeled_entry(basic_frame, "👥 Población:", self.pop_size, width=10)
        self.create_labeled_entry(basic_frame, "🔄 Generaciones:", self.num_generations, width=10)
    
    def create_advanced_parameters(self, parent):
        """Parámetros avanzados"""
        advanced_frame = tk.LabelFrame(parent, text="🔬 Parámetros Avanzados", 
                                      font=("Arial", 11, "bold"), bg='white')
        advanced_frame.pack(fill="both", expand=True)
        
        # Probabilidades
        self.create_labeled_entry(advanced_frame, "🔗 Prob. Cruzamiento:", self.prob_crossover, width=10)
        self.create_labeled_entry(advanced_frame, "🧬 Prob. Mutación X:", self.prob_mutation_x, width=10)
        self.create_labeled_entry(advanced_frame, "🧬 Prob. Mutación G:", self.prob_mutation_g, width=10)
        
        # Información calculada
        self.create_calculated_info(advanced_frame)
        
        # Botón ejecutar
        self.create_execute_button(advanced_frame)
    
    def create_objective_selector(self, parent):
        """Selector de objetivo (minimizar/maximizar)"""
        frame = tk.Frame(parent, bg='white')
        frame.pack(fill="x", pady=5, padx=5)
        
        tk.Label(frame, text="🎯 Objetivo:", bg='white', 
                font=("Arial", 10, "bold"), width=15, anchor="w").pack(side="left")
        
        objective_combo = ttk.Combobox(frame, textvariable=self.objective_type,
                                      values=["minimize", "maximize"],
                                      state="readonly", width=12)
        objective_combo.pack(side="right")
        
        # Callback para cambios
        objective_combo.bind("<<ComboboxSelected>>", self.on_objective_changed)
    
    def create_labeled_entry(self, parent, label: str, variable, width=12):
        """Crea entrada con etiqueta mejorada"""
        frame = tk.Frame(parent, bg='white')
        frame.pack(fill="x", pady=3, padx=5)
        
        tk.Label(frame, text=label, bg='white', 
                font=("Arial", 10, "bold"), width=15, anchor="w").pack(side="left")
        
        entry = tk.Entry(frame, textvariable=variable, width=width, 
                        font=("Arial", 10), relief="solid", bd=1)
        entry.pack(side="right")
        return entry
    
    def create_calculated_info(self, parent):
        """Información calculada"""
        info_frame = tk.LabelFrame(parent, text="📊 Información Calculada", 
                                  font=("Arial", 10, "bold"), bg='white')
        info_frame.pack(fill="x", pady=10, padx=5)
        
        self.create_info_display(info_frame, "🔢 # Puntos:", self.num_points)
        self.create_info_display(info_frame, "💾 # Bits:", self.num_bits)
        self.create_info_display(info_frame, "🔝 Máx. Decimal:", self.max_decimal)
    
    def create_info_display(self, parent, label: str, variable):
        """Crea display de información"""
        frame = tk.Frame(parent, bg='white')
        frame.pack(fill="x", pady=2, padx=5)
        
        tk.Label(frame, text=label, bg='white', 
                font=("Arial", 9, "bold"), width=12, anchor="w").pack(side="left")
        
        info_label = tk.Label(frame, textvariable=variable, bg='#e3f2fd', 
                             relief="solid", bd=1, width=10, 
                             font=("Arial", 9, "bold"), fg='#1976d2')
        info_label.pack(side="right")
    
    def create_execute_button(self, parent):
        """Botón de ejecución"""
        button_frame = tk.Frame(parent, bg='white')
        button_frame.pack(fill="x", pady=15, padx=5)
        
        execute_btn = tk.Button(button_frame, text="🚀 EJECUTAR ALGORITMO", 
                               command=self.execute_algorithm,
                               bg='#4CAF50', fg='white', 
                               font=("Arial", 12, "bold"),
                               height=2, relief="raised", bd=3)
        execute_btn.pack(fill="x")
    
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
            
            if x_min >= x_max or delta_x <= 0:
                self.num_points.set("---")
                self.num_bits.set("---")
                self.max_decimal.set("---")
                return
            
            derived = self.controller.calculate_derived_parameters(x_min, x_max, delta_x)
            
            self.num_points.set(str(derived['num_points']))
            self.num_bits.set(str(derived['num_bits']))
            self.max_decimal.set(str(derived['max_decimal']))
            
        except Exception:
            self.num_points.set("...")
            self.num_bits.set("...")
            self.max_decimal.set("...")
    
    def on_objective_changed(self, event=None):
        """Callback cuando cambia el objetivo"""
        # Por ahora solo actualiza, en futuras versiones podría cambiar el ejercicio
        pass
    
    def execute_algorithm(self):
        """Ejecuta el algoritmo genético"""
        try:
            # Validar parámetros básicos
            if not self.validate_parameters():
                return
            
            params = {
                'x_min': self.interval_a.get(),
                'x_max': self.interval_b.get(),
                'delta_x': self.delta_x.get(),
                'population_size': self.pop_size.get(),
                'num_generations': self.num_generations.get(),
                'crossover_probability': self.prob_crossover.get(),
                'mutation_x_probability': self.prob_mutation_x.get(),
                'mutation_g_probability': self.prob_mutation_g.get(),
                'objective_type': self.objective_type.get()
            }
            
            self.execute_callback(params)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener parámetros: {str(e)}")
    
    def validate_parameters(self) -> bool:
        """Valida parámetros antes de ejecutar"""
        try:
            # Validar intervalos
            if self.interval_a.get() >= self.interval_b.get():
                messagebox.showerror("Error de Validación", 
                                   "El intervalo A debe ser menor que el intervalo B")
                return False
            
            # Validar precisión
            if self.delta_x.get() <= 0:
                messagebox.showerror("Error de Validación", 
                                   "La precisión Δx debe ser mayor que 0")
                return False
            
            # Validar población
            if self.pop_size.get() < 4:
                messagebox.showerror("Error de Validación", 
                                   "El tamaño de población debe ser al menos 4")
                return False
            
            # Validar generaciones
            if self.num_generations.get() < 1:
                messagebox.showerror("Error de Validación", 
                                   "El número de generaciones debe ser al menos 1")
                return False
            
            # Validar probabilidades
            probabilities = [
                (self.prob_crossover.get(), "cruzamiento"),
                (self.prob_mutation_x.get(), "mutación X"),
                (self.prob_mutation_g.get(), "mutación G")
            ]
            
            for prob, name in probabilities:
                if not (0.0 <= prob <= 1.0):
                    messagebox.showerror("Error de Validación", 
                                       f"La probabilidad de {name} debe estar entre 0.0 y 1.0")
                    return False
            
            return True
            
        except Exception as e:
            messagebox.showerror("Error de Validación", f"Error en validación: {str(e)}")
            return False