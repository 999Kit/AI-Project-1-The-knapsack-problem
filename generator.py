import random
with open("INPUT_0.txt", 'w') as f:
    W = random.randrange(50, 100)
    m = random.randrange(10, 11)
    n = random.randrange(300, 400)
    print(n, m)
    f.write(str(W) + '\n')
    f.write(str(m) + '\n')
    for _ in range(n):
        val = str(random.randrange(20, 30))
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

