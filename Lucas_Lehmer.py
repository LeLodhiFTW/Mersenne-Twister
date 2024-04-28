def Lucas_Lehmer(p: int):
    s = 4
    M = (2**p) - 1
    for i in range(p-2):
        s = ((s*s) - 2) % M
    if s == 0:
        return 'You found a Mersene Prime!'
    else:
        return 'Nope...'
