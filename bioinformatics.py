# Local Alignment

# Region: Import NumPy

import numpy as np

# Region End


# Region: Quadratic Dynamic Programming

def dynprog(alphabet, scoringMatrix, sequence1, sequence2):

    # Initialise vMatrix and backTraceMatrix (all 0s)
    vMatrix = []
    backTraceMatrix = []
    for i in range(len(sequence1) + 1):
        vMatrixRow = []
        backTraceMatrixRow = []
        for j in range(len(sequence2) + 1):
            vMatrixRow.append(0)
            backTraceMatrixRow.append(["N"])
        vMatrix.append(vMatrixRow)
        backTraceMatrix.append(backTraceMatrixRow)

    # Calculate best possible score for each position
    for i in range(len(sequence1)):
        for j in range(len(sequence2)):
            (vMatrix[i+1][j+1],
             backTraceMatrix[i+1][j+1]) = dynprogScore(i+1, j+1,
                                                       alphabet,
                                                       scoringMatrix,
                                                       sequence1, sequence2,
                                                       vMatrix)

    # printMatrix(vMatrix, sequence1, sequence2)
    # printMatrix(backTraceMatrix, sequence1, sequence2)

    # Back Track for best local alignment
    # Scan for highest number in vMatrix (this is highest scoring alignment)
    bestScore = 1
    bestAlignmentStartCell = [-1, -1]
    for i in range(len(sequence1) + 1):
        for j in range(len(sequence2) + 1):
            if vMatrix[i][j] > bestScore:
                bestScore = vMatrix[i][j]
                bestAlignmentStartCell = [i, j]

    # print("bestScore: {0}".format(bestScore))
    # print("bestAlignmentStartCell: {0}".format(bestAlignmentStartCell))

    alignmentLetters1 = ""
    alignmentIndices1 = []
    alignmentLetters2 = ""
    alignmentIndices2 = []
    i, j = bestAlignmentStartCell
    # print("i: {0}".format(i))
    # print("j: {0}".format(j))
    # print("backTraceMatrix[i][j]: {0}".format(backTraceMatrix[i][j]))
    while "N" not in backTraceMatrix[i][j]:
        # If diagonal move is optimal
        if backTraceMatrix[i][j][0] == "D":
            iLetter = sequence1[i-1]
            alignmentLetters1 = iLetter + alignmentLetters1
            alignmentIndices1.insert(0, i-1)
            jLetter = sequence2[j-1]
            alignmentLetters2 = jLetter + alignmentLetters2
            alignmentIndices2.insert(0, j-1)
            i -= 1
            j -= 1
        # If up move is optimal
        elif backTraceMatrix[i][j][0] == "U":
            iLetter = sequence1[i-1]
            alignmentLetters1 = iLetter + alignmentLetters1
            jLetter = "-"
            alignmentLetters2 = jLetter + alignmentLetters2
            i -= 1
        # If left move is optimal
        elif backTraceMatrix[i][j][0] == "L":
            iLetter = "-"
            alignmentLetters1 = iLetter + alignmentLetters1
            jLetter = sequence2[j-1]
            alignmentLetters2 = jLetter + alignmentLetters2
            j -= 1

    # print("alignmentLetters1: {0}".format(alignmentLetters1))
    # print("alignmentIndices1: {0}".format(alignmentIndices1))
    # print("alignmentLetters1: {0}".format(alignmentLetters1))
    # print("alignmentIndices2: {0}".format(alignmentIndices2))

    return [bestScore, alignmentIndices1, alignmentIndices2]


# Input: Positions i and j, ...
# Output: Best score possible and backtrace move: [score, backTrace]
def dynprogScore(i, j, alphabet, scoringMatrix, sequence1, sequence2, vMatrix,
                 debug=False):

    if debug:
        printMatrix(vMatrix, sequence1, sequence2, [i, j])
    if debug:
        print("\nPosition i: {0}".format(i))
    if debug:
        print("Position j: {0}\n".format(j))

    # Diagonal Move
    vMatrixScore = vMatrix[i-1][j-1]
    if debug:
        print("vMatrixScore: {0}".format(vMatrixScore))

    iLetter = sequence1[i-1]
    iAlphabetPosition = alphabet.index(iLetter)
    jLetter = sequence2[j-1]
    jAlphabetPosition = alphabet.index(jLetter)
    matchScore = scoringMatrix[iAlphabetPosition][jAlphabetPosition]
    if debug:
        print("matchScore: {0}".format(matchScore))

    diagonalMoveScore = vMatrixScore + matchScore
    if debug:
        print("diagonalMoveScore: {0}\n".format(diagonalMoveScore))

    # Up Move
    vMatrixScore = vMatrix[i-1][j]
    if debug:
        print("vMatrixScore: {0}".format(vMatrixScore))

    iLetter = sequence1[i-1]
    iAlphabetPosition = alphabet.index(iLetter)
    jLetter = "-"
    jAlphabetPosition = len(alphabet)
    matchScore = scoringMatrix[iAlphabetPosition][jAlphabetPosition]
    if debug:
        print("matchScore: {0}".format(matchScore))

    upMoveScore = vMatrixScore + matchScore
    if debug:
        print("upMoveScore: {0}\n".format(upMoveScore))

    # Left Move
    vMatrixScore = vMatrix[i][j-1]
    if debug:
        print("vMatrixScore: {0}".format(vMatrixScore))

    iLetter = "-"
    iAlphabetPosition = len(alphabet)
    jLetter = sequence2[j-1]
    jAlphabetPosition = alphabet.index(jLetter)
    matchScore = scoringMatrix[iAlphabetPosition][jAlphabetPosition]
    if debug:
        print("matchScore: {0}".format(matchScore))

    leftMoveScore = vMatrixScore + matchScore
    if debug:
        print("leftMoveScore: {0}\n".format(leftMoveScore))

    # Start new match
    newMatchScore = 0
    if debug:
        print("newMatchScore: {0}\n".format(newMatchScore))

    bestScore = max(diagonalMoveScore,
                    upMoveScore,
                    leftMoveScore,
                    newMatchScore)
    if debug:
        print("bestScore: {0}".format(bestScore))

    backTrace = []
    if diagonalMoveScore == bestScore:
        backTrace.append("D")
    if upMoveScore == bestScore:
        backTrace.append("U")
    if leftMoveScore == bestScore:
        backTrace.append("L")
    if newMatchScore == bestScore:
        backTrace.append("N")

    if debug:
        print("backTrace: {0}\n".format(backTrace))

    return [bestScore, backTrace]


def printMatrix(matrix, sequence1, sequence2, highlightCell=[-1, -1]):

    sequence1 = list(" " + sequence1)
    sequence1.reverse()

    for letter in ("  " + sequence2):
        print("{0:<11s}".format(letter), end="")
    print("\n", end="")
    i = -1
    for row in matrix:
        print("{0:<11s}".format(str(sequence1.pop())), end="")
        i += 1
        j = -1
        for cell in row:
            j += 1
            if i == highlightCell[0] and j == highlightCell[1]:
                print("{0:<11s}".format(str(cell) + "*"), end="")
            else:
                print("{0:<11s}".format(str(cell)), end="")
        print("\n", end="")
    print()


# Region End

# Region: Linear Space Dynamic Programming

def dynproglin(alphabet, scoringMatrix, sequence1, sequence2):
    pass


# Region End

# Region: Heuristic Align Dynamic Programming

def heuralign(alphabet, scoringMatrix, sequence1, sequence2):
    pass


# Region End

tests = [["ABC",
          [[1, -1, -2, -1],
           [-1, 2, -4, -1],
           [-2, -4, 3, -2],
           [-1, -1, -2, 0]],
          "AABBAACA",
          "CBACCCBA"],

         ["ABCD",
          [[1, -5, -5, -5, -1],
           [-5, 1, -5, -5, -1],
           [-5, -5, 5, -5, -4],
           [-5, -5, -5, 6, -4],
           [-1, -1, -4, -4, -9]],
          "AAAAACCDDCCDDAAAAACC",
          "CCAAADDAAAACCAAADDCCAAAA"],

         ["ABCD",
          [[1, -5, -5, -5, -1],
           [-5, 1, -5, -5, -1],
           [-5, -5, 5, -5, -4],
           [-5, -5, -5, 6, -4],
           [-1, -1, -4, -4, -9]],
          "AACAAADAAAACAADAADAAA",
          "CDCDDD"],

         ["ABCD",
          [[1, -5, -5, -5, -1],
           [-5, 1, -5, -5, -1],
           [-5, -5, 5, -5, -4],
           [-5, -5, -5, 6, -4],
           [-1, -1, -4, -4, -9]],
          "DDCDDCCCDCAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACCCCDDDCDADCDCDCDCD",
          ("DDCDDCCCDCBCCCCDDDCDBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBDCDCD"
           "CDCD")]
         ]

for test in tests:
    result = dynprog(test[0], test[1], test[2], test[3])

    print("\nScore:   ", result[0])
    print("Indices: ", result[1], result[2])
