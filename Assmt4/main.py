from collections import defaultdict
import heapq
from itertools import combinations

# --------------------------
# PARSER (FIXED CORRECTLY)
# --------------------------
def parse_input(file_path):
    food_cost = {}
    assignments = {}
    deps = defaultdict(list)
    inputs = set()
    g = 1

    with open(file_path, 'r') as f:
        lines = f.readlines()

    output_map = {}

    # PASS 1
    for line in lines:
        line = line.strip()
        if not line or line.startswith('%'):
            continue

        if line.startswith('C'):
            _, food, cost = line.split()
            food_cost[food] = int(cost)

        elif line.startswith('G'):
            g = int(line.split()[1])

        elif line.startswith('I'):
            parts = line.split()[1:-1]
            inputs.update(map(int, parts))

    # PASS 2
    for line in lines:
        line = line.strip()
        if line.startswith('A'):
            parts = line.split()
            aid = int(parts[1])
            output = int(parts[4])
            output_map[output] = aid

    # PASS 3
    for line in lines:
        line = line.strip()
        if line.startswith('A'):
            parts = line.split()
            aid = int(parts[1])
            in1 = int(parts[2])
            in2 = int(parts[3])
            food = parts[5]

            assignments[aid] = food

            for inp in [in1, in2]:
                if inp in output_map:
                    deps[aid].append(output_map[inp])

    return assignments, deps, food_cost, g


# --------------------------
# GREEDY 1: FOOD COST
# --------------------------
def greedy_food(assignments, deps, g, food_cost):
    done = set()
    schedule = []

    while len(done) < len(assignments):

        available = [a for a in assignments
                     if a not in done and all(d in done for d in deps[a])]

        if not available:
            raise Exception("No available assignments → dependency issue")

        # sort by actual food cost
        available.sort(key=lambda x: food_cost[assignments[x]])

        today = []
        food_used = set()

        for a in available:
            if len(today) < g:
                today.append(a)
                food_used.add(assignments[a])

        for a in today:
            done.add(a)

        schedule.append((today, food_used))

    return schedule


# --------------------------
# GREEDY 2: EARLIEST DEADLINE
# --------------------------
def greedy_earliest(assignments, deps, g):
    done = set()
    schedule = []

    while len(done) < len(assignments):

        available = [a for a in assignments
                     if a not in done and all(d in done for d in deps[a])]

        if not available:
            raise Exception("No available assignments → dependency issue")

        available.sort()

        today = available[:g]
        food_used = set(assignments[a] for a in today)

        for a in today:
            done.add(a)

        schedule.append((today, food_used))

    return schedule


# --------------------------
# PRINT SCHEDULE
# --------------------------
def print_schedule(schedule, food_cost):
    total_cost = 0

    for i, (tasks, foods) in enumerate(schedule):
        cost = sum(food_cost[f] for f in foods)
        total_cost += cost

        menu_str = ", ".join(foods)
        print(f"Day-{i+1}: {tasks} Menu: {menu_str} Cost: {cost}")

    print(f"\nTotal Days: {len(schedule)}")
    print(f"Total Cost: {total_cost}")

    return total_cost


# --------------------------
# A* HELPER
# --------------------------
def get_available(assignments, deps, done):
    return [a for a in assignments if a not in done and all(d in done for d in deps[a])]


# --------------------------
# HEURISTIC
# --------------------------
def heuristic(assignments, done, g, food_cost):
    remaining = len(assignments) - len(done)
    if remaining == 0:
        return 0

    min_food = min(food_cost.values())
    min_days = (remaining + g - 1) // g

    return min_days * min_food


# --------------------------
# A* SEARCH
# --------------------------
def astar(assignments, deps, food_cost, g):

    start = (frozenset(), [], 0)
    pq = []
    heapq.heappush(pq, (0, start))

    visited = set()
    states_explored = 0

    while pq:
        _, (done, schedule, cost_so_far) = heapq.heappop(pq)
        states_explored += 1

        if len(done) == len(assignments):
            return schedule, cost_so_far, states_explored

        if done in visited:
            continue
        visited.add(done)

        available = get_available(assignments, deps, done)

        for r in range(1, g + 1):
            for group in combinations(available, r):

                new_done = set(done)
                foods = set()

                for a in group:
                    new_done.add(a)
                    foods.add(assignments[a])

                day_cost = sum(food_cost[f] for f in foods)
                new_cost = cost_so_far + day_cost

                new_schedule = schedule + [(list(group), foods)]

                h = heuristic(assignments, new_done, g, food_cost)
                f = new_cost + h

                heapq.heappush(pq, (f, (frozenset(new_done), new_schedule, new_cost)))

    return None


# --------------------------
# PRINT A*
# --------------------------
def print_astar(schedule, food_cost, states):
    total_cost = 0

    for i, (tasks, foods) in enumerate(schedule):
        cost = sum(food_cost[f] for f in foods)
        total_cost += cost

        menu_str = ", ".join(foods)
        print(f"Day-{i+1}: {tasks} Menu: {menu_str} Cost: {cost}")

    print(f"\nTotal Days: {len(schedule)}")
    print(f"Total Cost: {total_cost}")
    print(f"States Explored: {states}")


# --------------------------
# MAIN
# --------------------------
if __name__ == "__main__":

    files = ["input1.txt", "input2.txt", "input3.txt"]

    for file_path in files:
        print(f"\n==============================")
        print(f"Running for: {file_path}")
        print(f"==============================")

        assignments, deps, food_cost, g = parse_input(file_path)

        print("\n--- Greedy by Food Cost ---")
        s1 = greedy_food(assignments, deps, g, food_cost)
        cost_greedy = print_schedule(s1, food_cost)

        print("\n--- Greedy by Earliest Deadline ---")
        s2 = greedy_earliest(assignments, deps, g)
        print_schedule(s2, food_cost)

        print("\n--- A* Optimal Schedule ---")
        schedule, cost_astar, states = astar(assignments, deps, food_cost, g)
        print_astar(schedule, food_cost, states)

        # Comparison
        print("\n--- Comparison ---")
        print(f"Greedy Cost: {cost_greedy}")
        print(f"A* Cost: {cost_astar}")
        print(f"Cost Difference: {cost_greedy - cost_astar}")
        print(f"Day Difference: {len(s1) - len(schedule)}")