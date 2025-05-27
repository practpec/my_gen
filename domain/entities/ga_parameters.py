from dataclasses import dataclass
import numpy as np


@dataclass
class GAParameters:
    """Parámetros del algoritmo genético"""
    
    x_min: float
    x_max: float
    delta_x: float
    population_size: int
    num_generations: int
    crossover_probability: float
    mutation_x_probability: float
    mutation_g_probability: float
    
    def __post_init__(self):
        if self.x_min >= self.x_max:
            raise ValueError("x_min debe ser menor que x_max")
        if self.delta_x <= 0:
            raise ValueError("delta_x debe ser mayor que 0")
        if self.population_size <= 0:
            raise ValueError("population_size debe ser mayor que 0")
    
    def calculate_num_bits(self) -> int:
        """Calcula número de bits necesarios"""
        if self.x_min == 0 and self.x_max == 31 and self.delta_x == 1.0:
            return 5
        elif self.x_min >= 0 and self.x_max == int(self.x_max) and self.delta_x == 1.0:
            range_size = int(self.x_max - self.x_min) + 1
            return int(np.ceil(np.log2(range_size)))
        else:
            num_divisions = int((self.x_max - self.x_min) / self.delta_x)
            return int(np.ceil(np.log2(num_divisions + 1)))
    
    def calculate_max_decimal(self) -> int:
        """Valor decimal máximo"""
        num_bits = self.calculate_num_bits()
        return 2**num_bits - 1
    
    def calculate_actual_precision(self) -> float:
        """Precisión real alcanzable"""
        max_decimal = self.calculate_max_decimal()
        return (self.x_max - self.x_min) / max_decimal if max_decimal > 0 else 0.0
    
    def calculate_num_points(self) -> int:
        """Número de puntos discretos en el intervalo"""
        return int((self.x_max - self.x_min) / self.delta_x) + 1