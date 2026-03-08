class RBNode:
    RED = 0
    BLACK = 1

    def __init__(self, key, color=RED, left=None, right=None, parent=None):
        self.key = key
        self.color = color
        self.left = left
        self.right = right
        self.parent = parent

    def __str__(self):
        color_str = "R" if self.color == RBNode.RED else "B"
        return f"{self.key}({color_str})"


class RedBlackTree:
    def __init__(self):
        self.NIL = RBNode(key=None, color=RBNode.BLACK)
        self.root = self.NIL

    def search(self, key):
        curr = self.root
        while curr != self.NIL and key != curr.key:
            if key < curr.key:
                curr = curr.left
            else:
                curr = curr.right
        return curr

    def minimum(self, node):
        while node.left != self.NIL:
            node = node.left
        return node

    def maximum(self, node):
        while node.right != self.NIL:
            node = node.right
        return node

    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.NIL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def right_rotate(self, y):
        x = y.left
        y.left = x.right
        if x.right != self.NIL:
            x.right.parent = y
        x.parent = y.parent
        if y.parent is None:
            self.root = x
        elif y == y.parent.right:
            y.parent.right = x
        else:
            y.parent.left = x
        x.right = y
        y.parent = x

    def insert(self, key):
        new_node = RBNode(key, left=self.NIL, right=self.NIL)
        y = None
        x = self.root

        while x != self.NIL:
            y = x
            if new_node.key < x.key:
                x = x.left
            else:
                x = x.right

        new_node.parent = y
        if y is None:
            self.root = new_node
        elif new_node.key < y.key:
            y.left = new_node
        else:
            y.right = new_node

        new_node.color = RBNode.RED
        self._insert_fixup(new_node)

    def _insert_fixup(self, k):
        while k.parent and k.parent.color == RBNode.RED:
            if k.parent == k.parent.parent.left:
                u = k.parent.parent.right  
                if u.color == RBNode.RED:
                    k.parent.color = RBNode.BLACK
                    u.color = RBNode.BLACK
                    k.parent.parent.color = RBNode.RED
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        k = k.parent
                        self.left_rotate(k)
                    k.parent.color = RBNode.BLACK
                    k.parent.parent.color = RBNode.RED
                    self.right_rotate(k.parent.parent)
            else:
                u = k.parent.parent.left
                if u.color == RBNode.RED:
                    k.parent.color = RBNode.BLACK
                    u.color = RBNode.BLACK
                    k.parent.parent.color = RBNode.RED
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        self.right_rotate(k)
                    k.parent.color = RBNode.BLACK
                    k.parent.parent.color = RBNode.RED
                    self.left_rotate(k.parent.parent)
            if k == self.root: break
        self.root.color = RBNode.BLACK

    def delete(self, key):
        z = self.search(key)
        if z == self.NIL: return  

        y = z
        y_original_color = y.color
        if z.left == self.NIL:
            x = z.right
            self._transplant(z, z.right)
        elif z.right == self.NIL:
            x = z.left
            self._transplant(z, z.left)
        else:
            y = self.minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self._transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
            self._transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color

        if y_original_color == RBNode.BLACK:
            self._delete_fixup(x)

    def _transplant(self, u, v):
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def _delete_fixup(self, x):
        while x != self.root and x.color == RBNode.BLACK:
            if x == x.parent.left:
                s = x.parent.right
                if s.color == RBNode.RED:
                    s.color = RBNode.BLACK
                    x.parent.color = RBNode.RED
                    self.left_rotate(x.parent)
                    s = x.parent.right
                if s.left.color == RBNode.BLACK and s.right.color == RBNode.BLACK:
                    s.color = RBNode.RED
                    x = x.parent
                else:
                    if s.right.color == RBNode.BLACK:
                        s.left.color = RBNode.BLACK
                        s.color = RBNode.RED
                        self.right_rotate(s)
                        s = x.parent.right
                    s.color = x.parent.color
                    x.parent.color = RBNode.BLACK
                    s.right.color = RBNode.BLACK
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                s = x.parent.left
                if s.color == RBNode.RED:
                    s.color = RBNode.BLACK
                    x.parent.color = RBNode.RED
                    self.right_rotate(x.parent)
                    s = x.parent.left
                if s.right.color == RBNode.BLACK and s.left.color == RBNode.BLACK:
                    s.color = RBNode.RED
                    x = x.parent
                else:
                    if s.left.color == RBNode.BLACK:
                        s.right.color = RBNode.BLACK
                        s.color = RBNode.RED
                        self.left_rotate(s)
                        s = x.parent.left
                    s.color = x.parent.color
                    x.parent.color = RBNode.BLACK
                    s.left.color = RBNode.BLACK
                    self.right_rotate(x.parent)
                    x = self.root
        x.color = RBNode.BLACK

    def print_tree(self, node, indent="", last=True):
        if node != self.NIL:
            print(indent, end="")
            if last:
                print("R----", end="")
                indent += "     "
            else:
                print("L----", end="")
                indent += "|    "
            print(str(node))
            self.print_tree(node.left, indent, False)
            self.print_tree(node.right, indent, True)


#Usage Example
if __name__ == "__main__":
    tree = RedBlackTree()

    #Insert nodes
    for val in [10, 20, 30, 15, 25, 5]:
        tree.insert(val)

    print("RB Tree Structure after insertions:")
    tree.print_tree(tree.root)

    #Min/Max
    print(f"\nMinimum: {tree.minimum(tree.root)}")
    print(f"Maximum: {tree.maximum(tree.root)}")

    #Search
    target = 15
    found = tree.search(target)
    print(f"\nSearching for {target}: {'Found' if found != tree.NIL else 'Not Found'}")

    #Delete
    print(f"\nDeleting 20...")
    tree.delete(20)
    tree.print_tree(tree.root)
