import time
from mergesort import mergesort
from quicksort import quicksort, quicksort_random
from heapsort import heap_sort
import random

sum_merge = 0
sum_quick = 0
sum_quick_r = 0
sum_heap = 0
iterations = 10**0
n = 10**6
for i in range(iterations):
    arr1 = [random.randint(0, n*10) for x in range(n)]
    arr2 = arr1[:]
    arr3 = arr1[:]
    arr4 = arr1[:]
    # print(arr)
    t1 = time.monotonic_ns()
    mergesort(arr1, 0, len(arr1)-1)
    t2 = time.monotonic_ns()
    quicksort(arr2, 0, len(arr2)-1)
    t3 = time.monotonic_ns()
    quicksort_random(arr3, 0, len(arr3) - 1)
    t4 = time.monotonic_ns()
    heap_sort(arr4)
    t5 = time.monotonic_ns()
    # print(f'Mergesort: {(t2-t1)/10**6}ms\nQuicksort: {(t3-t2)/10**6}ms')
    sum_merge += (t2-t1)/10**6
    sum_quick += (t3-t2)/10**6
    sum_quick_r += (t4-t3)/10**6
    sum_heap += (t5-t4)/10**6

print(f'Avg mergesort: {sum_merge/iterations}ms')
print(f'Avg quicksort: {sum_quick/iterations}ms')
print(f'Avg quicksort random pivot: {sum_quick_r/iterations}ms')
print(f'Avg heapsort: {sum_heap/iterations}ms')
