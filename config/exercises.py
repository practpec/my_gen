
from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class ExerciseConfig:
    """Configuración de un ejercicio específico"""
    
    student_name: str
    student_id: str
    group: str
    title: str
    
    function_expression: str
    function_description: str
    objective_type: str  # 'minimize' o 'maximize'
    
    x_min: float
    x_max: float
    precision: float
    
    pairing_strategy: str
    crossover_strategy: str
    mutation_strategy: str
    selection_strategy: str
    
    strategy_params: Dict[str, Any]
    
    default_population_size: int = 20
    default_generations: int = 100
    default_crossover_prob: float = 0.8
    default_mutation_prob: float = 0.1


# Ejercicio específico de Julio César
EXERCISE_JULIO_CESAR = ExerciseConfig(
    student_name="PEREZ ORTIZ JULIO CESAR",
    student_id="223189",
    group="08B",
    title="Minimización con estrategias específicas",
    
    function_expression="ln(1 + abs(x^7)) + π cos(x) + sen(15.5x)",
    function_description="Función logarítmica con componentes trigonométricas",
    objective_type="minimize",
    
    x_min=6.30,
    x_max=15.30,
    precision=0.05,
    
    pairing_strategy="threshold_pairing",
    crossover_strategy="two_point_crossover",
    mutation_strategy="threshold_swap_mutation",
    selection_strategy="prune_worst",
    
    strategy_params={
        'pc_threshold': 0.75,
        'pmi_threshold': 0.20,
        'pmg_threshold': 0.15,
        'prune_percentage': 0.30,
        'elitism_count': 2,
    },
    
    default_population_size=25,
    default_generations=150,
    default_crossover_prob=0.75,
    default_mutation_prob=0.20,
)


class ExerciseManager:
    """Gestor de ejercicios"""
    
    AVAILABLE_EXERCISES = {
        'julio_cesar': EXERCISE_JULIO_CESAR,
    }
    
    @classmethod
    def get_exercise(cls, exercise_key: str) -> ExerciseConfig:
        """Obtiene configuración de ejercicio"""
        return cls.AVAILABLE_EXERCISES[exercise_key]
    
    @classmethod
    def get_current_exercise(cls) -> ExerciseConfig:
        """Obtiene ejercicio actual"""
        return cls.get_exercise('julio_cesar')
    
    @classmethod
    def list_exercises(cls) -> Dict[str, str]:
        """Lista ejercicios disponibles"""
        return {
            key: f"{config.student_name} - {config.title}"
            for key, config in cls.AVAILABLE_EXERCISES.items()
        }