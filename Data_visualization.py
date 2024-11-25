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


def plot_data(data, group_by, y_col, kind, title, xlabel, ylabel, is_horizontal=False, colors=None, autopct=None):
    """
    Hàm vẽ biểu đồ linh hoạt cho các phân tích dữ liệu.
    Args:
        data (pd.DataFrame): DataFrame chứa dữ liệu.
        group_by (str): Cột cần nhóm.
        y_col (str): Cột giá trị.
        kind (str): Loại biểu đồ ('bar', 'pie', 'barh', 'line').
        title (str): Tiêu đề biểu đồ.
        xlabel (str): Nhãn trục X.
        ylabel (str): Nhãn trục Y.
        is_horizontal (bool): Nếu True, vẽ biểu đồ ngang.
        colors (list): Danh sách màu sắc cho biểu đồ.
        autopct (str): Định dạng phần trăm (áp dụng cho biểu đồ tròn).
    """
    try:
        plt.figure(figsize=(10, 6))
        if kind == 'pie':
            values = data[y_col].sum()
            data.plot(kind=kind, y=y_col, autopct=autopct, startangle=140, colors=colors)
        else:
            group_data = data.groupby(group_by)[y_col].sum().sort_values()
            if is_horizontal:
                group_data.plot(kind=kind, color=colors, edgecolor='black')
            else:
                group_data.plot(kind=kind, color='skyblue', edgecolor='black')

        plt.title(title, fontsize=14)
        plt.xlabel(xlabel, fontsize=12)
        plt.ylabel(ylabel, fontsize=12)
        plt.tight_layout()
        plt.show()
    except Exception as e:
        raise ValueError(f"Lỗi khi vẽ biểu đồ: {e}")


def plot_sales_by_year(data):
    """Vẽ biểu đồ doanh số theo năm."""
    plot_data(data, group_by='Year', y_col='Global_Sales', kind='bar',
              title='Doanh số toàn cầu theo năm', xlabel='Năm', ylabel='Doanh số (triệu bản)')


def plot_sales_by_genre(data):
    """Vẽ biểu đồ doanh số theo thể loại."""
    plot_data(data, group_by='Genre', y_col='Global_Sales', kind='barh',
              title='Doanh số toàn cầu theo thể loại', xlabel='Doanh số (triệu bản)', ylabel='Thể loại', is_horizontal=True)


def plot_region_sales(data):
    """Vẽ biểu đồ tỷ lệ doanh số theo khu vực."""
    required_columns = ['NA_Sales', 'PAL_Sales', 'JP_Sales', 'Other_Sales']
    missing_columns = [col for col in required_columns if col not in data.columns]
    if missing_columns:
        raise KeyError(f"Các cột sau không tồn tại trong dữ liệu: {missing_columns}")

    region_sales = data[required_columns].sum()
    region_sales.plot(kind='pie', autopct='%1.1f%%', startangle=140,
                      colors=['gold', 'skyblue', 'lightcoral', 'green'])
    plt.title('Tỷ lệ doanh số theo khu vực', fontsize=14)
    plt.ylabel('')
    plt.tight_layout()
    plt.show()


def plot_top_10_games(data):
    """Vẽ biểu đồ top 10 trò chơi bán chạy nhất."""
    top_10_games = data.nlargest(10, 'Global_Sales')
    plot_data(top_10_games, group_by='Name', y_col='Global_Sales', kind='barh',
              title='Top 10 trò chơi bán chạy nhất toàn cầu', xlabel='Doanh số (triệu bản)', ylabel='Tên trò chơi', is_horizontal=True)
