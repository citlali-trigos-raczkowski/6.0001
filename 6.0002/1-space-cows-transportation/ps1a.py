###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name: Citlali Trigos
# Collaborators: none
# Date: 6/12/20
from ps1_partition import get_partitions
import time

#================================
# Part A: Transporting Space Cows
#================================

# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    file = open(filename, 'r')
    cows = {}
    for line in file:
        list_split = line.split(',')
        cows[list_split[0]] = int(list_split[1])
    return cows 

# Problem 2
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    trips = []
    sorted_cows = sorted(cows.items(), key=lambda x: x[1], reverse=True)
    for (cow_name, cow_weight) in sorted_cows:
        already_used = False
        for trip in trips:
            current_trip_weight = 0 
            for cow in trip:
                current_trip_weight+= cows[cow]
            if current_trip_weight+cow_weight<=limit:
                trip.append(cow_name)
                already_used = True
        if not already_used: trips.append([cow_name])
    return trips 




# Problem 3
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    best_partition, fewest_trips = None, None #[[x,y,]]
    for partition in get_partitions(cows.keys()): #[[[x,y], [z]], [[x,y,z]], [[x], [y,z]]]
        ok_partition= True 
        if fewest_trips is None or len(partition)< fewest_trips :  # we should only try to improve 
            for trip in partition: # for each trip 
                total_sum = 0 # let's make sure we're good with weight 
                for cow in trip: total_sum+=cows[cow]
                if total_sum>limit:  #over limit 
                    ok_partition = False 
                    break 
            if ok_partition: 
                fewest_trips = len(partition)
                best_partition = partition
    return best_partition
        

        
# Problem 4
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    cows = load_cows('ps1_cow_data.txt')
    start_brute = time.time()
    brute_force = brute_force_cow_transport(cows,limit=10)
    end_brute = time.time()
    start_greedy = time.time()
    greedy_approach = greedy_cow_transport(cows,limit=10)
    end_greedy = time.time()
    greedy_time = end_greedy-start_greedy
    brute_time = end_brute-start_brute
    print('Brute force: ', len(brute_force), ' total trips. Time: ', brute_time)
    print('Greedy approach:', len(greedy_approach), ' total trips. Time: ', greedy_time)
    print('Greedy ran faster by ', brute_time - greedy_time, ' seconds.' )

if __name__ == '__main__':
    compare_cow_transport_algorithms()

# **********************************************************************************************
# Writeup:

# Brute Force will always return the optimal solution, because by definition the brute force 
# appoach enumerates every possible solution and selects the ideal one. The drawback is the time 
# (and/or space) requirement. 

# The greedy approach does NOT necessarily return the optimal solution. It's an algorithm that 
# searches for the local optimal choice in the process of finding the global optimum, with no going
# back. It's like going for a hike and only walking up in altitude thinking that's how to get to the
# tallest mountain. Perhaps the tallest mountain (the global max) starts lower than where you are. 
# The benefit is the one-track mind - with a single goal in mind (choose the local best), it is 
# significantly faster than the brute force algorithm.
