class BTreeNode:
    def __init__(self, leaf=False):
        self.leaf = leaf
        self.keys = []
        self.children = []

class BTree:
    def __init__(self, t):
        self.root = BTreeNode(True)
        self.t = t

    def search(self, k, x=None):
        if x is None:
            x = self.root
        i = 0
        while i < len(x.keys) and k > x.keys[i]:
            i += 1
        if i < len(x.keys) and k == x.keys[i]:
            return (x, i)
        elif x.leaf:
            return None
        else:
            return self.search(k, x.children[i])

    def insert(self, k):
        r = self.root
        if len(r.keys) == (2 * self.t) - 1:
            s = BTreeNode(False)
            self.root = s
            s.children.insert(0, r)
            self._split_child(s, 0, r)
            self._insert_non_full(s, k)
        else:
            self._insert_non_full(r, k)

    def _insert_non_full(self, x, k):
        i = len(x.keys) - 1
        if x.leaf:
            x.keys.append(None)
            while i >= 0 and k < x.keys[i]:
                x.keys[i + 1] = x.keys[i]
                i -= 1
            x.keys[i + 1] = k
        else:
            while i >= 0 and k < x.keys[i]:
                i -= 1
            i += 1
            if len(x.children[i].keys) == (2 * self.t) - 1:
                self._split_child(x, i, x.children[i])
                if k > x.keys[i]:
                    i += 1
            self._insert_non_full(x.children[i], k)

    def _split_child(self, x, i, y):
        t = self.t
        z = BTreeNode(y.leaf)
        z.keys = y.keys[t : (2 * t) - 1]
        if not y.leaf:
            z.children = y.children[t : 2 * t]
        median_key = y.keys[t - 1]
        y.keys = y.keys[0 : t - 1]
        x.children.insert(i + 1, z)
        x.keys.insert(i, median_key)

#Test Case
if __name__ == "__main__":
    btree = BTree(3)
    keys_to_insert = [10, 20, 5, 6, 12, 30, 7, 17]

    for key in keys_to_insert:
        btree.insert(key)

    search_key = 12
    result = btree.search(search_key)

    if result:
        node, index = result
        print(f"Key {search_key} found in node with keys {node.keys}")
    else:
        print(f"Key {search_key} not found.")