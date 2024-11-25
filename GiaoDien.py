import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from Data_visualization import read_data, plot_sales_by_year, plot_sales_by_genre, plot_region_sales, plot_top_10_games
from threading import Thread
import CRUD
import Search

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
    global df, file_path, total_pages, current_page
    try:
        df = pd.read_csv(file_path, low_memory=False)
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

         # Hiển thị dữ liệu lên Treeview
        for _, row in page_data.iterrows():
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

file_path = None
def open_file():
    '''Hàm mở File csv được người dùng lựa chọn'''
    global file_path, df, manager
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])

    if file_path:  # Trường hợp đã chọn file
        try:
            new_df = pd.read_csv(file_path, low_memory=False)
            if new_df.empty:
                messagebox.showwarning("Cảnh báo", "File CSV không có dữ liệu.")
                return
            df=new_df
            # Khởi tạo manager với đường dẫn file
            manager = CRUD.CSVManager(file_path)
            load_data_to_treeview(show_message=True)
        except Exception as e:  # Bắt bất kỳ ngoại lệ nào.
            messagebox.showerror("Lỗi", f"Không thể mở file CSV: {e}")
    else:  # Trường hợp chưa chọn file
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
    # Thêm vào phần nút sắp xếp trong giao diện
    sort_combobox = ttk.Combobox(function_frame, values=list(df.columns), state="readonly")
    sort_combobox.grid(row=2, column=5, padx=5, pady=5)
    order_combobox = ttk.Combobox(function_frame, values=["Tăng dần", "Giảm dần"], state="readonly")
    order_combobox.grid(row=2, column=6, padx=5, pady=5)
    sort_btn = tk.Button(
        function_frame, 
        text="Sắp xếp",
        bg="#8BC34A",
        fg="white", 
        font=("Arial", 10, "bold"),
        command=lambda: sort_data(sort_combobox.get(), order_combobox.get() == "Tăng dần")
    )
    sort_btn.grid(row=2, column=7, padx=5, pady=5)

    search_label = tk.Label(function_frame, text="Tìm kiếm theo:", bg="#f0f0f0", font=("Arial", 10, "bold"))
    search_label.grid(row=2, column=9, padx=5, pady=5)

    search_combobox = ttk.Combobox(function_frame, values=["Rank", "Name", "Platform", "Year", "Genre" ,"Publisher"])
    search_combobox.grid(row=2, column=10, padx=5, pady=5)

    search_btn = tk.Button(function_frame, text="Tìm", bg="#2e8b57", fg="white", font=("Arial", 10, "bold"),
                       command=lambda: search_data(search_combobox.get()))
    search_btn.grid(row=2, column=11, padx=5, pady=5)

# Biến cho các chức năng CRUD
def create_entry():
    '''Hàm xử lý sự kiện chức năng thêm hàng mới'''
    global manager
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

        # Kiểm tra và chuyển đổi dữ liệu đầu vào
        name = new_data["Name"]
        platform = new_data["Platform"]
        year = int(new_data["Year"])
        genre = new_data["Genre"]
        publisher = new_data["Publisher"]
        na_sales = float(new_data["NA_Sales"])
        pal_sales = float(new_data["PAL_Sales"])
        jp_sales = float(new_data["JP_Sales"])
        other_sales = float(new_data["Other_Sales"])

        # Gọi hàm create trong manager
        manager.create(name, platform, year, genre, publisher, na_sales, pal_sales, jp_sales, other_sales)

        # Tải lại Treeview sau khi thêm hàng mới
        load_data_to_treeview()
        messagebox.showinfo("Thành công", "Dữ liệu đã được thêm thành công!")
    except ValueError:
        messagebox.showerror("Lỗi", "Dữ liệu nhập không đúng định dạng (ví dụ: Năm hoặc Doanh số phải là số).")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể thêm dữ liệu: {e}")

    
def update_entry():
    '''Hàm xử lý sự kiện cho chức năng cập nhật hàng'''
    global manager
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
        selected_item = int(selected_item)

        # Kiểm tra và chuyển đổi dữ liệu đầu vào
        name = new_data["Name"]
        platform = new_data["Platform"]
        year = int(new_data["Year"])
        genre = new_data["Genre"]
        publisher = new_data["Publisher"]
        na_sales = float(new_data["NA_Sales"])
        pal_sales = float(new_data["PAL_Sales"])
        jp_sales = float(new_data["JP_Sales"])
        other_sales = float(new_data["Other_Sales"])

        # Gọi hàm update trong manager
        manager.update(selected_item, name, platform, year, genre, publisher, na_sales, pal_sales, jp_sales, other_sales)

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
    global manager
    try:
        selected_item = tree.selection()[0] # Lấy ID của phần tử đầu tiên được chọn (ID này đã được đặt theo rank)
        manager.delete(selected_item)
        load_data_to_treeview()
        messagebox.showinfo("Thành công", "Dữ liệu đã được xóa thành công!")
    except IndexError:
        messagebox.showwarning("Cảnh báo", "Chưa chọn dòng để xóa.")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể xóa dữ liệu: {e}")
        import matplotlib.pyplot as plt


def choose_graphic():
    """Hàm chọn loại biểu đồ để vẽ."""
    try:
        graphic_window = tk.Toplevel(root)
        graphic_window.title("Chọn Loại Biểu Đồ")
        graphic_window.geometry("400x300")
        graphic_window.configure(bg="#f0f0f0")

        tk.Label(graphic_window, text="Chọn loại biểu đồ:", font=("Arial", 12, "bold"), bg="#f0f0f0").pack(pady=10)
         # Kiểm tra nếu `df` có dữ liệu
        if df.empty:
            messagebox.showerror("Lỗi", "Không có dữ liệu để vẽ biểu đồ. Vui lòng mở file CSV trước.")
            return

        def call_plot_sales_by_year():
            plot_sales_by_year(df)

        def call_plot_sales_by_genre():
            plot_sales_by_genre(df)

        def call_plot_region_sales():
            plot_region_sales(df)

        def call_plot_top_10_games():
            plot_top_10_games(df)

        tk.Button(graphic_window, text="Doanh số theo năm", command=call_plot_sales_by_year, bg="#4CAF50", fg="white").pack(pady=10)
        tk.Button(graphic_window, text="Doanh số theo thể loại", command=call_plot_sales_by_genre, bg="#2196F3", fg="white").pack(pady=10)
        tk.Button(graphic_window, text="Tỷ lệ doanh số theo khu vực", command=call_plot_region_sales, bg="#FF9800", fg="white").pack(pady=10)
        tk.Button(graphic_window, text="Top 10 trò chơi bán chạy", command=call_plot_top_10_games, bg="#800080", fg="white").pack(pady=10)
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể tạo giao diện biểu đồ: {e}")



def sort_data(column, ascending=True):
    """Sắp xếp dữ liệu trong DataFrame và cập nhật trực tiếp Treeview."""
    global df, current_page

    if df.empty:
        messagebox.showwarning("Cảnh báo", "Không có dữ liệu để sắp xếp.")
        return

    if column not in df.columns:
        messagebox.showerror("Lỗi", f"Cột '{column}' không tồn tại trong dữ liệu.")
        return

    try:
        # Chuẩn hóa dữ liệu cột (nếu cột là số)
        if df[column].dtype != 'object':  # Nếu không phải chuỗi
            df[column] = pd.to_numeric(df[column], errors='coerce')  # Chuyển đổi giá trị không hợp lệ thành NaN
            df = df.dropna(subset=[column])  # Loại bỏ hàng có giá trị NaN

        # Sắp xếp dữ liệu
        df = df.sort_values(by=column, ascending=ascending).reset_index(drop=True)

        # Xóa dữ liệu cũ trong Treeview
        for item in tree.get_children():
            tree.delete(item)

        # Hiển thị lại dữ liệu từ DataFrame đã sắp xếp
        start_row = (current_page - 1) * ROWS_PER_PAGE
        end_row = start_row + ROWS_PER_PAGE
        page_data = df.iloc[start_row:end_row]

        for _, row in page_data.iterrows():
            tree.insert("", "end", values=list(row))

        # Hiển thị thông báo
        order_text = "tăng dần" if ascending else "giảm dần"
        messagebox.showinfo("Thành công", f"Dữ liệu đã được sắp xếp theo cột '{column}' ({order_text}).")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể sắp xếp dữ liệu: {e}")


def search_data(column_name):
    """Hàm hiển thị kết quả tìm kiếm trong cửa sổ mới."""
    global file_path, df


    def execute_search():
        value = search_entry.get()  # Lấy giá trị từ ô nhập
        search = Search.Search(file_path)

        # Chuyển đổi kiểu dữ liệu phù hợp với cột đang tìm kiếm
        try:
            if column_name == "Year" or column_name == "Rank":
                value = int(value)  # Chuyển thành int với cột là năm
        except ValueError:
            messagebox.showerror("Lỗi", "Dữ liệu nhập không phù hợp với kiểu của cột.")
            return

        # Thực hiện tìm kiếm
        result = search.search_by_column(column_name, value)

        if result.empty:
            messagebox.showinfo("Kết quả", "Không tìm thấy dữ liệu phù hợp.")
        else:
            display_results(result)

    def display_results(result_df):
        """Hiển thị kết quả tìm kiếm trong cửa sổ riêng."""
        result_window = tk.Toplevel(root)
        result_window.title("Kết quả tìm kiếm")
        result_window.geometry("800x400")
        result_window.configure(bg="#f0f0f0")

        # Tạo Treeview trong cửa sổ kết quả
        result_tree = ttk.Treeview(result_window, height=15)
        result_tree.pack(fill=tk.BOTH, expand=True)

        # Đặt tên cột và hiển thị dữ liệu
        result_tree["column"] = list(result_df.columns)
        result_tree["show"] = "headings"
        for col in result_tree["column"]:
            result_tree.heading(col, text=col)
            result_tree.column(col, width=120, anchor="center")

        # Hiển thị dữ liệu tìm kiếm
        for index, row in result_df.iterrows():
            result_tree.insert("", "end", iid=row["Rank"], values=list(row))

        # Nút đóng cửa sổ
        close_btn = tk.Button(result_window, text="Đóng", command=result_window.destroy, bg="#f44336", fg="white",
                              font=("Arial", 10, "bold"))
        close_btn.pack(pady=10)

    # Tạo cửa sổ nhỏ cho chức năng tìm kiếm
    search_window = tk.Toplevel(root)
    search_window.title("Tìm kiếm")
    search_window.geometry("700x400")
    search_window.configure(bg="#f0f0f0")
    
    # Nhãn hướng dẫn
    tk.Label(search_window, text="Nhập từ khóa tìm kiếm:", bg="#f0f0f0", font=("Arial", 10, "bold")).pack(pady=10)
    
    # Ô nhập từ khóa
    search_entry = tk.Entry(search_window, width=30)
    search_entry.pack(pady=5)

    # Nút tìm kiếm
    search_btn = tk.Button(
        search_window, text="Tìm kiếm", font=("Arial", 10, "bold"), bg= "#48d1cc", command=execute_search
    )
    search_btn.pack(pady=10)

# Tạo menu
menu = tk.Menu(root)
root.config(menu=menu)

file_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

root.mainloop()
