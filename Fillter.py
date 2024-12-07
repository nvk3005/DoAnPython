import pandas as pd

class Fillter_Class:
    '''Lớp thực hiện lọc dữ liệu trên cột'''
    def __init__(self, file_path):
        self.data_file = file_path

    def fillter_by_column(self, column_name: str, min_value: float, max_value: float):
        try:
            data = pd.read_csv(self.data_file)
        except Exception as e:
            return f"Lỗi đọc File: {e}"
        

        filtered_data = data[(data[column_name] >= min_value) & (data[column_name] <= max_value)]
        if not filtered_data.empty:
            return filtered_data
        else:
            return "Không tìm thấy dữ liệu trong phù hợp."

