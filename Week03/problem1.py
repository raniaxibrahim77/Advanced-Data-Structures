import heapq


class LiveLeaderboard:
    def __init__(self):
        self.scores = {}

    def add_player(self, name, score):
        self.scores[name] = score

    def update_player(self, name, delta):
        if name in self.scores:
            self.scores[name] += delta

    def remove_player(self, name):
        if name in self.scores:
            del self.scores[name]

    def top_k(self, k):
        top_players = heapq.nlargest(
            k,
            self.scores.items(),
            key=lambda item: (item[1], item[0])
        )

        for name, score in top_players:
            print(f"{name} {score}")
        print()


#Example from file
def run_simulation():
    lb = LiveLeaderboard()

    lb.add_player("Alice", 120)

    lb.add_player("Bob", 90)

    lb.add_player("Carol", 150)

    lb.update_player("Bob", 50)

    lb.top_k(2)

    lb.remove_player("Carol")

    lb.top_k(2)


if __name__ == "__main__":
    run_simulation()