from collections import deque

def get_successors(state):
    """
    Generates all valid successor states for the Rabbit Leap problem.
    'E' are east-bound rabbits (can only move right).
    'W' are west-bound rabbits (can only move left).
    '_' is the empty stone.
    """
    successors = []
    empty_index = state.find('_')

    # Possible moves for East-bound rabbits ('E') moving right
    # Slide right: E_ -> _E
    if empty_index > 0 and state[empty_index - 1] == 'E':
        new_state = list(state)
        new_state[empty_index], new_state[empty_index - 1] = new_state[empty_index - 1], new_state[empty_index]
        successors.append("".join(new_state))

    # Jump right: EW_ -> _WE
    if empty_index > 1 and state[empty_index - 2] == 'E' and state[empty_index - 1] == 'W':
        new_state = list(state)
        new_state[empty_index], new_state[empty_index - 2] = new_state[empty_index - 2], new_state[empty_index]
        successors.append("".join(new_state))

    # Possible moves for West-bound rabbits ('W') moving left
    # Slide left: _W -> W_
    if empty_index < len(state) - 1 and state[empty_index + 1] == 'W':
        new_state = list(state)
        new_state[empty_index], new_state[empty_index + 1] = new_state[empty_index + 1], new_state[empty_index]
        successors.append("".join(new_state))

    # Jump left: _EW -> WE_
    if empty_index < len(state) - 2 and state[empty_index + 2] == 'W' and state[empty_index + 1] == 'E':
        new_state = list(state)
        new_state[empty_index], new_state[empty_index + 2] = new_state[empty_index + 2], new_state[empty_index]
        successors.append("".join(new_state))

    return successors

def solve_with_bfs(start_state, goal_state):
    """Solves the problem using Breadth-First Search."""
    queue = deque([(start_state, [start_state])])
    visited = {start_state}
    max_queue_size = 1
    nodes_visited = 0

    while queue:
        nodes_visited += 1
        current_state, path = queue.popleft()

        if current_state == goal_state:
            return path, nodes_visited, max_queue_size

        for successor in get_successors(current_state):
            if successor not in visited:
                visited.add(successor)
                new_path = path + [successor]
                queue.append((successor, new_path))
                if len(queue) > max_queue_size:
                    max_queue_size = len(queue)

    return None, nodes_visited, max_queue_size

def solve_with_dfs(start_state, goal_state):
    """Solves the problem using Depth-First Search."""
    stack = [(start_state, [start_state])]
    visited = set()
    max_stack_size = 1
    nodes_visited = 0

    while stack:
        nodes_visited += 1
        current_state, path = stack.pop()

        if current_state == goal_state:
            return path, nodes_visited, max_stack_size
        
        # To avoid cycles in DFS
        if current_state in visited:
            continue
        visited.add(current_state)

        # We add successors in reverse to explore them in a more "natural" order
        for successor in reversed(get_successors(current_state)):
            if successor not in visited:
                new_path = path + [successor]
                stack.append((successor, new_path))
                if len(stack) > max_stack_size:
                    max_stack_size = len(stack)

    return None, nodes_visited, max_stack_size

def print_solution(algorithm, solution_path, nodes_visited, max_size):
    """Prints the formatted results for a given algorithm."""
    print(f"--- {algorithm} Solution ---")
    if solution_path:
        print("Solution found!")
        for i, state in enumerate(solution_path):
            print(f"Step {i}: {state}")
        print("\n--- Performance Metrics ---")
        print(f"Total Nodes Visited: {nodes_visited}")
        print(f"Max Size of Queue/Stack: {max_size}")
        print(f"Number of Nodes in Solution Path: {len(solution_path)}")
    else:
        print("No solution found.")
    print("-" * 25 + "\n")


if __name__ == "__main__":
    initial_state = "EEE_WWW"
    goal_state = "WWW_EEE"

    print(f"Starting Rabbit Leap puzzle from '{initial_state}' to '{goal_state}'.\n")

    # Solve with BFS
    bfs_path, bfs_nodes, bfs_max_q = solve_with_bfs(initial_state, goal_state)
    print_solution("BFS", bfs_path, bfs_nodes, bfs_max_q)

    # Solve with DFS
    dfs_path, dfs_nodes, dfs_max_s = solve_with_dfs(initial_state, goal_state)
    print_solution("DFS", dfs_path, dfs_nodes, dfs_max_s)

    # Final Comparison
    print("--- Overall Comparison ---")
    if bfs_path and dfs_path:
        print(f"BFS Solution Length: {len(bfs_path)} nodes ({len(bfs_path)-1} steps)")
        print(f"DFS Solution Length: {len(dfs_path)} nodes ({len(dfs_path)-1} steps)")
        print("\nBFS guarantees an optimal solution in terms of path length.")
        print("DFS is more memory-efficient but does not guarantee optimality, though in this case it found an optimal path.")
    else:
        print("Could not find solutions to compare.")
