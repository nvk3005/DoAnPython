import pandas as pd


class CSVManager:
    def __init__(self, file_path):
        self.file_path = file_path

    def create(self, name, platform, year, genre, publisher, na_sales, pal_sales, jp_sales, other_sales):
        try:
            na_sales, pal_sales, jp_sales, other_sales = map(float, [na_sales, pal_sales, jp_sales, other_sales])
        except ValueError:
            print("Error: Sales data must be numeric.")
            return

        global_sales = na_sales + pal_sales + jp_sales + other_sales

        try:
            df = pd.read_csv(self.file_path)
        except FileNotFoundError:
            print(f"Error: File '{self.file_path}' not found.")
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
        print(f"Game '{name}' was added with Rank ID {assigned_rank}.")

    def update(self, rank_id, name=None, platform=None, year=None, genre=None, publisher=None, na_sales=None, pal_sales=None, jp_sales=None, other_sales=None):
        try:
            df = pd.read_csv(self.file_path)
        except FileNotFoundError:
            print(f"Error: File '{self.file_path}' not found.")
            return

        if "Rank" not in df.columns:
            print("Error: The dataset does not have a 'Rank' column.")
            return

        # Ensure rank_id is an integer
        try:
            rank_id = int(rank_id)
        except ValueError:
            print("Error: Rank ID must be an integer.")
            return

        if rank_id not in df["Rank"].values:
            print(f"Error: Rank ID {rank_id} not found.")
            return

        row_index = df[df["Rank"] == rank_id].index[0]

        # Update the row with new values if provided
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

        # Recalculate Global Sales for the updated row
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
        print(f"Game with previous Rank ID {rank_id} has been updated.")
        print(f"The new Rank ID for '{name}' is {new_rank_id}.")

    def delete(self, rank_id):
        try:
            df = pd.read_csv(self.file_path)
        except FileNotFoundError:
            print(f"Error: File '{self.file_path}' not found.")
            return

        try:
            rank_id = int(rank_id)
        except ValueError:
            print("Error: Rank ID must be an integer.")
            return

        if rank_id not in df["Rank"].values:
            print(f"Error: Rank ID {rank_id} not found.")
            return

        df = df[df["Rank"] != rank_id]
        df = df.sort_values(by="Global_Sales", ascending=False).reset_index(drop=True)
        df["Rank"] = df.index + 1

        df.to_csv(self.file_path, index=False)
        print(f"Game with Rank ID {rank_id} has been successfully deleted.")
