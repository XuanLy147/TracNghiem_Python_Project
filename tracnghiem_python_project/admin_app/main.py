import sys
import os
import tkinter as tk

# Khai báo đường dẫn để import được file db.py từ thư mục shared
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from admin_app.ui.login_ui import show_login_window

def open_main_dashboard(admin):
    # Đây là cửa sổ chính hiện ra SAU KHI đăng nhập thành công
    dashboard = tk.Tk()
    dashboard.title("Trang Quản Trị")
    dashboard.geometry("500x300")

    tk.Label(dashboard, text=f"Xin chào Admin: {admin['username']}", font=("Arial", 16)).pack(pady=20)
    tk.Label(dashboard, text="Các nút chức năng hệ thống sẽ được vẽ ở đây...").pack()

    dashboard.mainloop()

if __name__ == "__main__":
    # Bắt đầu chương trình: Gọi hàm hiện cửa sổ đăng nhập. 
    # Nếu thành công thì truyền hàm open_main_dashboard vào để chạy tiếp.
    show_login_window(on_success_callback=open_main_dashboard)