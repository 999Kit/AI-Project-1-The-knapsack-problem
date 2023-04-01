import random
with open("INPUT_1.txt", 'w') as f:
    W = random.randrange(1000, 5000)
    m = random.randrange(5, 10)
    n = random.randrange(100, 200)
    f.write(str(W) + '\n')
    f.write(str(m) + '\n')
    for _ in range(n):
        val = str(random.randrange(1, W // n + 100))
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

