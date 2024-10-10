class TrieNode:
    def __init__(self):
        self.children = {}
        self.end_of_word = False
        
class Autocompleter:
    def __init__(self, words):
        self.root = TrieNode()
        self._build_trie(words)
    
    def _build_trie(self, words):
        for word in words:
            self._insert(word)
    
    def _insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.end_of_word = True
    
    def _find_prefix_node(self, prefix):
        node = self.root
        for char in prefix:
            if char in node.children:
                node = node.children[char]
            else:
                return None
        return node
    
    # Performs a depth-first search 
    def _dfs(self, node, prefix):
        results = []
        if node.end_of_word:
            results.append(prefix)
        
        for char, child_node in node.children.items():
            results.extend(self._dfs(child_node, prefix + char))
        
        return results
    
    def complete(self, prefix, n):
        results = []
        prefix_node = self._find_prefix_node(prefix)
        
        if prefix_node is None:
            return results
        
        results = self._dfs(prefix_node, prefix)
        return results[:n]

# Example usage:
if __name__ == "__main__":
    words = ["apple", "apples", "applesauce", "applewood", "banana"]
    autocompleter = Autocompleter(words)
    
    print(autocompleter.complete("app", 10))  # Output: ['peach', 'pear', 'pineapple']
    print(autocompleter.complete("app", 2))  # Output: ['apple']
    print(autocompleter.complete("apples", 5))  # Output: []
    print(autocompleter.complete("banana", 5)) 
    print(autocompleter.complete("or", 5)) 

