from typing import List
from dataclasses import dataclass
from .individual import Individual
import statistics


@dataclass
class Population:
    """Población de individuos"""
    
    individuals: List[Individual]
    generation: int = 0
    
    def __post_init__(self):
        if not self.individuals:
            raise ValueError("La población no puede estar vacía")
    
    @classmethod
    def create_random(cls, size: int, num_bits: int, generation: int = 0) -> 'Population':
        """Crea población aleatoria"""
        individuals = [Individual.create_random(num_bits) for _ in range(size)]
        return cls(individuals=individuals, generation=generation)
    
    def get_best_individual(self) -> Individual:
        """Mejor individuo"""
        return max(self.individuals, key=lambda ind: ind.fitness)
    
    def get_best_fitness(self) -> float:
        """Mejor fitness"""
        return self.get_best_individual().fitness
    
    def get_diversity(self, x_min: float, x_max: float) -> float:
        """Diversidad de la población"""
        if len(self.individuals) < 2:
            return 0.0
        
        decimal_values = [ind.to_decimal(x_min, x_max) for ind in self.individuals]
        return statistics.stdev(decimal_values)
    
    def size(self) -> int:
        """Tamaño de población"""
        return len(self.individuals)
    
    def copy(self) -> 'Population':
        """Crea copia"""
        copied_individuals = [ind.copy() for ind in self.individuals]
        return Population(individuals=copied_individuals, generation=self.generation)
    
    def __len__(self) -> int:
        return len(self.individuals)
    
    def __iter__(self):
        return iter(self.individuals)