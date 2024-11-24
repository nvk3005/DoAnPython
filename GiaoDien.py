import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
import Standardization
from Data_visualization import VideoGameBarChart

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
        if df.empty:
            messagebox.showwarning("Cảnh báo", "Chưa có dữ liệu để hiển thị.")
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
            tree.insert("", "end", iid=index, values=list(row))

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

def open_file():
    '''Hàm mở File csv được người dùng lựa chọn'''
    global file_path, df
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])

    if file_path:  # Trường hợp đã chọn file
        try:
            df = pd.read_csv(file_path, low_memory=False)
            if df.empty:
                messagebox.showwarning("Cảnh báo", "File CSV không có dữ liệu.")
                return
            load_data_to_treeview(show_message=True)
        except Exception as e:  # Bắt bất kỳ ngoại lệ nào.
            messagebox.showerror("Lỗi", f"Không thể mở file CSV: {e}")
    else:  # Trường hợp chưa chọn file
        messagebox.showinfo("Thông báo", "Chưa chọn file CSV nào.")

def sort_data(column, ascending=True):
    """Hàm sắp xếp dữ liệu theo cột đã chọn với thứ tự tăng hoặc giảm."""
    global df
    if df.empty:
        messagebox.showwarning("Cảnh báo", "Chưa có dữ liệu để sắp xếp.")
        return

    if not column:
        messagebox.showerror("Lỗi", "Vui lòng chọn một cột để sắp xếp.")
        return

    if column not in df.columns:
        messagebox.showerror("Lỗi", f"Cột '{column}' không tồn tại trong dữ liệu.")
        return

    try:
        # Sắp xếp dữ liệu
        df = df.sort_values(by=column, ascending=ascending).reset_index(drop=True)

        # Cập nhật Treeview
        load_data_to_treeview()
        order_text = "tăng dần" if ascending else "giảm dần"
        messagebox.showinfo("Thành công", f"Dữ liệu đã được sắp xếp theo cột '{column}' ({order_text}).")

    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể sắp xếp dữ liệu: {e}")

def create_entry_fields():
    """Hàm tạo các trường nhập dữ liệu và các nút chức năng"""
    # Xóa các widget cũ trong frame
    for widget in function_frame.winfo_children():
        widget.destroy()

    global entries
    entries = {}

    # Tạo các trường nhập liệu cho từng cột
    if not df.empty:
        columns = list(df.columns)  # Danh sách các tiêu đề cột
        for i, col in enumerate(columns):
            label = tk.Label(function_frame, text=col, bg="#f0f0f0", font=("Arial", 10, "bold"))
            label.grid(row=0, column=i, padx=5, pady=5, sticky="w")
            entry = tk.Entry(function_frame, width=15)
            entry.grid(row=1, column=i, padx=5, pady=5, sticky="w")
            entries[col] = entry  # Tham chiếu tiêu đề cột với entry nhập liệu

    # Thêm các nút chức năng CRUD
    create_btn = tk.Button(function_frame, text="Create", bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), command=create_entry)
    create_btn.grid(row=2, column=0, padx=5, pady=5)

    update_btn = tk.Button(function_frame, text="Update", bg="#FFA500", fg="white", font=("Arial", 10, "bold"), command=update_entry)
    update_btn.grid(row=2, column=1, padx=5, pady=5)

    delete_btn = tk.Button(function_frame, text="Delete", bg="#f44336", fg="white", font=("Arial", 10, "bold"), command=delete_entry)
    delete_btn.grid(row=2, column=2, padx=5, pady=5)

    plot_btn = tk.Button(function_frame, text="Graphic", bg="#2196F3", fg="white", font=("Arial", 10, "bold"), command=choose_graphic)
    plot_btn.grid(row=2, column=3, padx=5, pady=5)

    # Thêm chức năng sắp xếp
    sort_label = tk.Label(function_frame, text="Sắp xếp theo:", bg="#f0f0f0", font=("Arial", 10, "bold"))
    sort_label.grid(row=2, column=4, padx=5, pady=5)

    # Combobox chọn cột để sắp xếp
    sort_combobox = ttk.Combobox(function_frame, values=list(df.columns), state="readonly")
    sort_combobox.grid(row=2, column=5, padx=5, pady=5)

    # Combobox chọn kiểu sắp xếp
    order_label = tk.Label(function_frame, text="Kiểu sắp xếp:", bg="#f0f0f0", font=("Arial", 10, "bold"))
    order_label.grid(row=2, column=6, padx=5, pady=5)

    order_combobox = ttk.Combobox(function_frame, values=["Tăng dần", "Giảm dần"], state="readonly")
    order_combobox.grid(row=2, column=7, padx=5, pady=5)

    # Nút sắp xếp
    sort_btn = tk.Button(function_frame, text="Sắp xếp", bg="#8BC34A", fg="white", font=("Arial", 10, "bold"),
                         command=lambda: sort_data(sort_combobox.get(), order_combobox.get() == "Tăng dần"))
    sort_btn.grid(row=2, column=8, padx=5, pady=5)

# Biến cho các chức năng CRUD
def create_entry():
    '''Hàm xử lý sự kiện chức năng thêm hàng mới'''
    global df
    try:
        # Lấy dữ liệu từ các ô nhập
        new_data = {col: entries[col].get() for col in entries}

        # Kiểm tra nếu có trường nào để trống
        missing_fields = [field for field, value in new_data.items() if not value]
        if missing_fields:
            messagebox.showerror(
                "Lỗi",
                f"Các trường sau đang bị bỏ trống: {', '.join(missing_fields)}"
            )
            return

        # Thêm dữ liệu vào DataFrame
        df = df.append(new_data, ignore_index=True)

        # Tải lại Treeview sau khi thêm hàng mới
        load_data_to_treeview()
        messagebox.showinfo("Thành công", "Dữ liệu đã được thêm thành công!")
    except ValueError:
        messagebox.showerror("Lỗi", "Dữ liệu nhập không đúng định dạng (ví dụ: Năm hoặc Doanh số phải là số).")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể thêm dữ liệu: {e}")

def update_entry():
    '''Hàm xử lý sự kiện cho chức năng cập nhật hàng'''
    global df
    try:
        # Lấy dữ liệu mới từ các ô nhập
        new_data = {col: entries[col].get() for col in entries}

        # Kiểm tra nếu có trường nào để trống
        missing_fields = [field for field, value in new_data.items() if not value]
        if missing_fields:
            messagebox.showerror(
                "Lỗi",
                f"Các trường sau đang bị bỏ trống: {', '.join(missing_fields)}"
            )
            return

        # Lấy dòng được chọn từ Treeview
        selected_item = tree.selection()[0]
        selected_index = int(selected_item)

        # Cập nhật dữ liệu trong DataFrame
        for col, value in new_data.items():
            df.at[selected_index, col] = value

        # Tải lại Treeview sau khi cập nhật
        load_data_to_treeview()
        messagebox.showinfo("Thành công", "Dữ liệu đã được cập nhật thành công!")
    except IndexError:
        messagebox.showwarning("Cảnh báo", "Chưa chọn dòng để cập nhật.")
    except ValueError:
        messagebox.showerror("Lỗi", "Dữ liệu nhập không đúng định dạng (ví dụ: Năm hoặc Doanh số phải là số).")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể cập nhật dữ liệu: {e}")

def delete_entry():
    '''Hàm xử lý sự kiện cho chức năng xóa hàng'''
    global df
    try:
        selected_item = tree.selection()[0] # Lấy ID của phần tử đầu tiên được chọn
        selected_index = int(selected_item)

        # Xóa dòng trong DataFrame
        df = df.drop(selected_index).reset_index(drop=True)

        # Tải lại Treeview sau khi xóa
        load_data_to_treeview()
        messagebox.showinfo("Thành công", "Dữ liệu đã được xóa thành công!")
    except IndexError:
        messagebox.showwarning("Cảnh báo", "Chưa chọn dòng để xóa.")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể xóa dữ liệu: {e}")

def choose_graphic():
    """Hàm hiển thị giao diện chọn loại biểu đồ."""
    try:
        if df.empty:
            messagebox.showwarning("Cảnh báo", "Vui lòng tải dữ liệu trước khi vẽ biểu đồ.")
            return

        # Lọc các cột có dữ liệu số
        numeric_columns = [col for col in df.columns if pd.api.types.is_numeric_dtype(df[col])]
        if not numeric_columns:
            messagebox.showwarning("Cảnh báo", "Không có cột nào chứa dữ liệu số để vẽ biểu đồ.")
            return

        # Cửa sổ chọn loại biểu đồ
        select_window = tk.Toplevel(root)
        select_window.title("Chọn Loại Biểu Đồ")
        select_window.geometry("400x500")
        select_window.configure(bg="#f0f0f0")

        # Dropdown để chọn loại biểu đồ
        chart_types = ["Bar Chart", "Pie Chart", "Line Chart"]
        chart_type_var = tk.StringVar(value=chart_types[0])
        tk.Label(select_window, text="Chọn loại biểu đồ:", bg="#f0f0f0").pack(pady=10)
        chart_type_menu = ttk.Combobox(select_window, textvariable=chart_type_var, values=chart_types, state="readonly")
        chart_type_menu.pack(pady=10)

        # Listbox để chọn cột dữ liệu
        tk.Label(select_window, text="Chọn cột dữ liệu:", bg="#f0f0f0").pack(pady=10)
        listbox = tk.Listbox(select_window, selectmode="multiple")
        listbox.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        for col in numeric_columns:
            listbox.insert(tk.END, col)

        # Hàm vẽ biểu đồ
        def plot_selected():
            selected_indices = listbox.curselection()
            if not selected_indices:
                messagebox.showwarning("Cảnh báo", "Vui lòng chọn ít nhất một cột để vẽ biểu đồ.")
                return

            selected_columns = [numeric_columns[i] for i in selected_indices]
            chart_type = chart_type_var.get()

            # Lấy dữ liệu từ các cột đã chọn
            data = df[selected_columns]

            # Vẽ biểu đồ dựa trên loại đã chọn
            plt.figure(figsize=(10, 6))
            if chart_type == "Bar Chart":
                data.sum().plot(kind='bar', title="Biểu đồ cột")
                plt.xlabel("Cột dữ liệu")
                plt.ylabel("Giá trị tổng")
            elif chart_type == "Pie Chart":
                if len(selected_columns) > 1:
                    messagebox.showwarning("Cảnh báo", "Biểu đồ tròn chỉ hỗ trợ một cột dữ liệu.")
                    return
                pie_data = data[selected_columns[0]].value_counts()
                if len(pie_data) > 10:
                    pie_data = pd.concat([pie_data.iloc[:9], pd.Series([pie_data.iloc[9:].sum()], index=["Khác"])])
                pie_data.plot(kind='pie', title="Biểu đồ tròn", autopct='%1.1f%%')
                plt.ylabel("")
            elif chart_type == "Line Chart":
                data.plot(kind='line', title="Biểu đồ đường")
                plt.xlabel("Chỉ mục")
                plt.ylabel("Giá trị")
            else:
                messagebox.showerror("Lỗi", "Loại biểu đồ không được hỗ trợ.")
                return

            # Hiển thị biểu đồ
            plt.tight_layout()
            plt.show()

        # Nút vẽ biểu đồ
        plot_btn = tk.Button(select_window, text="Vẽ Biểu Đồ", command=plot_selected, bg="#2196F3", fg="white", font=("Arial", 12, "bold"))
        plot_btn.pack(pady=10)

    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể vẽ biểu đồ: {e}")

# Tạo menu
menu = tk.Menu(root)
root.config(menu=menu)

file_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

root.mainloop()
