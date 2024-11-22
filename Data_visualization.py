import matplotlib.pyplot as plt

class VideoGameBarChart:
    def __init__(self, genres, counts):
        # Khởi tạo các thuộc tính genres và counts
        self.genres = genres
        self.counts = counts

    def plot_bar_chart(self):
        """Vẽ biểu đồ cột."""
        plt.figure(figsize=(12, 6))
        plt.bar(self.genres, self.counts, color='blue')

        plt.title("Total Video Games by Genre", fontsize=16)
        plt.xlabel("Genre", fontsize=12)
        plt.ylabel("Count of Video Games", fontsize=12)
        plt.xticks(rotation=45)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.show()

    def plot_pie_chart(self):
        """Vẽ biểu đồ tròn."""
        plt.figure(figsize=(8, 8))
        plt.pie(
            self.counts,
            labels=self.genres,
            autopct='%1.1f%%',
            startangle=90,
            colors=plt.cm.Paired.colors
        )
        plt.title("Percentage of Video Games by Genre", fontsize=16)
        plt.axis('equal')  # Đảm bảo biểu đồ tròn không bị méo
        plt.show()

    def plot_line_chart(self):
        """Vẽ biểu đồ đường."""
        plt.figure(figsize=(12, 6))
        plt.plot(self.genres, self.counts, marker='o', linestyle='-', color='green')

        plt.title("Trend of Video Games by Genre", fontsize=16)
        plt.xlabel("Genre", fontsize=12)
        plt.ylabel("Count of Video Games", fontsize=12)
        plt.xticks(rotation=45)
        plt.grid(axis='both', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.show()


# Sử dụng class để vẽ biểu đồ
genres = [
    "Action", "Adventure", "Fighting", "Misc", "Platform", 
    "Puzzle", "Racing", "Role-Playing", "Shooter", 
    "Simulation", "Sports", "Strategy"
]
counts = [3200, 1000, 700, 1700, 800, 500, 1100, 1500, 1400, 900, 1800, 600]

# Tạo đối tượng và vẽ các biểu đồ
chart = VideoGameBarChart(genres, counts)
chart.plot_bar_chart()  # Vẽ biểu đồ cột
chart.plot_pie_chart()  # Vẽ biểu đồ tròn
chart.plot_line_chart()  # Vẽ biểu đồ đường
