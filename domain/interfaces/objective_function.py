from typing import Protocol


class ObjectiveFunction(Protocol):
    """Interface para funciones objetivo"""
    
    def evaluate(self, x: float) -> float:
        """Evalúa la función objetivo en x"""
        ...
    
    def get_name(self) -> str:
        """Nombre de la función"""
        ...
    
    def get_description(self) -> str:
        """Descripción de la función"""
        ...