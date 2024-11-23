import csv

class CSVManager:
    def __init__(self, file_path):
        self.file_path = file_path

    def create(self, data):
        """Thêm dữ liệu vào file CSV."""
        print(data)
        with open(self.file_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(data)
        print("Dữ liệu đã được thêm thành công!")

    def update(self, identifier, data):
        """Cập nhật một hoặc nhiều giá trị trong file CSV dựa trên một điều kiện."""
        rows = []
        print(data)
        with open(self.file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader)
            for row in reader:
                if row[0] == identifier:
                    print("Cập nhật thông tin cho:", row)
                    # Cập nhật hàng với dữ liệu mới từ danh sách data
                    for index in range(len(data)):  # Bắt đầu từ cột thứ 1
                        if index + 1 < len(row):  # Kiểm tra xem chỉ số có hợp lệ không
                            row[index + 1] = data[index]  # Cập nhật giá trị từ data
                rows.append(row)

        with open(self.file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(rows)

        print(f"Dữ liệu của {identifier} đã được cập nhật thành công!")

    def delete(self, rank_id):
        """Xóa một hàng trong file CSV dựa trên Rank ID."""
        rows = []
        with open(self.file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader)
            for row in reader:
                if row[0] != rank_id:
                    rows.append(row)


        with open(self.file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(rows)

        print(f"Hàng có Rank ID {rank_id} đã được xóa thành công!")


