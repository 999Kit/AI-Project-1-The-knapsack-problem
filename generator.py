import random
with open("INPUT_0.txt", 'w') as f:
    W = random.randrange(60, 70)
    m = random.randrange(2, 4)
    n = random.randrange(6, 7)
    print(n, m)
    f.write(str(W) + '\n')
    f.write(str(m) + '\n')
    for _ in range(n):
        val = str(random.randrange(10, 30))
        if _ != n - 1: val += ', '
        f.write(val)
    f.write('\n')
    for _ in range(n):
        val = str(random.randrange(10, 100))
        if _ != n - 1: val += ', '
        f.write(val)
    f.write('\n')
    for _ in range(n):
        val = str(random.randrange(1, m + 1))
        if _ != n - 1: val += ', '
        f.write(val)

