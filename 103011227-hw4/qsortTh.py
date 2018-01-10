import  threading

def Partition(A, p, r):
    x = A[r]
    i = p - 1
    for j in range(p, r):
        if (A[j] <= x):
            i = i + 1
            A[i], A[j] = A[j], A[i]
    A[i+1], A[r] = A[r], A[i+1]
    return i + 1
numOfThread=0

def QuickSort(A, p, r):
    lthread = None
    rthread = None
    if threading.active_count()<10:
        if p < r:
            q = Partition(A, p, r)
            lthread = threading.Thread(target=lambda: QuickSort(A, p, q-1))
            lthread.start()
            rthread = threading.Thread(target=lambda: QuickSort(A, q+1, r))
            rthread.start()

        if lthread is not None: lthread.join()
        if rthread is not None: rthread.join()
    else:
        if p < r:
            q = Partition(A, p, r)
            QuickSort(A, p, q - 1)
            QuickSort(A, q + 1, r)

if __name__ == '__main__':
    LEN = 20000000
    L = list(range(LEN)) # in Python3, do L = list(range(LEN)) instead
    import random
    random.shuffle(L)
    QuickSort(L, 0, len(L)-1)
    if L == list(range(LEN)):  # Python3 list(range(LEN)) instead of range(LEN)
        print("successfully sorted")
    else:
        print("sort failed: %s" % L)



