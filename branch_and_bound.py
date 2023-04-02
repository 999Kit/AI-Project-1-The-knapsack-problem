import sys
from utils import *
import math
import heapq
sys.set_int_max_str_digits(0)



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
    total_weight = cur_tw
    total_value = cur_tv

    for i in range(level, len(items)):
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


def branch_and_bound(problem: KnapsackProblem):
    size = len(problem.w)
    # ---------- Sort the items based on the value/weight ratio descendingly ----------
    # an item is (ratio, value, weight, class)
    items = [(problem.v[i]/problem.w[i], problem.v[i], problem.w[i], problem.c[i]) for i in range(len(problem.v))]
    items.sort(reverse=True)
    # ---------- initialize step ----------------
    min_upper = 0  # initialize max value = 0 because all others are negative
    cur_state = 0
    final_state = 0
    final_ub = float('inf')
    class_set = set()  # store the classes explored
    # --------- place the first node of which no items are selected --------------
    # a node is (lower_bound, upper_bound, total_weight, total_value, class_set, current_level, selected)
    pq = [(0, 0, 0, 0, class_set, 0, 0)]
    heapq.heapify(pq)

    while len(pq) > 0:
        lb, ub, total_weight, total_value, class_set, current_level, selected = heapq.heappop(pq)
        # print(f"Current level is {current_level}")
        if len(class_set) == problem.m and lb >= final_ub:
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
            if len(class_set) == problem.m and ub < final_ub:
                final_ub = ub
                final_state = cur_state
            continue

        # right node: excludes the current item
        right_lb = lower_bound(items, total_value, total_weight, problem.W, current_level + 1)
        right_ub = upper_bound(items, total_value, total_weight, problem.W, current_level + 1)
        right_node = (right_lb, right_ub, total_weight, total_value, class_set.copy(), current_level + 1, False)

        # ----- check if adding the current item exceeds capacity -------
        if total_weight + items[current_level][2] > problem.W:
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

            left_node = (left_lb, left_ub, left_weight, left_val, class_set.copy(), current_level + 1, True)

        # ----- Update upper bound -----
        min_upper = min(min_upper, left_ub, right_ub)
        # if lower bound is larger than upper bound then we prune
        if left_lb != 1 and (min_upper >= left_lb or len(class_set) < problem.m):
            heapq.heappush(pq, left_node)
        if min_upper >= right_lb or len(class_set) < problem.m:
            heapq.heappush(pq, right_node)

    if final_ub == float('inf'):
        final_ub = 0
    return final_state, -final_ub