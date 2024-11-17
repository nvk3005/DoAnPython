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

    def update(self, identifier):
        """Cập nhật một hoặc nhiều giá trị trong file CSV dựa trên một điều kiện."""
        rows = []
        with open(self.file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader)
            for row in reader:
                if row[0] == identifier:
                    print("Cập nhật thông tin cho:", row)
                    updates = {}
                    for index in range(1, len(header)):
                        col_name = header[index]
                        new_value = input(f"Nhập dữ liệu cần thay đổi cho '{col_name}' (hiện tại: '{row[index]}'): ")
                        updates[index] = new_value
                    # cập nhật hàng với dữ liệu mới
                    for column_index, new_value in updates.items():
                        if column_index < len(row):
                            row[column_index] = new_value
                rows.append(row)

        with open(self.file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(rows)

        print(f"Dữ liệu của {identifier} đã được cập nhật thành công!")

    def delete(self, identifier):
        """Xóa một hàng trong file CSV dựa trên một điều kiện."""
        rows = []
        with open(self.file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader)
            for row in reader:
                if row[0] != identifier:
                    rows.append(row)

        with open(self.file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(rows)

        print(f"Hàng của {identifier} đã được xóa thành công!")


# if __name__ == "__main__":
#     csv_file = 'testData.csv'
#     manager = CSVManager(csv_file)

# Thêm dữ liệu
# manager.create([10, 'PUBG', 'PC', '15.55', 'Test'])

# Cập nhật dữ liệu
# manager.update('9') 9 là thứ tự hàng cần thay đổi


# # Xóa dữ liệu
# manager.delete('10')
