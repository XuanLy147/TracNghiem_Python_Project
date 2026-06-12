import tkinter as tk
from tkinter import ttk, messagebox
from shared.db import fetch_data, execute_query

def show_student_management(parent):
    # Xóa các widget cũ
    for widget in parent.winfo_children():
        widget.destroy()

    # Container chính
    main_frame = tk.Frame(parent, bg="#F8F9FB")
    main_frame.pack(fill="both", expand=True)

    # ==========================================
    # 1. KHUNG NHẬP LIỆU (Bên trái hoặc ở trên)
    # ==========================================
    form_frame = tk.LabelFrame(main_frame, text="Thông Tin Học Viên", bg="#FFFFFF", font=("Arial", 10, "bold"), fg="#0D2340")
    form_frame.pack(side="top", fill="x", padx=10, pady=10)

    # Biến lưu trữ
    var_id = tk.StringVar()
    var_username = tk.StringVar()
    var_password = tk.StringVar()
    var_fullname = tk.StringVar()

    # Layout form
    tk.Label(form_frame, text="ID:", bg="#FFFFFF").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    tk.Entry(form_frame, textvariable=var_id, state="readonly", width=10).grid(row=0, column=1, padx=10, pady=5, sticky="w")

    tk.Label(form_frame, text="Username:", bg="#FFFFFF").grid(row=0, column=2, padx=10, pady=5, sticky="e")
    tk.Entry(form_frame, textvariable=var_username, width=20).grid(row=0, column=3, padx=10, pady=5, sticky="w")

    tk.Label(form_frame, text="Password:", bg="#FFFFFF").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    tk.Entry(form_frame, textvariable=var_password, width=20).grid(row=1, column=1, padx=10, pady=5, sticky="w")

    tk.Label(form_frame, text="Họ tên:", bg="#FFFFFF").grid(row=1, column=2, padx=10, pady=5, sticky="e")
    tk.Entry(form_frame, textvariable=var_fullname, width=25).grid(row=1, column=3, padx=10, pady=5, sticky="w")

    # Các nút chức năng
    btn_frame = tk.Frame(form_frame, bg="#FFFFFF")
    btn_frame.grid(row=2, column=0, columnspan=4, pady=10)

    def load_students():
        for row in tree_student.get_children():
            tree_student.delete(row)
        students = fetch_data("SELECT * FROM students")
        for s in students:
            tree_student.insert("", "end", values=(s['student_id'], s['username'], s['password_hash'], s['full_name']))

    def clear_form():
        var_id.set("")
        var_username.set("")
        var_password.set("")
        var_fullname.set("")

    def add_student():
        username = var_username.get().strip()
        password = var_password.get().strip()
        fullname = var_fullname.get().strip()
        
        if not username or not password or not fullname:
            messagebox.showwarning("Lỗi", "Vui lòng nhập đủ thông tin!")
            return
            
        success = execute_query(
            "INSERT INTO students (username, password_hash, full_name) VALUES (%s, %s, %s)",
            (username, password, fullname)
        )
        if success:
            messagebox.showinfo("Thành công", "Đã thêm học viên mới!")
            clear_form()
            load_students()

    def update_student():
        s_id = var_id.get()
        if not s_id:
            messagebox.showwarning("Lỗi", "Vui lòng chọn học viên để sửa!")
            return
            
        username = var_username.get().strip()
        password = var_password.get().strip()
        fullname = var_fullname.get().strip()
        
        success = execute_query(
            "UPDATE students SET username=%s, password_hash=%s, full_name=%s WHERE student_id=%s",
            (username, password, fullname, s_id)
        )
        if success:
            messagebox.showinfo("Thành công", "Cập nhật thành công!")
            clear_form()
            load_students()

    def delete_student():
        s_id = var_id.get()
        if not s_id:
            messagebox.showwarning("Lỗi", "Vui lòng chọn học viên để xóa!")
            return
            
        if messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa học viên ID={s_id}?"):
            success = execute_query("DELETE FROM students WHERE student_id=%s", (s_id,))
            if success:
                messagebox.showinfo("Thành công", "Đã xóa học viên!")
                clear_form()
                load_students()

    tk.Button(btn_frame, text="Thêm", bg="#28A745", fg="white", width=10, command=add_student).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Sửa", bg="#FFC107", fg="black", width=10, command=update_student).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Xóa", bg="#DC3545", fg="white", width=10, command=delete_student).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Clear", bg="#0D2340", fg="white", width=10, command=clear_form).pack(side="left", padx=5)

    # ==========================================
    # 2. BẢNG DANH SÁCH & LỊCH SỬ THI
    # ==========================================
    bottom_frame = tk.Frame(main_frame, bg="#F8F9FB")
    bottom_frame.pack(side="bottom", fill="both", expand=True, padx=10, pady=10)
    
    # 2.1 Bảng Học viên
    list_frame = tk.LabelFrame(bottom_frame, text="Danh Sách Học Viên", bg="#FFFFFF")
    list_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))

    columns = ("ID", "Username", "Password", "Họ Tên")
    tree_student = ttk.Treeview(list_frame, columns=columns, show="headings", height=10)
    for col in columns:
        tree_student.heading(col, text=col)
    
    tree_student.column("ID", width=50, anchor="center")
    tree_student.column("Username", width=100)
    tree_student.column("Password", width=100)
    tree_student.column("Họ Tên", width=150)
    
    tree_student.pack(fill="both", expand=True, padx=5, pady=5)

    # 2.2 Bảng Lịch sử thi
    history_frame = tk.LabelFrame(bottom_frame, text="Lịch Sử Thi (Chọn 1 học viên để xem)", bg="#FFFFFF")
    history_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))

    hist_cols = ("Môn Học", "Độ Khó", "Số Câu", "Điểm", "Thời Gian")
    tree_history = ttk.Treeview(history_frame, columns=hist_cols, show="headings", height=10)
    for col in hist_cols:
        tree_history.heading(col, text=col)
        
    tree_history.column("Môn Học", width=100)
    tree_history.column("Độ Khó", width=70)
    tree_history.column("Số Câu", width=60, anchor="center")
    tree_history.column("Điểm", width=60, anchor="center")
    tree_history.column("Thời Gian", width=120)
    
    tree_history.pack(fill="both", expand=True, padx=5, pady=5)

    def load_history(student_id):
        for row in tree_history.get_children():
            tree_history.delete(row)
            
        query = """
            SELECT s.subject_name, q.difficulty_level, q.total_questions, q.score, q.started_at
            FROM quiz_attempts q
            JOIN subjects s ON q.subject_id = s.subject_id
            WHERE q.student_id = %s
            ORDER BY q.started_at DESC
        """
        history = fetch_data(query, (student_id,))
        for h in history:
            score = float(h['score'])
            if score > 10:
                score = round(score / 10, 1)
            else:
                score = round(score, 1)
                
            tree_history.insert("", "end", values=(
                h['subject_name'], 
                h['difficulty_level'], 
                h['total_questions'], 
                score, 
                h['started_at']
            ))

    def on_student_select(event):
        selected = tree_student.selection()
        if selected:
            item = tree_student.item(selected[0], "values")
            var_id.set(item[0])
            var_username.set(item[1])
            var_password.set(item[2])
            var_fullname.set(item[3])
            
            # Load lịch sử thi
            load_history(item[0])

    tree_student.bind("<<TreeviewSelect>>", on_student_select)

    # Khởi tạo dữ liệu
    load_students()
