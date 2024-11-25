import pandas as pd

class Search:
    def __init__(self, data_file):
        self.data_file = data_file
    
    def search_by_column(self, column_name, value_search):
        try:
            data = pd.read_csv(self.data_file)
        except Exception as e:
            return f"Lỗi đọc File: {e}"
        
        if column_name not in data.columns:
            return f"Tên cột '{column_name}' không có trong dataset."
        
        filtered_data = data[data[column_name] == value_search]
        return filtered_data