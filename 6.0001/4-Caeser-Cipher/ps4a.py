# Problem Set 4A
# Name: Citlali Trigos
# Collaborators: none 
# Date: 6/7/20

def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    'ab'
    '''

    if len(sequence) ==1: return [sequence]
    permutations = []
    for word in get_permutations(sequence[1:]): 
        for i in range(len(word)+1):
            permutations.append(word[:i] + sequence[0] +word[i:])
    return permutations
    

if __name__ == '__main__':
#    # Put three example test cases here (for your sanity, limit your inputs
#    to be three characters or fewer as you will have n! permutations for a 
#    sequence of length n)

    def test(input, correct_output):
        output = get_permutations(input)
        output.sort(), correct_output.sort()
        if not output == correct_output: 
            print('Failed on input: ' + input)
        return 'passed'


    correct_ab = ['ab', 'ba']
    correct_abc = ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']
    correct_abcd = ['abcd', 'bacd', 'bcad', 'bcda', 'acbd', 'cabd', 'cbad', 'cbda', 'acdb', 'cadb', 'cdab', 'cdba', 'abdc', 'badc', 'bdac', 'bdca', 'adbc', 'dabc', 'dbac', 'dbca', 'adcb', 'dacb', 'dcab', 'dcba']
    if test('ab', correct_ab) == test('abc', correct_abc) == test('abcd', correct_abcd) =='passed':
        print('*****************')
        print('Supa nice: All tests passed!')
