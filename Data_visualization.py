import pandas as pd
import matplotlib.pyplot as plt


def read_data(file_path, sep=';'):
    """
    Đọc dữ liệu từ tệp CSV và chuẩn hóa cột "Year".
    Args:
        file_path (str): Đường dẫn đến file CSV.
        sep (str): Ký tự phân cách trong file CSV. Mặc định là ';'.
    Returns:
        pd.DataFrame: DataFrame chứa dữ liệu đã đọc.
    """
    try:
        data = pd.read_csv(file_path, sep=sep)
        if 'Year' in data.columns:
            data['Year'] = data['Year'].fillna(0).astype(int)
        return data
    except Exception as e:
        raise ValueError(f"Lỗi khi đọc dữ liệu: {e}")


def plot_sales_by_year(data):
    """
    Vẽ biểu đồ doanh số toàn cầu theo năm.
    """
    sales_by_year = data.groupby('Year')['Global_Sales'].sum()
    plt.figure(figsize=(10, 6))
    sales_by_year.plot(kind='bar', color='skyblue', edgecolor='black')
    plt.title('Doanh số toàn cầu theo năm', fontsize=14)
    plt.xlabel('Năm', fontsize=12)
    plt.ylabel('Doanh số (triệu bản)', fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def plot_sales_by_genre(data):
    """
    Vẽ biểu đồ doanh số toàn cầu theo thể loại.
    """
    sales_by_genre = data.groupby('Genre')['Global_Sales'].sum()
    plt.figure(figsize=(10, 6))
    sales_by_genre.sort_values().plot(kind='barh', color='lightgreen', edgecolor='black')
    plt.title('Doanh số toàn cầu theo thể loại', fontsize=14)
    plt.xlabel('Doanh số (triệu bản)', fontsize=12)
    plt.ylabel('Thể loại', fontsize=12)
    plt.tight_layout()
    plt.show()


def plot_region_sales(data):
    """
    Vẽ biểu đồ tỷ lệ doanh số theo khu vực.
    """
    required_columns = ['NA_Sales', 'PAL_Sales', 'JP_Sales', 'Other_Sales']
    missing_columns = [col for col in required_columns if col not in data.columns]
    if missing_columns:
        raise KeyError(f"Các cột sau không tồn tại trong dữ liệu: {missing_columns}")

    region_sales = data[required_columns].sum()
    plt.figure(figsize=(8, 8))
    region_sales.plot(kind='pie', autopct='%1.1f%%', startangle=140,
                      colors=['gold', 'skyblue', 'lightcoral', 'green'])
    plt.title('Tỷ lệ doanh số theo khu vực', fontsize=14)
    plt.ylabel('')
    plt.tight_layout()
    plt.show()


def plot_top_10_games(data):
    """
    Vẽ biểu đồ top 10 trò chơi bán chạy nhất toàn cầu.
    """
    top_10_games = data.nlargest(10, 'Global_Sales')
    plt.figure(figsize=(10, 6))
    plt.barh(top_10_games['Name'], top_10_games['Global_Sales'], color='purple', edgecolor='black')
    plt.title('Top 10 trò chơi bán chạy nhất toàn cầu', fontsize=14)
    plt.xlabel('Doanh số (triệu bản)', fontsize=12)
    plt.ylabel('Tên trò chơi', fontsize=12)
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()


def plot_top_10_platform(data):
    """
    Vẽ biểu đồ top 10 nền tảng có doanh số cao nhất.
    """
    sales_by_platform = data.groupby('Platform')['Global_Sales'].sum()
    plt.figure(figsize=(10, 6))
    sales_by_platform.sort_values(ascending=False).head(10).plot(kind='bar', color='orange', edgecolor='black')
    plt.title('Top 10 nền tảng có doanh số cao nhất', fontsize=14)
    plt.xlabel('Nền tảng', fontsize=12)
    plt.ylabel('Doanh số (triệu bản)', fontsize=12)
    plt.tight_layout()
    plt.show()
