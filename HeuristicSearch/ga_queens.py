# ga_queens.py
# Genetic Algorithm (SimpleAI) cho N-Queens (N=8)
from simpleai.search import SearchProblem, genetic
import random

class NQueensGA(SearchProblem):
    def __init__(self, N=8):
        # trạng thái: tuple length N, state[i] = row index of queen in column i
        super().__init__(initial_state=tuple(random.randint(0, N-1) for _ in range(N)))
        self.N = N

    def actions(self, state):
        # GA không cần actions, return empty
        return []

    def result(self, state, action):
        return state

    def value(self, state):
        # fitness = số cặp không xung đột (càng lớn càng tốt)
        conflicts = 0
        for i in range(self.N):
            for j in range(i+1, self.N):
                if state[i] == state[j] or abs(state[i]-state[j]) == abs(i-j):
                    conflicts += 1
        max_pairs = self.N*(self.N-1)//2
        return max_pairs - conflicts

    def generate_random_state(self):
        return tuple(random.randint(0, self.N-1) for _ in range(self.N))

    def crossover(self, s1, s2):
        cut = random.randint(1, self.N-1)
        return s1[:cut] + s2[cut:]

    def mutate(self, s):
        lst = list(s)
        idx = random.randrange(self.N)
        lst[idx] = random.randrange(self.N)
        return tuple(lst)

def run_ga(runs=10, pop=100, mutation_chance=0.03, iterations_limit=1000):
    best_state = None
    best_val = -1
    for r in range(runs):
        prob = NQueensGA()
        res = genetic(prob, population_size=pop, mutation_chance=mutation_chance, iterations_limit=iterations_limit)
        val = prob.value(res.state)
        print(f"Run {r+1}: {res.state}, Fitness={val}/{28}")
        if val > best_val:
            best_val = val
            best_state = res.state
    print("Best found:", best_state, "Fitness:", best_val)
    if best_val == 28:
        print("=> Nghiệm tối ưu (không cặp xung đột).")

if __name__ == "__main__":
    run_ga()
