from collections import Counter, defaultdict

def legal(s):
    return len(s) <= 9 and '-' not in s

def contains(sup, sub):
    i_sup, i_sub = 0, 0
    while i_sup < len(sup) and i_sub < len(sub):
        if sub[i_sub] == sup[i_sup]:
            i_sub += 1
        i_sup += 1

    return i_sub == len(sub)

def init():
    with open('./dictionary.csv') as f:
        words = list(filter(legal,f.read().splitlines()))

    grouped = {i:defaultdict(list) for i in range(1,10)}
    for w in words:
        grouped[len(w)][''.join(sorted(w))].append(w)

    return grouped

def matches(grouped, letters):
    sup = sorted(letters)
    found = []
    for i in range(9, 4, -1):
        for sub, cands in grouped[i].items():
            if contains(sup, sub):
                found.extend(cands)
        if i <= 6 and found:
            break
    return max(map(len, found)), found

def interact(grouped):
    print('Words, plz')
    while True:
        inp = input('Letters: ')

        if len(inp) < 5:
            if inp:
                print('at least 5 letters!')
            continue
        break

    mlen, res = matches(grouped, inp)
    print(f'Found {len(res)} words. Longest one of length {mlen}.')
    for r in sorted(res, key=lambda x: (len(x), x)):
        print(f'{len(r)}: {r}')

def main():
    grouped = init()
    while True:
        interact(grouped)

if __name__ == '__main__':
    main()
