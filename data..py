import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc

# Kết nối đến cơ sở dữ liệu
conx = pyodbc.connect(r'DRIVER={ODBC Driver 17 for SQL Server};SERVER=Admin\SQLEXPRESS;DATABASE=QUANLYKHOHANG; UID=minhngoc; PWD=luandz123')
cursor = conx.cursor()

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Database Manipulation")

# Tạo danh sách dropdown chứa tên của tất cả các bảng
table_names = [row.TABLE_NAME for row in cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'")]
table_name = tk.StringVar()
table_dropdown = ttk.Combobox(root, textvariable=table_name, values=table_names)
table_dropdown.pack()

# Tạo bảng để hiển thị dữ liệu
tree = ttk.Treeview(root)
tree.pack()

# Hàm để cập nhật bảng khi một bảng mới được chọn từ danh sách dropdown
def update_table(event):
    tree.delete(*tree.get_children())
    columns = [row.COLUMN_NAME for row in cursor.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name.get()}'")]
    tree["columns"] = columns
    for column in columns:
        tree.heading(column, text=column)
    for row in cursor.execute(f"SELECT * FROM {table_name.get()}"):
        tree.insert('', 'end', values= list(row))

table_dropdown.bind("<<ComboboxSelected>>", update_table)
# Hàm để thêm dữ liệu mới khi nút "Add" được nhấn
def add_data():
    def submit():
        values = [entry.get() for entry in entries]
        try:
            cursor.execute(f"INSERT INTO {table_name.get()} VALUES ({', '.join('?' * len(values))})", values)
            conx.commit()  # Lưu thay đổi vào cơ sở dữ liệu
            update_table(None)  # Cập nhật lại bảng hiển thị
            add_window.destroy()  # Đóng cửa sổ thêm dữ liệu
        except pyodbc.IntegrityError as e:
            messagebox.showerror("Lỗi", "Không thể thêm bản ghi: " + str(e))  # Hiển thị thông báo lỗi
            # Xử lý lỗi ở đây, ví dụ: làm trống các ô nhập liệu, đưa con trỏ vào ô đầu tiên,...
        cursor.execute(f"INSERT INTO {table_name.get()} VALUES ({', '.join('?' * len(values))})", values)
        conx.commit()
        update_table(None)
        add_window.destroy()

    add_window = tk.Toplevel(root)
    add_window.title("Add Data")
    columns = [row.COLUMN_NAME for row in cursor.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name.get()}'")]
    entries = []
    for column in columns:
        label = tk.Label(add_window, text=column)
        label.pack()
        entry = tk.Entry(add_window)
        entry.pack()
        entries.append(entry)
    submit_button = tk.Button(add_window, text="Submit", command=submit)
    submit_button.pack()
    
    

# Hàm để chỉnh sửa dữ liệu khi nút "Edit" được nhấn
def edit_data():
    def submit():
        values = [entry.get() for entry in entries]
        maphanphoi = values[1]  # Lấy giá trị MaPhanPhoi từ danh sách values (giả sử nó ở vị trí thứ hai)
        max_length = 50  # Ví dụ: giới hạn độ dài MaPhanPhoi là 50 ký tự

        # Kiểm tra độ dài của MaPhanPhoi
        if len(maphanphoi) > max_length:
            messagebox.showerror("Lỗi", "Giá trị MaPhanPhoi quá dài!")
        else:
            try:
                cursor.execute(
                    f"UPDATE {table_name.get()} SET {', '.join(f'{column} = ?' for column in columns)} WHERE {columns[0]} = ?",
                    *values,
                    tree.item(tree.selection())['values'][0]
                )
                conx.commit()
                messagebox.showinfo("Thông báo", "Đã cập nhật học sinh thành công!")
                edit_window.destroy()
            except pyodbc.Error as e:
                messagebox.showerror("Lỗi", "Không thể cập nhật học sinh: " + str(e))
        cursor.execute(f"UPDATE {table_name.get()} SET {', '.join(f'{column} = ?' for column in columns)} WHERE {columns[0]} = ?", *values, tree.item(tree.selection())['values'][0])
        conx.commit()
        update_table(None)
        edit_window.destroy()

    edit_window = tk.Toplevel(root)
    edit_window.title("Edit Data")
    columns = [row.COLUMN_NAME for row in cursor.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name.get()}'")]
    entries = []
    for column, value in zip(columns, tree.item(tree.selection())['values']):
        label = tk.Label(edit_window, text=column)
        label.pack()
        entry = tk.Entry(edit_window)
        entry.insert(0, value)
        entry.pack()
        entries.append(entry)
    submit_button = tk.Button(edit_window, text="Submit", command=submit)
    submit_button.pack()

# Hàm để xóa dữ liệu khi nút "Delete" được nhấn
def delete_data():
    cursor.execute(f"DELETE FROM {table_name.get()} WHERE {tree['columns'][0]} = ?", tree.item(tree.selection())['values'][0])
    conx.commit()
    update_table(None)

# Tạo các nút "Add", "Edit", và "Delete"
add_button = tk.Button(root, text="Add", command=add_data)
add_button.pack()
edit_button = tk.Button(root, text="Edit", command=edit_data)
edit_button.pack()
delete_button = tk.Button(root, text="Delete", command=delete_data)
delete_button.pack()



root.mainloop()
