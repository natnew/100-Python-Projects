import random
import string
from typing import List, Tuple

TARGET_PHRASE = "PYTHON_AGENTS_EVOLVE"
GENES = string.ascii_uppercase + "_"

class Agent:
    def __init__(self, dna: str = ""):
        if dna:
            self.dna = dna
        else:
             # Random Init
             self.dna = "".join(random.choice(GENES) for _ in range(len(TARGET_PHRASE)))
        self.fitness = 0.0

    def calc_fitness(self):
        score = 0
        for i in range(len(self.dna)):
            if self.dna[i] == TARGET_PHRASE[i]:
                score += 1
        self.fitness = score / len(TARGET_PHRASE)

    def __repr__(self):
        return f"[{self.dna}] ({self.fitness:.2f})"

class EvolutionSim:
    def __init__(self, pop_size: int = 20, mutation_rate: float = 0.05):
        self.population = [Agent() for _ in range(pop_size)]
        self.mutation_rate = mutation_rate
        self.generation = 1

    def run(self):
        print(f"🧬 Target: {TARGET_PHRASE}")
        
        while True:
            # 1. Evaluate
            for agent in self.population:
                agent.calc_fitness()
                
            # 2. Sort
            self.population.sort(key=lambda x: x.fitness, reverse=True)
            best = self.population[0]
            
            print(f"Gen {self.generation}: {best}")
            
            if best.dna == TARGET_PHRASE:
                print("🏆 Evolution Complete!")
                break
            
            if self.generation > 1000: # Safety break
                print("🚫 Max generations reached.")
                break

            # 3. Next Gen (Elitism: Keep top 20%)
            split = int(len(self.population) * 0.2)
            new_pop = self.population[:split]
            
            # 4. Fill rest
            while len(new_pop) < len(self.population):
                p1 = random.choice(self.population[:split])
                p2 = random.choice(self.population[:split])
                child = self._crossover(p1, p2)
                self._mutate(child)
                new_pop.append(child)
                
            self.population = new_pop
            self.generation += 1

    def _crossover(self, p1: Agent, p2: Agent) -> Agent:
        mid = len(p1.dna) // 2
        child_dna = p1.dna[:mid] + p2.dna[mid:]
        return Agent(child_dna)

    def _mutate(self, agent: Agent):
        chars = list(agent.dna)
        for i in range(len(chars)):
            if random.random() < self.mutation_rate:
                chars[i] = random.choice(GENES)
        agent.dna = "".join(chars)

# --- Example Usage ---

if __name__ == "__main__":
    sim = EvolutionSim(pop_size=100, mutation_rate=0.05)
    sim.run()
