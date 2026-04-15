from copy import deepcopy
backtracking_moves = 0


# ------------------------------------------
# Read Sudoku board from file
# ------------------------------------------
def read_board(filename):
    board = []
    with open(filename, "r") as file:
        for line in file:
            board.append([int(num) for num in line.strip()])
    return board


def print_board(board):
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("-" * 21)

        for j in range(9):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")

            print(board[i][j], end=" ")

        print()
    print()


# ------------------------------------------
# Getting all neighbors for each cell
# ------------------------------------------
def get_neighbors():
    neighbors = {}

    for row in range(9):
        for col in range(9):
            cell = (row, col)
            neighbors[cell] = set()

            # Same row and column
            for i in range(9):
                if i != col:
                    neighbors[cell].add((row, i))
                if i != row:
                    neighbors[cell].add((i, col))

            # Same 3x3 box
            start_row = (row // 3) * 3
            start_col = (col // 3) * 3

            for r in range(start_row, start_row + 3):
                for c in range(start_col, start_col + 3):
                    if (r, c) != cell:
                        neighbors[cell].add((r, c))

    return neighbors


NEIGHBORS = get_neighbors()


# ------------------------------------------
# Initializing domains
# ------------------------------------------
def initialize_domains(board):
    domains = {}

    for row in range(9):
        for col in range(9):
            if board[row][col] != 0:
                domains[(row, col)] = {board[row][col]}
            else:
                domains[(row, col)] = set(range(1, 10))

    return domains


# ------------------------------------------
# AC-3
# ------------------------------------------
def revise(domains, xi, xj):
    revised = False

    if len(domains[xj]) == 1:
        value = next(iter(domains[xj]))

        if value in domains[xi]:
            domains[xi].remove(value)
            revised = True

    return revised


# ------------------------------------------
# AC-3 Algorithm
# ------------------------------------------
def ac3(domains):
    queue = []

    for cell in domains:
        for neighbor in NEIGHBORS[cell]:
            queue.append((cell, neighbor))

    while queue:
        xi, xj = queue.pop(0)

        if revise(domains, xi, xj):
            if len(domains[xi]) == 0:
                return False

            for neighbor in NEIGHBORS[xi]:
                if neighbor != xj:
                    queue.append((neighbor, xi))

    return True


# ------------------------------------------
# Check complete assignment
# ------------------------------------------
def is_complete(domains):
    return all(len(domains[cell]) == 1 for cell in domains)


# ------------------------------------------
# Select unassigned variable (MRV)
# ------------------------------------------
def select_unassigned_variable(domains):
    unassigned = [cell for cell in domains if len(domains[cell]) > 1]
    return min(unassigned, key=lambda cell: len(domains[cell]))


# ------------------------------------------
# Forward Checking
# ------------------------------------------
def forward_check(domains, cell, value):
    for neighbor in NEIGHBORS[cell]:
        if value in domains[neighbor]:
            domains[neighbor].discard(value)

            if len(domains[neighbor]) == 0:
                return False

    return True


# ------------------------------------------
# Backtracking Search
# ------------------------------------------
def backtrack(domains):
    global backtracking_moves
    backtracking_moves += 1

    if is_complete(domains):
        return domains

    cell = select_unassigned_variable(domains)

    for value in sorted(domains[cell]):
        new_domains = deepcopy(domains)
        new_domains[cell] = {value}

        if forward_check(new_domains, cell, value):
            if ac3(new_domains):
                result = backtrack(new_domains)

                if result:
                    return result

    return None


# ------------------------------------------
# Convert domains to board
# ------------------------------------------
def domains_to_board(domains):
    board = [[0] * 9 for _ in range(9)]

    for (row, col), value in domains.items():
        board[row][col] = next(iter(value))

    return board


# ------------------------------------------
# Solve Sudoku
# ------------------------------------------
def solve_sudoku(board):
    global backtracking_moves
    backtracking_moves = 0

    domains = initialize_domains(board)

    if not ac3(domains):
        return None

    solution = backtrack(domains)

    if solution:
        return domains_to_board(solution)

    return None


# ==========================================
# MAIN 
# ==========================================
if __name__ == "__main__":

    while True:
        print("---------------------------------------")
        print("      CSP Based Sudoku Solver")
        print("---------------------------------------")
        print("1. Easy")
        print("2. Medium")
        print("3. Hard")
        print("4. Very Hard")
        print("5. Exit")
        print("---------------------------------------")

        choice = input("Enter your choice (1-5): ")

        match choice:
            case "1":
                filename = "easy.txt"
            case "2":
                filename = "medium.txt"
            case "3":
                filename = "hard.txt"
            case "4":
                filename = "veryhard.txt"
            case "5":
                print("Exiting program...")
                break
            case _:
                print("Invalid choice! Please try again.\n")
                continue

        print(f"\nReading puzzle from: {filename}\n")

        board = read_board(filename)

        print("Original Sudoku Board:")
        print_board(board)

        solution = solve_sudoku(board)

        if solution:
            print("Solved Sudoku Board:")
            print_board(solution)
        else:
            print("No solution found.")

        print(f"Backtracking moves taken: {backtracking_moves}\n")
        print(f"\n\nDeveloped by Muhammad Luqman @23F-0640")
