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


# Find Borders function
def SW_and_borders(a, b, match_score=2, gap_cost=3):
    max_all = MaxCell(score=0, i=0, j=0, current_i=0, current_j=0)
    arr_first = np.empty(len(b) + 1, dtype=object)
    arr_second = np.empty(len(b) + 1, dtype=object)

    for x in range(len(arr_first)):
        arr_first[x] = Cell(score=0, i=0, j=x)

    for idx_m in range(1, len(a) + 1):
        for idx_b, c2 in enumerate(arr_second):
            if (idx_b == 0):
                arr_second[idx_b] = Cell(score=0, i=0, j=0)
            else:
                match = arr_first[idx_b - 1].score + (match_score if a[idx_m - 1] == b[idx_b - 1] else - match_score)
                delete = arr_first[idx_b].score - gap_cost
                insert = arr_second[idx_b - 1].score - gap_cost

                max_score = max(match, delete, insert, 0)

                if max_score == match:
                    c2 = Cell(score=max_score, i=arr_first[idx_b - 1].i, j=arr_first[idx_b - 1].j)
                elif max_score == delete:
                    c2 = Cell(score=max_score, i=arr_first[idx_b].i, j=arr_first[idx_b].j)
                elif max_score == insert:
                    c2 = Cell(score=max_score, i=arr_second[idx_b - 1].i, j=arr_second[idx_b - 1].j)
                elif max_score == 0:
                    c2 = Cell(score=max_score, i=0, j=0)

                if (max_all.score < max_score):
                    max_all.score = max_score
                    max_all.i = c2.i
                    max_all.j = c2.j
                    max_all.current_i = idx_m
                    max_all.current_j = idx_b

                arr_second[idx_b] = c2

        """copy the bottom array to the top one"""
        arr_first = arr_second
        arr_second = np.empty(len(b) + 1, dtype=object)
    return max_all


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

print("Borders:")
test = SW_and_borders(a, b, match_score=2, gap_cost=3)
print("The coordinate of the start are: ", test.i, ",", test.j)
print("The coordinate of the end are: ", test.current_i, ",", test.current_j)
print("The score is: ", test.score)
