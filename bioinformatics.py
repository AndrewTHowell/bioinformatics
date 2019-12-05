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

    bestScore = 1
    bestAlignmentStartCell = [-1, -1]
    for i in range(len(sequence1) + 1):
        for j in range(len(sequence2) + 1):
            if vMatrix[i][j] > bestScore:
                bestScore = vMatrix[i][j]
                bestAlignmentStartCell = [i, j]

    alignmentLetters1 = ""
    alignmentIndices1 = []
    alignmentLetters2 = ""
    alignmentIndices2 = []
    i, j = bestAlignmentStartCell
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

    print("sequence1: {0}".format(sequence1))
    print("sequence2: {0}\n".format(sequence2))

    [endPointScore, endPointPosition] = F(len(sequence1), len(sequence1),
                                          alphabet, scoringMatrix,
                                          sequence1, sequence2, local=True)
    print(endPointScore, endPointPosition)
    print()

    [startPointScore, startPointPosition] = B(0, 0, alphabet, scoringMatrix,
                                              sequence1, sequence2, local=True)
    print(startPointScore, startPointPosition)

    if startPointScore != endPointScore:
        print("PROBLEM: start and end scores not equal")

    optimalSequence1 = sequence1[startPointPosition[0]:endPointPosition[0]]
    optimalSequence2 = sequence2[startPointPosition[1]:endPointPosition[1]]

    # print("\noptimalSequence1: {0}".format(optimalSequence1))
    # print("optimalSequence2: {0}".format(optimalSequence2))

    optimalAlignment = dynproglinRecurse(alphabet, scoringMatrix,
                                         optimalSequence1, optimalSequence2)

    print("optimalAlignment: {0}".format(optimalAlignment))


def dynproglinRecurse(alphabet, scoringMatrix, sequence1, sequence2):

    print("\n\nsequence1: {0}".format(sequence1))
    print("sequence2: {0}".format(sequence2))

    # Base Case
    if len(sequence2) == 1:
        # Align sequence1 with sequence2
        print("BASE CASE")

    else:
        # Find i where best alignment crosses (i, n/2)
        midpoint = len(sequence1)//2

        bestScore = 0
        bestI = -1
        for i in range(len(sequence1)+1):
            print("\ni: {0}".format(i))
            # Find best alignment score along midpoint column
            print("F:")
            fGlobalScore = F(i, midpoint, alphabet, scoringMatrix,
                             sequence1, sequence2, local=False)
            print("B:")
            bGlobalScore = B(i, midpoint, alphabet, scoringMatrix,
                             sequence1, sequence2, local=False)

            bestAlignmentScoreThroughij = fGlobalScore + bGlobalScore
            print("fGlobalScore: {0}".format(fGlobalScore))
            print("bGlobalScore: {0}".format(bGlobalScore))
            print("bestAlignmentScoreThroughij: {0}"
                  .format(bestAlignmentScoreThroughij))
            if bestAlignmentScoreThroughij > bestScore:
                bestScore = bestAlignmentScoreThroughij
                bestI = i

        F(len(sequence1), len(sequence1), alphabet, scoringMatrix,
          sequence1, sequence2, local=False)
        print("bestPosition: [{0},{1}]".format(bestI, midpoint))

        # Split sequence1 (y-axis)
        sequence1L = sequence1[:bestI]
        sequence1R = sequence1[bestI:]
        # Split sequence 2 (x-axis)
        sequence2L = sequence2[:midpoint]
        sequence2R = sequence2[midpoint:]

        # Recurse to find optimal alignments
        print("\n\n\nLEFT RECURSION WITH SEQUENCES:")
        print("sequence1L: {0}".format(sequence1L))
        print("sequence2L: {0}".format(sequence2L))
        optimalAlignmentL = dynproglinRecurse(alphabet, scoringMatrix,
                                              sequence1L, sequence2L)
        print("RIGHT RECURSION WITH SEQUENCES:")
        print("sequence1R: {0}".format(sequence1R))
        print("sequence2R: {0}".format(sequence2R))
        optimalAlignmentR = dynproglinRecurse(alphabet, scoringMatrix,
                                              sequence1R, sequence2R)

        return optimalAlignmentL + optimalAlignmentR


def F(i, j, alphabet, scoringMatrix, sequence1, sequence2, local):

    restrictedSequence1 = sequence1[:i]
    restrictedSequence2 = sequence2[:j]

    print("restrictedSequence1: {0}".format(restrictedSequence1))
    print("restrictedSequence2: {0}".format(restrictedSequence2))

    if local:
        return FBfunction(i, j, alphabet, scoringMatrix,
                          restrictedSequence1, restrictedSequence2)

    else:
        return globalFBfunction(i, j, alphabet, scoringMatrix,
                                restrictedSequence1, restrictedSequence2)


def B(i, j, alphabet, scoringMatrix, sequence1, sequence2, local):

    restrictedSequence1 = sequence1[i:]
    restrictedSequence2 = sequence2[j:]

    reversedRestrictedSequence1 = restrictedSequence1[::-1]
    reversedRestrictedSequence2 = restrictedSequence2[::-1]

    print("restrictedSequence1: {0}".format(restrictedSequence1))
    print("restrictedSequence2: {0}".format(restrictedSequence2))

    if local:
        [bestScore,
         bestScorePosition] = FBfunction(i, j, alphabet, scoringMatrix,
                                         reversedRestrictedSequence1,
                                         reversedRestrictedSequence2)

        bestScorePosition[0] = (len(reversedRestrictedSequence1)
                                - bestScorePosition[0])
        bestScorePosition[1] = (len(reversedRestrictedSequence2)
                                - bestScorePosition[1])

        return [bestScore, bestScorePosition]

    else:
        return globalFBfunction(i, j, alphabet, scoringMatrix,
                                reversedRestrictedSequence1,
                                reversedRestrictedSequence2)


def FBfunction(i, j, alphabet, scoringMatrix, sequence1, sequence2):

    # Initialise 2 rows (previous and current) (all 0s)
    rows = [[], []]
    for j in range(len(sequence2)+1):
        rows[0].append(0)
        rows[1].append(0)

    bestScore = 0
    bestScorePosition = [0, 0]
    # Calculate best possible score for each position
    print(rows[1])
    for i in range(len(sequence1)):
        rows[1][0] = 0
        for j in range(len(sequence2)):
            score = dynproglinScore(i+1, j+1, alphabet, scoringMatrix,
                                    sequence1, sequence2,
                                    rows)
            rows[1][j+1] = score

            if score > bestScore:
                bestScore = score
                bestScorePosition = [i+1, j+1]

        print(rows[1])
        rows.reverse()

    return [bestScore, bestScorePosition]


def globalFBfunction(i, j, alphabet, scoringMatrix, sequence1, sequence2):

    # Initialise 2 rows (previous and current) (all 0s)
    rows = [[], []]
    rows[0].append(0)
    for j in range(len(sequence2)):
        rows[0].append(rows[0][-1]
                       + scoringMatrix[alphabet.index(sequence2[j-1])][-1])
        rows[1].append(0)
    rows[1].append(0)

    globalScore = 0
    # Calculate best possible score for each position
    print(rows[0])
    for i in range(len(sequence1)):
        rows[1][0] = (rows[0][0]
                      + scoringMatrix[alphabet.index(sequence1[i])][-1])
        for j in range(len(sequence2)):
            score = dynproglinScore(i+1, j+1, alphabet, scoringMatrix,
                                    sequence1, sequence2,
                                    rows)
            rows[1][j+1] = score
            globalScore = score

        print(rows[1])
        rows.reverse()

    return globalScore


def dynproglinScore(i, j, alphabet, scoringMatrix, sequence1, sequence2,
                    vMatrix, debug=False):

    if debug:
        printMatrix(vMatrix, sequence1, sequence2, [i, j])
    if debug:
        print("\nPosition i: {0}".format(i))
    if debug:
        print("Position j: {0}\n".format(j))

    # Diagonal Move
    vMatrixScore = vMatrix[0][j-1]
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
    vMatrixScore = vMatrix[0][j]
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
    vMatrixScore = vMatrix[1][j-1]
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

    return bestScore


# Region End

# Region: Heuristic Align Dynamic Programming

def heuralign(alphabet, scoringMatrix, sequence1, sequence2):
    pass


# Region End

tests = [["AB",
          [[1, -1, -2],
           [-1, 1, -2],
           [-2, -2, -10]],
          "AABBAA",
          "AAABAA"],

         ["ABC",
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
    result = dynproglin(test[0], test[1], test[2], test[3])

    print("\nScore:   ", result[0])
    print("Indices: ", result[1], result[2])
