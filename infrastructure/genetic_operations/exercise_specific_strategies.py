"""
Estrategias específicas para el ejercicio de Julio César
"""

import random
from typing import List

# IMPORTACIONES ABSOLUTAS (SIN ... ni ..)
from domain.entities.individual import Individual
from domain.entities.population import Population


class ThresholdPairingSelection:
    """Emparejamiento con umbral PC"""
    
    def __init__(self, pc_threshold: float = 0.75):
        self.pc_threshold = pc_threshold
    
    def select(self, population: Population, num_parents: int) -> List[Individual]:
        """Selecciona individuos usando emparejamiento con umbral"""
        individuals = population.individuals
        selected = []
        
        # Mantener el mejor
        best = population.get_best_individual().copy()
        selected.append(best)
        
        # Selección con umbral
        for _ in range(num_parents - 1):
            if random.random() <= self.pc_threshold:
                individual = random.choice(individuals).copy()
                selected.append(individual)
            else:
                selected.append(best.copy())
        
        return selected
    
    def get_name(self) -> str:
        return f"Emparejamiento con Umbral (PC={self.pc_threshold})"


class ThresholdSwapMutation:
    """Mutación con umbrales PMI y PMG"""
    
    def __init__(self, pmi_threshold: float = 0.20, pmg_threshold: float = 0.15):
        self.pmi_threshold = pmi_threshold
        self.pmg_threshold = pmg_threshold
    
    def mutate(self, individual: Individual, probability: float) -> Individual:
        """Aplica mutación con umbrales"""
        mutated_genes = individual.genes.copy()
        
        # Verificar si el individuo debe mutar (PMI)
        if random.random() > self.pmi_threshold:
            return Individual(genes=mutated_genes)
        
        # Determinar qué genes van a mutar (PMG)
        genes_to_mutate = []
        for i in range(len(mutated_genes)):
            if random.random() <= self.pmg_threshold:
                genes_to_mutate.append(i)
        
        # Intercambiar genes
        if len(genes_to_mutate) >= 2:
            for _ in range(len(genes_to_mutate) // 2):
                if len(genes_to_mutate) >= 2:
                    pos1 = genes_to_mutate.pop(random.randint(0, len(genes_to_mutate) - 1))
                    pos2 = genes_to_mutate.pop(random.randint(0, len(genes_to_mutate) - 1))
                    mutated_genes[pos1], mutated_genes[pos2] = mutated_genes[pos2], mutated_genes[pos1]
        
        return Individual(genes=mutated_genes)
    
    def get_name(self) -> str:
        return f"Mutación con Umbrales (PMI={self.pmi_threshold}, PMG={self.pmg_threshold})"


class PruneWorstSelection:
    """Poda eliminando peores individuos (Truncamiento)"""
    
    def __init__(self, prune_percentage: float = 0.30, elitism_count: int = 2):
        self.prune_percentage = prune_percentage
        self.elitism_count = elitism_count
    
    def select(self, population: Population, target_size: int) -> List[Individual]:
        """
        Selecciona supervivientes usando truncamiento.
        Solo elimina individuos si la población excede el tamaño objetivo.
        """
        current_size = len(population.individuals)
        
        # Si la población no excede el tamaño objetivo, mantener todos
        if current_size <= target_size:
            return [ind.copy() for ind in population.individuals]
        
        # Si excede, aplicar truncamiento (eliminar los peores)
        # Ordenar por fitness (descendente - mejores primero)
        sorted_individuals = sorted(
            population.individuals,
            key=lambda ind: ind.fitness,
            reverse=True
        )
        
        # Calcular cuántos mantener
        # Aplicar porcentaje de poda, pero respetar elitismo y tamaño objetivo
        individuals_to_eliminate = int(current_size * self.prune_percentage)
        individuals_to_keep = current_size - individuals_to_eliminate
        
        # Asegurar que mantenemos al menos el tamaño objetivo y el elitismo
        individuals_to_keep = max(
            target_size,
            self.elitism_count,
            individuals_to_keep
        )
        
        # No podemos mantener más de los que tenemos
        individuals_to_keep = min(individuals_to_keep, current_size)
        
        # Seleccionar los mejores
        kept_individuals = sorted_individuals[:individuals_to_keep]
        
        return [ind.copy() for ind in kept_individuals]
    
    def get_name(self) -> str:
        return f"Truncamiento ({self.prune_percentage*100:.0f}% eliminación máxima)"


class StrategyFactory:
    """Factory para crear estrategias"""
    
    @classmethod
    def create_pairing_strategy(cls, strategy_name: str, params: dict):
        """Crea estrategia de emparejamiento"""
        if strategy_name == "threshold_pairing":
            return ThresholdPairingSelection(
                pc_threshold=params.get('pc_threshold', 0.75)
            )
        else:
            return ThresholdPairingSelection()
    
    @classmethod
    def create_mutation_strategy(cls, strategy_name: str, params: dict):
        """Crea estrategia de mutación"""
        if strategy_name == "threshold_swap_mutation":
            return ThresholdSwapMutation(
                pmi_threshold=params.get('pmi_threshold', 0.20),
                pmg_threshold=params.get('pmg_threshold', 0.15)
            )
        else:
            return ThresholdSwapMutation()
    
    @classmethod
    def create_selection_strategy(cls, strategy_name: str, params: dict):
        """Crea estrategia de selección"""
        if strategy_name == "prune_worst":
            return PruneWorstSelection(
                prune_percentage=params.get('prune_percentage', 0.30),
                elitism_count=params.get('elitism_count', 2)
            )
        else:
            return PruneWorstSelection()