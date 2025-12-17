def count_pos(xs: list[int]) -> int:
    acc = 0
    for x in xs:
        if x > 0:
            acc += 1
    return acc


_ = count_pos([1, 0, -2, 7, 3])
