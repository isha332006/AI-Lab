Project: Assignment Scheduling using Greedy and A* Search
Course: MA3206 - Artificial Intelligence

----------------------------------------
HOW TO RUN
----------------------------------------
1. Place all input files (input1.txt, input2.txt, input3.txt, etc.) in the same directory as the Python file.

2. Run the program using:
   python main.py

3. The program will automatically execute all test cases and print:
   - Greedy (Food Cost) schedule
   - Greedy (Earliest Deadline) schedule
   - A* Optimal schedule
   - Comparison results

----------------------------------------
GREEDY STRATEGIES IMPLEMENTED
----------------------------------------

1. Greedy by Food Cost:
   - At each step, selects assignments with lower food cost.
   - Attempts to minimize total daily menu cost.

2. Greedy by Earliest Deadline:
   - Selects assignments in topological (ID-based) order.
   - Prioritizes completing tasks as early as possible.

----------------------------------------
A* SEARCH
----------------------------------------
- A* is used to find the optimal schedule minimizing total food cost.
- Uses:
   g(n): Cost accumulated so far
   h(n): Estimated remaining cost

- Heuristic:
   h(n) = minimum food cost × minimum days required

----------------------------------------
DEPENDENCIES
----------------------------------------
- Python 3.x
- No external libraries required

----------------------------------------
FILES INCLUDED
----------------------------------------
- main.py (main code)
- input1.txt, input2.txt, input3.txt
- README.txt
- report.pdf

----------------------------------------
NOTES
----------------------------------------
- Each assignment requires one food item.
- Daily menu cost is computed as sum of distinct food items.
- Maximum group size constraint is respected.
- Dependencies between assignments are strictly enforced.

