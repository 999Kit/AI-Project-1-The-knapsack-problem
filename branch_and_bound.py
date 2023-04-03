import sys
from utils import *
import math
import heapq
import time
sys.set_int_max_str_digits(0)

# globals
size = 0

def branch_and_bound(problem):
    def solve(problem, state, curIndex):
        if curIndex < 0:
            evaluation_value = problem.evaluation_function(state)
            return state, evaluation_value
        if problem.evaluation_function(state) < 0: return state, 0
        return max(solve(problem, state, curIndex - 1), solve(problem, state | (1 << curIndex), curIndex - 1),
                   key=lambda x: x[1])

    return solve(problem, 0, len(problem.w) - 1)


def upper_bound(items, cur_tv, cur_tw, capacity, level):
    """Calculate the values of remaining items after the items already selected. Add the fraction part"""
    total_weight = cur_tw
    total_value = cur_tv

    for i in range(level, len(items)):
        if total_weight + items[i][2] > capacity:
            break
        else:
            total_value -= items[i][1]
            total_weight += items[i][2]

    return total_value


def lower_bound(items, cur_tv, cur_tw, capacity, level):
    """Calculate the values of remaining items after the items already selected. Add the fraction part"""
    global size
    total_weight = cur_tw
    total_value = cur_tv

    for i in range(level, size):
        if total_weight + items[i][2] > capacity:
            total_value -= (capacity - total_weight) * items[i][0]
            break
        else:
            total_value -= items[i][1]
            total_weight += items[i][2]

    # penalty: If no more items can be added and the number of classes
    # remaining to be assigned is non zero then set value of state to be zero.
    # if classes_chosen + 1 != 1 << classes_num:
    #     return 0

    return total_value


def branch_and_bound_bfs(problem: KnapsackProblem):
    global size
    start_time = time.time()

    size = len(problem.w)
    # ---------- Sort the items based on the value/weight ratio descendingly ----------
    # an item is (ratio, value, weight, class, idx)
    items = [(problem.v[i]/problem.w[i], problem.v[i], problem.w[i], problem.c[i], i) for i in range(size)]
    items.sort(reverse=True)
    # ---------- initialize step ----------------
    min_upper = 0  # initialize max value = 0 because all others are negative
    initial_state = 0
    final_state = 0
    final_ub = float('inf')
    class_set = set()  # store the classes explored
    # --------- place the first node of which no items are selected --------------
    # a node is (lower_bound, upper_bound, total_weight, total_value, class_set, current_level, selected, cur_state)
    pq = [(0, 0, 0, 0, class_set, 0, 0, initial_state)]
    heapq.heapify(pq)

    while len(pq) > 0:
        if time.time() - start_time > 3:
            return problem.W + 1, problem.W + 1
        lb, ub, total_weight, total_value, class_set, current_level, selected, cur_state = heapq.heappop(pq)
        # print(f"Current level is {current_level}")
        if len(class_set) == problem.m and (lb > min_upper or lb >= final_ub):
            # allow pruning when lower bound is larger than upper bound and there is at least 1 item of one class
            continue

        # update current path
        if current_level != 0:
            i = size - 1 - (current_level - 1)
            if selected:
                cur_state |= (1 << i)
            else:
                cur_state &= ~(1 << i)  # clear the bit at current_level - 1

        # ---- reached last level => check at least 1 item from each class is added
        if current_level == size:
            # if current ub is smaller (better) than final_ub
            if len(class_set) == problem.m and ub < final_ub:
                final_ub = ub
                # convert integer to binary string, remove '0b' prefix, and pad with zeros to length 'size'
                binary_string = bin(cur_state)[2:].zfill(size)

                # convert each character in the binary string to True or False
                bool_list = [c == '1' for c in binary_string]
                final_state_list = [False] * size
                for i in range(size):
                    final_state_list[items[i][4]] = bool_list[i]

                # Convert True/False list to binary string and prepend '0b' to represent it as a binary number
                binary_string = '0b' + ''.join(['1' if b else '0' for b in final_state_list])

                # Convert binary string to integer using the int() function
                final_state = int(binary_string, 2)

            continue

        # right node: excludes the current item
        right_lb = lower_bound(items, total_value, total_weight, problem.W, current_level + 1)
        right_ub = upper_bound(items, total_value, total_weight, problem.W, current_level + 1)
        right_class_set = class_set.copy()
        right_node = (right_lb, right_ub, total_weight, total_value, right_class_set, current_level + 1,
                      False, cur_state)

        # ----- check if adding the current item exceeds capacity -------
        if total_weight + (items[current_level][2]) > problem.W:
            # guarantees left node will not be extended next
            left_ub = 1
            left_lb = 1
        else:
            left_val = total_value - items[current_level][1]
            left_weight = total_weight + items[current_level][2]
            left_lb = lower_bound(items, left_val, left_weight, problem.W, current_level + 1)
            left_ub = upper_bound(items, left_val, left_weight, problem.W, current_level + 1)
            new_item_class = items[current_level][3]

            if new_item_class not in class_set:
                class_set.add(new_item_class)

            left_node = (left_lb, left_ub, left_weight, left_val, class_set.copy(), current_level + 1, True, cur_state)

        # ----- Update upper bound -----
        min_upper = min(min_upper, left_ub, right_ub)
        # if lower bound is larger than upper bound then we prune
        if current_level == size - 1:
            if len(class_set) == problem.m and left_lb != 1:
                heapq.heappush(pq, left_node)
        else:
            if left_lb != 1 and (min_upper >= left_lb or len(class_set) < problem.m):
                heapq.heappush(pq, left_node)
        # if these leaf nodes do not have at least one item per class then do not add to queue
        if current_level == size - 1 and len(right_class_set) < problem.m:
            continue
        if min_upper >= right_lb or len(right_class_set) < problem.m:
            heapq.heappush(pq, right_node)

    if final_ub == float('inf'):
        final_ub = 0

    print(f"--- Running time for branch and bound: %s ms ---" % ((time.time() - start_time) * 1000))
    # convert integer to binary string, remove '0b' prefix, and pad with zeros to length 'size'
    binary_string = bin(final_state)[2:].zfill(size)

    # convert each character in the binary string to True or False
    ans_list = [1 if c == '1' else 0 for c in binary_string]
    return ans_list, -final_ub