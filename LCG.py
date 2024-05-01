class LCG:
    def __init__(self, seed, a, c, m):
        self.seed = seed
        self.a = a
        self.c = c
        self.m = m

    def next(self):
        self.seed = (self.a * self.seed + self.c) % self.m
        return self.seed

seed = 7  # Initial seed
a = 11    # Multiplier
c = 7     # Increment
m = 10    # Modulus

lcg = LCG(seed, a, c, m)
for _ in range(15):
    print(lcg.next())
