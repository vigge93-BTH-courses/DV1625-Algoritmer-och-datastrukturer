import test_code as test_code

from quicksort_inplace import quicksort_inplace
from quicksort_notinplace import quicksort_notinplace
from mergesort_inplace import mergesort_inplace
from mergesort_notinplace import mergesort_notinplace
from mergesort_notinplace_mt import mergesort_notinplace_mt
from heapsort_inplace import heapsort_inplace
from heapsort_notinplace import heapsort_notinplace


if __name__ == "__main__":

    sortfunc_list = [
        test_code.python_sort,
        quicksort_inplace,
        quicksort_notinplace,
        mergesort_inplace,
        mergesort_notinplace,
        # mergesort_notinplace_mt,
        heapsort_inplace,
        heapsort_notinplace
    ]
    test_code.create_report(sortfunc_list)
