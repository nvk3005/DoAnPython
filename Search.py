import pandas as pd

class Search_Class:
    '''Lớp thực hiện chức năng tìm kiếm trên cột'''
    def __init__(self, data_file):
        self.data_file = data_file
    
    def search_by_column(self, column_name: str, value_search):
        try:
            data = pd.read_csv(self.data_file)
        except Exception as e:
            return f"Lỗi đọc File: {e}"

        search_data = data[data[column_name] == value_search]
        if not search_data.empty:
            return search_data
        else:
            return "Không tìm thấy dữ liệu trong phù hợp."