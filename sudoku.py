import math
import copy
import numpy as np
import scipy.optimize


def make_2d_list_dense(sparse_list):
    dense_list = copy.deepcopy(sparse_list)

    for i in range(len(dense_list)):
        for j in range(len(dense_list[i])):
            if len(dense_list[i][j]) < 1:
                dense_list[i][j].append(0.0)

    return dense_list


def print_puzzle(puzzle_array):
    output_strings = []

    for i in range(len(puzzle_array)):
        if (i != 0 and i != 8) and i % 3 == 0:
            output_strings.append("-----------")

        output_string = ""

        for j in range(len(puzzle_array[i])):
            if (j != 0 and j != 8) and j % 3 == 0:
                output_string = "{0}{1}".format(output_string, '|')

            output_string = "{0}{1}".format(output_string, str(int(round(puzzle_array[i][j]))))

        output_strings.append(output_string)

    for i in range(len(output_strings)):
        print(output_strings[i])

    return True


def get_puzzle():
    puzzle_list = [[[5], [3], [ ], [ ], [7], [ ], [ ], [ ], [ ]],
                   [[6], [ ], [ ], [1], [9], [5], [ ], [ ], [ ]],
                   [[ ], [9], [8], [ ], [ ], [ ], [ ], [6], [ ]],
                   [[8], [ ], [ ], [ ], [6], [ ], [ ], [ ], [3]],
                   [[4], [ ], [ ], [8], [ ], [3], [ ], [ ], [1]],
                   [[7], [ ], [ ], [ ], [2], [ ], [ ], [ ], [6]],
                   [[ ], [6], [ ], [ ], [ ], [ ], [2], [8], [ ]],
                   [[ ], [ ], [ ], [4], [1], [9], [ ], [ ], [5]],
                   [[ ], [ ], [ ], [ ], [8], [ ], [ ], [7], [9]]]

    puzzle_array = np.asfarray(make_2d_list_dense(puzzle_list)).squeeze()

    print_puzzle(puzzle_array)

    return puzzle_list, puzzle_array


def get_guess(puzzle_list):
    pars = 0

    for i in range(len(puzzle_list)):
        for j in range(len(puzzle_list[i])):
            if len(puzzle_list[i][j]) < 1:
                pars = pars + 1

    guess = np.random.uniform(low=1.0, high=9.0, size=pars)

    return guess


def fill_blanks(blanks, puzzle_list, puzzle_array):
    new_puzzle_array = puzzle_array.copy()

    blanks_index = 0

    for i in range(len(puzzle_list)):
        for j in range(len(puzzle_list[i])):
            if len(puzzle_list[i][j]) < 1:
                new_puzzle_array[i][j] = blanks[blanks_index]

                blanks_index = blanks_index + 1

    return new_puzzle_array


def vertical_constraint(guess, puzzle_list, puzzle_array):
    ground_truth = 9.0 + 8.0 + 7.0 + 6.0 + 5.0 + 4.0 + 3.0 + 2.0 + 1.0

    new_puzzle_array = fill_blanks(guess, puzzle_list, puzzle_array)

    vertical_puzzle_array_sum = np.sum(new_puzzle_array, axis=0)

    constraint_value = vertical_puzzle_array_sum - ground_truth

    print("Constraint value: {0}".format(constraint_value))

    return constraint_value


def horizontal_constraint(guess, puzzle_list, puzzle_array):
    ground_truth = 9.0 + 8.0 + 7.0 + 6.0 + 5.0 + 4.0 + 3.0 + 2.0 + 1.0
    
    new_puzzle_array = fill_blanks(guess, puzzle_list, puzzle_array)

    horizontal_puzzle_array_sum = np.sum(new_puzzle_array, axis=1)

    constraint_value = horizontal_puzzle_array_sum - ground_truth

    print("Constraint value: {0}".format(constraint_value))

    return constraint_value


def square_constraint(guess, puzzle_list, puzzle_array):
    ground_truth = 9.0 + 8.0 + 7.0 + 6.0 + 5.0 + 4.0 + 3.0 + 2.0 + 1.0

    new_puzzle_array = fill_blanks(guess, puzzle_list, puzzle_array)

    square_puzzle_array_sum = np.asfarray(get_square_puzzle_array_sum(new_puzzle_array))

    constraint_value = square_puzzle_array_sum - ground_truth

    print("Constraint value: {0}".format(constraint_value))

    return constraint_value


def objective_function_0(guess, puzzle_list, puzzle_array):
    return 0.0


def objective_function_1(guess, puzzle_list, puzzle_array):
    objective_value = 0.0

    new_puzzle_array = fill_blanks(guess, puzzle_list, puzzle_array)

    for i in range(len(puzzle_list)):
        for j in range(len(puzzle_list[i])):
            if len(puzzle_list[i][j]) < 1:
                is_valid = True

                for k in range(9):
                    if i == k:
                        continue

                    if math.isclose(round(new_puzzle_array[i][j]), round(new_puzzle_array[k][j])):
                        objective_value = objective_value + 1.0

                        is_valid = False

                        break

                if is_valid:
                    for k in range(9):
                        if j == k:
                            continue

                        if math.isclose(round(new_puzzle_array[i][j]), round(new_puzzle_array[i][k])):
                            objective_value = objective_value + 1.0

                            is_valid = False

                            break

                if is_valid:
                    for m in range(round(i) % 3, (round(i) % 3) + 3):
                        for n in range(round(j) % 3, (round(j) % 3) + 3):
                            if i == m and j == n:
                                continue

                            if math.isclose(round(new_puzzle_array[i][j]), round(new_puzzle_array[m][n])):
                                objective_value = objective_value + 1.0

                                is_valid = False

                        if not is_valid:
                            break

    print("Objective value: {0}".format(str(objective_value)))

    return objective_value


def get_square_puzzle_array_sum(puzzle_array):
    square_puzzle_array_sum = []

    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            current_sum = 0.0

            for k in range(i, i + 3):
                for l in range(j, j + 3):
                    current_sum = current_sum + puzzle_array[k][l]

            square_puzzle_array_sum.append(current_sum)

    return square_puzzle_array_sum


def objective_function_2(guess, puzzle_list, puzzle_array):
    ground_truth = 9.0 + 8.0 + 7.0 + 6.0 + 5.0 + 4.0 + 3.0 + 2.0 + 1.0

    new_puzzle_array = fill_blanks(guess, puzzle_list, puzzle_array)

    vertical_puzzle_array_sum = np.sum(new_puzzle_array, axis=0)

    vertical_puzzle_array_sum_mse = 0.0

    for i in range(len(vertical_puzzle_array_sum)):
        vertical_puzzle_array_sum_mse = vertical_puzzle_array_sum_mse + math.pow((ground_truth - vertical_puzzle_array_sum[i]), 2.0)

    horizontal_puzzle_array_sum = np.sum(new_puzzle_array, axis=1)

    horizontal_puzzle_array_sum_mse = 0.0

    for i in range(len(horizontal_puzzle_array_sum)):
        horizontal_puzzle_array_sum_mse = horizontal_puzzle_array_sum_mse + math.pow((ground_truth - horizontal_puzzle_array_sum[i]), 2.0)

    square_puzzle_array_sum = get_square_puzzle_array_sum(new_puzzle_array)

    square_puzzle_array_sum_mse = 0.0

    for i in range(len(square_puzzle_array_sum)):
        square_puzzle_array_sum_mse = square_puzzle_array_sum_mse + math.pow((ground_truth - square_puzzle_array_sum[i]), 2.0)

    objective_value = vertical_puzzle_array_sum_mse + horizontal_puzzle_array_sum_mse + square_puzzle_array_sum_mse

    print("Objective value: {0}".format(str(objective_value)))

    return objective_value


def objective_function_3(guess, puzzle_list, puzzle_array):
    objective_value = objective_function_1(guess, puzzle_list, puzzle_array) * objective_function_2(guess, puzzle_list, puzzle_array)

    print("Objective value: {0}".format(str(objective_value)))

    return objective_value


def print_guess(guess):
    output_string = ""

    for i in range(len(guess)):
        output_string = "{0}{1},".format(output_string, str(int(round(guess[i]))))

    output_string = output_string[:-1]

    print(output_string)

    return True


def optimise(objective_function_index):
    puzzle_list, puzzle_array = get_puzzle()

    guess = get_guess(puzzle_list)

    bounds = []

    for i in range(len(guess)):
        bounds.append((1.0, 9.0))

    constraints = [{'type': 'eq', 'fun': vertical_constraint, 'args': (puzzle_list, puzzle_array)},
                   {'type': 'eq', 'fun': horizontal_constraint, 'args': (puzzle_list, puzzle_array)},
                   {'type': 'eq', 'fun': square_constraint, 'args': (puzzle_list, puzzle_array)}]

    output_guess = guess

    if objective_function_index == 0:
        output_guess = scipy.optimize.minimize(objective_function_0, guess, args=(puzzle_list, puzzle_array), method="trust-constr", bounds=bounds, constraints=constraints).x
    else:
        if objective_function_index == 1:
            output_guess = scipy.optimize.minimize(objective_function_1, guess, args=(puzzle_list, puzzle_array), method="trust-constr", bounds=bounds, constraints=constraints).x
        else:
            if objective_function_index == 2:
                output_guess = scipy.optimize.minimize(objective_function_2, guess, args=(puzzle_list, puzzle_array), method="trust-constr", bounds=bounds, constraints=constraints).x
            else:
                if objective_function_index == 3:
                    output_guess = scipy.optimize.minimize(objective_function_3, guess, args=(puzzle_list, puzzle_array), method="trust-constr", bounds=bounds, constraints=constraints).x

    print("Number of invalid guesses: {0}".format(objective_function_1(output_guess, puzzle_list, puzzle_array)))

    print_guess(output_guess)

    output_puzzle_array = fill_blanks(output_guess, puzzle_list, puzzle_array)

    print_puzzle(output_puzzle_array)


optimise(2)
