"""
Caso de uso para ejecutar algoritmo genético según configuración de ejercicio
"""

from typing import Optional, Callable
from dataclasses import dataclass

# IMPORTACIONES ABSOLUTAS (SIN ... ni ..)
from domain.entities.individual import Individual
from domain.entities.population import Population
from domain.entities.ga_parameters import GAParameters
from config.exercises import ExerciseConfig, ExerciseManager
from infrastructure.genetic_operations.exercise_specific_functions import FunctionFactory
from infrastructure.genetic_operations.exercise_specific_strategies import StrategyFactory
from infrastructure.genetic_operations.crossover_strategies import TwoPointCrossover


@dataclass
class ExerciseResult:
    """Resultado de la ejecución del algoritmo genético"""
    
    best_individual: Individual
    best_x: float
    best_fitness: float
    final_population: Population
    population_history: list
    fitness_history: list
    best_fitness_history: list
    parameters: GAParameters
    total_evaluations: int
    improvement: float
    exercise_config: ExerciseConfig
    original_best_value: float
    is_minimization: bool
    
    def get_display_result(self) -> float:
        """Resultado a mostrar"""
        return self.original_best_value


class RunExerciseGeneticAlgorithm:
    """Caso de uso para ejecutar AG según ejercicio"""
    
    def __init__(self, exercise_key: str = None):
        if exercise_key:
            self.exercise_config = ExerciseManager.get_exercise(exercise_key)
        else:
            self.exercise_config = ExerciseManager.get_current_exercise()
        
        self._setup_components()
    
    def _setup_components(self):
        """Configura componentes según ejercicio"""
        # Función objetivo
        self.objective_function = FunctionFactory.create_from_exercise_config(
            self.exercise_config
        )
        
        # Estrategias
        params = self.exercise_config.strategy_params
        
        self.selection_strategy = StrategyFactory.create_pairing_strategy(
            self.exercise_config.pairing_strategy, params
        )
        
        self.crossover_strategy = TwoPointCrossover()
        
        self.mutation_strategy = StrategyFactory.create_mutation_strategy(
            self.exercise_config.mutation_strategy, params
        )
        
        self.survivor_selection = StrategyFactory.create_selection_strategy(
            self.exercise_config.selection_strategy, params
        )
    
    def execute(
        self, 
        custom_parameters: Optional[GAParameters] = None,
        progress_callback: Optional[Callable] = None
    ) -> ExerciseResult:
        """Ejecuta el algoritmo genético"""
        
        # Parámetros
        if custom_parameters:
            parameters = custom_parameters
        else:
            parameters = self._create_default_parameters()
        
        # Ejecutar algoritmo
        result = self._run_algorithm(parameters, progress_callback)
        
        # Calcular valor original
        original_value = self.objective_function.evaluate_original(result['best_x'])
        is_minimization = self.exercise_config.objective_type == "minimize"
        
        # Crear resultado extendido
        return ExerciseResult(
            best_individual=result['best_individual'],
            best_x=result['best_x'],
            best_fitness=result['best_fitness'],
            final_population=result['final_population'],
            population_history=result['population_history'],
            fitness_history=result['fitness_history'],
            best_fitness_history=result['best_fitness_history'],
            parameters=result['parameters'],
            total_evaluations=result['total_evaluations'],
            improvement=result['improvement'],
            exercise_config=self.exercise_config,
            original_best_value=original_value,
            is_minimization=is_minimization
        )
    
    def _create_default_parameters(self) -> GAParameters:
        """Crea parámetros por defecto"""
        config = self.exercise_config
        return GAParameters(
            x_min=config.x_min,
            x_max=config.x_max,
            delta_x=config.precision,
            population_size=config.default_population_size,
            num_generations=config.default_generations,
            crossover_probability=config.default_crossover_prob,
            mutation_x_probability=config.default_mutation_prob,
            mutation_g_probability=config.default_mutation_prob
        )
    
    def _run_algorithm(self, parameters: GAParameters, progress_callback=None) -> dict:
        """Ejecuta el algoritmo genético"""
        
        # Calcular bits
        num_bits = parameters.calculate_num_bits()
        
        # Población inicial
        current_population = Population.create_random(
            size=parameters.population_size,
            num_bits=num_bits,
            generation=0
        )
        
        # Historial
        population_history = []
        fitness_history = []
        best_fitness_history = []
        total_evaluations = 0
        
        # Evaluar población inicial
        self._evaluate_population(current_population, parameters)
        total_evaluations += len(current_population)
        
        # Guardar estado inicial
        initial_best_fitness = current_population.get_best_fitness()
        population_history.append(current_population.copy())
        fitness_history.append([ind.fitness for ind in current_population])
        best_fitness_history.append(initial_best_fitness)
        
        # Progreso inicial
        if progress_callback:
            progress_callback(0, parameters.num_generations, initial_best_fitness, {})
        
        # Evolución
        for generation in range(1, parameters.num_generations + 1):
            # Nueva generación
            new_population = self._create_next_generation(
                current_population, parameters, generation
            )
            
            # Evaluar
            self._evaluate_population(new_population, parameters)
            total_evaluations += len(new_population)
            
            # Supervivientes
            surviving_population = self._apply_survivor_selection(
                new_population, parameters.population_size
            )
            
            current_population = surviving_population
            current_population.generation = generation
            
            # Historial
            population_history.append(current_population.copy())
            fitness_history.append([ind.fitness for ind in current_population])
            best_fitness_history.append(current_population.get_best_fitness())
            
            # Progreso
            if progress_callback:
                progress_callback(generation, parameters.num_generations, 
                                current_population.get_best_fitness(), {})
        
        # Resultado final
        best_individual = current_population.get_best_individual()
        best_x = best_individual.to_decimal(parameters.x_min, parameters.x_max)
        
        return {
            'best_individual': best_individual,
            'best_x': best_x,
            'best_fitness': best_individual.fitness,
            'final_population': current_population,
            'population_history': population_history,
            'fitness_history': fitness_history,
            'best_fitness_history': best_fitness_history,
            'parameters': parameters,
            'total_evaluations': total_evaluations,
            'improvement': best_individual.fitness - initial_best_fitness
        }
    
    def _evaluate_population(self, population: Population, parameters: GAParameters):
        """Evalúa fitness de población"""
        for individual in population:
            x = individual.to_decimal(parameters.x_min, parameters.x_max)
            individual.fitness = self.objective_function.evaluate(x)
    
    def _create_next_generation(self, current_population: Population, parameters: GAParameters, generation: int) -> Population:
        """Crea siguiente generación"""
        
        # Selección de padres
        parents = self.selection_strategy.select(
            current_population, parameters.population_size
        )
        
        # Descendencia
        offspring = []
        
        i = 0
        while len(offspring) < parameters.population_size:
            parent1 = parents[i % len(parents)]
            parent2 = parents[(i + 1) % len(parents)]
            
            # Cruzamiento
            child1, child2 = self.crossover_strategy.crossover(
                parent1, parent2, parameters.crossover_probability
            )
            
            # Mutación
            child1 = self.mutation_strategy.mutate(child1, parameters.mutation_x_probability)
            child2 = self.mutation_strategy.mutate(child2, parameters.mutation_g_probability)
            
            offspring.append(child1)
            if len(offspring) < parameters.population_size:
                offspring.append(child2)
            
            i += 1
        
        return Population(
            individuals=offspring[:parameters.population_size],
            generation=generation
        )
    
    def _apply_survivor_selection(self, population: Population, target_size: int) -> Population:
        """Aplica selección de supervivientes"""
        survivors = self.survivor_selection.select(population, target_size)
        return Population(
            individuals=survivors[:target_size],
            generation=population.generation
        )
    
    def get_exercise_info(self) -> dict:
        """Información del ejercicio"""
        return {
            'student_name': self.exercise_config.student_name,
            'student_id': self.exercise_config.student_id,
            'group': self.exercise_config.group,
            'title': self.exercise_config.title,
            'function': self.exercise_config.function_expression,
            'interval': f"[{self.exercise_config.x_min}, {self.exercise_config.x_max}]",
            'precision': self.exercise_config.precision,
            'objective': self.exercise_config.objective_type
        }
    
    def change_exercise(self, exercise_key: str):
        """Cambia ejercicio"""
        self.exercise_config = ExerciseManager.get_exercise(exercise_key)
        self._setup_components()