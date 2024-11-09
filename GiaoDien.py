import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from tkinter.filedialog import askopenfilename, asksaveasfilename
import matplotlib.pyplot as plt

# Khởi tạo cửa sổ chính
root = tk.Tk()
root.title("Quản Lý Dữ Liệu Video Game Sales")
root.geometry("1000x600")

# Khung chính để hiển thị dữ liệu
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

tree = ttk.Treeview(main_frame)
tree.pack(fill=tk.BOTH, expand=True)

# Biến lưu trữ DataFrame
df = pd.DataFrame()

# Khung nhập liệu cho các thao tác CRUD
entry_frame = tk.Frame(root)
entry_frame.pack(fill=tk.X)

# Hàm để tải dữ liệu từ tệp CSV vào Treeview
def load_data_to_treeview():
    global df
    df = pd.read_csv(file_path)

    # Xóa dữ liệu cũ trong Treeview
    for item in tree.get_children():
        tree.delete(item)

    # Đặt tên cột và hiển thị dữ liệu
    tree["column"] = list(df.columns)
    tree["show"] = "headings"

    for col in tree["column"]:
        tree.heading(col, text=col)
        tree.column(col, width=100)

    for idx, row in df.iterrows():
        tree.insert("", "end", values=list(row))

# Hàm mở file CSV
def open_file():
    global file_path
    file_path = askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if file_path:
        load_data_to_treeview()
        create_entry_fields()

# Tạo các trường nhập liệu cho CRUD
def create_entry_fields():
    for widget in entry_frame.winfo_children():
        widget.destroy()

    global entries
    entries = {}

    for i, col in enumerate(df.columns):
        label = tk.Label(entry_frame, text=col)
        label.grid(row=0, column=i)
        entry = tk.Entry(entry_frame)
        entry.grid(row=1, column=i)
        entries[col] = entry

    # Thêm các nút CRUD
    create_btn = tk.Button(entry_frame, text="Thêm", command=create_entry)
    create_btn.grid(row=2, column=0)
    update_btn = tk.Button(entry_frame, text="Cập nhật", command=update_entry)
    update_btn.grid(row=2, column=1)
    delete_btn = tk.Button(entry_frame, text="Xóa", command=delete_entry)
    delete_btn.grid(row=2, column=2)
    quit_btn = tk.Button(entry_frame, text="Thoát", command=root.quit)
    quit_btn.grid(row=2, column=3)
    plot_btn = tk.Button(entry_frame, text="Vẽ Biểu Đồ", command=paint_graphic)
    plot_btn.grid(row=2, column=4)

# Thêm một hàng mới
def create_entry():
    global df
    new_data = {col: entry.get() for col, entry in entries.items()}
    df = df.append(new_data, ignore_index=True)
    df.to_csv(file_path, index=False)
    load_data_to_treeview()
    messagebox.showinfo("Thành công", "Đã thêm dữ liệu mới!")

# Cập nhật hàng được chọn
def update_entry():
    global df
    selected_item = tree.selection()
    if selected_item:
        idx = int(selected_item[0])
        updated_data = {col: entry.get() for col, entry in entries.items()}
        for col, value in updated_data.items():
            df.at[idx, col] = value
        df.to_csv(file_path, index=False)
        load_data_to_treeview()
        messagebox.showinfo("Thành công", "Đã cập nhật dữ liệu!")
    else:
        messagebox.showwarning("Cảnh báo", "Chưa chọn mục cần cập nhật!")

# Xóa hàng được chọn
def delete_entry():
    global df
    selected_item = tree.selection()
    if selected_item:
        idx = int(selected_item[0])
        df = df.drop(idx).reset_index(drop=True)
        df.to_csv(file_path, index=False)
        load_data_to_treeview()
        messagebox.showinfo("Thành công", "Đã xóa dữ liệu!")
    else:
        messagebox.showwarning("Cảnh báo", "Chưa chọn mục cần xóa!")

# Hàm vẽ biểu đồ
def paint_graphic():
    if df.empty:
        messagebox.showwarning("Cảnh báo", "Chưa có dữ liệu để vẽ biểu đồ!")
        return

    plt.figure(figsize=(10, 6))
    df['Year'].value_counts().sort_index().plot(kind='bar')
    plt.title("Phân phối số lượng game theo năm")
    plt.xlabel("Năm")
    plt.ylabel("Số lượng game")
    plt.show()

# Tạo menu
menu = tk.Menu(root)
root.config(menu=menu)

file_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Tệp", menu=file_menu)
file_menu.add_command(label="Mở", command=open_file)
file_menu.add_separator()
file_menu.add_command(label="Thoát", command=root.quit)

# Chạy vòng lặp chính của Tkinter
root.mainloop()
