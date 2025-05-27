from typing import List
from dataclasses import dataclass
import random


@dataclass
class Individual:
    """Individuo del algoritmo genético"""
    
    genes: List[int]
    fitness: float = 0.0
    
    def __post_init__(self):
        if not all(gene in [0, 1] for gene in self.genes):
            raise ValueError("Los genes deben ser 0 o 1")
    
    @classmethod
    def create_random(cls, num_bits: int) -> 'Individual':
        """Crea individuo aleatorio"""
        genes = [random.randint(0, 1) for _ in range(num_bits)]
        return cls(genes=genes)
    
    def to_decimal(self, x_min: float, x_max: float) -> float:
        """Convierte a valor decimal"""
        decimal = 0
        for bit in self.genes:
            decimal = decimal * 2 + bit
        
        max_decimal = 2**len(self.genes) - 1
        if max_decimal == 0:
            return x_min
        
        x = x_min + (decimal / max_decimal) * (x_max - x_min)
        return x
    
    def copy(self) -> 'Individual':
        """Crea copia"""
        return Individual(genes=self.genes.copy(), fitness=self.fitness)
    
    def get_binary_string(self) -> str:
        """Representación binaria como string"""
        return ''.join(map(str, self.genes))