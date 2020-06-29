# Problem Set 4C
# Name: Citlali Trigos 
# Date: 6/10/20
# Collaborators: none

import string
from ps4a import get_permutations

### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list


### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

# you may find these constants helpful
VOWELS_LOWER = 'aeiou'
VOWELS_UPPER = 'AEIOU'
CONSONANTS_LOWER = 'bcdfghjklmnpqrstvwxyz'
CONSONANTS_UPPER = 'BCDFGHJKLMNPQRSTVWXYZ'

class SubMessage(object):
    def __init__(self, text):
        '''
        Initializes a SubMessage object
                
        text (string): the message's text

        A SubMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)

    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        return self.message_text

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.
        
        Returns: a COPY of self.valid_words
        '''
        return self.valid_words.copy()
                
    def build_transpose_dict(self, vowels_permutation):
        '''
        vowels_permutation (string): a string containing a permutation of vowels (a, e, i, o, u)
        
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to an
        uppercase and lowercase letter, respectively. Vowels are shuffled 
        according to vowels_permutation. The first letter in vowels_permutation 
        corresponds to a, the second to e, and so on in the order a, e, i, o, u.
        The consonants remain the same. The dictionary should have 52 
        keys of all the uppercase letters and all the lowercase letters.

        Example: When input "eaiuo":
        Mapping is a->e, e->a, i->i, o->u, u->o
        and "Hello World!" maps to "Hallu Wurld!"

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        shift_dict = {}
        vowels = ['a', 'e', 'i', 'o', 'u']
        for i in range(5): # for vowels
            shift_dict[vowels[i]] = vowels_permutation[i]
            shift_dict[vowels[i].upper()] = vowels_permutation[i].upper()
        for i in string.ascii_lowercase: # for consonant
            if i not in vowels_permutation:  
                shift_dict[i] = i
                shift_dict[i.upper()] = i .upper()
        return shift_dict
    
    def apply_transpose(self, transpose_dict):
        '''
        transpose_dict (dict): a transpose dictionary
        
        Returns: an encrypted version of the message text, based 
        on the dictionary
        '''
        
        text = self.get_message_text()
        encrypted_text = [transpose_dict[i] if i in transpose_dict else i for i in text]
        return ''.join(encrypted_text)

class EncryptedSubMessage(SubMessage):
    def __init__(self, text):
        '''
        Initializes an EncryptedSubMessage object

        text (string): the encrypted message text

        An EncryptedSubMessage object inherits from SubMessage and has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        SubMessage.__init__(self, text)

    def decrypt_message(self):
        '''
        Attempt to decrypt the encrypted message 
        
        Idea is to go through each permutation of the vowels and test it
        on the encrypted message. For each permutation, check how many
        words in the decrypted text are valid English words, and return
        the decrypted message with the most English words.
        
        If no good permutations are found (i.e. no permutations result in 
        at least 1 valid word), return the original string. If there are
        multiple permutations that yield the maximum number of words, return any
        one of them.

        Returns: the best decrypted message    
        
        Hint: use your function from Part 4A
        '''
        vowels = 'aeiou'
        vowel_permutations = get_permutations(vowels)
        max_words = 0
        best_decryption = None
        valid_words = self.get_valid_words()
        for permutation in vowel_permutations:
            transpose_dict = self.build_transpose_dict(permutation)
            transpose = self.apply_transpose(transpose_dict).split(' ')
            total_valid_words = 0
            for i in transpose: 
                if is_word(valid_words, i): total_valid_words+=1
            if total_valid_words> max_words:
                max_words = total_valid_words
                best_decryption = transpose 
        return ' '.join(best_decryption)
    

if __name__ == '__main__':

    def Test(message, permutation, expected):
        message = message = SubMessage(message)
        enc_dict = message.build_transpose_dict(permutation)
        original_message = message.get_message_text()
        actual_encryption = message.apply_transpose(enc_dict)
        enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
        decrypted_message = enc_message.decrypt_message()
        if actual_encryption!= expected or original_message!= decrypted_message:
            print('TEST FAILED: ')
            print("Original message: ", original_message, " Permutation:", permutation)
            print("Expected encryption: ", expected, " But received encryption:", actual_encryption)
            print("Decrypted message: ", decrypted_message)
        else: 
            return True

    test_1 = Test("Hello World!", "eaiuo", "Hallu Wurld!")
    test_2 = Test('Hi it is me!', 'iouea', 'Hu ut us mo!')
    test_3 = Test('Welcome to the house of Vegetables, my lady', 'eiuao', 'Wilcami ta thi haosi af Vigiteblis, my ledy')
    if test_1 == test_2 == test_3 and test_2: print('All tests passed! congrats!!')
