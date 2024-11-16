import matplotlib.pyplot as plt

class VideoGameBarChart:
    def __init__(self, genres, counts):
        # Khởi tạo các thuộc tính genres và counts
        self.genres = genres
        self.counts = counts

    def plot_chart(self):
        # Tạo figure và vẽ biểu đồ
        plt.figure(figsize=(12, 6))
        plt.bar(self.genres, self.counts, color='blue')

        # Thêm tiêu đề và nhãn cho trục
        plt.title("Total Video Games by Genre", fontsize=16)
        plt.xlabel("Genre", fontsize=12)
        plt.ylabel("Count of Video Games", fontsize=12)

        # Đặt xoay cho các nhãn trục x
        plt.xticks(rotation=45)

        # Thêm lưới cho trục y
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        # Sử dụng tight_layout để tránh việc nhãn bị cắt
        plt.tight_layout()

        # Hiển thị biểu đồ
        plt.show()

# Sử dụng class để vẽ biểu đồ
genres = [
    "Action", "Adventure", "Fighting", "Misc", "Platform", 
    "Puzzle", "Racing", "Role-Playing", "Shooter", 
    "Simulation", "Sports", "Strategy"
]
counts = [3200, 1000, 700, 1700, 800, 500, 1100, 1500, 1400, 900, 1800, 600]

# Tạo đối tượng và vẽ biểu đồ
chart = VideoGameBarChart(genres, counts)
chart.plot_chart()
