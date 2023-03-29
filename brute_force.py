import sys
sys.set_int_max_str_digits(0)


def read_data_from_file(file_handle):
    lines = file_handle.readlines()
    max_w, num_c = int(lines[0]), int(lines[1])

    w_list = []
    v_list = []
    c_list = []

    for w in lines[2].split(", "):
        w_list.append(int(w))

    for v in lines[3].split(", "):
        v_list.append(int(v))

    for c in lines[4].split(", "):
        c_list.append(int(c))

    return max_w, num_c, w_list, v_list, c_list


def write_solution_to_file(file_handle, total_value, model, num_of_objects):
    file_handle.write(str(total_value) + "\n")
    file_handle.write(str(model & 1))
    for k in range(1, num_of_objects):
        file_handle.write(", " + str((model >> k) & 1))


def brute_force(weights, values, classes, max_capacity, num_classes):
    def evaluation_function(model):
        classes_chosen = 0
        total_weight = 0
        total_value = 0

        for idx in range(len(weight_list)):
            if (model[0] >> idx) & 1 == 1:
                total_weight += weights[idx]

                if total_weight > max_capacity:
                    return 0

                total_value += values[idx]
                classes_chosen |= 1 << (classes[idx] - 1)

        if classes_chosen != 2 ** num_classes - 1:
            return 0

        return total_value

    def solve(solution, best_value, model, model_length):
        if model_length[0] == len(weights):
            evaluation_value = evaluation_function(model)

            if evaluation_value > best_value[0]:
                best_value[0] = evaluation_value
                solution[0] = model[0]

            return

        model_length[0] += 1
        solve(solution, best_value, model, model_length)

        model_length[0] -= 1
        model[0] ^= 1 << model_length[0]

        model_length[0] += 1
        solve(solution, best_value, model, model_length)

        model_length[0] -= 1
        model[0] ^= 1 << model_length[0]

    solution_model = [0]
    solution_value = [0]

    state = [0]
    state_length = [0]

    solve(solution_model, solution_value, state, state_length)
    return solution_model[0], solution_value[0]


if __name__ == "__main__":
    num_of_files = int(input("Enter number of input files: "))
    for i in range(0, num_of_files):
        with open(f"INPUT_{i}.txt", "r") as input_file, open(f"OUTPUT_{i}.txt", "w") as output_file:
            max_weight, num_of_classes, weight_list, value_list, class_list = read_data_from_file(input_file)
            sol, sol_val = brute_force(weight_list, value_list, class_list, max_weight, num_of_classes)
            write_solution_to_file(output_file, sol_val, sol, len(weight_list))
