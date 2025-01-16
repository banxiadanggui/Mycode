import math 
import numpy as np

class GeneticTSP:
    def __init__(self, cities, pop_size=100, mutation_rate=0.01, generations=1000):
        self.cities = cities
        self.pop_size = pop_size
        self.mutation_rate = mutation_rate
        self.generations = generations
        self.num_cities = len(cities)
        self.population = [np.random.permutation(self.num_cities) for _ in range(self.pop_size)]
        self.dist_matrix = self.calculate_distance_matrix()
    
    def calculate_distance_matrix(self):
        num_cities = len(self.cities)
        dist_matrix = np.zeros((num_cities, num_cities))
        for i in range(num_cities):
            for j in range(i+1, num_cities):
                dist_matrix[i][j] = np.linalg.norm(self.cities[i] - self.cities[j])
                dist_matrix[j][i] = dist_matrix[i][j]
        return dist_matrix
    
    def fitness(self, route):
        total_distance = 0
        for i in range(self.num_cities - 1):
            total_distance += self.dist_matrix[route[i], route[i+1]]
        total_distance += self.dist_matrix[route[-1], route[0]]  # Return to starting city
        return 1 / total_distance  # Lower distance means higher fitness
    
    def selection(self):
        fitnesses = np.array([self.fitness(ind) for ind in self.population])
        probabilities = fitnesses / fitnesses.sum()
        idx = np.random.choice(np.arange(self.pop_size), size=self.pop_size, p=probabilities)
        return [self.population[i] for i in idx]
    
    def crossover(self, parent1, parent2):
        start, end = sorted(np.random.randint(0, self.num_cities, 2))        
        # Initialize child with a slice from parent1
        child = [-1] * self.num_cities
        child[start:end] = parent1[start:end]
        # Fill the rest with the cities from parent2 in the order they appear, skipping cities already in the child
        current_pos = end
        for city in parent2:
            if city not in child:
                if current_pos >= self.num_cities:
                    current_pos = 0
                child[current_pos] = city
                current_pos += 1        
        return np.array(child)
    
    def mutate(self, route):
        if np.random.rand() < self.mutation_rate:
            i, j = np.random.randint(0, self.num_cities, 2)
            route[i], route[j] = route[j], route[i]  # Swap two cities
        return route
    
    def evolve_population(self):
        selected_population = self.selection()
        sorted_population = sorted(self.population, key=lambda x: self.fitness(x), reverse=True)
        elite_count = 10 
        next_generation = sorted_population[:elite_count]        
        for i in range(elite_count, self.pop_size, 2):
            parent1, parent2 = selected_population[i % self.pop_size], selected_population[(i + 1) % self.pop_size]
            child1 = self.mutate(self.crossover(parent1, parent2))
            child2 = self.mutate(self.crossover(parent2, parent1))
            next_generation.append(child1)
            next_generation.append(child2)        
        self.population = next_generation[:self.pop_size]
    
    def find_best_route(self):
        for _ in range(self.generations):
            self.evolve_population()
        
        best_route = max(self.population, key=lambda x: self.fitness(x))
        best_distance = 1 / self.fitness(best_route)
        return best_route, best_distance

np.random.seed(6100)
N=50
# cities = np.random.rand(N, 2) * 100  # Random cities on a 100x100 grid
xs=np.sin(np.linspace(0.0,2*math.pi,N))
ys=np.cos(np.linspace(0.0,2*math.pi,N))
cities=np.array([xs,ys]).T
tsp_solver = GeneticTSP(cities)
best_route, best_distance = tsp_solver.find_best_route()
print("Best route:", best_route)
print("Best distance:", best_distance)