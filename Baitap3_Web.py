from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Khởi tạo Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Tạo cơ sở dữ liệu SQLite để lưu người dùng
def init_sqlite_db():
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')
init_sqlite_db()

# Tạo User class kế thừa từ UserMixin để sử dụng với Flask-Login
class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def get_id(self):
        return str(self.id)

# Hàm load_user cho Flask-Login
@login_manager.user_loader
def load_user(user_id):
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        row = cursor.fetchone()
        if row:
            return User(id=row[0], username=row[1], password=row[2])
        return None

# Trang chủ chuyển hướng đến trang đăng nhập
@app.route('/')
def home():
    return redirect(url_for('login'))

# Trang đăng ký
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with sqlite3.connect('users.db') as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
                conn.commit()
                flash('Đăng ký thành công. Bạn có thể đăng nhập ngay bây giờ.', 'success')
                return redirect(url_for('login'))
            except sqlite3.IntegrityError:
                flash('Tên đăng nhập đã tồn tại.', 'danger')
    return render_template('register.html')

# Trang đăng nhập
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with sqlite3.connect('users.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
            row = cursor.fetchone()
            if row:
                user = User(id=row[0], username=row[1], password=row[2])
                login_user(user)
                flash('Đăng nhập thành công.', 'success')
                return redirect(url_for('dashboard'))
            flash('Tên đăng nhập hoặc mật khẩu không đúng.', 'danger')
    return render_template('login.html')

# Trang đăng xuất
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Bạn đã đăng xuất.', 'info')
    return redirect(url_for('login'))

# Trang dashboard yêu cầu đăng nhập
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', username=current_user.username)

if __name__ == '__main__':
    app.run(debug=True)