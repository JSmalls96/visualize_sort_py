# implementation of bubble sort


def bubble_sort(arr):
    # list of swap position accumulated over time
    global swaps
    swaps = []

    for i in range(len(arr)):
        for k in range(len(arr)-1, i, -1):
            if arr[k] < arr[k-1]:
                swaps.append([k, k-1])
                arr[k], arr[k-1], = arr[k-1], arr[k]
    return arr, swaps

def quicksort(arr, low=0, high=None):
    global swaps
    swaps = []
    if high is None:
        high = len(arr) - 1

    def _quicksort(arr, low, high):
        global swaps
        if low >= high:
            return
        # partition index, arr[pi] is now at right place
        pi, new_swaps = partition(arr, low, high)
        swaps += new_swaps
        _quicksort(arr, low, pi - 1)
        _quicksort(arr, pi + 1, high)
    return _quicksort(arr, low, high), swaps


def partition(array, low, high):
    pivot = low
    swaps = []
    for i in range(low + 1, high + 1):
        if array[i] <= array[low]:
            pivot += 1
            array[i], array[pivot] = array[pivot], array[i]
            swaps.append([i, pivot])
    array[pivot], array[low] = array[low], array[pivot]
    swaps.append([pivot, low])
    return pivot, swaps


