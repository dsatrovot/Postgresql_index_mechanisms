class BTreeNode:
    def __init__(self, leaf=True,level_name="children"):
        self.keys = []
        self.children = []
        self.leaf = leaf
        self.level_name = level_name

class  BTree:
    def __init__(self, t=2):
        self.root = BTreeNode(level_name = "root")
        self.t = t


    def search(self, key, node=None):
        if node is None:
            node = self.root

        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            
            i += 1

        if i < len(node.keys) and key == node.keys[i]:
            return node

        if node.leaf:
            return None

        # for li in node.children:
        #     print(f"children -> for {li.keys}")
        # print(f"{node.keys} -> {node.children[i].keys} -> {i} -> {node.children}")
        return self.search(key, node.children[i])

    def split_child(self,parent,i):
        t = self.t
        full = parent.children[i]
        print(f"children keys - > {full.keys}")

        right = BTreeNode(leaf=full.leaf)

        middle_key=full.keys[t-1]
        print(f"middle_key after split node -> {middle_key}")
        right.keys=full.keys[t:]
        print(f"right_keys after split node -> {right.keys}")

        full.keys=full.keys[:t-1]

        print(f"left keys after split node -> {full.keys}")
        print(f"full is leaf -> {full.leaf}")
        if not full.leaf:
            right.children = full.children[t:]
            full.children = full.children[:t]
        
        parent.keys.insert(i,middle_key)
        print(f"new parent node key {parent.keys}")
        parent.children.insert(i+1,right)
        print(f"new root childrens -> {parent.children}")

    def insert(self, key):
        root = self.root
        max_keys = 2 * self.t - 1

        if len(root.keys) == max_keys:
            print(f"new root -> {root.keys}")
            new_root=BTreeNode(leaf=False,level_name="root")
            root.level_name="children"
            new_root.children.append(root)
            print(vars(self))
            
            self.root = new_root
            print(vars(self.root))
            self.split_child(new_root,0)

        self._insert_non_full(self.root,key)
        print(self.root.keys)

    def _insert_non_full(self,node,key):
        i = len(node.keys) - 1

        if node.leaf:
            print(f"key {key} in in node {node.level_name}")
            node.keys.append(None)

            while i >= 0 and key < node.keys[i]:
                node.keys[i+1] = node.keys[i]
                i -= 1
            
            node.keys[i+1]=key
            # print(f"in leaf -> {node.keys}")
            return

        while i >= 0 and key < node.keys[i]:
            i -= 1
        i += 1

        if len(node.children[i].keys) == 2 * self.t - 1:
            print(f"before right split {node.children[i].keys} but {node.children[i].children} ")
            self.split_child(node,i)
            print(f"after right split {node.children[i].keys} but {node.children[i].children}")
            if key > node.keys[i]:
                i += 1
        self._insert_non_full(node.children[i],key)

    def range_search(self, low, high):
        
        
        result = []
        # result_root = []
        # result_left_children_root=[]

        def walk(node):
            i = 0

            while i < len(node.keys):

                if not node.leaf and low < node.keys[i]:
                    walk(node.children[i])

                if low <= node.keys[i] <= high:
                    result.append(node.keys[i])
                i += 1
            if not node.leaf:
                walk(node.children[-1])
        walk(self.root)
        return sorted(result)


tree = BTree(2)
print(vars(tree))
for age in [25, 19, 32, 22, 28, 35, 40, 18, 50, 60, 27, 15]:
    tree.insert(age)

print(tree.search(50))

print(tree.range_search(16,32))