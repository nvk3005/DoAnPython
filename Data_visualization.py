import pandas as pd
import matplotlib.pyplot as plt

# Đọc dữ liệu từ tệp CSV
file_path = "/Users/thanhhoa240905icloud.com/vgsales.csv"
data = pd.read_csv(file_path, sep=';')  
# Xử lý dữ liệu
data['Year'] = data['Year'].fillna(0).astype(int)  

# 1. Phân bố doanh số toàn cầu theo năm
sales_by_year = data.groupby('Year')['Global_Sales'].sum()
plt.figure(figsize=(10, 6))
sales_by_year.plot(kind='bar', color='skyblue', edgecolor='black')
plt.title('Doanh số toàn cầu theo năm', fontsize=14)
plt.xlabel('Năm', fontsize=12)
plt.ylabel('Doanh số (triệu bản)', fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 2. Phân bố doanh số theo thể loại
sales_by_genre = data.groupby('Genre')['Global_Sales'].sum()
plt.figure(figsize=(10, 6))
sales_by_genre.sort_values().plot(kind='barh', color='lightgreen', edgecolor='black')
plt.title('Doanh số toàn cầu theo thể loại', fontsize=14)
plt.xlabel('Doanh số (triệu bản)', fontsize=12)
plt.ylabel('Thể loại', fontsize=12)
plt.tight_layout()
plt.show()

# 3. So sánh doanh số giữa các khu vực
region_sales = data[['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales']].sum()
plt.figure(figsize=(10, 6))
region_sales.plot(kind='pie', autopct='%1.1f%%', startangle=140, colors=['gold', 'skyblue', 'lightcoral', 'green'])
plt.title('Tỷ lệ doanh số theo khu vực', fontsize=14)
plt.ylabel('')  # Ẩn nhãn trục Y
plt.tight_layout()
plt.show()

# 4. Doanh số theo nền tảng
sales_by_platform = data.groupby('Platform')['Global_Sales'].sum()
plt.figure(figsize=(10, 6))
sales_by_platform.sort_values(ascending=False).head(10).plot(
    kind='bar', color='orange', edgecolor='black'
)
plt.title('Top 10 nền tảng có doanh số cao nhất', fontsize=14)
plt.xlabel('Nền tảng', fontsize=12)
plt.ylabel('Doanh số (triệu bản)', fontsize=12)
plt.tight_layout()
plt.show()

# 5. Top 10 trò chơi bán chạy nhất
top_10_games = data.nlargest(10, 'Global_Sales')
plt.figure(figsize=(10, 6))
plt.barh(top_10_games['Name'], top_10_games['Global_Sales'], color='purple', edgecolor='black')
plt.title('Top 10 trò chơi bán chạy nhất toàn cầu', fontsize=14)
plt.xlabel('Doanh số (triệu bản)', fontsize=12)
plt.ylabel('Tên trò chơi', fontsize=12)
plt.gca().invert_yaxis()  # Đảo ngược trục Y để hiển thị từ trên xuống
plt.tight_layout()
plt.show()
