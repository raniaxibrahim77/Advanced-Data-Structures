class BinomialNode:
    def __init__(self, key):
        self.key = key
        self.degree = 0
        self.p = None
        self.child = None
        self.sibling = None

class BinomialHeap:
    def __init__(self):
        self.head = None

    def binomial_link(self, y, z):
        y.p = z
        y.sibling = z.child
        z.child = y
        z.degree += 1

    def _merge(self, h1, h2):
        if not h1: return h2
        if not h2: return h1
        if h1.degree <= h2.degree:
            head = h1
            h1 = h1.sibling
        else:
            head = h2
            h2 = h2.sibling
        curr = head
        while h1 and h2:
            if h1.degree <= h2.degree:
                curr.sibling = h1
                h1 = h1.sibling
            else:
                curr.sibling = h2
                h2 = h2.sibling
            curr = curr.sibling
        curr.sibling = h1 or h2
        return head

    def union(self, other_heap):
        self.head = self._merge(self.head, other_heap.head)
        if not self.head: return
        prev_x = None
        x = self.head
        next_x = x.sibling
        while next_x:
            if (x.degree != next_x.degree) or \
               (next_x.sibling and next_x.sibling.degree == x.degree):
                prev_x = x
                x = next_x
            elif x.key <= next_x.key:
                x.sibling = next_x.sibling
                self.binomial_link(next_x, x)
            else:
                if not prev_x:
                    self.head = next_x
                else:
                    prev_x.sibling = next_x
                self.binomial_link(x, next_x)
                x = next_x
            next_x = x.sibling

    def insert(self, key):
        new_node = BinomialNode(key)
        new_h = BinomialHeap()
        new_h.head = new_node
        self.union(new_h)

    def extract_min(self):
        if not self.head: return None
        min_prev, prev = None, None
        min_node = self.head
        curr = self.head
        while curr:
            if curr.key < min_node.key:
                min_node, min_prev = curr, prev
            prev=curr
            curr = curr.sibling
        if min_prev: min_prev.sibling = min_node.sibling
        else: self.head = min_node.sibling
        child_h = BinomialHeap()
        prev_c, curr_c = None, min_node.child
        while curr_c:
            next_c = curr_c.sibling
            curr_c.sibling = prev_c
            curr_c.p = None
            prev_c, curr_c = curr_c, next_c
        child_h.head = prev_c
        self.union(child_h)
        return min_node

    def decrease_key(self, node, k):
        if k > node.key: return
        node.key = k
        y = node
        z = y.p
        while z and y.key < z.key:
            y.key, z.key = z.key, y.key
            y = z
            z = y.p

def print_heap(node, depth=0):
    while node:
        print("  " * depth + f"Key: {node.key} (Degree: {node.degree})")
        if node.child:
            print_heap(node.child, depth + 1)
        node = node.sibling

if __name__ == "__main__":
    h = BinomialHeap()
    for val in [10, 20, 5, 15, 3]:
        h.insert(val)

    print("Binomial Heap Structure:")
    print_heap(h.head)

    m = h.extract_min()
    print(f"\nExtracted Min: {m.key}")

    print("\nStructure after extraction:")
    print_heap(h.head)