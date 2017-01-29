# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: In order to solve the naked twins problem we search the units looking for boxes where there are only two remaining possible values. Upon finding such a box, we compare it to the other boxes in the group to see if there is another box with only those possible solutions as well. If there is one, then we know that those two numbers must be in those two boxes and not in any other boxes within the group. Thus, we can then remove the two numbers from the possible solutions for the other boxes in the group.

Continuing this idea, it seems like we could extend it to n-tuplets if you will. As long as you have n-boxes sharing the same n-numbers you know that those numbers cannot be in the other boxes and could therefore remove them from the other boxes in the group. Beyond 3 numbers though, it seems like this would be an uncommon occurrence.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: We can use constraint propagation to solve the diagonal sudoku by viewing the diagonals as additional units. Simply creating a lits of the two diagonals and appending it to the list of other units enforces the diagonal constraint while running our solver.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project.
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solution.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.
