import csv


class CSVManager:
    def __init__(self, file_path):
        self.file_path = file_path

    def create(self, data):
        """Thêm dữ liệu vào file CSV."""
        with open(self.file_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(data)
        print("Dữ liệu đã được thêm thành công!")

    def update(self, identifier, column_index, new_value):
        """Cập nhật một giá trị trong file CSV dựa trên một điều kiện."""
        rows = []
        with open(self.file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader)  # Lưu tiêu đề
            for row in reader:
                if row[0] == identifier:  # Kiểm tra điều kiện
                    row[column_index] = new_value  # Cập nhật giá trị
                rows.append(row)

        with open(self.file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(header)  # Ghi tiêu đề
            writer.writerows(rows)  # Ghi các hàng đã cập nhật

        print(f"Dữ liệu của {identifier} đã được cập nhật thành công!")

    def delete(self, identifier):
        """Xóa một hàng trong file CSV dựa trên một điều kiện."""
        rows = []
        with open(self.file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader)  # Lưu tiêu đề
            for row in reader:
                if row[0] != identifier:  # Kiểm tra điều kiện
                    rows.append(row)  # Chỉ thêm hàng không phải của identifier

        with open(self.file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(header)  # Ghi tiêu đề
            writer.writerows(rows)  # Ghi các hàng đã cập nhật

        print(f"Hàng của {identifier} đã được xóa thành công!")

# if __name__ == "__main__":
#     csv_file = 'testData.csv'
#     manager = CSVManager(csv_file)

# Thêm dữ liệu
# manager.create([10, 'PUBG', 'PC', '15.55', 'Test'])

# Cập nhật dữ liệu
# manager.update('10', 1, 'BOOM!')
# manager.update('10', 2, 'mobile')

# # Xóa dữ liệu
# manager.delete('10')
