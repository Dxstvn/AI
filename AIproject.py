from copy import copy, deepcopy
from os import path
import ast

def tiles_input():
    # Takes start state, goal state, and weight as inputs

    start_state = ast.literal_eval(input("Start State: "))
    end_state = ast.literal_eval(input("End State: "))
    weight = float(input("Weight: "))
    start_state_two = ast.literal_eval(input("Start State: "))
    end_state_two = ast.literal_eval(input("End State: "))
    weight_two = float(input("Weight: "))
    start_state_three = ast.literal_eval(input("Start State: "))
    end_state_three = ast.literal_eval(input("End State: "))
    weight_three = float(input("Weight: "))
    '''
    start_state = [[2, 0, 6, 4], [3, 10, 7, 9], [11, 5, 8, 1]]
    end_state = [[2, 10, 6, 4], [11, 3, 8, 9], [0, 7, 5, 1]]
    weight = 1
    start_state_two = [[2, 0, 6, 4], [3, 10, 7, 9], [11, 5, 8, 1]]
    end_state_two = [[2, 7, 8, 4], [10, 6, 9, 1], [3, 11, 0, 5]]
    weight_two = 1
    start_state_three = [[8, 7, 2, 4], [10, 6, 9, 1], [0, 11, 5, 3]]
    end_state_three = [[10, 6, 8, 4], [9, 7, 0, 2], [11, 5, 3, 1]]
    weight_three = 1
    '''
    return start_state, end_state, weight, start_state_two, end_state_two, weight_two, start_state_three, end_state_three, weight_three

def find_space(node_space):
    # Iterates through list to find 0
    # 0 is considered blank tile
    for i in range(len(node_space)):
        for j in range(len(node_space[i])):
            if node_space[i][j] == 0:
                return i, j

# Instantiate a start node
start_state, end_state, weight, start_state_two, end_state_two, weight_two, start_state_three, end_state_three, weight_three = tiles_input()
start_node = {}
# Keeps track of path taken
start_node['state'] = [start_state]
# Keeps track of space for each node
start_node['space'] = find_space(start_state)
# Keeps track of node's f(n) score
start_node['f(n) score'] = [0]
start_node['direction'] = []

start_node_two = {}
# Keeps track of path taken
start_node_two['state'] = [start_state_two]
# Keeps track of space for each node
start_node_two['space'] = find_space(start_state_two)
# Keeps track of node's f(n) score
start_node_two['f(n) score'] = [0]
start_node_two['direction'] = []

start_node_three = {}
# Keeps track of path taken
start_node_three['state'] = [start_state_three]
# Keeps track of space for each node
start_node_three['space'] = find_space(start_state_three)
# Keeps track of node's f(n) score
start_node_three['f(n) score'] = [0]
start_node_three['direction'] = []


# Function to move tiles

def function_score(states_lst, goal_coord):
    # calculate manhattan distance for each tile
    h_score = 0
    for i in range(len(states_lst)):
        for j in range(len(states_lst[i])):
            h_score += abs(i - goal_coord[states_lst[i][j]][0]) + abs(j - goal_coord[states_lst[i][j]][1])
    # add given g(n) score (len of path) to calculated h(n) score
    f_score = len(states_lst) + (weight * h_score)
    return f_score


def move_tile(state_space, goal_coord): # (state, space_index tuple)
    possible_nodes = []
    # Unpacks space tile coordinates
    row, col = state_space['space']
    # for loop for movement possibilities
    for x, y in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        #copies puzzle board and applies movement
        copy_state = deepcopy(state_space['state'][-1])
        temp = copy_state[row][col]
        if ((row + x) <= len(copy_state) - 1 and ((row + x) >= 0)) and (((col + y) <= len(copy_state[0]) - 1) and ((col + y) >= 0)):
            copy_state[row][col] = copy_state[row + x][col + y]
            copy_state[row + x][col + y] = temp
            direction = ''
            # declares new space coordinate
            new_space = (row + x, col + y)
            # calculate f(n) score for each possible node
            new_f_score = function_score(copy_state, goal_coord)
            # Tracks direction of movement
            if x == 1 and y == 0:
                direction = 'up'
            if x == -1 and y == 0:
                direction = 'down'
            if x == 0 and y == 1:
                direction = 'right'
            if x == 0 and y == -1:
                direction = 'left'
            # Keeps track of state, space, f(n) score, and direction on each node on optimal path
            new_state_space = {'state': state_space['state'] + [copy_state], 'space': new_space, 'f(n) score': state_space['f(n) score'] + [new_f_score], 'direction': state_space['direction'] + [direction]}
            # Adds possible nodes to list
            if copy_state not in state_space['state']:
                possible_nodes.append(new_state_space)
    return possible_nodes


def generate_tree(start_node, goal_node): #goal_node is state
    # Give each tile in goal node a coordinate position
    goal_coordinates = {}
    for i in range(len(goal_node)):
        for j in range(len(goal_node[i])):
            goal_coordinates[goal_node[i][j]] = (i, j)
    # curr_nodes represents list of possible nodes
    curr_nodes = []
    # Generates possible nodes and moves them into a list
    curr_nodes += move_tile(start_node, goal_coordinates)
    while curr_nodes:
        # Takes node with lowest f(n) score
        min_node = min(curr_nodes, key=lambda node : node['f(n) score'])
        # If last node in path is goal, return node
        if min_node['state'][-1] == goal_node:
            return min_node
        # else, continue search
        curr_nodes.remove(min_node)
        curr_nodes += move_tile(min_node, goal_coordinates)

def print_output_one(final_state):
    # Bunch of cases to output path formally
    f1 = open("output_one.txt", "w+")
    for i in range(len(final_state['state'])):
        if i == 0:
            print("Start State: ", end = "", file = f1)
            print('{state}'.format(state = final_state['state'][i]), end='\n', file = f1)
        else:
            if i == len(final_state['state']) - 1:
                print("Goal State:  ", end='', file = f1)
                print(final_state['state'][i], file = f1)
            else:
                print('             {state} Direction: {direction}, f(n) score: {f_score}'.format(state = final_state['state'][i], direction = final_state['direction'][i], f_score = final_state['f(n) score'][i]), end='\n', file = f1)
        # Prints down arrow
        if i < len(final_state['state']) - 1:
            print(u'                                    \u2193', file = f1)
    print('Weight: {weight}'.format(weight = weight), file = f1)
    print('Depth: {depth}'.format(depth = len(final_state['state'])), file = f1)
    f1.close()

def print_output_two(final_state):
    # Bunch of cases to output path formally
    f2 = open("output_two.txt", "w+")
    for i in range(len(final_state['state'])):
        if i == 0:
            print("Start State: ", end = "", file = f2)
            print('{state}'.format(state = final_state['state'][i]), end='\n', file = f2)
        else:
            if i == len(final_state['state']) - 1:
                print("Goal State:  ", end='', file = f2)
                print(final_state['state'][i], file = f2)
            else:
                print('             {state} Direction: {direction}, f(n) score: {f_score}'.format(state = final_state['state'][i], direction = final_state['direction'][i], f_score = final_state['f(n) score'][i]), end='\n', file = f2)
        # Prints down arrow
        if i < len(final_state['state']) - 1:
            print(u'                                    \u2193', file = f2)
    print('Weight: {weight}'.format(weight = weight), file = f2)
    print('Depth: {depth}'.format(depth = len(final_state['state'])), file = f2)
    f2.close()

def print_output_three(final_state):
    # Bunch of cases to output path formally
    f3 = open("output_three.txt", "w+")
    for i in range(len(final_state['state'])):
        if i == 0:
            print("Start State: ", end = "", file = f3)
            print('{state}'.format(state = final_state['state'][i]), end='\n', file = f3)
        else:
            if i == len(final_state['state']) - 1:
                print("Goal State:  ", end='', file = f3)
                print(final_state['state'][i], file = f3)
            else:
                print('             {state} Direction: {direction}, f(n) score: {f_score}'.format(state = final_state['state'][i], direction = final_state['direction'][i], f_score = final_state['f(n) score'][i]), end='\n', file = f3)
        # Prints down arrow
        if i < len(final_state['state']) - 1:
            print(u'                                    \u2193', file = f3)
    print('Weight: {weight}'.format(weight = weight), file = f3)
    print('Depth: {depth}'.format(depth = len(final_state['state'])), file = f3)
    f3.close()
def main():
    print_output_one((generate_tree(start_node, end_state)))
    print_output_two((generate_tree(start_node_two, end_state_two)))
    print_output_three((generate_tree(start_node_three, end_state_three)))
   

main()



'''
    Note!!!
        I used a nested list as input and a 0 to represent the space.
        Additionally, I printed the elements of the final list
        in order to show the initial state, nodes on path taken
        and goal state. I also used the down arrows between the states. 

'''








