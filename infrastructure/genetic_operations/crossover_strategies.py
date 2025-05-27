"""
Estrategias de cruzamiento
"""

import random
from typing import Tuple

# IMPORTACIÓN ABSOLUTA (SIN ... ni ..)
from domain.entities.individual import Individual


class TwoPointCrossover:
    """Cruzamiento de dos puntos"""
    
    def crossover(self, parent1: Individual, parent2: Individual, probability: float) -> Tuple[Individual, Individual]:
        """Realiza cruzamiento de dos puntos"""
        if random.random() >= probability or len(parent1.genes) < 3:
            return parent1.copy(), parent2.copy()
        
        # Seleccionar dos puntos
        point1, point2 = sorted(random.sample(range(1, len(parent1.genes)), 2))
        
        # Crear descendencia
        child1_genes = (parent1.genes[:point1] + 
                       parent2.genes[point1:point2] + 
                       parent1.genes[point2:])
        
        child2_genes = (parent2.genes[:point1] + 
                       parent1.genes[point1:point2] + 
                       parent2.genes[point2:])
        
        return Individual(genes=child1_genes), Individual(genes=child2_genes)
    
    def get_name(self) -> str:
        return "Dos Puntos"