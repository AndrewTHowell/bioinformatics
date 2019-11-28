import numpy as np


# Basic Dynamic Programming
# Output: [score of best alignment,
#          sequence1]
def dynprog(alphabet, scoring_matrix, sequence1, sequence2):
    pass


def dynproglin(alphabet, scoring_matrix, sequence1, sequence2):
    pass


def heuralign(alphabet, scoring_matrix, sequence1, sequence2):
    pass


a = dynprog("ABC",
            [[1, -1, -2, -1],
             [-1, 2, -4, -1],
             [-2, -4, 3, -2],
             [-1, -1, -2, 0]],
            "AABBAACA",
            "CBACCCBA")

print("Score:   ", a[0])
print("Indices: ", a[1], a[2])
