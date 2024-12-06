import pandas as pd


class CSVManager:
    def __init__(self, file_path):
        self.file_path = file_path

    def create(self, name, platform, year, genre, publisher, na_sales, pal_sales, jp_sales, other_sales):
        try:
            na_sales, pal_sales, jp_sales, other_sales = map(float, [na_sales, pal_sales, jp_sales, other_sales])
        except ValueError:
            print("Thông số bán hàng không phải dạng số")
            return

        global_sales = na_sales + pal_sales + jp_sales + other_sales

        try:
            df = pd.read_csv(self.file_path)
        except FileNotFoundError:
            print(f"Không mở được file '{self.file_path}'")
            return

        new_row = pd.DataFrame([{
            "Name": name,
            "Platform": platform,
            "Year": year,
            "Genre": genre,
            "Publisher": publisher,
            "NA_Sales": na_sales,
            "PAL_Sales": pal_sales,
            "JP_Sales": jp_sales,
            "Other_Sales": other_sales,
            "Global_Sales": global_sales
        }])
        df = pd.concat([df, new_row], ignore_index=True)

        df = df.sort_values(by="Global_Sales", ascending=False).reset_index(drop=True)
        df["Rank"] = df.index + 1

        df.to_csv(self.file_path, index=False)
        assigned_rank = df[df["Name"] == name]["Rank"].values[0]
        print(f"Tạo thành công ID  {assigned_rank}")

    def update(self, rank_id, name=None, platform=None, year=None, genre=None, publisher=None, na_sales=None,
               pal_sales=None, jp_sales=None, other_sales=None):
        try:
            df = pd.read_csv(self.file_path)
        except FileNotFoundError:
            print(f"Không mở được file '{self.file_path}' ")
            return

        if "Rank" not in df.columns:
            print("Không có hàng cần thay thế")
            return

        try:
            rank_id = int(rank_id)
        except ValueError:
            print("Rank ID đã nhập không phải là số")
            return

        if rank_id not in df["Rank"].values:
            print(f"Không tìm thấy rank ID {rank_id}")
            return

        row_index = df[df["Rank"] == rank_id].index[0]

        # Cập nhật hàng với các giá trị đã đưa vào
        if name:
            df.at[row_index, "Name"] = name
        if platform:
            df.at[row_index, "Platform"] = platform
        if year:
            df.at[row_index, "Year"] = year
        if genre:
            df.at[row_index, "Genre"] = genre
        if publisher:
            df.at[row_index, "Publisher"] = publisher
        if na_sales is not None:
            df.at[row_index, "NA_Sales"] = float(na_sales)
        if pal_sales is not None:
            df.at[row_index, "PAL_Sales"] = float(pal_sales)
        if jp_sales is not None:
            df.at[row_index, "JP_Sales"] = float(jp_sales)
        if other_sales is not None:
            df.at[row_index, "Other_Sales"] = float(other_sales)

        # Tính global sales bằng tổng các giá trị sale còn lại
        df.at[row_index, "Global_Sales"] = (
                df.at[row_index, "NA_Sales"]
                + df.at[row_index, "PAL_Sales"]
                + df.at[row_index, "JP_Sales"]
                + df.at[row_index, "Other_Sales"]
        )

        df = df.sort_values(by="Global_Sales", ascending=False).reset_index(drop=True)
        df["Rank"] = df.index + 1

        df.to_csv(self.file_path, index=False)
        new_rank_id = df[df["Name"] == name]["Rank"].values[0]
        print(f"Cập nhật ID {rank_id} thành công")
        print(f"Hàng vừa cập nhật ở rank ID {new_rank_id}")

    def delete(self, listRankID):
        try:
            df = pd.read_csv(self.file_path)
        except FileNotFoundError:
            print(f"Không tìm thấy file '{self.file_path}' ")
            return

        try:
            listRankID = [int(rank_id) for rank_id in listRankID]
        except ValueError:
            print("Rank ID nhập vào không phải dạng số")
            return

        notFoundID = []
        for rank_id in listRankID:
            if rank_id not in df["Rank"].values:
                notFoundID.append(rank_id)
        if notFoundID:
            print(f"Không tìm thấy các rank ID sau: {notFoundID}")
            return

        for rank_id in listRankID:
            df = df[df["Rank"] != rank_id]

        df = df.sort_values(by="Global_Sales", ascending=False).reset_index(drop=True)
        df["Rank"] = df.index + 1

        df.to_csv(self.file_path, index=False)
        print(f"Xóa thành công các ID {listRankID}")
