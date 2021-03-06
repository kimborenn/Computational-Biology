import itertools
import numpy as np

# Matrix function
# Test Change
def SW(a, b, match_score=2, gap_cost=3):
    H = np.zeros((len(a) + 1, len(b) + 1), np.int)
    H_out = np.empty((len(a) + 1, len(b) + 1), np.int)

    global maxScore
    maxScore = 0
    global maxScore_i, maxScore_j
    for i, j in itertools.product(range(1, H.shape[0]), range(1, H.shape[1])):
        match = H[i - 1, j - 1] + (match_score if a[i - 1] == b[j - 1] else - match_score)
        delete = H[i - 1, j] - gap_cost
        insert = H[i, j - 1] - gap_cost
        H[i, j] = max(match, delete, insert, 0)

        if (H[i, j] == match):  # match is 3, up is 2, left is 1, none is 0,
            H_out[i, j] = 3

        if (H[i, j] == delete):
            H_out[i, j] = 2

        if (H[i, j] == insert):
            H_out[i, j] = 1

        if (H[i, j] == 0):
            H_out[i, j] = 0

        if (maxScore < H[i, j]):
            maxScore = H[i, j]
            maxScore_i = i
            maxScore_j = j

    print(H)
    return H, H_out

# Traceback function
def tracebackSW(H, H_out, a, b, i, j):
    alignment_a = ""
    alignment_b = ""

    while (H[i, j] != 0):
        if (H_out[i, j] == 3):
            i = i - 1
            j = j - 1
            alignment_a += a[i]
            alignment_b += b[j]
        elif (H_out[i, j] == 2):
            i = i - 1
            alignment_a += a[i]
            alignment_b += "-"
        elif (H_out[i, j] == 1):
            j = j - 1
            alignment_a += "-"
            alignment_b += b[j]
        elif (H_out[i, j] == 0):
            break

    return "".join(list(reversed(alignment_a))), "".join(list(reversed(alignment_b)))


"""class Cell that saves his ancestor coordinates"""
class Cell:
    def __init__(self, score, i, j):
        self.score = score
        self.i = i
        self.j = j


"""The maximum cell that saves his current position and his ancestor"""
class MaxCell:
    def __init__(self, score, i, j, current_i, current_j):
        self.score = score
        self.i = i
        self.j = j
        self.current_i = current_i
        self.current_j = current_j




a, b = 'ATAAGGCATTGACCGTATTGCCAA', 'CCCATAGGTGCGGTAGCC'  # S and T

print("\na. The matrix of values:\n")

H, H_out = SW(a, b)  # print the 25x19 matrix

print("\nThe maximum score is: ", H[maxScore_i, maxScore_j])

print("\nb.+c.  The alignment is:\n")

print(tracebackSW(H, H_out, a, b, maxScore_i, maxScore_j))

print("\nd. Another alignment that doesn't overlap the first one (i=17, j =15)\n")

print(tracebackSW(H, H_out, a, b, 17, 15))

print("\ne. There are alignments that overlap each other: \n")
print("ATAAGG\nAT_AGG\nand\nATAAGG\nATA_GG")


