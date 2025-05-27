"""
Función objetivo específica para Julio César
"""

import numpy as np


class JulioCesarFunction:
    """
    f(x) = ln(1 + abs(x^7)) + π cos(x) + sen(15.5x)
    OBJETIVO: Minimizar
    """
    
    def evaluate(self, x: float) -> float:
        """Evalúa función (negativo para minimizar)"""
        try:
            term1 = np.log(1 + abs(x**7))
            term2 = np.pi * np.cos(x)
            term3 = np.sin(15.5 * x)
            result = term1 + term2 + term3
            return -result  # Negativo para minimizar
        except:
            return float('-inf')
    
    def evaluate_original(self, x: float) -> float:
        """Evalúa función original (sin negativo)"""
        try:
            term1 = np.log(1 + abs(x**7))
            term2 = np.pi * np.cos(x)
            term3 = np.sin(15.5 * x)
            return term1 + term2 + term3
        except:
            return float('inf')
    
    def get_name(self) -> str:
        return "ln(1 + |x^7|) + π cos(x) + sen(15.5x)"
    
    def get_description(self) -> str:
        return "Función para minimización - Julio César Pérez Ortiz"
    
    def get_objective_type(self) -> str:
        return "minimize"


class FunctionFactory:
    """Factory para crear funciones objetivo"""
    
    @classmethod
    def create_from_exercise_config(cls, exercise_config):
        """Crea función desde configuración"""
        if "ln(1 + abs(x^7))" in exercise_config.function_expression:
            return JulioCesarFunction()
        else:
            # Función por defecto
            return JulioCesarFunction()