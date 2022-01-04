from collections import defaultdict
import copy
import random
input_file  = open("input1.txt", "r")
content = input_file.readlines()
"print(content)"
"print(var_info)"
var_info = []
places_names = []
colors = []
array_2d = []


# To see info clearer
def code_format(file):
    for i in range(len(file)):
        '''
        print(i)
        print(len(file))
        '''
        if i == 0:
            var_info = list(file[i].strip().split(" "))
            "print(var_info)"
            for k in range(len(var_info)):
                var_info[k] = int(var_info[k])
            "print(var_info)"
        elif i == 1:
            "print(yeezy_two)"
            regions = list(file[i].strip().split(" "))
        elif i == 2:
            "print(yeezy_three)"
            colors = list(file[i].strip().split(" "))
        else:
            array_2d.append(list(file[i].strip().split(" ")))
            for l in range(len(array_2d)):
                for m in range(len(array_2d[l])):
                    array_2d[l][m] = int(array_2d[l][m])

    return var_info, regions, colors, array_2d


var_info, places_names, colors, array_2d = code_format(content)
'''
print(var_info)
print(places_names)
print(colors)
print(array_2d)
'''


class Region:
    def __init__(self, domain):
        self.name = ""
        self.colors = {color : 0 for color in domain}
        self.poss_color = 3
        self.neighbors = []
        self.assigned = False
        
        
'''
assignment = [regions: check if a color = 1]


'''

'''
NSW = 0
NT = 1
Q = 2
SA = 3
WA = 4
V = 5

          
          [NSW, NT, Q, SA, WA. V]
 NSW = 0  [[0, 0, 1, 1, 0, 1], 
NT = 1    [0, 0, 1, 1, 1, 0],   
Q = 2     [1, 1, 0, 1, 0, 0], 
SA = 3    [1, 1, 1, 0, 1, 1], 
WA = 4    [0, 1, 0, 1, 0, 0],
V = 5     [1, 0, 0, 1, 0, 0]]
                
                
                
                 
                


'''

#Created Region class
# Generates regions using place names and colors list
def gen_regions(places_names, colors):
    "Adding region types to a list"
    places = []
    for i in range(len(places_names)):
        region = Region(colors)
        region.name = places_names[i]
        places.append(region)
    return places


# Detects elements with 1 and makes y a neighbor of x
def calc_neigh(csp, regions):
    for i in range(len(csp)):
        for j in range(len(csp[i])):
            if csp[i][j] == 1:
                regions[i].neighbors.append(regions[j])

    #return regions
# Checks if regions was assigned
def check_assignment(region):
    flag = False
    for key in region.colors.keys():
        # Checks if region is assigned  
        if region.colors[key] == 1:
            flag = True
            break
        else:
            continue
    return flag

#Does MRV and degree heuristic to choose next variable
def unassign_var(unassign_lst):
    "Minimum remaining values"
    region_val = []
    min_regions = []
    for region in unassign_lst:
        region_val.append(region.poss_color)
        #print(region_val)
    min_num = min(region_val)
    for i in range(len(region_val)):
        if region_val[i] == min_num:
            min_regions.append(unassign_lst[i])

    "Degree Hueristic"
    # If only one possible region, just return it
    if len(min_regions) <= 1:
        return min_regions[0]
    #print(min_regions)
    #print("")
    region_neighbors_counter = defaultdict(lambda : 0)
    for remain_reg in min_regions:
        # Will hold # of assigned neighbors for each remaining region
        for neighbor in remain_reg.neighbors:
            if check_assignment(neighbor) == False:
                    region_neighbors_counter[remain_reg] += 1
                    #print(region_neighbors_counter)
        #print(region_neighbors_counter)            
        #print("")
    
    # Gets region with maximum # of unassigned neighbors
    try:
        holder = max(region_neighbors_counter, key=lambda element: region_neighbors_counter[element])
    except ValueError:
        return min_regions[0]
    #Checking if there's multiple regions with same degree
    counter = 0
    for key in region_neighbors_counter.keys():
        if region_neighbors_counter[key] == region_neighbors_counter[holder]:
            counter += 1
    # If no explicit maximum, choose random region
    if counter > 1:
        return random.choice(region_neighbors_counter.keys())
    else:
        return holder
    

"""" Didn't create order-domain-values because I ordered values in Region class"""

#def inference()
# Returns color of region
def assignment_color(region):
    color = ""
    for key in region.colors:
        if region.colors[key] == 1:
            color = key
            break
    return color

# Checks if neighbors have color assigned
# If not, color can be assigned to region
def color_valid(color, region):
    valid = True
    for neighbor in region.neighbors:
        if neighbor.colors[color] == 1:
            valid = False
            return False
    return True
        

def inference(region):
    # Returns True if failure
    # -1 means color is removed
    # Removes color possibility from neighbors by setting color equal to -1
    color = assignment_color(region)
    for neighbor in region.neighbors:
        neighbor.colors[color] = -1
        neighbor.poss_color -= 1
    failure = True
    # Checks if any neighbor has all possibilities removec
    for neighbor in region.neighbors:
        for color in neighbor.colors.keys():
            if neighbor.colors[color] == -1:
                failure = True
            else:
                failure = False
                break
        if failure == True:
            return True
    return False

def backtracking(regions):
    solution = []
    complete = True
    # Check if all variables are assigned
    #print(regions)
    for region in regions:
        for key in region.colors.keys():
            if region.colors[key] == 0:
                complete = False
                break
    if complete == True:
        for place in regions:
            #solution.append(f"{place.name}: {assignment_color(place)}")
            solution.append("{name}: {color}".format(name=place.name, color=assignment_color(place)))
        return solution

    unassigned_lst = []
    # Generates list of unassigned variales using check_assignment()
    for territory in regions:
        #print(check_assignment(territory))
        if check_assignment(territory) == False:
            unassigned_lst.append(territory)
            #print(unassigned_lst)
    var = unassign_var(unassigned_lst)
    #print(var)
    #Iterates through colors and uses color_valid() to determine if color can be assigned to region
    for color in var.colors.keys():
        if color_valid(color, var) == True:
            var.colors[color] = 1
            #If it did not fail // It passed
            # Runs inference()
            if inference(var) != True:
                #print(inference(var))
                new_regions = copy.deepcopy(regions)
                result = backtracking(new_regions) 
                return result  
            else:
                return True
   
    
    #return True;
#True means failure


regions = gen_regions(places_names, colors)
calc_neigh(array_2d, regions)
solution_one = backtracking(regions)


output_file_one = open("output_file_one.txt", "w")
output_file_one.write("{solution}".format(solution = solution_one))
output_file_one.write("\n")

if solution_one is not True:
    for line in solution_one:
        output_file_one.write(line)
        output_file_one.write("\n")
output_file_one.close()

print(solution_one)
if solution_one is not True:
    for line in solution_one:
        print(line)







    #If value is valid 
    #then var = val
    #append to assignment




    










