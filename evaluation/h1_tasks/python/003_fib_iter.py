def fib(n: int) -> int:
    a, b = 0, 1
    i = 0
    while i < n:
        a, b = b, a + b
        i += 1
    return a


_ = fib(20)
