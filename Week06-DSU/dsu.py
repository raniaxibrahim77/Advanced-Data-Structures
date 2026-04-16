class SocialNetwork:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.num_groups = n

    def find(self, i):
        if self.parent[i] == i:
            return i
        self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, i, j):
        root_i = self.find(i)
        root_j = self.find(j)

        if root_i != root_j:
            if self.rank[root_i] < self.rank[root_j]:
                self.parent[root_i] = root_j
            elif self.rank[root_i] > self.rank[root_j]:
                self.parent[root_j] = root_i
            else:
                self.parent[root_i] = root_j
                self.rank[root_j] += 1

            self.num_groups -= 1
            return True
        return False

    def get_groups(self):
        groups = {}
        for i in range(len(self.parent)):
            root = self.find(i)
            if root not in groups:
                groups[root] = []
            groups[root].append(i)
        return groups


#Example
n = 7
friendships = [(0, 1), (1, 2), (3, 4), (5, 6)]
network = SocialNetwork(n)

for u, v in friendships:
    network.union(u, v)

all_groups = network.get_groups()
print(f"Total Groups: {network.num_groups}")
for i, members in enumerate(all_groups.values(), 1):
    print(f"Group {i}: {set(members)} (Size: {len(members)})")