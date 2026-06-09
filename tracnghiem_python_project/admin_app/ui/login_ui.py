
# python admin_app/main.py

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

    deco_canvas = tk.Canvas(left_frame, width=330, height=480, bg="#0D2340", highlightthickness=0)
    deco_canvas.place(x=0, y=0)
    deco_canvas.create_oval(200, -100, 430, 130, outline="#C9972B", width=35, stipple="gray25")
    deco_canvas.create_oval(-60, 340, 120, 520, outline="#C9972B", width=22, stipple="gray12")
    for row in range(4):
        for col in range(6):
            x = 28 + col * 12
            y = 28 + row * 12
            deco_canvas.create_oval(x-2, y-2, x+2, y+2, fill="#C9972B", outline="")

    content_frame = tk.Frame(left_frame, bg="#0D2340")
    content_frame.place(x=36, y=240)

    badge_outer = tk.Frame(content_frame, bg="#C9972B", width=62, height=62)
    badge_outer.pack(anchor="w", pady=(0, 0))
    badge_outer.pack_propagate(False)
    badge_inner = tk.Frame(badge_outer, bg="#0D2340", width=56, height=56)
    badge_inner.place(relx=0.5, rely=0.5, anchor="center")
    tk.Label(badge_inner, text="SG", font=("Georgia", 16, "bold"), fg="#C9972B", bg="#0D2340").place(relx=0.5, rely=0.5, anchor="center")

    tk.Frame(content_frame, bg="#C9972B", width=36, height=2).pack(anchor="w", pady=(16, 12))
    tk.Label(content_frame, text="HỆ THỐNG TRẮC NGHIỆM", font=("Arial", 9, "bold"), fg="#C9972B", bg="#0D2340").pack(anchor="w", pady=(8, 4))


    # ==========================================
    # KHUNG PHẢI — Form đăng nhập
    # ==========================================
    right_frame = tk.Frame(root, bg="#F8F9FB", width=490, height=480)
    right_frame.pack(side="right", fill="both", expand=True)
    right_frame.pack_propagate(False)

    form_box = tk.Frame(right_frame, bg="#F8F9FB")
    form_box.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(form_box, text="Đăng nhập", font=("Georgia", 22, "bold"), fg="#0D2340", bg="#F8F9FB").pack(anchor="w")
    tk.Label(form_box, text="------------------------------------------------", font=("Arial", 10), fg="#8A9BB0", bg="#F8F9FB").pack(anchor="w", pady=(4, 24))

    # --- Ô TÊN ĐĂNG NHẬP ---
    tk.Label(form_box, text="TÊN ĐĂNG NHẬP", font=("Arial", 8, "bold"), fg="#0D2340", bg="#F8F9FB").pack(anchor="w")
    user_frame = tk.Frame(form_box, bg="#FFFFFF", highlightthickness=1.5, highlightbackground="#E2E8EF", highlightcolor="#C9972B")
    user_frame.pack(fill="x", pady=(6, 16), ipadx=4, ipady=2)

    txt_user = tk.Entry(user_frame, font=("Arial", 12), width=28, relief="flat", bg="#FFFFFF", fg="#8A9BB0", insertbackground="#0D2340")
    txt_user.pack(padx=12, pady=8, fill="x")
    txt_user.insert(0, "Nhập tên đăng nhập...")

    def on_focus_user(e):
        user_frame.config(highlightbackground="#C9972B")
        if txt_user.get() == "Nhập tên đăng nhập...":
            txt_user.delete(0, 'end')
            txt_user.config(fg="#0D2340")

    def on_leave_user(e):
        user_frame.config(highlightbackground="#E2E8EF")
        if not txt_user.get():
            txt_user.insert(0, "Nhập tên đăng nhập...")
            txt_user.config(fg="#8A9BB0")

    txt_user.bind("<FocusIn>", on_focus_user)
    txt_user.bind("<FocusOut>", on_leave_user)

    # --- Ô MẬT KHẨU ---
    tk.Label(form_box, text="MẬT KHẨU", font=("Arial", 8, "bold"), fg="#0D2340", bg="#F8F9FB").pack(anchor="w")
    pass_frame = tk.Frame(form_box, bg="#FFFFFF", highlightthickness=1.5, highlightbackground="#E2E8EF", highlightcolor="#C9972B")
    pass_frame.pack(fill="x", pady=(6, 22), ipadx=4, ipady=2)

    txt_pass = tk.Entry(pass_frame, font=("Arial", 12), width=24, relief="flat", bg="#FFFFFF", fg="#8A9BB0", insertbackground="#0D2340")
    txt_pass.pack(side="left", padx=(12, 0), pady=8, fill="x", expand=True)
    txt_pass.insert(0, "Nhập mật khẩu...")

    # Nút ẩn/hiện mật khẩu
    btn_toggle_pw = tk.Label(pass_frame, text="👁", font=("Arial", 12), bg="#FFFFFF", fg="#8A9BB0", cursor="hand2")
    btn_toggle_pw.pack(side="right", padx=10)

    is_password_visible = False

    def toggle_password(e=None):
        nonlocal is_password_visible
        if txt_pass.get() != "Nhập mật khẩu...":
            is_password_visible = not is_password_visible
            if is_password_visible:
                txt_pass.config(show="")
                btn_toggle_pw.config(text="🙈", fg="#0D2340")
            else:
                txt_pass.config(show="●")
                btn_toggle_pw.config(text="👁", fg="#8A9BB0")

    btn_toggle_pw.bind("<Button-1>", toggle_password)

    def on_focus_pass(e):
        pass_frame.config(highlightbackground="#C9972B")
        if txt_pass.get() == "Nhập mật khẩu...":
            txt_pass.delete(0, 'end')
            txt_pass.config(fg="#0D2340", show="●" if not is_password_visible else "")

    def on_leave_pass(e):
        pass_frame.config(highlightbackground="#E2E8EF")
        if not txt_pass.get():
            txt_pass.config(show="")
            txt_pass.insert(0, "Nhập mật khẩu...")
            txt_pass.config(fg="#8A9BB0")
            btn_toggle_pw.config(fg="#8A9BB0", text="👁")

    txt_pass.bind("<FocusIn>", on_focus_pass)
    txt_pass.bind("<FocusOut>", on_leave_pass)

    # --- KIỂM TRA ĐĂNG NHẬP ---
    def check_login(event=None):
        username = txt_user.get().strip()
        password = txt_pass.get().strip()

        if username == "Nhập tên đăng nhập..." or password == "Nhập mật khẩu...":
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ tài khoản và mật khẩu!")
            return

        users = fetch_data("SELECT * FROM admins WHERE username = %s", (username,))

        if len(users) > 0:
            admin = users[0]
            if password == admin['password_hash']:
                root.destroy()
                on_success_callback(admin)
            else:
                messagebox.showerror("Sai mật khẩu", "Mật khẩu không đúng. Vui lòng thử lại.")
        else:
            messagebox.showerror("Không tìm thấy", "Tài khoản không tồn tại trong hệ thống.")

    txt_pass.bind("<Return>", check_login)
    txt_user.bind("<Return>", lambda e: txt_pass.focus())

    # --- NÚT ĐĂNG NHẬP ---
    btn_login = tk.Button(
        form_box, text="ĐĂNG NHẬP  →", font=("Arial", 10, "bold"),
        bg="#0D2340", fg="#FFFFFF", activebackground="#16345A", activeforeground="#C9972B",
        width=30, height=2, relief="flat", cursor="hand2", command=check_login
    )
    btn_login.pack()

    def btn_enter(e): btn_login.config(bg="#16345A")
    def btn_leave(e): btn_login.config(bg="#0D2340")
    btn_login.bind("<Enter>", btn_enter)    
    btn_login.bind("<Leave>", btn_leave)

    sep = tk.Frame(form_box, bg="#E2E8EF", height=1, width=300)
    sep.pack(pady=(24, 12))

    root.mainloop()
