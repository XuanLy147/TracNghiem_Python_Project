import sys
import os

# Thêm thư mục gốc (tracnghiem_python_project) vào hệ thống tìm kiếm module của Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from ui.login_ui import show_login_window
from ui.student_ui import show_student_management
from ui.question_ui import show_question_management
from ui.subject_ui import show_subject_management
class AdminDashboard:
    def __init__(self, root, admin_info):
        self.root = root
        self.admin_info = admin_info
        
        self.root.title("Dashboard Quản Trị - Hệ Thống Trắc Nghiệm")
        self.root.geometry("1100x700")
        self.root.configure(bg="#F8F9FB")

        self.setup_layout()

    def setup_layout(self):
        # ==========================================
        # 1. SIDEBAR TRÁI (Layer Chức Năng)
        # ==========================================
        self.sidebar = tk.Frame(self.root, bg="#0D2340", width=260)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False) # Cố định chiều rộng sidebar

        # Logo / Tên hệ thống
        tk.Label(self.sidebar, text="TRẮC NGHIỆM\nADMIN", font=("Arial", 16, "bold"), 
                 fg="#C9972B", bg="#0D2340", justify="center").pack(pady=(30, 20))
        tk.Frame(self.sidebar, bg="#C9972B", height=2, width=200).pack(pady=(0, 20))

        # Lưu trữ các nút để dễ đổi màu khi Active
        self.menu_buttons = []

        # Tạo các nút chức năng
        self.btn_subjects = self.create_nav_button("🏷 Quản Lý Môn Học", self.show_subjects)
        self.btn_questions = self.create_nav_button("📚 Ngân Hàng Câu Hỏi", self.show_questions)
        self.btn_students = self.create_nav_button("👥 Quản Lý Học Viên", self.show_students)

        # Nút đăng xuất ở đáy
        btn_logout = tk.Button(self.sidebar, text="🚪 Đăng Xuất", font=("Arial", 11, "bold"), 
                               bg="#16345A", fg="white", activebackground="#E2E8EF", 
                               activeforeground="#E63946", relief="flat", cursor="hand2", 
                               command=self.logout)
        btn_logout.pack(side="bottom", fill="x", pady=20, padx=15)

        # ==========================================
        # 2. PANEL PHẢI (Thông tin chức năng & Ứng dụng)
        # ==========================================
        self.right_panel = tk.Frame(self.root, bg="#F8F9FB")
        self.right_panel.pack(side="right", fill="both", expand=True)

        # Topbar Header (Tiêu đề trang & Info Admin)
        self.header = tk.Frame(self.right_panel, bg="#FFFFFF", height=65, 
                               highlightthickness=1, highlightbackground="#E2E8EF")
        self.header.pack(side="top", fill="x")
        self.header.pack_propagate(False)

        self.lbl_page_title = tk.Label(self.header, text="Trang Chủ", 
                                       font=("Arial", 14, "bold"), fg="#0D2340", bg="#FFFFFF")
        self.lbl_page_title.pack(side="left", padx=25)

        tk.Label(self.header, text=f"👤 {self.admin_info.get('username', 'Admin')}", 
                 font=("Arial", 11, "bold"), fg="#8A9BB0", bg="#FFFFFF").pack(side="right", padx=25)

        # KHUNG NỘI DUNG ĐỘNG (Nơi load UI của từng chức năng)
        self.main_content = tk.Frame(self.right_panel, bg="#F8F9FB")
        self.main_content.pack(side="top", fill="both", expand=True, padx=25, pady=25)

        # Bật trang mặc định khi vừa đăng nhập xong
        self.show_subjects()

    # --- Các hàm hỗ trợ giao diện ---
    def create_nav_button(self, text, command):
        """Hàm tạo nút Menu với hiệu ứng Hover"""
        btn = tk.Button(self.sidebar, text=text, font=("Arial", 11, "bold"), bg="#0D2340", 
                        fg="white", activebackground="#C9972B", activeforeground="#0D2340", 
                        relief="flat", anchor="w", padx=20, pady=12, cursor="hand2", command=command)
        btn.pack(fill="x", pady=2)
        
        # Hiệu ứng Hover đơn giản
        btn.bind("<Enter>", lambda e: btn.config(bg="#16345A") if btn['bg'] != "#C9972B" else None)
        btn.bind("<Leave>", lambda e: btn.config(bg="#0D2340") if btn['bg'] != "#C9972B" else None)
        
        self.menu_buttons.append(btn)
        return btn

    def set_active_menu(self, active_btn, title_text):
        """Hàm đổi màu nút đang chọn và đổi tiêu đề Header, đồng thời dọn dẹp frame cũ"""
        # Reset màu tất cả nút
        for btn in self.menu_buttons:
            btn.config(bg="#0D2340", fg="white")
        # Đổi màu nút đang click
        active_btn.config(bg="#C9972B", fg="#0D2340")
        
        # Đổi tiêu đề Header
        self.lbl_page_title.config(text=title_text)

        # HỦY toàn bộ nội dung cũ trong main_content để nhường chỗ cho UI mới
        for widget in self.main_content.winfo_children():
            widget.destroy()

    # --- Logic chuyển trang ---
    def show_subjects(self):
        self.set_active_menu(self.btn_subjects, "Quản Lý Môn Học")
        show_subject_management(self.main_content)

    def show_questions(self):
        self.set_active_menu(self.btn_questions, "Quản Lý Ngân Hàng Câu Hỏi")
        show_question_management(self.main_content)

    def show_students(self):
        self.set_active_menu(self.btn_students, "Quản Lý Học Viên")
        show_student_management(self.main_content)

    def logout(self):
        self.root.destroy()
        start_app() # Quay lại màn hình đăng nhập

# ==========================================
# KHỞI CHẠY LUỒNG ỨNG DỤNG
# ==========================================
def open_dashboard(admin_info):
    """Callback chạy sau khi đăng nhập thành công"""
    root = tk.Tk()
    app = AdminDashboard(root, admin_info)
    root.mainloop()

def start_app():
    """Bật cửa sổ đăng nhập đầu tiên"""
    show_login_window(on_success_callback=open_dashboard)

if __name__ == "__main__":
    start_app()
