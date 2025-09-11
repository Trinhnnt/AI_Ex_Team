# puzzle_astar.py
# A* cho 8-puzzle — so sánh 2 heuristic: h_misplaced và h_manhattan
# Save as: puzzle_astar.py
import time
from simpleai.search import SearchProblem, astar
from simpleai.search.viewers import BaseViewer

class EightPuzzleProblem(SearchProblem):
    """Trạng thái: tuple of tuples 3x3. Dùng self.goal lưu trạng thái đích."""
    def __init__(self, initial, goal, heuristic_fn):
        super().__init__(initial_state=initial)
        self.goal = goal
        self.heuristic_fn = heuristic_fn

    def actions(self, state):
        # trả về danh sách tọa độ ô sẽ hoán đổi với ô trống
        empty_i = empty_j = None
        for i in range(3):
            for j in range(3):
                if state[i][j] == 0:
                    empty_i, empty_j = i, j
                    break
            if empty_i is not None:
                break
        moves = []
        if empty_i > 0: moves.append((empty_i-1, empty_j))
        if empty_i < 2: moves.append((empty_i+1, empty_j))
        if empty_j > 0: moves.append((empty_i, empty_j-1))
        if empty_j < 2: moves.append((empty_i, empty_j+1))
        return moves

    def result(self, state, action):
        # action là tọa độ (i,j) của ô sẽ đổi chỗ với ô trống
        grid = [list(row) for row in state]
        # tìm ô trống
        empty_i = empty_j = None
        for i in range(3):
            for j in range(3):
                if grid[i][j] == 0:
                    empty_i, empty_j = i, j
                    break
            if empty_i is not None:
                break
        ti, tj = action
        grid[empty_i][empty_j], grid[ti][tj] = grid[ti][tj], grid[empty_i][empty_j]
        return tuple(tuple(r) for r in grid)

    def cost(self, state1, action, state2):
        return 1

    def is_goal(self, state):
        # *Quan trọng*: so sánh với self.goal (không dùng biến toàn cục GOAL)
        return state == self.goal

    def heuristic(self, state):
        return self.heuristic_fn(state, self.goal)

# Heuristics
def h_misplaced(state, goal):
    c = 0
    for i in range(3):
        for j in range(3):
            v = state[i][j]
            if v != 0 and v != goal[i][j]:
                c += 1
    return c

def h_manhattan(state, goal):
    # map value -> goal pos
    goal_pos = {}
    for i in range(3):
        for j in range(3):
            goal_pos[ goal[i][j] ] = (i,j)
    s = 0
    for i in range(3):
        for j in range(3):
            v = state[i][j]
            if v != 0:
                gi,gj = goal_pos[v]
                s += abs(i-gi) + abs(j-gj)
    return s

# Utils in
def print_state(state):
    for row in state:
        print(" ".join(str(x) for x in row))
    print()

def print_result(name, result, elapsed, stats):
    print(f"--- {name} ---")
    if (result is None) or (result.state is None):
        print("Không tìm thấy giải pháp")
        return
    print("Cost:", result.cost)
    print("Depth:", result.depth)
    print("Nodes expanded:", stats.get('nodes_expanded', 0))
    print("Nodes created:", stats.get('nodes_created', 0))
    print("Time (s):", round(elapsed,6))
    print("Path states:")
    # in đường đi
    n = result
    path = []
    while n is not None:
        path.append(n.state)
        n = n.parent
    path.reverse()
    for s in path:
        print_state(s)
        print("-")

if __name__ == "__main__":
    initial = ((1,2,3),(0,8,4),(7,6,5))
    goal    = ((1,2,3),(8,0,4),(7,6,5))

    print("Initial:")
    print_state(initial)
    print("Goal:")
    print_state(goal)

    # chạy với h1
    viewer1 = BaseViewer()
    p1 = EightPuzzleProblem(initial, goal, h_misplaced)
    t0 = time.time()
    res1 = astar(p1, viewer=viewer1)
    t1 = time.time()
    print_result("h1 (misplaced)", res1, t1-t0, viewer1.stats)

    # chạy với h2
    viewer2 = BaseViewer()
    p2 = EightPuzzleProblem(initial, goal, h_manhattan)
    t0 = time.time()
    res2 = astar(p2, viewer=viewer2)
    t1 = time.time()
    print_result("h2 (manhattan)", res2, t1-t0, viewer2.stats)

    # so sánh đơn giản
    print("So sánh: nodes_expanded h1 vs h2:",
          viewer1.stats.get('nodes_expanded',0),
          "vs",
          viewer2.stats.get('nodes_expanded',0))
