# Task: compute sum(1..n)

def sum_to(n: int) -> int:
    acc = 0
    i = 1
    while i <= n:
        acc += i
        i += 1
    return acc

print(sum_to(10))
