import os
from math import sqrt


# ================================================(Useful stuff)========================================================


def length(a: tuple) -> float:
    return sqrt(sum(map(lambda x: x ** 2, a)))


def dot(a: tuple, b: tuple) -> float:
    return sum(map(lambda i, j: i * j, a, b))


def distance(a: tuple, b: tuple) -> float:
    return length(tuple(map(lambda i, j: i - j, b, a)))


def normal(a: tuple) -> tuple:
    len_a = length(a)
    if len_a == 0:
        return 0, 0
    return tuple(map(lambda x: x / len_a, a))


def direction(a: tuple, b: tuple) -> tuple:
    return normal(tuple(map(lambda i, j: i - j, b, a)))


def projection(l1: tuple, l2: tuple, p: tuple) -> tuple:
    a = direction(l1, l2)
    d = dot(a, tuple(map(lambda i, j: i - j, p, l1)))
    return tuple(map(lambda i, j: i + j * d, l1, a))


def wrap(val, _min, _max):
    if _max <= _min:
        return 0
    ans = val
    dif = _max - _min + 1
    while ans < _min:
        ans = ans + dif
    while ans > _max:
        ans = ans - dif
    return ans


def apply_ndir(a: tuple, b: tuple, ndir: int) -> tuple:
    ab_dir = direction(a, b)
    return ab_dir[1] * -ndir, ab_dir[0] * ndir


def get_ndir(poly, i) -> int:
    maxI = len(poly) - 1
    p = poly[wrap(i, 0, maxI)]
    a = poly[wrap(i - 1, 0, maxI)]
    b = poly[wrap(i + 1, 0, maxI)]
    proj = projection(a, b, p)
    norm = direction(proj, p)
    applied = apply_ndir(a, b, 1)
    d = dot(norm, applied)
    return int(d / abs(d))


# ======================================================================================================================


# =========================================(Polygon dividing function)==================================================


def polygon(poly: list[tuple]) -> list[tuple]:
    # if polygon has fewer than 4 vertices it is convex, so return empty list
    if len(poly) < 4:
        return []
    # initializing some variables, where 'subPoly' is a remaining polygon after cutting some parts
    # and 'cutPoly' is a list of vertices you want to cut
    result = []
    subPoly = poly.copy()
    cutPoly = []
    # 'v' is the most left vertex, and because of that it's corresponding corner is convex and 'i' is its index
    v = min(poly, key=lambda x: x[0])
    i = poly.index(v)
    # 'ndir' is used for determining a direction algorithm goes through the polygon:
    # -1 is for clockwise and 1 is for counterclockwise
    ndir = get_ndir(poly, i)
    # current is used for remembering last concave corner
    current = ()
    # here is the loop for going through the polygon in one direction
    # where 'i' stands for index and 'v' stands for vertex
    for i, v in enumerate(poly):
        # here it checks if the corner turns in the opposite direction of that determined in 'ndir'
        # basically, it checks if the con
        if ndir == -get_ndir(poly, i):
            # if so and if there was some 'current' remembered it cuts a polygon described in 'cutPoly'
            # and loops it too using recursion
            if len(current) > 0:
                result.append((current, v))
                p = [current]
                p += cutPoly
                p.append(v)
                result += polygon(p)
                [subPoly.remove(e) for e in cutPoly]
                cutPoly.clear()
            # also, current vertex is stored to current because it is concave
            current = v
        # if concave angle was previously detected current vertex will be added to 'cutPoly'
        elif len(current) > 0:
            cutPoly.append(v)
    if len(current) > 0 and len(result) == 0:
        # if polygon has only 1 concave angle it will cut 1 triangle from polygon
        i = subPoly.index(current)
        result.append((subPoly[wrap(i + 2, 0, len(subPoly) - 1)], current))
        subPoly.remove(subPoly[wrap(i + 1, 0, len(subPoly) - 1)])
    if len(result) > 0:
        # if something was cut from polygon it will check remaining polygon recursively
        result += polygon(subPoly)
    # and after all checks it returns 'result'
    return result


# ======================================================================================================================


def main():
    poly = []
    cwd = os.getcwd()
    inf = os.path.join(cwd, input('Enter the input file: '))
    outf = os.path.join(cwd, input('Enter the output file: '))
    with open(inf, 'r') as f:
        lines = f.readlines()
        for line in lines:
            poly.append(tuple(map(float, line.split())))
    result = polygon(poly)
    lines = [f'{line[0]} {line[1]}\n' for line in result]
    with open(outf, 'w') as f:
        f.writelines(lines)


if __name__ == '__main__':
    main()
