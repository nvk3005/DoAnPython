import csv


class CSVManager:
    def __init__(self, file_path):
        self.file_path = file_path

    def create(self):
        """Thêm dữ liệu vào file CSV."""
        rank = input()
        name = input()
        platform = input()
        year = input()
        genre = input()
        publisher = input()

        na_sales = float(input())
        pal_sales = float(input())
        jp_sales = float(input())
        other_sales = float(input())

        global_sales = na_sales + pal_sales + jp_sales + other_sales

        data = [rank, name, platform, year, genre, publisher, na_sales, pal_sales, jp_sales, other_sales, global_sales]

        with open(self.file_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(data)

    def update(self):
        """Cập nhật một hoặc nhiều giá trị trong file CSV dựa trên một điều kiện."""
        identifier = input()
        rows = []
        with open(self.file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader)
            for row in reader:
                if row[0] == identifier:
                    for index in range(1, len(row) - 1):
                        new_value = input()
                        if index >= 6 and index < 10:
                            new_value = float(new_value)
                        row[index] = new_value

                    row[10] = sum(row[6:10])

                rows.append(row)

        with open(self.file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(rows)

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


if __name__ == "__main__":
    csv_file = 'cleanData.csv'
    manager = CSVManager(csv_file)

    # manager.create()
    # manager.update()
    # manager.delete()
