import random


def generate_small_dataset():
    for i in range(10):
        with open(f"INPUT_{i}.txt", 'w') as f:
            W = random.randrange(1000, 5000)
            m = random.randrange(2, 4)
            n = random.randint(10, 40)
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

