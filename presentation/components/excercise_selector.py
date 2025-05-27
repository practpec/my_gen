"""
Componente selector de ejercicios
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable


class ExerciseSelector:
    """Selector de ejercicios"""
    
    def __init__(self, parent, controller, change_callback: Callable[[str], bool]):
        self.parent = parent
        self.controller = controller
        self.change_callback = change_callback
        
        self.selected_exercise = tk.StringVar()
        self.info_labels = {}
        
        self.create_selector()
        self.update_exercise_list()
    
    def create_selector(self):
        """Crea el selector"""
        # Frame principal
        self.main_frame = tk.LabelFrame(
            self.parent, 
            text="Seleccionar Ejercicio", 
            font=("Arial", 12, "bold"), 
            bg='white', 
            padx=10, 
            pady=10
        )
        self.main_frame.pack(fill="x", padx=10, pady=5)
        
        # Dropdown
        selector_frame = tk.Frame(self.main_frame, bg='white')
        selector_frame.pack(fill="x", pady=5)
        
        tk.Label(selector_frame, text="Ejercicio:", bg='white', 
                font=("Arial", 10, "bold")).pack(side="left")
        
        self.exercise_dropdown = ttk.Combobox(
            selector_frame, 
            textvariable=self.selected_exercise,
            state="readonly",
            width=35
        )
        self.exercise_dropdown.pack(side="right", padx=(10, 0))
        self.exercise_dropdown.bind("<<ComboboxSelected>>", self.on_exercise_changed)
        
        # Información del ejercicio
        self.info_frame = tk.LabelFrame(
            self.main_frame, 
            text="Información del Ejercicio", 
            font=("Arial", 10, "bold"), 
            bg='white'
        )
        self.info_frame.pack(fill="x", pady=(10, 0))
        
        # Crear displays de información
        self.create_info_displays()
        
        # Botón cambiar
        change_btn = tk.Button(
            self.main_frame,
            text="Cambiar Ejercicio",
            command=self.change_exercise,
            bg='#2196F3',
            fg='white',
            font=("Arial", 10, "bold")
        )
        change_btn.pack(pady=(10, 0))
    
    def create_info_displays(self):
        """Crea displays de información"""
        info_items = [
            ("Estudiante:", "student_name"),
            ("Matrícula:", "student_id"),
            ("Grupo:", "group"),
            ("Función:", "function"),
        ]
        
        for i, (label_text, key) in enumerate(info_items):
            frame = tk.Frame(self.info_frame, bg='white')
            frame.pack(fill="x", pady=1)
            
            label = tk.Label(frame, text=label_text, bg='white', width=10, anchor="w")
            label.pack(side="left")
            
            value_label = tk.Label(frame, text="...", bg='#f8f8f8', 
                                 relief="sunken", bd=1, anchor="w", 
                                 wraplength=250, justify="left")
            value_label.pack(side="right", fill="x", expand=True, padx=(5, 0))
            
            self.info_labels[key] = value_label
    
    def update_exercise_list(self):
        """Actualiza lista de ejercicios"""
        try:
            exercises = self.controller.get_available_exercises()
            self.exercise_dropdown['values'] = list(exercises.values())
            self.exercise_mapping = {v: k for k, v in exercises.items()}
            
            # Seleccionar actual
            current_info = self.controller.get_current_exercise_info()
            current_display_name = f"{current_info['student_name']} - {current_info['title']}"
            
            if current_display_name in exercises.values():
                self.selected_exercise.set(current_display_name)
            
            self.update_exercise_info()
            
        except Exception as e:
            print(f"Error actualizando ejercicios: {e}")
    
    def update_exercise_info(self):
        """Actualiza información del ejercicio"""
        try:
            info = self.controller.get_current_exercise_info()
            
            self.info_labels['student_name'].config(text=info.get('student_name', '...'))
            self.info_labels['student_id'].config(text=info.get('student_id', '...'))
            self.info_labels['group'].config(text=info.get('group', '...'))
            self.info_labels['function'].config(text=info.get('function', '...'))
            
        except Exception as e:
            print(f"Error actualizando info: {e}")
    
    def on_exercise_changed(self, event=None):
        """Callback cuando cambia selección"""
        pass  # Esperar confirmación del botón
    
    def change_exercise(self):
        """Cambia al ejercicio seleccionado"""
        selected_name = self.selected_exercise.get()
        
        if selected_name and selected_name in self.exercise_mapping:
            exercise_key = self.exercise_mapping[selected_name]
            
            if messagebox.askyesno(
                "Confirmar Cambio", 
                f"¿Cambiar al ejercicio:\n{selected_name}?\n\n"
                "Esto limpiará los resultados actuales."
            ):
                success = self.change_callback(exercise_key)
                if success:
                    self.update_exercise_info()
                else:
                    # Revertir selección
                    current_info = self.controller.get_current_exercise_info()
                    current_display = f"{current_info['student_name']} - {current_info['title']}"
                    self.selected_exercise.set(current_display)
    
    def get_main_frame(self):
        """Frame principal"""
        return self.main_frame