import numpy as np


# Region: Quadratic Dynamic Programming

def dynprog(alphabet, scoringMatrix, sequence1, sequence2):
    pass


# Region End

# Region: Linear Space Dynamic Programming

def dynproglin(alphabet, scoringMatrix, sequence1, sequence2):
    pass


# Region End

# Region: Heuristic Align Dynamic Programming

def heuralign(alphabet, scoringMatrix, sequence1, sequence2):
    pass


# Region End

result = dynprog("ABC",
                 [[1, -1, -2, -1],
                  [-1, 2, -4, -1],
                  [-2, -4, 3, -2],
                  [-1, -1, -2, 0]],
                 "AABBAACA",
                 "CBACCCBA")

print("Score:   ", result[0])
print("Indices: ", result[1], result[2])
