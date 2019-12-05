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

def dynproglin(alphabet, scoringMatrix, sequence1, sequence2, debug=False):

    if debug:
        print("\n*************************************************************"
              "***************************************************************")
    if debug:
        print("sequence1: {0}".format(sequence1))
        print("sequence2: {0}\n".format(sequence2))

    [endPointScore, endPointPosition] = F(len(sequence1), len(sequence1),
                                          alphabet, scoringMatrix,
                                          sequence1, sequence2,
                                          debug, local=True)

    [startPointScore, startPointPosition] = B(0, 0, alphabet, scoringMatrix,
                                              sequence1, sequence2,
                                              debug, local=True)
    if debug:
        print(startPointScore, startPointPosition)
        print(endPointScore, endPointPosition)

    if startPointScore != endPointScore:
        print("PROBLEM: start and end scores not equal")

    optimalSequence1 = sequence1[startPointPosition[0]:endPointPosition[0]]
    optimalSequence2 = sequence2[startPointPosition[1]:endPointPosition[1]]

    if debug:
        print("\noptimalSequence1: {0}".format(optimalSequence1))
        print("optimalSequence2: {0}".format(optimalSequence2))

    optimalAlignment = dynproglinRecurse(alphabet, scoringMatrix,
                                         optimalSequence1, optimalSequence2,
                                         startPointPosition, debug)

    if debug:
        print("optimalAlignment: {0}".format(optimalAlignment))

    return optimalAlignment


def dynproglinRecurse(alphabet, scoringMatrix, sequence1, sequence2,
                      indexOffset, debug):

    if debug:
        print("sequence1: {0}".format(sequence1))
        print("len(sequence1): {0}".format(len(sequence1)))
        print("sequence2: {0}".format(sequence2))
        print("len(sequence2): {0}".format(len(sequence2)))
        print("indexOffset: {0}\n".format(indexOffset))

    # Base Cases
    if sequence1 == "" or sequence2 == "":
        if debug:
            print("BASE CASE: Align with Del")
        return [0, [], []]
    elif len(sequence1) <= 1 and len(sequence2) <= 1:
        if debug:
            print("BASE CASE: Align")
        return [0, [indexOffset[0]], [indexOffset[1]]]
    elif len(sequence2) == 1:
        if debug:
            print("BASE CASE: Align sequence2 letter with best in sequence1")
        bestMatch = None
        bestMatchScore = None
        for i in range(len(sequence1)):
            matchScore = (scoringMatrix[alphabet.index(sequence2[0])]
                          [alphabet.index(sequence1[i])])
            if bestMatch is None or matchScore > bestMatchSco6re:
                bestMatch = i
                bestMatchScore = matchScore
        midpoint = len(sequence1)//2
        indexOffset[0] = indexOffset[0] - midpoint
        if debug:
            print("bestMatch: {0}".format(bestMatch))
            print("bestMatchScore: {0}".format(bestMatchScore))
        return [0, [indexOffset[0] + i], [indexOffset[1]]]
    elif len(sequence1) == 1:
        if debug:
            print("BASE CASE: Align sequence1 letter with best in sequence2")
        bestMatch = None
        bestMatchScore = None
        for j in range(len(sequence2)):
            matchScore = (scoringMatrix[alphabet.index(sequence1[0])]
                          [alphabet.index(sequence2[j])])
            if bestMatch is None or matchScore > bestMatchScore:
                bestMatch = j
                bestMatchScore = matchScore
        midpoint = len(sequence2)//2
        indexOffset[1] = indexOffset[1] - midpoint
        if debug:
            print("bestMatch: {0}".format(bestMatch))
            print("bestMatchScore: {0}".format(bestMatchScore))
        return [0, [indexOffset[0]], [indexOffset[1] + j]]

    else:
        # Find i where best alignment crosses (i, n/2)
        midpoint = len(sequence1)//2

        bestScore = None
        bestI = None
        for i in range(len(sequence1)+1):
            # if debug:
            #     print("\ni: {0}".format(i))
            # Find best alignment score along midpoint column
            # if debug:
            #     print("F:")
            fGlobalScore = F(i, midpoint, alphabet, scoringMatrix,
                             sequence1, sequence2, False, local=False)
            # if debug:
            #     print("B:")
            bGlobalScore = B(i, midpoint, alphabet, scoringMatrix,
                             sequence1, sequence2, False, local=False)

            if fGlobalScore is not None and bGlobalScore is not None:
                bestAlignmentScoreThroughij = fGlobalScore + bGlobalScore
            else:
                bestAlignmentScoreThroughij = None

            # if debug:
            #     print("fGlobalScore: {0}".format(fGlobalScore))
            #     print("bGlobalScore: {0}".format(bGlobalScore))
            #     print("bestAlignmentScoreThroughij: {0}"
            #           .format(bestAlignmentScoreThroughij))

            if bestScore is None:
                bestScore = bestAlignmentScoreThroughij
                bestI = i
            if (bestAlignmentScoreThroughij is not None
                and bestAlignmentScoreThroughij > bestScore):
                bestScore = bestAlignmentScoreThroughij
                bestI = i

        bestPosition = [bestI, midpoint]
        if debug:
            print("\nbestScore: {0}".format(bestScore))
            print("bestPosition: {0}".format(bestPosition))

        # Split sequence1 (y-axis)
        sequence1L = sequence1[:bestI]
        sequence1R = sequence1[bestI:]
        # Split sequence 2 (x-axis)
        sequence2L = sequence2[:midpoint]
        sequence2R = sequence2[midpoint:]

        rIndexOffset = [indexOffset[0] + len(sequence1L),
                        indexOffset[1] + len(sequence2L)]

        # Recurse to find optimal alignments
        if debug:
            print("\nLEFT RECURSION WITH SEQUENCES:")
        optimalAlignmentL = dynproglinRecurse(alphabet, scoringMatrix,
                                              sequence1L, sequence2L,
                                              indexOffset, debug)
        if debug:
            print("\nRIGHT RECURSION WITH SEQUENCES:")
            print("indexOffset: {0}".format(indexOffset))
        optimalAlignmentR = dynproglinRecurse(alphabet, scoringMatrix,
                                              sequence1R, sequence2R,
                                              rIndexOffset, debug)

        if debug:
            print("\n**********************************")
            print("optimalAlignment: {0} + {1}".format(optimalAlignmentL[1],
                                                       optimalAlignmentR[1]))
            print("optimalAlignment: {0} + {1}".format(optimalAlignmentL[2],
                                                       optimalAlignmentR[2]))
            print("**********************************\n")

        return [bestScore, optimalAlignmentL[1] + optimalAlignmentR[1],
                optimalAlignmentL[2] + optimalAlignmentR[2]]


def F(i, j, alphabet, scoringMatrix, sequence1, sequence2, debug, local):

    restrictedSequence1 = sequence1[:i]
    restrictedSequence2 = sequence2[:j]

    if debug:
        print("restrictedSequence1: {0}".format(restrictedSequence1))
    if debug:
        print("restrictedSequence2: {0}".format(restrictedSequence2))

    if local:
        return localFBfunction(i, j, alphabet, scoringMatrix,
                               restrictedSequence1, restrictedSequence2,
                               debug)

    else:
        return globalFBfunction(i, j, alphabet, scoringMatrix,
                                restrictedSequence1, restrictedSequence2,
                                debug)


def B(i, j, alphabet, scoringMatrix, sequence1, sequence2, debug, local):

    restrictedSequence1 = sequence1[i:]
    restrictedSequence2 = sequence2[j:]

    reversedRestrictedSequence1 = restrictedSequence1[::-1]
    reversedRestrictedSequence2 = restrictedSequence2[::-1]

    if debug:
        print("restrictedSequence1: {0}".format(restrictedSequence1))
    if debug:
        print("restrictedSequence2: {0}".format(restrictedSequence2))

    if local:
        [bestScore,
         bestScorePosition] = localFBfunction(i, j, alphabet, scoringMatrix,
                                              reversedRestrictedSequence1,
                                              reversedRestrictedSequence2,
                                              debug, B=True)

        bestScorePosition[0] = (len(reversedRestrictedSequence1)
                                - bestScorePosition[0])
        bestScorePosition[1] = (len(reversedRestrictedSequence2)
                                - bestScorePosition[1])

        return [bestScore, bestScorePosition]

    else:
        return globalFBfunction(i, j, alphabet, scoringMatrix,
                                reversedRestrictedSequence1,
                                reversedRestrictedSequence2, debug)


def localFBfunction(i, j, alphabet, scoringMatrix, sequence1, sequence2,
                    debug, B=False):

    # Initialise 2 rows (previous and current) (all 0s)
    rows = [[], []]
    for j in range(len(sequence2)+1):
        rows[0].append(0)
        rows[1].append(0)

    bestScore = 0
    bestScorePosition = [0, 0]
    # Calculate best possible score for each position
    if debug:
        print(rows[1])
    for i in range(len(sequence1)):
        rows[1][0] = 0
        for j in range(len(sequence2)):
            score = dynproglinScore(i+1, j+1, alphabet, scoringMatrix,
                                    sequence1, sequence2,
                                    rows, local=True)
            rows[1][j+1] = score

            if B:
                if score >= bestScore:
                    bestScore = score
                    bestScorePosition = [i+1, j+1]
            else:
                if score > bestScore:
                    bestScore = score
                    bestScorePosition = [i+1, j+1]

        if debug:
            print(rows[1])
        rows.reverse()

    return [bestScore, bestScorePosition]


def globalFBfunction(i, j, alphabet, scoringMatrix, sequence1, sequence2,
                     debug):

    if len(sequence1) == 0 and len(sequence2) == 0:
        return None

    # Initialise 2 rows (previous and current) (all 0s)
    rows = [[], []]
    rows[0].append(0)
    for j in range(len(sequence2)):
        previousScore = rows[0][-1]
        rows[0].append(previousScore
                       + scoringMatrix[alphabet.index(sequence2[j])][-1])

    for j in range(len(sequence2)+1):
        rows[1].append(0)

    globalScore = rows[0][-1]
    # Calculate best possible score for each position
    if debug:
        print(rows[0])
    for i in range(len(sequence1)):
        previousScore = rows[0][0]
        rows[1][0] = (previousScore
                      + scoringMatrix[alphabet.index(sequence1[i])][-1])
        globalScore = rows[1][0]
        for j in range(len(sequence2)):
            score = dynproglinScore(i+1, j+1, alphabet, scoringMatrix,
                                    sequence1, sequence2,
                                    rows, local=False)
            rows[1][j+1] = score
            globalScore = score

        if debug:
            print(rows[1])
        rows.reverse()

    return globalScore


def dynproglinScore(i, j, alphabet, scoringMatrix, sequence1, sequence2,
                    vMatrix, local, debug=False):

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

    if local:
        bestScore = max(diagonalMoveScore,
                        upMoveScore,
                        leftMoveScore,
                        newMatchScore)
    else:
        bestScore = max(diagonalMoveScore,
                        upMoveScore,
                        leftMoveScore)

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
          "ABA",
          "ABA"],

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

test = tests[2]
result = dynproglin(test[0], test[1], test[2], test[3], debug=True)

print("\nScore:   ", result[0])
print("Indices:  ", result[1], result[2])
print("Expected: ",  [5, 6, 7, 8, 9, 10, 11, 12, 18, 19], [0, 1, 5, 6, 11, 12, 16, 17, 18, 19])
