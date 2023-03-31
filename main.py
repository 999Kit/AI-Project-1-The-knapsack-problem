from GA import *
from utils import *
from brute_force import *
from branch_and_bound import *
from local_beam import *

def read_data_from_file(file_handle):
    lines = file_handle.readlines()
    max_w, num_c = int(lines[0]), int(lines[1])

    w_list = list(map(int, lines[2].split(', ')))
    v_list = list(map(int, lines[3].split(', ')))
    c_list = list(map(int, lines[4].split(', ')))

    return max_w, num_c, w_list, v_list, c_list

def write_solution_to_file(file_handle, total_value, model, num_of_objects):
    file_handle.write(str(total_value) + '\n')
    if type(model) is list:
        for i in range(len(model)):
            file_handle.write(str(model[i]))
            if(i != len(model) - 1): file_handle.write(', ',)
    else:
        file_handle.write(str(model & 1))
        for k in range(1, num_of_objects):
            file_handle.write(", " + str((model >> k) & 1))

if __name__ == '__main__':
    num_of_files = int(input("Enter number of input files: "))
    for i in range(0, num_of_files):
        with open(f"INPUT_{i}.txt", "r") as input_file, open(f"OUTPUT_{i}.txt", "w") as output_file:
            max_weight, num_of_classes, weight_list, value_list, class_list = read_data_from_file(input_file)
            kp = KnapsackProblem(max_weight, num_of_classes, weight_list, class_list, value_list)
            # sol, sol_val = brute_force(kp) # BRUTE FORCE
            # Branch and Bound
            # sol, sol_val = branch_and_bound(kp)
            # Local beam search
            # sol, sol_val = local_beam(kp)
            # GA
            # print(len(kp.w))
            # population = population_generator(kp, 150)
            # sol, sol_val = genetic_algorithm(kp, population, 5000)
            write_solution_to_file(output_file, sol_val, sol, len(weight_list))
