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
                total_value += self.v[i]
                mask |= (1 << (self.c[i] - 1))
        if(total_weight > self.W):
            return self.W - total_weight
        if(mask == (1 << self.m) - 1):
            return total_value
        return 0
    
    def evaluation_function(self, model):
        classes_chosen = 0
        total_weight = 0
        total_value = 0

        for idx in range(len(self.w)):
            if (model >> idx) & 1 == 1:
                total_weight += self.w[idx]

                if total_weight > self.W:
                    return -1

                total_value += self.v[idx]
                classes_chosen |= 1 << (self.c[idx] - 1)

        if classes_chosen + 1 != 1 << self.m:
            return 0

        return total_value

class Node:
    def __init__(self, state, value=0):
        self.state = state
        self.value = 0
    def __lt__(self, other):
        return self.value < other.value
    def __repr__(self):
        return self.value + '\n' + self.state