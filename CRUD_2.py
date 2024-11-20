import csv


class CSVManager:
    def __init__(self, file_path):
        self.file_path = file_path

    def create(self):
        """Thêm dữ liệu vào file CSV."""
        # Nhập thông tin cho các cột
        rank = input("Rank ID: ")
        name = input("Name: ")
        platform = input("Platform: ")
        year = input("Year: ")
        genre = input("Genre: ")
        publisher = input("Publisher: ")

        # Nhập các giá trị doanh thu
        na_sales = float(input("NA_Sales: "))
        pal_sales = float(input("PAL_Sales: "))
        jp_sales = float(input("JP_Sales: "))
        other_sales = float(input("Other_Sales: "))

        # Tính toán Global_Sales
        global_sales = na_sales + pal_sales + jp_sales + other_sales

        data = [rank, name, platform, year, genre, publisher, na_sales, pal_sales, jp_sales, other_sales, global_sales]

        # Ghi dữ liệu vào file CSV
        with open(self.file_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(data)
        print("Dữ liệu đã được thêm thành công!")

    def update(self):
        """Cập nhật một hoặc nhiều giá trị trong file CSV dựa trên một điều kiện."""
        identifier = input("Nhập Rank ID của trò chơi bạn muốn cập nhật: ")
        rows = []
        with open(self.file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader)
            for row in reader:
                if row[0] == identifier:
                    print("Cập nhật thông tin cho:", row)
                    for index in range(1, len(row) - 1):
                        col_name = header[index]
                        new_value = input(f"Nhập dữ liệu cần thay đổi cho '{col_name}' (hiện tại: '{row[index]}'): ")
                        if index >= 6 and index < 10:
                            new_value = float(new_value)
                        row[index] = new_value

                    # Tính toán Global_Sales
                    row[10] = sum(row[6:10])

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


if __name__ == "__main__":
    csv_file = 'cleanData.csv'
    manager = CSVManager(csv_file)

    # manager.create()
    # manager.update()
    # manager.delete()
