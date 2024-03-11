@check
def bucketsort(arr:List[int], k:int) -> List[int]:
    from pygt2.mychecker import TypeCheckMemo
    from pygt2.mychecker._functions import check_argument_types, check_return_type
    memo = TypeCheckMemo(globals(), locals())
    check_argument_types('bucketsort', {'arr': (arr, List[int]), 'k': (k,
        int)}, memo)
    counts = [0] * k
    for x in arr:
        counts[x] += 1
    sorted_arr = []
    for i, count in enumerate(counts):
        sorted_arr.extend([i] * count)
    return check_return_type('bucketsort', sorted_arr, List[int], memo)
