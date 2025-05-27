"""
Diálogo de progreso para la ejecución del algoritmo
"""

import tkinter as tk
from tkinter import ttk


class ProgressDialog:
    """Diálogo de progreso"""
    
    def __init__(self, parent, max_generations: int):
        self.parent = parent
        self.max_generations = max_generations
        self.window = None
        self.progress_bar = None
        self.progress_label = None
        self.fitness_label = None
        self.create_dialog()
    
    def create_dialog(self):
        """Crea el diálogo"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("Ejecutando Algoritmo Genético")
        self.window.geometry("450x150")
        self.window.configure(bg='#f0f0f0')
        self.window.resizable(False, False)
        
        # Centrar ventana
        self.center_window()
        
        # Modal
        self.window.transient(self.parent)
        self.window.grab_set()
        
        # Contenido
        self.create_content()
        self.window.update()
    
    def center_window(self):
        """Centra la ventana"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_content(self):
        """Crea contenido del diálogo"""
        # Título
        title_label = tk.Label(
            self.window, 
            text="Ejecutando algoritmo genético...", 
            font=("Arial", 12, "bold"), 
            bg='#f0f0f0'
        )
        title_label.pack(pady=(20, 10))
        
        # Barra de progreso
        self.progress_bar = ttk.Progressbar(
            self.window, 
            mode='determinate', 
            maximum=self.max_generations,
            length=350
        )
        self.progress_bar.pack(pady=10, padx=20)
        
        # Etiqueta de progreso
        self.progress_label = tk.Label(
            self.window, 
            text=f"Generación 0 / {self.max_generations}", 
            font=("Arial", 10), 
            bg='#f0f0f0'
        )
        self.progress_label.pack(pady=5)
        
        # Etiqueta de fitness
        self.fitness_label = tk.Label(
            self.window, 
            text="Mejor fitness: --", 
            font=("Arial", 10), 
            bg='#f0f0f0',
            fg='#666666'
        )
        self.fitness_label.pack(pady=(0, 20))
    
    def update_progress(self, generation: int, total_generations: int, best_fitness: float):
        """Actualiza el progreso"""
        if self.window and self.window.winfo_exists():
            self.progress_bar['value'] = generation
            self.progress_label.config(text=f"Generación {generation} / {total_generations}")
            self.fitness_label.config(text=f"Mejor fitness: {best_fitness:.6f}")
            self.window.update()
    
    def close(self):
        """Cierra el diálogo"""
        if self.window and self.window.winfo_exists():
            self.window.grab_release()
            self.window.destroy()
            self.window = None