import itertools
import numpy as np


def LongestCommonSubstring_2Mismatches(a, b, k=2):
    n = len(a)
    m = len(b)
    l = 0
    global r_1
    global r_2
    r_1 = 0
    r_2 = 0
    Q = []

    for d in range(-m+1, n-1):
        i = max(-d,0) + d
        j = max(-d,0)
        Q.clear()
        s = 0
        p = 0

        while(p <= min(n-i, m-j) - 1):
            if(a[i+p] != b[j+p]):
                if(len(Q) == k):
                    s = min(Q) + 1
                    Q.pop(0)
                Q.append(p)
            p = p + 1
            if(p - s > l):
                l = p - s
                r_1 = i + s
                r_2 = j + s

    print("\n\n\n l: ",l)



def LongestCommonSubstring(a, b):
    H = np.zeros((len(a) + 1, len(b) + 1), np.int)

    global maxScore, maxScore_i, maxScore_j
    maxScore = 0

    for i, j in itertools.product(range(1, H.shape[0]), range(1, H.shape[1])):

        if(a[i-1] == b[j-1]):
            H[i, j] = H[i-1, j-1] + 1
        else:
            H[i, j] = 0

        if(H[i, j] > maxScore):
            maxScore = H[i, j]
            maxScore_i = i
            maxScore_j = j

    subString = ""
    for idx in range(maxScore):
        subString += a[maxScore_i - 1]
        maxScore_i -= 1



    print("The matrix is: \n", H)
    print("\nand the longest common sub string is: ", subString[::-1]) #[::-1] to reverse the traceback
    return H


#a, b = "ABCDE", "AFGHI"
a, b = 'ATAAGGCATTGACCGTATTGCCAA', 'CCCATAGGTGCGGTAGCC'
LongestCommonSubstring(a, b)

LongestCommonSubstring_2Mismatches(a,b)