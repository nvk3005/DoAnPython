import matplotlib.pyplot as plt

class VideoGameBarChart:
    def __init__(self, genres, counts):
        self.genres = genres
        self.counts = counts

    def plot_chart(self):
        plt.figure(figsize=(12, 6))
        plt.bar(self.genres, self.counts, color='blue')

        plt.title("Total Video Games by Genre", fontsize=16)
        plt.xlabel("Genre", fontsize=12)
        plt.ylabel("Count of Video Games", fontsize=12)

        plt.xticks(rotation=45)

        plt.grid(axis='y', linestyle='--', alpha=0.7)

        plt.tight_layout()

        plt.show()

genres = [
    "Action", "Adventure", "Fighting", "Misc", "Platform", 
    "Puzzle", "Racing", "Role-Playing", "Shooter", 
    "Simulation", "Sports", "Strategy"
]
counts = [3200, 1000, 700, 1700, 800, 500, 1100, 1500, 1400, 900, 1800, 600]

chart = VideoGameBarChart(genres, counts)
chart.plot_chart()
