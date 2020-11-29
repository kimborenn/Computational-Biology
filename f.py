import numpy as np
import itertools


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

out_1, out_2 = Hirschberg(a, b)
print(out_1)
print(out_2)


H_needl, H_out_needl = NW(a, b) # print the 25x19 matrix

# print(H_needl)
print(traceback_NW(a, b, H_needl, H_out_needl, i=len(a), j=len(b)))
