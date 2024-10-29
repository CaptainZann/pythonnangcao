import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Kết nối tới cơ sở dữ liệu SQLite
def connect_db():
    with sqlite3.connect('students.db') as conn:
        cursor = conn.cursor()
        # Tạo bảng mới với cột student_id
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT NOT NULL,
                name TEXT NOT NULL,
                age INTEGER NOT NULL
            )
        ''')

# Hàm thêm sinh viên vào cơ sở dữ liệu
def add_student():
    student_id = student_id_entry.get().strip()
    name = name_entry.get().strip()
    age = age_entry.get().strip()
    # Kiểm tra tính hợp lệ của mã số sinh viên
    if len(student_id) != 13:
        messagebox.showwarning('Cảnh báo', 'Mã số sinh viên phải đúng 13 ký tự')
        return

    if student_id and name and age:
        try:
            with sqlite3.connect('students.db') as conn:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO students (student_id, name, age) VALUES (?, ?, ?)', (student_id, name, age))
            messagebox.showinfo('Thông báo', 'Đã thêm sinh viên thành công!')
            student_id_entry.delete(0, tk.END)
            name_entry.delete(0, tk.END)
            age_entry.delete(0, tk.END)
            show_students()
        except Exception as e:
            messagebox.showerror('Lỗi', str(e))
    else:
        messagebox.showwarning('Cảnh báo', 'Vui lòng nhập đầy đủ thông tin')

# Hàm xóa sinh viên
def delete_student():
    selected_item = student_list.selection()
    if not selected_item:
        messagebox.showwarning('Cảnh báo', 'Vui lòng chọn sinh viên để xóa')
        return

    student_id = student_list.item(selected_item)['values'][0]
    with sqlite3.connect('students.db') as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM students WHERE id = ?', (student_id,))
    messagebox.showinfo('Thông báo', 'Đã xóa sinh viên thành công!')
    show_students()

# Hàm sửa thông tin sinh viên
def update_student():
    selected_item = student_list.selection()
    if not selected_item:
        messagebox.showwarning('Cảnh báo', 'Vui lòng chọn sinh viên để sửa')
        return

    student_id = student_list.item(selected_item)['values'][0]
    new_student_id = student_id_entry.get().strip()
    new_name = name_entry.get().strip()
    new_age = age_entry.get().strip()

    # Kiểm tra tính hợp lệ của mã số sinh viên
    if len(new_student_id) != 13:
        messagebox.showwarning('Cảnh báo', 'Mã số sinh viên phải đúng 13 ký tự')
        return

    if new_student_id and new_name and new_age:
        with sqlite3.connect('students.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE students SET student_id = ?, name = ?, age = ? WHERE id = ?
            ''', (new_student_id, new_name, new_age, student_id))
        messagebox.showinfo('Thông báo', 'Đã cập nhật thông tin sinh viên thành công!')
        student_id_entry.delete(0, tk.END)
        name_entry.delete(0, tk.END)
        age_entry.delete(0, tk.END)
        show_students()
    else:
        messagebox.showwarning('Cảnh báo', 'Vui lòng nhập đầy đủ thông tin')

# Hàm hiển thị danh sách sinh viên
def show_students():
    for item in student_list.get_children():
        student_list.delete(item)
    with sqlite3.connect('students.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM students')
        rows = cursor.fetchall()
    for row in rows:
        student_list.insert('', tk.END, values=row)

# Hàm chọn sinh viên từ danh sách để điền vào form
def select_student(event):
    selected_item = student_list.selection()
    if selected_item:
        student = student_list.item(selected_item)['values']
        student_id_entry.delete(0, tk.END)
        student_id_entry.insert(0, student[1])
        name_entry.delete(0, tk.END)
        name_entry.insert(0, student[2])
        age_entry.delete(0, tk.END)
        age_entry.insert(0, student[3])

# Tạo giao diện với Tkinter
root = tk.Tk()
root.title('Quản lý Sinh viên')

# Nhãn và Entry cho mã số sinh viên
tk.Label(root, text='Mã số sinh viên:').grid(row=0, column=0, padx=10, pady=5)
student_id_entry = tk.Entry(root)
student_id_entry.grid(row=0, column=1, padx=10, pady=5)

# Nhãn và Entry cho tên và tuổi
tk.Label(root, text='Tên sinh viên:').grid(row=1, column=0, padx=10, pady=5)
name_entry = tk.Entry(root)
name_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text='Tuổi:').grid(row=2, column=0, padx=10, pady=5)
age_entry = tk.Entry(root)
age_entry.grid(row=2, column=1, padx=10, pady=5)

# Nút thêm, xóa và sửa sinh viên
add_button = tk.Button(root, text='Thêm Sinh Viên', command=add_student)
add_button.grid(row=3, column=0, pady=10)

delete_button = tk.Button(root, text='Xóa Sinh Viên', command=delete_student)
delete_button.grid(row=3, column=1, pady=10)

update_button = tk.Button(root, text='Sửa Sinh Viên', command=update_student)
update_button.grid(row=3, column=2, pady=10)

# Bảng danh sách sinh viên
columns = ('ID', 'Mã số sinh viên', 'Tên', 'Tuổi')
student_list = ttk.Treeview(root, columns=columns, show='headings')
for col in columns:
    student_list.heading(col, text=col)
student_list.grid(row=4, column=0, columnspan=3, pady=10)

# Ràng buộc sự kiện chọn sinh viên
student_list.bind('<<TreeviewSelect>>', select_student)

# Kết nối cơ sở dữ liệu và hiển thị dữ liệu ban đầu
connect_db()
show_students()

# Chạy giao diện
root.mainloop()
