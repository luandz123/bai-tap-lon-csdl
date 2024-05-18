import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc

# Kết nối đến cơ sở dữ liệu
conx = pyodbc.connect(r'DRIVER={SQL Server};SERVER=Admin\SQLEXPRESS;DATABASE=luanne; UID=minhngoc; PWD=luandz123')
cursor = conx.cursor()

# Tạo cửa sổ tkinter
window = tk.Tk()
window.title("Thêm học sinh")

# Tạo các ô nhập liệu
mahocsinh_entry = ttk.Entry(window, width=30)
mahocsinh_entry.grid(row=0, column=1)
tk.Label(window, text="Mã học sinh:").grid(row=0)

ten_entry = ttk.Entry(window, width=30)
ten_entry.grid(row=1, column=1)
tk.Label(window, text="Tên:").grid(row=1)

tuoi_entry = ttk.Entry(window, width=30)
tuoi_entry.grid(row=2, column=1)
tk.Label(window, text="Tuổi:").grid(row=2)

# Hàm thêm học sinh vào cơ sở dữ liệu
def submit():
    mahocsinh = mahocsinh_entry.get()
    ten = ten_entry.get()
    tuoi = tuoi_entry.get()
    cursor.execute("INSERT INTO hocsinh (mahocsinh, ten, tuoi) VALUES (?, ?, ?)", (mahocsinh, ten, tuoi))
    conx.commit()
    messagebox.showinfo("Thông báo", "Đã thêm học sinh thành công!")

# Tạo nút Submit
submit_button = ttk.Button(window, text="Submit", command=submit)
submit_button.grid(row=3, column=0, columnspan=2)

window.mainloop()