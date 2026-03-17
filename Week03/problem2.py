import heapq
from collections import defaultdict


class DynamicMedian:
    def __init__(self):
        self.lower = []
        self.upper = []
        self.to_remove = defaultdict(int)
        self.lower_size = 0
        self.upper_size = 0

    def add(self, x):
        if not self.lower or x <= -self.lower[0]:
            heapq.heappush(self.lower, -x)
            self.lower_size += 1
        else:
            heapq.heappush(self.upper, x)
            self.upper_size += 1
        self._rebalance()

    def remove(self, x):
        if x in self.to_remove or (self.lower and x <= -self.lower[0]) or (self.upper and x >= self.upper[0]):
            self.to_remove[x] += 1
            if self.lower and x <= -self.lower[0]:
                self.lower_size -= 1
            else:
                self.upper_size -= 1

            self._clean_heap(self.lower, True)
            self._clean_heap(self.upper, False)
            self._rebalance()

    def median(self):
        self._clean_heap(self.lower, True)
        return -self.lower[0]

    def _clean_heap(self, heap, is_lower):
        while heap:
            val = -heap[0] if is_lower else heap[0]
            if self.to_remove[val] > 0:
                self.to_remove[val] -= 1
                heapq.heappop(heap)
            else:
                break

    def _rebalance(self):
        if self.lower_size > self.upper_size + 1:
            val = -heapq.heappop(self.lower)
            self.lower_size -= 1
            self._clean_heap(self.lower, True)
            heapq.heappush(self.upper, val)
            self.upper_size += 1
        elif self.lower_size < self.upper_size:
            val = heapq.heappop(self.upper)
            self.upper_size -= 1
            self._clean_heap(self.upper, False)
            heapq.heappush(self.lower, -val)
            self.lower_size += 1

        self._clean_heap(self.lower, True)
        self._clean_heap(self.upper, False)


#Example from file
dm = DynamicMedian()
commands = [
    ("ADD", 5), ("ADD", 2), ("ADD", 10), ("MEDIAN",),
    ("ADD", 7), ("MEDIAN",),
    ("REMOVE", 5), ("MEDIAN",)
]

for cmd in commands:
    if cmd[0] == "ADD":
        dm.add(cmd[1])
    elif cmd[0] == "REMOVE":
        dm.remove(cmd[1])
    elif cmd[0] == "MEDIAN":
        print(dm.median())