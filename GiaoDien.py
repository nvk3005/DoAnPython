import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
import threading
import CRUD
import Standardization

# Khởi tạo cửa sổ chính
root = tk.Tk()
root.title("Quản Lý Dữ Liệu Video Game Sales")
root.geometry("1400x700")
root.configure(bg="#f0f0f0")

# Khung chính để hiển thị dữ liệu
main_frame = tk.Frame(root, bg="#f0f0f0")
main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Khung dành cho cơ chế phân trang
nav_frame = tk.Frame(root, bg="#f0f0f0")
nav_frame.pack(fill=tk.X, padx=10, pady=10)

# Khung dành cho các hàm chức năng
function_frame = tk.Frame(root, bg="#f0f0f0")
function_frame.pack(fill=tk.X, padx=10, pady=10)

# Biến lưu trữ DataFrame
df = pd.DataFrame()

# Tạo Treeview để hiển thị dữ liệu
tree = ttk.Treeview(main_frame, height=11) 
tree.pack(fill=tk.BOTH, expand=True)

# Các biến phân trang
ROWS_PER_PAGE = 20  # Số dòng hiển thị trên mỗi trang
current_page = 1  # Trang hiện tại
total_pages = 1  # Tổng số trang


def load_data_to_treeview(show_message=False):
    ''' Hàm hiển thị dữ liệu từ File ra màn hình'''
    global df, file_path, total_pages
    try:
        df = pd.read_csv(file_path)
        if df.empty:
            messagebox.showwarning("Cảnh báo", "File CSV không có dữ liệu.")
            return

        total_pages = len(df) // ROWS_PER_PAGE + (1 if len(df) % ROWS_PER_PAGE > 0 else 0)

        # Xóa dữ liệu cũ trong Treeview
        for item in tree.get_children():
            tree.delete(item)

        # Đặt tên cột và hiển thị dữ liệu 
        tree["column"] = list(df.columns)
        tree["show"] = "headings"
        for col in tree["column"]:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor="center")

        # Hiển thị các hàng trên trang hiện tại
        start_row = (current_page - 1) * ROWS_PER_PAGE
        end_row = start_row + ROWS_PER_PAGE
        page_data = df.iloc[start_row: end_row]
        for index, row in page_data.iterrows():
            tree.insert("", "end", iid=row["Rank"], values=list(row))

        # Cập nhật trạng thái nút chuyển trang
        update_navigation_buttons()

        # Hiển thị các nút chức năng
        create_entry_fields()

        if show_message:
            messagebox.showinfo("Thành công", "Dữ liệu đã được tải lên thành công!")

    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể tải dữ liệu: {e}")

def update_navigation_buttons():
    '''Hàm cập nhật trạng thái các nút của cơ chế phân trang'''
    global current_page, total_pages

    # Xóa các nút cũ trong nav_frame
    for widget in nav_frame.winfo_children():
        widget.destroy()

    # Nút Trang trước
    prev_btn = tk.Button(nav_frame, text="Trang Trước", command=prev_page, state=tk.NORMAL if current_page > 1 else tk.DISABLED)
    prev_btn.grid(row=0, column=0, padx=5, pady=5)

    # Nút Trang sau
    next_btn = tk.Button(nav_frame, text="Trang Sau", command=next_page, state=tk.NORMAL if current_page < total_pages else tk.DISABLED)
    next_btn.grid(row=0, column=1, padx=5, pady=5)

    # Hiển thị số trang
    page_label = tk.Label(nav_frame, text=f"Trang {current_page} / {total_pages}", font=("Arial", 10, "bold"))
    page_label.grid(row=0, column=2, padx=5, pady=5)

    # Tạo nhãn nhập số trang
    input_label = tk.Label(nav_frame, text="Nhập trang bạn muốn đi tới", font=("Arial", 10, "bold"), bg= "#708090")
    input_label.grid(row=0, column=3, padx=5, pady=5, sticky='e')

    global input_entry
    # Tạo ô nhập dữ liệu số trang muốn đi tới
    input_entry = tk.Entry(nav_frame, width=15)
    input_entry.grid(row=0, column=4, padx=5, pady=5)

    # Tạo nút nhập cho số trang
    input_btn = tk.Button(nav_frame, text="Nhập", font=("Arial", 10, "bold"), command=input_page)
    input_btn.grid(row=1, column=4, padx=5, pady=5)

def prev_page():
    '''Hàm chuyển đến trang trước'''
    global current_page
    if current_page > 1:
        current_page -= 1
        load_data_to_treeview()

def next_page():
    '''Hàm chuyển đến trang sau'''
    global current_page
    if current_page < total_pages:
        current_page += 1
        load_data_to_treeview()

def input_page():
    '''Hàm nhập số thứ tự trang mà người dùng muốn xem'''
    global input_entry, total_pages, current_page
    page = int(input_entry.get())
    if 1 <= page <= total_pages:
        current_page = page
        load_data_to_treeview()
    else:
        messagebox.showerror("Lỗi", "Trang bạn nhập không tồn tại")

def open_file():
    '''Hàm mở File csv được người dùng lựa chọn'''
    global file_path, df
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])

    if file_path: # Trường hợp đã chọn file
        try:
            df = pd.read_csv(file_path)
            if df.empty:
                messagebox.showwarning("Cảnh báo", "File CSV không có dữ liệu.")
                return
            load_data_to_treeview(show_message=True)
        except Exception as e: # Bắt bất kỳ ngoại lệ nào.
            messagebox.showerror("Lỗi", f"Không thể mở file CSV: {e}")
    else: # Trường hợp chưa chọn file
        messagebox.showinfo("Thông báo", "Chưa chọn file CSV nào.")


def create_entry_fields():
    '''Hàm tạo các trường nhập dữ liệu cho các nút chức năng'''
    for widget in function_frame.winfo_children():
        widget.destroy()

    global entries
    entries = {}

    if not df.empty:
        columns = list(df.columns) # tên các tiêu đề cột
        i = 0
        for col in range(1, len(columns)-1):
            label = tk.Label(function_frame, text=columns[col], bg="#f0f0f0", font=("Arial", 10, "bold"))
            label.grid(row=0, column=i, padx=5, pady=5, sticky="w")
            entry = tk.Entry(function_frame, width=15)
            entry.grid(row=1, column=i, padx=5, pady=5, sticky="w")
            entries[columns[col]] = entry # Tham chiếu tên cột với ô nhập dữ liệu của cột đó
            i += 1

    create_btn = tk.Button(function_frame, text="Create", bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), command=create_entry)
    create_btn.grid(row=2, column=0, padx=5, pady=5)

    update_btn = tk.Button(function_frame, text="Update", bg="#FFA500", fg="white", font=("Arial", 10, "bold"), command=update_entry)
    update_btn.grid(row=2, column=1, padx=5, pady=5)

    delete_btn = tk.Button(function_frame, text="Delete", bg="#f44336", fg="white", font=("Arial", 10, "bold"), command=delete_entry)
    delete_btn.grid(row=2, column=2, padx=5, pady=5)

    plot_btn = tk.Button(function_frame, text="Graphic", bg="#2196F3", fg="white", font=("Arial", 10, "bold"), command=choose_graphic)
    plot_btn.grid(row=2, column=3, padx=5, pady=5)

    sort_label = tk.Label(function_frame, text="Sắp xếp theo:", bg="#f0f0f0", font=("Arial", 10, "bold"))
    sort_label.grid(row=2, column=4, padx=5, pady=5)

    sort_combobox = ttk.Combobox(function_frame, values=list(df.columns))
    sort_combobox.grid(row=2, column=5, padx=5, pady=5)

    sort_btn = tk.Button(function_frame, text="Sort", bg="#9C27B0", fg="white", font=("Arial", 10, "bold"),
                         command=lambda: sort_data(sort_combobox.get()))
    sort_btn.grid(row=2, column=6, padx=5, pady=5)

# Tạo biến cho các chức năng CRUD
manager = CRUD.CSVManager(file_path)

def create_entry():
    '''Hàm xử lý sự kiện chức năng thêm hàng mới'''
    global manager
    new_data = [entry.get() for entry in entries.values()]

    # Chuyển đổi giá trị Rank trong new_data về kiểu phù hợp
    try:
        rank_value = int(new_data[0])  # Nếu cột "Rank" là số, chuyển thành số nguyên
    except ValueError:
        messagebox.showerror("Lỗi", "Giá trị Rank phải là một số.")
        return

    # Kiểm tra xem rank_value đã tồn tại trong df["Rank"] hay chưa
    if rank_value in df["Rank"].values:
        messagebox.showerror("Lỗi", "Giá trị Rank bạn vừa nhập đã tồn tại.")
    else:
        manager.create(new_data)
        load_data_to_treeview()  # Tải lại Treeview sau khi thêm hàng mới

def update_entry():
    '''Hàm xử lý sự kiện cho chức năng cập nhật hàng'''
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
    '''Hàm xử lý sự kiện cho chức năng xóa hàng'''
    global file_path
    manager = CRUD.CSVManager(file_path)
    try:
        selected_item = tree.selection()[0] # Lấy ID của phần tử đầu tiên được chọn (ID này đã được đặt theo rank)
        manager.delete(selected_item)
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
    global file_path
    standardization = Standardization.Standardization(file_path)
    try:
        if column_name not in df.columns:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn cột hợp lệ để sắp xếp.")
            return
        standardization.sortByValues(column_name)
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