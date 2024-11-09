import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
import threading

# Khởi tạo cửa sổ chính
root = tk.Tk()
root.title("Quản Lý Dữ Liệu Video Game Sales")
root.geometry("1400x700")
root.configure(bg="#f0f0f0")

# Khung chính để hiển thị dữ liệu
main_frame = tk.Frame(root, bg="#f0f0f0")
main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Tạo Treeview để hiển thị dữ liệu
tree = ttk.Treeview(main_frame)
tree.pack(fill=tk.BOTH, expand=True)

# Thêm thanh cuộn dọc và ngang cho Treeview
tree_scroll_y = ttk.Scrollbar(main_frame, orient="vertical", command=tree.yview)
tree_scroll_y.pack(side="right", fill="y")
tree_scroll_x = ttk.Scrollbar(main_frame, orient="horizontal", command=tree.xview)
tree_scroll_x.pack(side="bottom", fill="x")

tree.configure(yscrollcommand=tree_scroll_y.set, xscrollcommand=tree_scroll_x.set)

# Biến lưu trữ DataFrame
df = pd.DataFrame()

# Khung nhập liệu cho các thao tác CRUD
entry_frame = tk.Frame(root, bg="#f0f0f0")
entry_frame.pack(fill=tk.X, padx=10, pady=10)

# Hàm tải dữ liệu từ tệp CSV vào Treeview
def load_data_to_treeview(show_message=False):
    global df
    try:
        # Xóa dữ liệu cũ trong Treeview
        for item in tree.get_children():
            tree.delete(item)

        # Đặt tên cột và hiển thị dữ liệu
        tree["column"] = list(df.columns)
        tree["show"] = "headings"

        for col in tree["column"]:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor="center")

        # Chèn dữ liệu từ DataFrame vào Treeview
        for index, row in df.iterrows():
            tree.insert("", "end", iid=index, values=list(row))

        create_entry_fields()

        if show_message:
            messagebox.showinfo("Thành công", "Dữ liệu đã được tải lên thành công!")

    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể tải dữ liệu: {e}")

# Hàm mở file CSV
def open_file():
    global file_path, df
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if file_path:
        try:
            df = pd.read_csv(file_path)
            if df.empty:
                messagebox.showwarning("Cảnh báo", "File CSV không có dữ liệu.")
                return
            load_data_to_treeview(show_message=True)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể mở file CSV: {e}")
    else:
        messagebox.showinfo("Thông báo", "Chưa chọn file CSV nào.")

# Hàm tạo các trường nhập liệu và các nút chức năng
def create_entry_fields():
    for widget in entry_frame.winfo_children():
        widget.destroy()

    global entries
    entries = {}

    if not df.empty:
        columns = df.columns
        num_columns = len(columns)
        for i, col in enumerate(columns):
            label = tk.Label(entry_frame, text=col, bg="#f0f0f0", font=("Arial", 10, "bold"))
            label.grid(row=0, column=i, padx=5, pady=5, sticky="w")
            entry = tk.Entry(entry_frame, width=15)  # Điều chỉnh độ rộng của ô nhập liệu
            entry.grid(row=1, column=i, padx=5, pady=5, sticky="w")
            entries[col] = entry

    create_btn = tk.Button(entry_frame, text="Add", bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), command=create_entry)
    create_btn.grid(row=2, column=0, padx=5, pady=5)

    update_btn = tk.Button(entry_frame, text="Update", bg="#FFA500", fg="white", font=("Arial", 10, "bold"), command=update_entry)
    update_btn.grid(row=2, column=1, padx=5, pady=5)

    delete_btn = tk.Button(entry_frame, text="Delete", bg="#f44336", fg="white", font=("Arial", 10, "bold"), command=delete_entry)
    delete_btn.grid(row=2, column=2, padx=5, pady=5)

    plot_btn = tk.Button(entry_frame, text="Graphic", bg="#2196F3", fg="white", font=("Arial", 10, "bold"), command=choose_graphic)
    plot_btn.grid(row=2, column=3, padx=5, pady=5)

    sort_label = tk.Label(entry_frame, text="Sắp xếp theo:", bg="#f0f0f0", font=("Arial", 10, "bold"))
    sort_label.grid(row=2, column=4, padx=5, pady=5)

    sort_combobox = ttk.Combobox(entry_frame, values=list(df.columns))
    sort_combobox.grid(row=2, column=5, padx=5, pady=5)

    sort_btn = tk.Button(entry_frame, text="Sort", bg="#9C27B0", fg="white", font=("Arial", 10, "bold"),
                         command=lambda: sort_data(sort_combobox.get()))
    sort_btn.grid(row=2, column=6, padx=5, pady=5)

# Các hàm CRUD cơ bản để thực hiện chức năng
def create_entry():
    if df.empty:
        messagebox.showwarning("Cảnh báo", "Bạn cần tải dữ liệu CSV trước khi thêm.")
        return

    new_data = [entry.get() for entry in entries.values()]
    if len(new_data) == len(df.columns):
        try:
            new_row = pd.Series(new_data, index=df.columns)
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            load_data_to_treeview()
            messagebox.showinfo("Thành công", "Dữ liệu đã được thêm thành công!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể thêm dữ liệu: {e}")
    else:
        messagebox.showwarning("Cảnh báo", "Hãy nhập đủ thông tin vào các trường dữ liệu.")

def update_entry():
    try:
        selected_item = tree.selection()[0]
        values = [entry.get() for entry in entries.values()]
        if len(values) == len(df.columns):
            for i, col in enumerate(df.columns):
                df.at[int(selected_item), col] = values[i]
            load_data_to_treeview()
            messagebox.showinfo("Thành công", "Dữ liệu đã được cập nhật thành công!")
        else:
            messagebox.showwarning("Cảnh báo", "Hãy nhập đủ thông tin vào các trường dữ liệu.")
    except IndexError:
        messagebox.showwarning("Cảnh báo", "Chưa chọn dòng để cập nhật.")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể cập nhật dữ liệu: {e}")

def delete_entry():
    try:
        selected_item = tree.selection()[0]
        df.drop(int(selected_item), inplace=True)
        df.reset_index(drop=True, inplace=True)
        load_data_to_treeview()
        messagebox.showinfo("Thành công", "Dữ liệu đã được xóa thành công!")
    except IndexError:
        messagebox.showwarning("Cảnh báo", "Chưa chọn dòng để xóa.")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể xóa dữ liệu: {e}")

def choose_graphic():
    try:
        columns = [col for col in df.columns if df[col].dtype in ['int64', 'float64']]
        if not columns:
            messagebox.showwarning("Cảnh báo", "Không có cột nào có dữ liệu số để vẽ biểu đồ.")
            return
        select_window = tk.Toplevel(root)
        select_window.title("Chọn Cột Vẽ Biểu Đồ")
        select_window.geometry("400x300")
        select_window.configure(bg="#f0f0f0")

        listbox = tk.Listbox(select_window, selectmode="multiple")
        listbox.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        for col in columns:
            listbox.insert(tk.END, col)

        def plot_selected():
            selected_indices = listbox.curselection()
            if not selected_indices:
                messagebox.showwarning("Cảnh báo", "Vui lòng chọn ít nhất một cột để vẽ biểu đồ.")
                return

            selected_columns = [columns[i] for i in selected_indices]

            # Tạo luồng mới để vẽ biểu đồ
            def plot_thread():
                plt.ion()  # Bật chế độ interactive mode
                try:
                    df[selected_columns].plot(kind='bar', figsize=(10, 6))
                    plt.title('Biểu Đồ So Sánh')
                    plt.xlabel('Index')
                    plt.ylabel('Giá Trị')
                    plt.xticks(rotation=90)
                    plt.tight_layout()
                    plt.show()
                except Exception as e:
                    messagebox.showerror("Lỗi", f"Không thể vẽ biểu đồ: {e}")

            thread = threading.Thread(target=plot_thread)
            thread.start()

        plot_btn = tk.Button(select_window, text="Vẽ Biểu Đồ", command=plot_selected, bg="#2196F3", fg="white", font=("Arial", 12, "bold"))
        plot_btn.pack(pady=10)

    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể vẽ biểu đồ: {e}")

def sort_data(column_name):
    try:
        if column_name not in df.columns:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn cột hợp lệ để sắp xếp.")
            return
        df.sort_values(by=column_name, inplace=True)
        load_data_to_treeview()
        messagebox.showinfo("Thành công", f"Dữ liệu đã được sắp xếp theo {column_name} thành công!")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể sắp xếp dữ liệu: {e}")

# Tạo menu
menu = tk.Menu(root)
root.config(menu=menu)

file_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

# Chạy vòng lặp chính của Tkinter
root.mainloop()
