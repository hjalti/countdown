import operator
import re
from collections import Counter

ADD = operator.add
SUB = operator.sub
MUL = operator.mul
DIV = operator.floordiv

OPERS = [ADD, SUB, MUL, DIV]

SYMBOLS = {
    ADD: '+',
    SUB: '-',
    MUL: '*',
    DIV: '/',
}

PAREN = {
    ADD: (False, False),
    SUB: (False, True),
    MUL: (True, True),
    DIV: (True, True),
}

def complexity(expr):
    if isinstance(expr, tuple):
        op, lef, rig = expr
        return 1 + complexity(lef) + complexity(rig)
    else:
        return 1

def display(expr, paren=False):
    if isinstance(expr, tuple):
        op, lef, rig = expr
        plef, prig = PAREN[op]
        res = f'{display(lef, plef)} {SYMBOLS[op]} {display(rig, prig)}'
        if paren:
            res = f'({res})'
        return res
    else:
        return str(expr)

def slv(numbers, target):
    return solve(Counter(numbers), target, 0, None)

def solve(numbers, target, curr, expr):
    res = []
    if expr is None:
        for n in [x for x,y in numbers.items() if y]:
            updated = Counter(numbers)
            updated[n] -= 1
            res.extend(solve(updated, target, n, n))
        return res
    for n in [x for x,y in numbers.items() if y]:
        for op in OPERS:
            if n > curr:
                new = op(n, curr)
                new_expr = (op, n, expr)
            else:
                new = op(curr, n)
                new_expr = (op, expr, n)

            if new == 0:
                continue

            if op is operator.floordiv and max(n, curr) != new * min(n, curr):
                continue

            if new == target:
                res.append(new_expr)
                continue

            updated = Counter(numbers)
            updated[n] -= 1

            res.extend(solve(updated, target, new, new_expr))

    if curr < target:
        tmp = solve(numbers, target - curr, 0, None)
        for ex in tmp:
            res.append( (ADD, ex, expr) )

    if curr > target:
        tmp = solve(numbers, curr - target, 0, None)
        for ex in tmp:
            res.append( (SUB, expr, ex) )

    if target % curr == 0:
        tmp = solve(numbers, target // curr, 0, None)
        for ex in tmp:
            res.append( (MUL, ex, expr) )

    if curr % target == 0:
        tmp = solve(numbers, curr // target, 0, None)
        for ex in tmp:
            res.append( (DIV, expr, ex) )

    return res


def min_sols(numbers, target):
    sols = slv(numbers, target)
    if not sols:
        return sols
    minc = min(map(complexity, sols))
    return [s for s in set(sols) if complexity(s) == minc]


def interact():
    print('Numbers!')
    while True:
        numstr = input('Numbers: ')
        nums = re.split('[ ,]+', numstr.strip())
        if len(nums) != 6:
            print('6 numbers!')
            continue
        try:
            nums = list(map(int, nums))
        except ValueError:
            print('Not all numbers')
            continue
        break

    while True:
        targstr = input('Target: ')
        try:
            target = int(targstr)
        except ValueError:
            print('Not a number')
            continue
        break

    sols = min_sols(nums, target)
    if not sols:
        print('No solutions')
    else:
        for s in sols:
            print(f'{display(s)} = {int(eval(display(s)))}')
