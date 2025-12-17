def sum_to(n: int) -> int:
    acc = 0
    i = 1
    while i <= n:
        acc += i
        i += 1
    return acc


_ = sum_to(50)
