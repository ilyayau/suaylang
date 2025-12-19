# Task: fold a small list with an accumulator

def fold3(xs: list[int]) -> int:
    if len(xs) == 3:
        a, b, c = xs
        return a + b + c
    return 0

print(fold3([10, 20, 30]))
