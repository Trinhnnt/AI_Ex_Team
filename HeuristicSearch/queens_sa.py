# queens_sa.py
# Simulated Annealing (SimpleAI) cho N-Queens (N=8)
from simpleai.search import SearchProblem, simulated_annealing, hill_climbing
import random

class NQueensLocal(SearchProblem):
    def __init__(self, N=8):
        super().__init__(initial_state=tuple(random.randint(0, N-1) for _ in range(N)))
        self.N = N

    def actions(self, state):
        # trả về các trạng thái láng giềng (mỗi action là một new_state tuple)
        neighbors = []
        for col in range(self.N):
            for row in range(self.N):
                if row != state[col]:
                    new = list(state)
                    new[col] = row
                    neighbors.append(tuple(new))
        return neighbors

    def result(self, state, action):
        # action chính là trạng thái mới
        return action

    def value(self, state):
        # maximize value: số cặp không xung đột
        conflicts = 0
        for i in range(self.N):
            for j in range(i+1, self.N):
                if state[i] == state[j] or abs(state[i]-state[j]) == abs(i-j):
                    conflicts += 1
        return (self.N*(self.N-1)//2) - conflicts

def run_searches(runs=10):
    best = (None, -1, -1)  # (state, value, run)
    for r in range(runs):
        prob = NQueensLocal()
        res_sa = simulated_annealing(prob, iterations_limit=2000)
        val_sa = prob.value(res_sa.state)
        print(f"SA Run {r+1}: {res_sa.state}, Value={val_sa}")
        if val_sa > best[1]:
            best = (res_sa.state, val_sa, r+1)
    print("BEST:", best)
    if best[1] == 28:
        print("=> Nghiệm tối ưu tìm thấy bằng SA!")

if __name__ == "__main__":
    run_searches()
