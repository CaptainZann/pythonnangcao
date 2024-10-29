import tkinter as tk
from tkinter import ttk

def Tru():
    perform_calculation(lambda a, b: a - b, "Hiệu là")

def Cong():
    perform_calculation(lambda a, b: a + b, "Tổng là")

def Nhan():
    perform_calculation(lambda a, b: a * b, "Tích là")

def Chia():
    perform_calculation(lambda a, b: a / b if b != 0 else None, "Thương là", error_msg="Lỗi: Không thể chia cho 0")

def perform_calculation(operation, result_text, error_msg=""):
    try:
        a = float(entry_a.get())
        b = float(entry_b.get())
        result_value = operation(a, b)
        if result_value is not None:
            result.set(f"{result_text}: {result_value}")
        else:
            result.set(error_msg)
    except ValueError:
        result.set("Lỗi: Vui lòng nhập số hợp lệ")

def reset_fields():
    entry_a.delete(0, tk.END)
    entry_b.delete(0, tk.END)
    result.set("")

# Tạo cửa sổ chính
win = tk.Tk()
win.title("Công cụ tính toán Promax")

# Nhập liệu
input_frame = ttk.LabelFrame(win, text='Nhập số liệu', labelanchor='n')  
input_frame.grid(column=0, row=0, padx=10, pady=10)

ttk.Label(input_frame, text="Nhập số a: ").grid(column=0, row=0, sticky=tk.W)
entry_a = ttk.Entry(input_frame)
entry_a.grid(column=1, row=0)  

ttk.Label(input_frame, text="Nhập số b: ").grid(column=0, row=1, sticky=tk.W)
entry_b = ttk.Entry(input_frame)
entry_b.grid(column=1, row=1)  

# Tính toán
calc_frame = ttk.LabelFrame(win, text='Tính toán', labelanchor='n') 
calc_frame.grid(column=1, row=0, padx=10, pady=10)

# Nút tính toán
ttk.Button(calc_frame, text="+", command=Cong).grid(row=0, column=0)
ttk.Button(calc_frame, text="-", command=Tru).grid(row=1, column=0)
ttk.Button(calc_frame, text="*", command=Nhan).grid(row=0, column=1)
ttk.Button(calc_frame, text="/", command=Chia).grid(row=1, column=1)

# Nút reset
ttk.Button(calc_frame, text="Reset", command=reset_fields).grid(row=2, column=0, columnspan=2)

# Kết quả
result_frame = ttk.LabelFrame(win, text='Kết quả') 
result_frame.grid(column=0, row=1, columnspan=2, padx=10, pady=10)

ttk.Label(result_frame, text="Kết quả là: ").grid(column=0, row=0, sticky=tk.W)
result = tk.StringVar()
ttk.Label(result_frame, textvariable=result).grid(column=1, row=0)

# Chạy vòng lặp chính
win.mainloop()
