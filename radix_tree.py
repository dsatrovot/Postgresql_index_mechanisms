class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:

    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word):
        # for key_char in self.root.children:
            # print(key_char )

        node = self.root
        
        for char in word:
            if char not in node.children:
                # print(char)
                node.children[char] = TrieNode()
                # print(len(node.children))
            node = node.children[char]
        
        node.is_end = True
        print(node.children)

    def search(self,word):
        node = self.root

        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        
        return node.is_end
    
    def get_words(self,prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]

        result = []

        def dfs(current,path):
            if current.is_end:
                result.append(path)
            for char,child in current.children.items():
                dfs(child,path+char)

        dfs(node,prefix)
        return result

    def delete(self,word):
        
        def remove(node,word,depth):
            if depth == len(word):
                
                if not node.is_end:
                    return False
                
                node.is_end = False

                return len(node.children) == 0
            
            char = word[depth]
            if char not in node.children:
                return False
            child = node.children[char]

            should_delete = remove(child,word,depth+1)

            if should_delete:
                del node.children[char]
            return (
                not node.is_end
                and len(node.children) == 0
            )
        remove(self.root,word,0)



prefix_trie = Trie()
prefix_trie.insert("app")
prefix_trie.insert("apple")
prefix_trie.insert("application")
print(prefix_trie.search("app"))
print(prefix_trie.search("apploid"))
print(prefix_trie)
print(prefix_trie.get_words("app"))
prefix_trie.delete("app")
print(prefix_trie.get_words("app"))