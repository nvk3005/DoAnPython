import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class VideoGameSalesApp:
    """
    Ứng dụng quản lý dữ liệu Video Game Sales với các tính năng:
    - Hiển thị dữ liệu với phân trang, tìm kiếm, và sắp xếp.
    - Chức năng CRUD cơ bản (Thêm, Xóa, Cập nhật).
    - Lưu dữ liệu ra file CSV.
    """

    def __init__(self, root):
        """
        Khởi tạo ứng dụng và giao diện.

        Parameters:
            root (Tk): Cửa sổ Tkinter chính.
        """
        self.root = root
        self.root.title("Quản Lý Dữ Liệu Video Game Sales")
        self.root.geometry("1400x700")
        self.root.configure(bg="#f0f0f0")

        # Thiết lập giao diện người dùng
        self.create_main_frame()
        self.create_menu()
        
    def create_main_frame(self):
        """Tạo khung chính và Treeview để hiển thị dữ liệu."""
        self.main_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(self.main_frame, selectmode="browse")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Thêm thanh cuộn dọc và ngang cho Treeview
        tree_scroll_y = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.tree.yview)
        tree_scroll_y.pack(side="right", fill="y")
        tree_scroll_x = ttk.Scrollbar(self.main_frame, orient="horizontal", command=self.tree.xview)
        tree_scroll_x.pack(side="bottom", fill="x")
        self.tree.configure(yscrollcommand=tree_scroll_y.set, xscrollcommand=tree_scroll_x.set)

        # Thêm sự kiện chọn dòng
        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)

    def load_data_to_treeview(self, show_message=False):
        """Tải dữ liệu từ DataFrame lên Treeview."""
        pass

    def on_row_select(self, event):
        """Khi người dùng chọn một dòng trong Treeview, dữ liệu của dòng đó sẽ được điền vào các trường nhập liệu."""
        pass

    def open_file(self):
        """Mở file CSV và tải dữ liệu vào DataFrame. Hiển thị dữ liệu trên Treeview nếu thành công."""
        pass

    def create_entry_fields(self):
        """Tạo các trường nhập liệu và các nút chức năng CRUD."""
        if hasattr(self, 'entry_frame'):
            self.entry_frame.destroy()

        self.entry_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.entry_frame.pack(fill=tk.BOTH, padx=10, pady=10)
        
        # Thêm các nút chức năng mà không cần xử lý dữ liệu
        btn_add = tk.Button(self.entry_frame, text="Add", command=self.create_entry, bg="#4CAF50", fg="white")
        btn_add.grid(row=2, column=0, padx=5, pady=5)

        btn_update = tk.Button(self.entry_frame, text="Update", command=self.update_entry, bg="#FFA500", fg="white")
        btn_update.grid(row=2, column=1, padx=5, pady=5)

        btn_delete = tk.Button(self.entry_frame, text="Delete", command=self.delete_entry, bg="#f44336", fg="white")
        btn_delete.grid(row=2, column=2, padx=5, pady=5)

        btn_save = tk.Button(self.entry_frame, text="Save", command=self.save_to_csv, bg="#00796B", fg="white")
        btn_save.grid(row=2, column=3, padx=5, pady=5)

    def create_entry(self):
        """Thêm một dòng mới vào DataFrame dựa trên các trường nhập liệu."""
        pass

    def update_entry(self):
        """Cập nhật dòng dữ liệu đã chọn dựa trên giá trị trong các trường nhập liệu."""
        pass

    def delete_entry(self):
        """Xóa dòng dữ liệu đã chọn trong DataFrame và cập nhật lại Treeview."""
        pass

    def save_to_csv(self):
        """Lưu DataFrame hiện tại ra tệp CSV theo đường dẫn người dùng chọn."""
        pass

    def sort_data(self, column_name):
        """Sắp xếp dữ liệu theo cột được chọn và hiển thị lại trên Treeview."""
        pass

    def create_menu(self):
        """Tạo menu với các tùy chọn File (Mở, Lưu, Thoát)."""
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        file_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_to_csv)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoGameSalesApp(root)
    root.mainloop()

# import tkinter as tk
# from tkinter import ttk, filedialog, messagebox
# import pandas as pd
# import matplotlib.pyplot as plt

# class VideoGameSalesApp:
#     """
#     Ứng dụng quản lý dữ liệu Video Game Sales với các tính năng:
#     - Hiển thị dữ liệu với phân trang, tìm kiếm, và sắp xếp.
#     - Chức năng CRUD cơ bản (Thêm, Xóa, Cập nhật).
#     - Vẽ biểu đồ cho các trường doanh số.
#     - Lưu dữ liệu ra file CSV.
#     """

#     def __init__(self, root):
#         """
#         Khởi tạo ứng dụng và giao diện.

#         Parameters:
#             root (Tk): Cửa sổ Tkinter chính.
#         """
#         self.root = root
#         self.root.title("Quản Lý Dữ Liệu Video Game Sales")
#         self.root.geometry("1400x700")
#         self.root.configure(bg="#f0f0f0")

#         self.df = pd.DataFrame()  # Khởi tạo DataFrame rỗng
#         self.sort_ascending = True  # Đặt thứ tự sắp xếp ban đầu

#         # Thiết lập giao diện người dùng
#         self.create_main_frame()
#         self.create_menu()
        
#     def create_main_frame(self):
#         """Tạo khung chính và Treeview để hiển thị dữ liệu."""
#         self.main_frame = tk.Frame(self.root, bg="#f0f0f0")
#         self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

#         self.tree = ttk.Treeview(self.main_frame, selectmode="browse")
#         self.tree.pack(fill=tk.BOTH, expand=True)

#         # Thêm thanh cuộn dọc và ngang cho Treeview
#         tree_scroll_y = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.tree.yview)
#         tree_scroll_y.pack(side="right", fill="y")
#         tree_scroll_x = ttk.Scrollbar(self.main_frame, orient="horizontal", command=self.tree.xview)
#         tree_scroll_x.pack(side="bottom", fill="x")
#         self.tree.configure(yscrollcommand=tree_scroll_y.set, xscrollcommand=tree_scroll_x.set)

#         # Thêm sự kiện chọn dòng
#         self.tree.bind("<<TreeviewSelect>>", self.on_row_select)

#     def load_data_to_treeview(self, show_message=False):
#         """
#         Tải dữ liệu từ DataFrame lên Treeview.

#         Parameters:
#             show_message (bool): Hiển thị thông báo thành công nếu có. Mặc định là False.
#         """
#         try:
#             # Xóa dữ liệu cũ trong Treeview
#             self.tree.delete(*self.tree.get_children())

#             # Đặt tên cột và hiển thị dữ liệu
#             self.tree["column"] = list(self.df.columns)
#             self.tree["show"] = "headings"

#             for col in self.tree["column"]:
#                 self.tree.heading(col, text=col, command=lambda _col=col: self.sort_data(_col))
#                 if col == "Name":
#                     self.tree.column(col, width=200, anchor="w")  # Đặt độ rộng cố định cho cột Name
#                 else:
#                     max_width = min(max(self.df[col].astype(str).map(len).max() * 8, 80), 120)  # Điều chỉnh độ rộng tối đa cho các cột khác
#                     self.tree.column(col, width=max_width, anchor="center")

#             # Chèn dữ liệu từ DataFrame vào Treeview
#             for index, row in self.df.iterrows():
#                 self.tree.insert("", "end", iid=index, values=list(row))

#             # Cập nhật các trường nhập liệu
#             self.create_entry_fields()

#             if show_message:
#                 messagebox.showinfo("Thành công", "Dữ liệu đã được tải lên thành công!")

#         except Exception as e:
#             messagebox.showerror("Lỗi", f"Không thể tải dữ liệu: {e}")

#     def on_row_select(self, event):
#         """
#         Khi người dùng chọn một dòng trong Treeview, dữ liệu của dòng đó
#         sẽ được điền vào các trường nhập liệu để người dùng chỉnh sửa.
#         """
#         selected_item = self.tree.selection()
#         if selected_item:
#             item = self.tree.item(selected_item)
#             row_values = item['values']
#             for i, col in enumerate(self.df.columns):
#                 if col in self.entries:
#                     self.entries[col].delete(0, tk.END)
#                     self.entries[col].insert(0, row_values[i])

#     def open_file(self):
#         """
#         Mở file CSV và tải dữ liệu vào DataFrame. 
#         Hiển thị dữ liệu trên Treeview nếu thành công.
#         """
#         file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
#         if file_path:
#             try:
#                 self.df = pd.read_csv(file_path)
#                 if self.df.empty:
#                     messagebox.showwarning("Cảnh báo", "File CSV không có dữ liệu.")
#                     return
#                 self.load_data_to_treeview(show_message=True)
#             except Exception as e:
#                 messagebox.showerror("Lỗi", f"Không thể mở file CSV: {e}")
#         else:
#             messagebox.showinfo("Thông báo", "Chưa chọn file CSV nào.")

#     def create_entry_fields(self):
#         """Tạo các trường nhập liệu và các nút chức năng CRUD."""
#         if hasattr(self, 'entry_frame'):
#             self.entry_frame.destroy()

#         self.entry_frame = tk.Frame(self.root, bg="#f0f0f0")
#         self.entry_frame.pack(fill=tk.BOTH, padx=10, pady=10)
        
#         # Lưu tất cả các trường nhập liệu trong từ điển
#         self.entries = {}
        
#         # Tạo nhãn và trường nhập liệu cho từng cột
#         for i, col in enumerate(self.df.columns):
#             label = tk.Label(self.entry_frame, text=col, bg="#f0f0f0", font=("Arial", 10, "bold"))
#             label.grid(row=0, column=i, padx=5, pady=5)
#             entry = tk.Entry(self.entry_frame)
#             entry.grid(row=1, column=i, padx=5, pady=5)
#             self.entries[col] = entry
        
#         # Tạo các nút chức năng
#         btn_add = tk.Button(self.entry_frame, text="Add", command=self.create_entry, bg="#4CAF50", fg="white")
#         btn_add.grid(row=2, column=0, padx=5, pady=5)

#         btn_update = tk.Button(self.entry_frame, text="Update", command=self.update_entry, bg="#FFA500", fg="white")
#         btn_update.grid(row=2, column=1, padx=5, pady=5)

#         btn_delete = tk.Button(self.entry_frame, text="Delete", command=self.delete_entry, bg="#f44336", fg="white")
#         btn_delete.grid(row=2, column=2, padx=5, pady=5)

#         btn_save = tk.Button(self.entry_frame, text="Save", command=self.save_to_csv, bg="#00796B", fg="white")
#         btn_save.grid(row=2, column=3, padx=5, pady=5)

#     def create_entry(self):
#         """Thêm một dòng mới vào DataFrame dựa trên các trường nhập liệu."""
#         new_data = [entry.get() for entry in self.entries.values()]
#         if len(new_data) == len(self.df.columns):
#             new_row = pd.Series(new_data, index=self.df.columns)
#             self.df = pd.concat([self.df, pd.DataFrame([new_row])], ignore_index=True)
#             self.load_data_to_treeview()

#     def update_entry(self):
#         """Cập nhật dòng dữ liệu đã chọn dựa trên giá trị trong các trường nhập liệu."""
#         selected_item = self.tree.selection()
#         if not selected_item:
#             messagebox.showwarning("Cảnh báo", "Chưa chọn dòng để cập nhật.")
#             return

#         item_id = selected_item[0]
#         values = [entry.get() for entry in self.entries.values()]
#         for i, col in enumerate(self.df.columns):
#             # Lấy kiểu dữ liệu của cột hiện tại
#             col_dtype = self.df[col].dtype
#             # Chuyển đổi giá trị đầu vào thành kiểu dữ liệu tương ứng
#             if col_dtype == 'int64':
#                 self.df.at[int(item_id), col] = int(values[i]) if values[i] else None
#             elif col_dtype == 'float64':
#                 self.df.at[int(item_id), col] = float(values[i]) if values[i] else None
#             else:
#                 self.df.at[int(item_id), col] = values[i]
        
#         self.load_data_to_treeview()

#     def delete_entry(self):
#         """Xóa dòng dữ liệu đã chọn trong DataFrame và cập nhật lại Treeview."""
#         try:
#             selected_item = self.tree.selection()[0]
#             self.df.drop(int(selected_item), inplace=True)
#             self.df.reset_index(drop=True, inplace=True)
#             self.load_data_to_treeview()
#         except IndexError:
#             messagebox.showwarning("Cảnh báo", "Chưa chọn dòng để xóa.")
#         except Exception as e:
#             messagebox.showerror("Lỗi", f"Không thể xóa dữ liệu: {e}")

#     def save_to_csv(self):
#         """Lưu DataFrame hiện tại ra tệp CSV theo đường dẫn người dùng chọn."""
#         file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
#         if file_path:
#             self.df.to_csv(file_path, index=False)
#             messagebox.showinfo("Thành công", "Dữ liệu đã được lưu thành công!")

#     def sort_data(self, column_name):
#         """Sắp xếp dữ liệu theo cột được chọn và hiển thị lại trên Treeview."""
#         try:
#             self.df.sort_values(by=column_name, inplace=True, ascending=self.sort_ascending)
#             self.df.reset_index(drop=True, inplace=True)
#             self.sort_ascending = not self.sort_ascending  # Đảo thứ tự sắp xếp cho lần sau
#             self.load_data_to_treeview()
#         except Exception as e:
#             messagebox.showerror("Lỗi", f"Không thể sắp xếp dữ liệu: {e}")

#     def create_menu(self):
#         """Tạo menu với các tùy chọn File (Mở, Lưu, Thoát)."""
#         menu = tk.Menu(self.root)
#         self.root.config(menu=menu)

#         file_menu = tk.Menu(menu, tearoff=0)
#         menu.add_cascade(label="File", menu=file_menu)
#         file_menu.add_command(label="Open", command=self.open_file)
#         file_menu.add_command(label="Save", command=self.save_to_csv)
#         file_menu.add_separator()
#         file_menu.add_command(label="Exit", command=self.root.quit)

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = VideoGameSalesApp(root)
#     root.mainloop()
