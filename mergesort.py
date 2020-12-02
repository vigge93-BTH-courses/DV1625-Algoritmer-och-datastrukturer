"""Mergesort algorithms."""
import math
import random


def merge(A, p, q, r):
    """Split A at q and merge together in order."""
    n_1 = q-p+1
    n_2 = r-q
    L = []
    R = []
    for i in range(n_1):
        L.append(A[p+i])
    for j in range(n_2):
        R.append(A[q+j+1])
    L.append(math.inf)
    R.append(math.inf)
    i = 0
    j = 0
    for k in range(p, r+1):
        if L[i] <= R[j]:
            A[k] = L[i]
            i += 1
        else:
            A[k] = R[j]
            j += 1


def merge_in_place(A, p, q, r):
    """Split A at q and merge together in order."""
    n_1 = q - p + 1
    n_2 = r - q
    L = 0
    R = 0
    for k in range(p, r+1):
        if A[p] <= A[q + 1]:
            A.insert(r+1, A[p])
            del A[p]
            L += 1
            q -= 1
        else:
            A.insert(r+1, A[q+1])
            del A[q+1]
            R += 1

        if L == n_1:
            A[r+1:r+1] = A[p:p+n_2-R]
            del A[p:p+n_2-R]
            break

        if R == n_2:
            A[r+1:r+1] = A[p:q+1]
            del A[p:q+1]
            break


def mergesort(A, p, r):
    """Sort array elements in A between p and r using mergesort."""
    if p < r:
        q = (p+r)//2
        mergesort(A, p, q)
        mergesort(A, q + 1, r)
        merge(A, p, q, r)


def mergesort_ip(A, p, r):
    """Sort array elements in A between p and r using mergesort inplace."""
    if p < r:
        q = (p+r)//2
        mergesort(A, p, q)
        mergesort(A, q + 1, r)
        merge_in_place(A, p, q, r)


if __name__ == "__main__":
    n = 11
    arr = [random.randint(0, n*10) for x in range(n)]
    mergesort(arr, 0, len(arr)-1)
    print(arr)
