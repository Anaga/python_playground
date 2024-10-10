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

def generate_combinations(word: str) -> List[str]:
    def helper(current: str, index: int) -> List[str]:
        if index == len(word):
            return [current]
        
        if word[index] == '?':
            results = []
            for key in morse_code_dict.keys():
                results.extend(helper(current + key, index + 1))
            return results
        else:
            return helper(current + word[index], index + 1)
    
    return helper('', 0)

# Example usage
print(generate_combinations('?'))  # Should return ['.', '-']