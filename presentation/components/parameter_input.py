"""
Panel mejorado para entrada de parámetros con mejor distribución del espacio
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
        """Crea el panel de parámetros con distribución mejorada"""
        # Frame principal dividido en 3 columnas
        main_frame = tk.Frame(self.parent, bg='white')
        main_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Configurar columnas con pesos específicos
        main_frame.grid_columnconfigure(0, weight=1)  # Columna 1: Parámetros básicos
        main_frame.grid_columnconfigure(1, weight=1)  # Columna 2: Parámetros avanzados  
        main_frame.grid_columnconfigure(2, weight=1)  # Columna 3: Info calculada + botón
        
        self.create_basic_parameters(main_frame)
        self.create_advanced_parameters(main_frame) 
        self.create_calculated_and_execute(main_frame)
    
    def create_basic_parameters(self, parent):
        """Parámetros básicos en columna 1"""
        basic_frame = tk.LabelFrame(parent, text="⚙️ Parámetros Básicos", 
                                   font=("Arial", 11, "bold"), bg='white')
        basic_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Objetivo (Combobox)
        self.create_objective_selector(basic_frame)
        
        # Intervalo y precisión
        self.create_compact_entry(basic_frame, "🎯 Intervalo A:", self.interval_a, width=8)
        self.create_compact_entry(basic_frame, "🎯 Intervalo B:", self.interval_b, width=8)
        self.create_compact_entry(basic_frame, "📏 Precisión Δx:", self.delta_x, width=8)
        
        # Población y generaciones
        self.create_compact_entry(basic_frame, "👥 Población:", self.pop_size, width=8)
        self.create_compact_entry(basic_frame, "🔄 Generaciones:", self.num_generations, width=8)
    
    def create_advanced_parameters(self, parent):
        """Parámetros avanzados en columna 2"""
        advanced_frame = tk.LabelFrame(parent, text="🔬 Parámetros Avanzados", 
                                      font=("Arial", 11, "bold"), bg='white')
        advanced_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
        # Probabilidades con mejor espaciado
        self.create_compact_entry(advanced_frame, "🔗 Prob. Cruzamiento:", self.prob_crossover, width=8)
        self.create_compact_entry(advanced_frame, "🧬 Prob. Mutación X:", self.prob_mutation_x, width=8)
        self.create_compact_entry(advanced_frame, "🧬 Prob. Mutación G:", self.prob_mutation_g, width=8)
        
        # # Espacio para estrategias info
        # self.create_strategies_info(advanced_frame)
    
    def create_calculated_and_execute(self, parent):
        """Información calculada y botón ejecutar en columna 3"""
        calc_frame = tk.LabelFrame(parent, text="📊 Info Calculada & Control", 
                                  font=("Arial", 11, "bold"), bg='white')
        calc_frame.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
        
        # Información calculada compacta
        self.create_compact_info(calc_frame, "🔢 # Puntos:", self.num_points)
        self.create_compact_info(calc_frame, "💾 # Bits:", self.num_bits)
        self.create_compact_info(calc_frame, "🔝 Máx. Decimal:", self.max_decimal)
        
        # Separador
        tk.Frame(calc_frame, height=10, bg='white').pack(pady=5)
        
        # # Botón ejecutar (prominente)
        # self.execute_btn = tk.Button(calc_frame, text="🚀 EJECUTAR\nALGORITMO", 
        #                             command=self.execute_algorithm,
        #                             bg='#4CAF50', fg='white', 
        #                             font=("Arial", 11, "bold"),
        #                             height=3, width=15)
        # self.execute_btn.pack(pady=10, padx=5)
    
    def create_objective_selector(self, parent):
        """Selector de objetivo compacto"""
        frame = tk.Frame(parent, bg='white')
        frame.pack(fill="x", pady=3, padx=5)
        
        tk.Label(frame, text="🎯 Objetivo:", bg='white', 
                font=("Arial", 9, "bold"), width=12, anchor="w").pack(side="left")
        
        objective_combo = ttk.Combobox(frame, textvariable=self.objective_type,
                                      values=["minimize", "maximize"],
                                      state="readonly", width=10)
        objective_combo.pack(side="right")
        objective_combo.bind("<<ComboboxSelected>>", self.on_objective_changed)
    
    def create_compact_entry(self, parent, label: str, variable, width=8):
        """Crea entrada compacta"""
        frame = tk.Frame(parent, bg='white')
        frame.pack(fill="x", pady=2, padx=5)
        
        tk.Label(frame, text=label, bg='white', 
                font=("Arial", 9, "bold"), width=12, anchor="w").pack(side="left")
        
        entry = tk.Entry(frame, textvariable=variable, width=width, 
                        font=("Arial", 9), relief="solid", bd=1)
        entry.pack(side="right")
        return entry
    
    def create_compact_info(self, parent, label: str, variable):
        """Crea display de información compacto"""
        frame = tk.Frame(parent, bg='white')
        frame.pack(fill="x", pady=2, padx=5)
        
        tk.Label(frame, text=label, bg='white', 
                font=("Arial", 9, "bold"), width=12, anchor="w").pack(side="left")
        
        info_label = tk.Label(frame, textvariable=variable, bg='#e3f2fd', 
                             relief="solid", bd=1, width=8, 
                             font=("Arial", 9, "bold"), fg='#1976d2')
        info_label.pack(side="right")
    
    def create_strategies_info(self, parent):
        """Información compacta de estrategias"""
        info_frame = tk.LabelFrame(parent, text="🛠️ Estrategias", 
                                  font=("Arial", 10, "bold"), bg='white')
        info_frame.pack(fill="x", pady=10, padx=5)
        
        try:
            strategies = self.controller.get_strategy_summary()
            
            info_text = f"• Emparejamiento: {strategies['emparejamiento']}\n"
            info_text += f"• Mutación: {strategies['mutacion']}\n" 
            info_text += f"• Selección: {strategies['seleccion']}"
            
            info_label = tk.Label(info_frame, text=info_text, bg='white',
                                 font=("Arial", 8), justify="left", wraplength=150)
            info_label.pack(pady=5, padx=5)
        except:
            tk.Label(info_frame, text="Estrategias cargadas", bg='white',
                    font=("Arial", 8)).pack(pady=5)
    
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