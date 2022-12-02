def comb(arr, length, chosen = [], start = 0):
    if len(chosen) == length:
        return print(chosen)

    for i in range(start, len(arr)):
        chosen.append(arr[i])
        comb(arr, length, chosen, start)
        start += 1
        chosen.pop()

comb([1, 2, 3, 4], 3)