import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from tkinter.filedialog import askopenfilename
import Standardization

# Khởi tạo cửa sổ chính
root = tk.Tk()
root.title("Đồ Án Python")
root.geometry("800x600")  # Kích thước cửa sổ

# Frame chính
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

# Khởi tạo Treeview để hiển thị dữ liệu
tree = ttk.Treeview(main_frame)
tree.pack(fill=tk.BOTH, expand=True)

# Frame cho CRUD
crud_frame = tk.Frame(root)
crud_frame.pack(fill=tk.X)

# Từ điển để lưu các ô nhập liệu cho từng cột
entries = {}

# Hàm để load dữ liệu từ DataFrame vào Treeview
def load_data_to_treeview():
    global df
    df = pd.read_csv(file_path)

    # Xóa dữ liệu cũ trên Treeview
    for item in tree.get_children():
        tree.delete(item)

    # Thêm dữ liệu mới vào Treeview
    tree["column"] = list(df.columns)  # Đặt tên các cột theo DataFrame
    tree["show"] = "headings"  # Ẩn cột đầu tiên (index)

    # Đặt tiêu đề cho mỗi cột
    for column in tree["columns"]:
        tree.heading(column, text=column)
        tree.column(column, width=100)  # Điều chỉnh độ rộng của các cột nếu cần

    # Chèn dữ liệu từ DataFrame vào Treeview
    for idx, row in df.iterrows():
        tree.insert("", "end", iid=idx, values=list(row))

#==================================================================================================
# Hàm thêm mới dữ liệu
def create_entry():
    # Them code cho chuc nang C trong (CRUD)
    load_data_to_treeview()

# Hàm cập nhật dữ liệu
def update_entry():
    # Them code cho chuc nang U trong (CRUD)
    load_data_to_treeview()  # Tải lại dữ liệu vào Treeview


# Hàm xóa dữ liệu
def delete_entry():
    # Thêm code cho chuc nang D trong (CRUD)
    load_data_to_treeview()

# Hàm vẽ đồ thị
def paint_graphic():
    # Them code ve bieu do phan tich du lieu bang Matplotlib o day
    plt.show()

def sort_value():
    St = Standardization.Standardization(file_path)
    St.sortByValues(key="Year")
    load_data_to_treeview()

#======================================================================================================

# Hàm mở file và đọc dữ liệu
def open_file():
    global file_path
    file_path = askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if file_path:
        global df
        df = pd.read_csv(file_path)  # Sử dụng file_path mà người dùng chọn
        load_data_to_treeview()  # Hiển thị dữ liệu lên Treeview
        
        # Xóa các Entry cũ nếu đã tồn tại
        for widget in crud_frame.winfo_children():
            widget.destroy()
        
        # Tạo các Label và Entry cho mỗi cột của DataFrame
        global entries
        entries = {}
        for i, column in enumerate(df.columns):
            label = tk.Label(crud_frame, text=column)
            label.grid(row=0, column=i)
            entry = tk.Entry(crud_frame)
            entry.grid(row=1, column=i)
            entries[column] = entry
        
        # Thêm các nút CRUD
        create_btn = tk.Button(crud_frame, text="Add", command=create_entry, bg="Yellow", fg="Blue")
        create_btn.grid(row=2, column=0)
        update_btn = tk.Button(crud_frame, text="Update", command=update_entry, bg="Yellow", fg="Blue")
        update_btn.grid(row=2, column=1)
        delete_btn = tk.Button(crud_frame, text="Delete", command=delete_entry, bg="Yellow", fg="Blue")
        delete_btn.grid(row=2, column=2)
        paint_btn = tk.Button(crud_frame, text="Graphic", command=paint_graphic, bg="Yellow", fg="Blue")
        paint_btn.grid(row=2, column=3)
        sort_btn = tk.Button(crud_frame, text="Sort", command=sort_value, bg="Yellow", fg="Blue")
        sort_btn.grid(row=2, column=4)

# Hàm thoát ứng dụng
def quit_app():
    root.quit()

# Thêm Menu vào cửa sổ
menu = tk.Menu(root)
root.config(menu=menu)

file_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=quit_app)

# Chạy vòng lặp chính của Tkinter
root.mainloop()
