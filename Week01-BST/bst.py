class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None


class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, key):
        if self.root is None:
            self.root = Node(key)
        else:
            self._insert_recursive(self.root, key)

    def _insert_recursive(self, node, key):
        if key < node.key:
            if node.left is None:
                node.left = Node(key)
            else:
                self._insert_recursive(node.left, key)
        else:
            if node.right is None:
                node.right = Node(key)
            else:
                self._insert_recursive(node.right, key)

    def search(self, key):
        return self._search_recursive(self.root, key)

    def _search_recursive(self, node, key):
        if node is None or node.key == key:
            return node
        if key < node.key:
            return self._search_recursive(node.left, key)
        return self._search_recursive(node.right, key)

    def find_min(self, node=None):
        current = node if node else self.root
        if not current: return None
        while current.left:
            current = current.left
        return current

    def find_max(self, node=None):
        current = node if node else self.root
        if not current: return None
        while current.right:
            current = current.right
        return current

    def delete(self, key):
        self.root = self._delete_recursive(self.root, key)

    def _delete_recursive(self, node, key):
        if node is None:
            return node

        if key < node.key:
            node.left = self._delete_recursive(node.left, key)
        elif key > node.key:
            node.right = self._delete_recursive(node.right, key)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left

            temp = self.find_min(node.right)
            node.key = temp.key
            node.right = self._delete_recursive(node.right, temp.key)

        return node

    def inorder_traversal(self, node, result=None):
        if result is None: result = []
        if node:
            self.inorder_traversal(node.left, result)
            result.append(node.key)
            self.inorder_traversal(node.right, result)
        return result


if __name__ == "__main__":
    bst = BinarySearchTree()
    for val in [50, 30, 70, 20, 40, 60, 80]:
        bst.insert(val)

    print(f"Initial Tree: {bst.inorder_traversal(bst.root)}")
    print(f"Min: {bst.find_min().key}")
    print(f"Max: {bst.find_max().key}")

    target = 40
    found = bst.search(target)
    print(f"Search {target}: {'Found' if found else 'Not Found'}")

    bst.delete(20)
    print(f"After deleting 20: {bst.inorder_traversal(bst.root)}")

    bst.delete(50)
    print(f"After deleting 50 (Root): {bst.inorder_traversal(bst.root)}")