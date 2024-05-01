import random

class mt19937():
    w, n, m, r = 32, 624, 397, 31
    f = 1812433253
    a = 0x9908B0DF
    u, d = 11, 0xFFFFFFFF
    s, b = 7, 0x9D2C5680
    t, c = 15, 0xEFC60000
    l = 18

    def my_int32(self, x):
        return(x & 0xFFFFFFFF)

    def __init__(self, seed):
        self.MT = [0] * self.n
        self.index = self.n + 1
        self.lower_mask = (1 << self.r) - 1
        self.upper_mask = self.my_int32(~self.lower_mask)
        self.MT[0] = self.my_int32(seed)
        for i in range(1, self.n):
            self.MT[i] = self.my_int32((self.f * (self.MT[i - 1] ^ (self.MT[i - 1] >> (self.w - 2))) + i))

    def extract_number(self):
        if self.index >= self.n:
            self.twist()
            self.index = 0
        y = self.MT[self.index]
        y = y ^ ((y >> self.u) & self.d)
        y = y ^ ((y << self.s) & self.b)
        y = y ^ ((y << self.t) & self.c)
        y = y ^ (y >> self.l)
        self.index += 1
        return self.my_int32(y)

    def twist(self):
        for i in range(0, self.n):
            x = (self.MT[i] & self.upper_mask) + (self.MT[(i + 1) % self.n] & self.lower_mask)
            xA = x >> 1
            if(x % 2) != 0:
                xA = xA ^ self.a
            self.MT[i] = self.MT[(i + self.m) % self.n] ^ xA

def untemper(y):
    y ^= y >> mt19937.l
    y ^= y << mt19937.t & mt19937.c
    for _ in range(7):
        y ^= y << mt19937.s & mt19937.b
    for _ in range(3):
        y ^= y >> mt19937.u & mt19937.d
    return y

if __name__ == "__main__":
    # create our own version of an MT19937 PRNG.
    myprng = mt19937(0)

    print("Seeding Python's built-in PRNG with the time...")

    print("Generating %i random numbers.\nWe'll use those values to create a clone of the current state of Python's built-in PRNG..." % (mt19937.n))
    for i in range(mt19937.n):
        myprng.MT[i] = untemper(random.randrange(0xFFFFFFFF))
    #print(myprng.MT)

    print("Now, we'll test the clone...")
    print("\nPython       Our clone")
    for i in range(20):
        r1 = random.randrange(0xFFFFFFFF)
        r2 = myprng.extract_number()
        print(f"{r1:10} - {r2:10} ({r1 == r2})")
        assert(r1 == r2)
