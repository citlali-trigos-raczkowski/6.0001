###########################
# 6.0002 Problem Set 1b: Space Change
# Name: Citlali Trigos
# Collaborators: none
# Date: 6/12/20

#================================
# Part B: Golden Eggs
#================================

# Problem 1
def dp_make_weight(egg_weights, target_weight):
    """
    Find number of eggs to bring back, using the smallest number of eggs. Assumes there is
    an infinite supply of eggs of each weight, and there is always a egg of value 1.
    
    Parameters:
    egg_weights - tuple of integers, available egg weights sorted from smallest to largest value (1 = d1 < d2 < ... < dk)
    target_weight - int, amount of weight we want to find eggs to fit
    memo - dictionary, OPTIONAL parameter for memoization (you may not need to use this parameter depending on your implementation)
    
    Returns: int, smallest number of eggs needed to make target weight
    """
    # BASE CASE: if no more egg options or target_weight met: return 0 
    # OTHERWISE: we always want the heaviest we can currently take so:
    # 1. sort eggs from largest to smallest
    # 2. if the largest is too heavy, remove it and return back 
    # 3. else return while taking it & update both vars 

    if egg_weights==[] or target_weight==0: return 0 
    sorted_eggs = sorted(egg_weights, reverse = True)
    if target_weight - sorted_eggs[0] < 0: return dp_make_weight(sorted_eggs[1:], target_weight)
    else: return 1 + dp_make_weight(sorted_eggs, target_weight - sorted_eggs[0])


# EXAMPLE TESTING CODE, feel free to add more if you'd like
if __name__ == '__main__':
    egg_weights = (1, 5, 10, 25)
    n = 99
    print("Egg weights = (1, 5, 10, 25)")
    print("n = 99")
    print("Expected ouput: 9 (3 * 25 + 2 * 10 + 4 * 1 = 99)")
    print("Actual output:", dp_make_weight(egg_weights, n))
    print()