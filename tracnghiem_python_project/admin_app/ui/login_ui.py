import tkinter as tk
from tkinter import messagebox
from shared.db import fetch_data

def show_login_window(on_success_callback):
    root = tk.Tk()
    root.title("Đăng Nhập - Hệ Thống Trắc Nghiệm")
    root.geometry("820x480")
    root.resizable(False, False)
    root.configure(bg="#0D2340")

    # ==========================================
    # KHUNG TRÁI — Nền xanh đậm sang trọng
    # ==========================================
    left_frame = tk.Frame(root, bg="#0D2340", width=330, height=480)
    left_frame.pack(side="left", fill="both")
    left_frame.pack_propagate(False)

    # Trang trí: canvas vẽ vòng tròn và chấm
    deco_canvas = tk.Canvas(left_frame, width=330, height=480, bg="#0D2340",
                            highlightthickness=0)
    deco_canvas.place(x=0, y=0)
    # Vòng tròn lớn góc trên phải
    deco_canvas.create_oval(200, -100, 430, 130,
                            outline="#C9972B", width=35, stipple="gray25")
    # Vòng tròn nhỏ góc dưới trái
    deco_canvas.create_oval(-60, 340, 120, 520,
                            outline="#C9972B", width=22, stipple="gray12")
    # Lưới chấm góc trên trái
    for row in range(4):
        for col in range(6):
            x = 28 + col * 12
            y = 28 + row * 12
            deco_canvas.create_oval(x-2, y-2, x+2, y+2, fill="#C9972B", outline="")

    # Nội dung chính (đặt trên canvas)
    content_frame = tk.Frame(left_frame, bg="#0D2340")
    content_frame.place(x=36, y=240)

    # Huy hiệu tròn giả lập bằng Label
    badge_outer = tk.Frame(content_frame, bg="#C9972B", width=62, height=62)
    badge_outer.pack(anchor="w", pady=(0, 0))
    badge_outer.pack_propagate(False)
    badge_inner = tk.Frame(badge_outer, bg="#0D2340", width=56, height=56)
    badge_inner.place(relx=0.5, rely=0.5, anchor="center")
    tk.Label(badge_inner, text="SG", font=("Georgia", 16, "bold"),
             fg="#C9972B", bg="#0D2340").place(relx=0.5, rely=0.5, anchor="center")

    # Đường kẻ vàng
    tk.Frame(content_frame, bg="#C9972B", width=36, height=2).pack(anchor="w", pady=(16, 12))

    # Tên hệ thống (Đã xóa thuộc tính letterSpacing bị lỗi)
    tk.Label(content_frame, text="HỆ THỐNG TRẮC NGHIỆM",
             font=("Arial", 9, "bold"), fg="#C9972B", bg="#0D2340").pack(anchor="w", pady=(8, 4))


    # ==========================================
    # KHUNG PHẢI — Form đăng nhập
    # ==========================================
    right_frame = tk.Frame(root, bg="#F8F9FB", width=490, height=480)
    right_frame.pack(side="right", fill="both", expand=True)
    right_frame.pack_propagate(False)

    form_box = tk.Frame(right_frame, bg="#F8F9FB")
    form_box.place(relx=0.5, rely=0.5, anchor="center")

    # Tiêu đề
    tk.Label(form_box, text="Đăng nhập",
             font=("Georgia", 22, "bold"), fg="#0D2340", bg="#F8F9FB").pack(anchor="w")

    tk.Label(form_box,
             text="------------------------------------------------",
             font=("Arial", 10), fg="#8A9BB0", bg="#F8F9FB").pack(anchor="w", pady=(4, 24))

    # --- Ô tên đăng nhập --- (Đã xóa thuộc tính letterSpacing bị lỗi)
    tk.Label(form_box, text="TÊN ĐĂNG NHẬP",
             font=("Arial", 8, "bold"), fg="#0D2340", bg="#F8F9FB").pack(anchor="w")

    user_frame = tk.Frame(form_box, bg="#FFFFFF",
                          highlightthickness=1.5, highlightbackground="#E2E8EF",
                          highlightcolor="#C9972B")
    user_frame.pack(fill="x", pady=(6, 16), ipadx=4, ipady=2)

    txt_user = tk.Entry(user_frame, font=("Arial", 12), width=28,
                        relief="flat", bg="#FFFFFF", fg="#0D2340",
                        insertbackground="#0D2340")
    txt_user.pack(padx=12, pady=8)
    txt_user.insert(0, "")

    # Focus highlight
    def on_focus_user(e):
        user_frame.config(highlightbackground="#C9972B")
    def on_leave_user(e):
        user_frame.config(highlightbackground="#E2E8EF")
    txt_user.bind("<FocusIn>", on_focus_user)
    txt_user.bind("<FocusOut>", on_leave_user)

    # --- Ô mật khẩu ---
    tk.Label(form_box, text="MẬT KHẨU",
             font=("Arial", 8, "bold"), fg="#0D2340", bg="#F8F9FB").pack(anchor="w")

    pass_frame = tk.Frame(form_box, bg="#FFFFFF",
                          highlightthickness=1.5, highlightbackground="#E2E8EF",
                          highlightcolor="#C9972B")
    pass_frame.pack(fill="x", pady=(6, 22), ipadx=4, ipady=2)

    txt_pass = tk.Entry(pass_frame, font=("Arial", 12), width=28,
                        relief="flat", bg="#FFFFFF", fg="#0D2340",
                        insertbackground="#0D2340", show="●")
    txt_pass.pack(padx=12, pady=8)

    def on_focus_pass(e):
        pass_frame.config(highlightbackground="#C9972B")
    def on_leave_pass(e):
        pass_frame.config(highlightbackground="#E2E8EF")
    txt_pass.bind("<FocusIn>", on_focus_pass)
    txt_pass.bind("<FocusOut>", on_leave_pass)

    # --- Hàm kiểm tra đăng nhập ---
    def check_login(event=None):
        username = txt_user.get().strip()
        password = txt_pass.get().strip()

        if not username or not password:
            messagebox.showwarning("Thiếu thông tin",
                                   "Vui lòng nhập đầy đủ tài khoản và mật khẩu!")
            return

        users = fetch_data("SELECT * FROM admins WHERE username = %s", (username,))

        if len(users) > 0:
            admin = users[0]
            if password == admin['password_hash']:
                root.destroy()
                on_success_callback(admin)
            else:
                messagebox.showerror("Sai mật khẩu",
                                     "Mật khẩu không đúng. Vui lòng thử lại.")
        else:
            messagebox.showerror("Không tìm thấy",
                                 "Tài khoản không tồn tại trong hệ thống.")

    # Cho phép nhấn Enter để đăng nhập
    txt_pass.bind("<Return>", check_login)
    txt_user.bind("<Return>", lambda e: txt_pass.focus())

    # Nút Đăng Nhập
    btn_login = tk.Button(
        form_box,
        text="ĐĂNG NHẬP  →",
        font=("Arial", 10, "bold"),
        bg="#0D2340", fg="#FFFFFF",
        activebackground="#16345A", activeforeground="#C9972B",
        width=30, height=2,
        relief="flat", cursor="hand2",
        command=check_login
    )
    btn_login.pack()

    # Hover effect cho nút
    def btn_enter(e): btn_login.config(bg="#16345A")
    def btn_leave(e): btn_login.config(bg="#0D2340")
    btn_login.bind("<Enter>", btn_enter)
    btn_login.bind("<Leave>", btn_leave)

    # Footer
    sep = tk.Frame(form_box, bg="#E2E8EF", height=1, width=300)
    sep.pack(pady=(24, 12))

    root.mainloop()