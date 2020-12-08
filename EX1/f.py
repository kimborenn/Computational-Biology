import numpy as np
import itertools


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


def NW(a, b, match_score=2, gap_cost=3):
    H = np.empty((len(a) + 1, len(b) + 1), np.int)
    H_out = np.empty((len(a) + 1, len(b) + 1), np.int)

    for i, j in itertools.product(range(0, H.shape[0]), range(0, H.shape[1])):
        if(i == 0 and j == 0):
            H[i,j] = 0
            H_out[i,j] = 0
        elif(i == 0 and j != 0):
            H[i,j] = H[i, j - 1] - gap_cost
            H_out[i,j] = 1
        elif (j == 0 and i != 0):
            H[i, j] = H[i - 1, j] - gap_cost
            H_out[i, j] = 2
        else:
            match = H[i - 1, j - 1] + (match_score if a[i - 1] == b[j - 1] else - match_score)
            delete = H[i - 1, j] - gap_cost
            insert = H[i, j - 1] - gap_cost
            H[i, j] = max(match, delete, insert)

            if (H[i, j] == match):  # match is 3, up is 2, left is 1, none is 0,
                H_out[i, j] = 3

            if (H[i, j] == delete):
                H_out[i, j] = 2

            if (H[i, j] == insert):
                H_out[i, j] = 1

    # print(H)
    return H, H_out


# Traceback function
def traceback_NW(a, b, H, H_out, i, j):
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

    return "".join(list(reversed(alignment_a))), "".join(list(reversed(alignment_b)))


def Hirschberg(a, b, match_score=2, gap_cost=3):
    Z = ""
    W = ""
    if len(a) == 0:
        for i in range(len(b)):
            Z = Z + '-'
            W = W + b[i]
    elif len(b) == 0:
        for i in range(len(a)):
            Z = Z + a[i]
            W = W + '-'
    elif len(a) == 1 or len(b) == 1:
        H, H_out = NW(a, b, match_score, gap_cost)
        Z, W = traceback_NW(a, b, H, H_out, i=len(a), j=len(b))
    else:
        amid = int(len(a) / 2)

        H, H_out = NW(a[0:amid], b)
        ScoreL = H[amid]
        H, H_out = NW(a[amid:][::-1], b[::-1])
        ScoreR = H[amid]

        row = [l + r for l, r in zip(ScoreL, ScoreR[::-1])]
        maxidx, maxval = max(enumerate(row), key=lambda a: a[1])

        bmid = maxidx

        aligned_a_left, aligned_b_left = Hirschberg(a[:amid], b[:bmid])
        aligned_a_right, aligned_b_right = Hirschberg(a[amid:], b[bmid:])
        Z = aligned_a_left + aligned_a_right
        W = aligned_b_left + aligned_b_right

    return Z, W

a, b = 'ATAAGGCATTGACCGTATTGCCAA', 'CCCATAGGTGCGGTAGCC'  # S and T

"""Collecting the borders of the sub Matrix"""
borders = SW_and_borders(a, b, match_score=2, gap_cost=3)
a_start = borders.i
b_start = borders.j
a_end = borders.current_i
b_end = borders.current_j

"""Splice the string to be the new sub strings"""
a = a[a_start:a_end]
b = b[b_start:b_end]


"""Running Hirschberg Algorithm"""
print("f. The alignment using Hirschberg's technique is:", Hirschberg(a,b), "\nand the score is: ", borders.score)





