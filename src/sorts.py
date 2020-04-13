# implementation of bubble sort
def bubble_sort(arr):
    # list of swap position accumulated over time
    swaps = []

    for i in range(len(arr)):
        for k in range(len(arr)-1, i, -1):
            if arr[k] < arr[k-1]:
                swaps.append([k, k-1])
                arr[k], arr[k-1], = arr[k-1], arr[k]
    return arr, swaps





