def gcd(a: int, b: int) -> int:
    x, y = a, b
    while y != 0:
        x, y = y, x % y
    return x


_ = gcd(1071, 462)
