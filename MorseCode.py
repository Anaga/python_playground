from typing import List

morse_code_dict = {
    '.': 'E', 
    '..': 'I', 
    '...': 'S', 
    '..-': 'U', 
    '.-': 'A', 
    '.-.': 'R', 
    '.--': 'W', 
    '-': 'T', 
    '-.': 'N', 
    '-..': 'D', 
    '-.-': 'K', 
    '--': 'M', 
    '--.': 'G', 
    '---': 'O'
}

def codeToLetter(code: str)-> str:
  return morse_code_dict.get(code, '')

def generate_combinations(word: str) -> List[str]:
    def helper(current: str, index: int) -> List[str]:
        if index == len(word):
            return [current]
        
        if word[index] == '?':
            results = []
            # Replace '?' with '.' and '-' respectively
            results.extend(helper(current + '.', index + 1))
            results.extend(helper(current + '-', index + 1))
            return results
        else:
            return helper(current + word[index], index + 1)
    
    # Generate combinations using the helper function
    return helper('', 0)

def possibilities(word: str) -> List[str]:
  if '?' in word:
    ret_list = []
    possible_list = generate_combinations(word)
    print(possible_list)
    for code in possible_list:
      ret_list.append(codeToLetter(code))
    return ret_list  
  else:
    return list(codeToLetter(word))

# Example usage
print(generate_combinations('?'))     # Output: ['.', '-']
print(generate_combinations('-.?'))   # Output: ['-..', '-.-']
print(generate_combinations('?.?'))   # Output: ['...', '..-', '-..', '-.-']
print(generate_combinations('---'))   # Output: ['---']
print(generate_combinations('.-.'))   # Output: ['.-.']

print(possibilities('?'))
print(possibilities('?.'))
print(possibilities('.?'))
print(possibilities('?.?'))
