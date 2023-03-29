class KnapsackProblem:
    def __init__(self, _W, _m, _w, _c, _v):
        self.W = _W
        self.m = _m
        self.w = _w
        self.c = _c
        self.v =_v
        self.typeList = [list() for _ in range(self.m)]
        for i, x in enumerate(self.c):
            self.typeList[x - 1].append(i)
    def fitness(self, individual):
        total_weight = 0
        total_value = 0
        mask = 0
        for i in range(len(individual)):
            if individual[i]:
                total_weight += self.w[i]
                if(total_weight > self.W):
                    return 0
                total_value += self.v[i]
                mask |= (1 << (self.c[i] - 1))
        if(mask == (1 << self.m) - 1):
            return total_value
        return 0

