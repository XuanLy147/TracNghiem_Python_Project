import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
from shared.db import fetch_data, execute_query
from utils.excel_handler import import_questions_from_excel

def show_subject_management(parent):
    # Xóa các widget cũ
    for widget in parent.winfo_children():
        widget.destroy()

    # Container chính
    main_frame = tk.Frame(parent, bg="#F8F9FB")
    main_frame.pack(fill="both", expand=True)

    # ==========================================
    # 1. KHUNG NHẬP LIỆU (Môn học)
    # ==========================================
    form_frame = tk.LabelFrame(main_frame, text="Thông Tin Môn Học", bg="#FFFFFF", font=("Arial", 10, "bold"), fg="#0D2340")
    form_frame.pack(side="top", fill="x", padx=10, pady=10)

    var_id = tk.StringVar()
    var_name = tk.StringVar()
    var_desc = tk.StringVar()

    tk.Label(form_frame, text="ID:", bg="#FFFFFF").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    tk.Entry(form_frame, textvariable=var_id, state="readonly", width=10).grid(row=0, column=1, padx=10, pady=5, sticky="w")

    tk.Label(form_frame, text="Tên môn học:", bg="#FFFFFF").grid(row=0, column=2, padx=10, pady=5, sticky="e")
    tk.Entry(form_frame, textvariable=var_name, width=30).grid(row=0, column=3, padx=10, pady=5, sticky="w")

    tk.Label(form_frame, text="Mô tả:", bg="#FFFFFF").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    tk.Entry(form_frame, textvariable=var_desc, width=55).grid(row=1, column=1, columnspan=3, padx=10, pady=5, sticky="w")

    # Các nút chức năng
    btn_frame = tk.Frame(form_frame, bg="#FFFFFF")
    btn_frame.grid(row=2, column=0, columnspan=4, pady=10)

    def load_subjects():
        for row in tree_subject.get_children():
            tree_subject.delete(row)
        subjects = fetch_data("SELECT * FROM subjects")
        for s in subjects:
            tree_subject.insert("", "end", values=(s['subject_id'], s['subject_name'], s['description']))

    def clear_form():
        var_id.set("")
        var_name.set("")
        var_desc.set("")

    def add_subject():
        name = var_name.get().strip()
        desc = var_desc.get().strip()
        if not name:
            messagebox.showwarning("Lỗi", "Vui lòng nhập tên môn học!")
            return
        success = execute_query("INSERT INTO subjects (subject_name, description) VALUES (%s, %s)", (name, desc))
        if success:
            messagebox.showinfo("Thành công", "Đã thêm môn học mới!")
            clear_form()
            load_subjects()

    def update_subject():
        s_id = var_id.get()
        if not s_id:
            messagebox.showwarning("Lỗi", "Vui lòng chọn môn học để sửa!")
            return
        name = var_name.get().strip()
        desc = var_desc.get().strip()
        success = execute_query("UPDATE subjects SET subject_name=%s, description=%s WHERE subject_id=%s", (name, desc, s_id))
        if success:
            messagebox.showinfo("Thành công", "Cập nhật môn học thành công!")
            clear_form()
            load_subjects()

    def delete_subject():
        s_id = var_id.get()
        if not s_id:
            messagebox.showwarning("Lỗi", "Vui lòng chọn môn học để xóa!")
            return
        if messagebox.askyesno("Xác nhận", f"Xóa môn học ID={s_id} sẽ xóa TOÀN BỘ câu hỏi thuộc môn này. Tiếp tục?"):
            success = execute_query("DELETE FROM subjects WHERE subject_id=%s", (s_id,))
            if success:
                messagebox.showinfo("Thành công", "Đã xóa môn học!")
                clear_form()
                load_subjects()

    def import_excel():
        file_path = filedialog.askopenfilename(
            title="Chọn file Excel",
            filetypes=(("Excel files", "*.xlsx *.xls"), ("All files", "*.*"))
        )
        if file_path:
            success = import_questions_from_excel(file_path)
            if success:
                messagebox.showinfo("Thành công", "Đã import dữ liệu từ Excel thành công!")
            else:
                messagebox.showerror("Lỗi", "Import thất bại. Vui lòng kiểm tra lại cấu trúc file Excel.")

    tk.Button(btn_frame, text="Thêm", bg="#28A745", fg="white", width=10, command=add_subject).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Sửa", bg="#FFC107", fg="black", width=10, command=update_subject).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Xóa", bg="#DC3545", fg="white", width=10, command=delete_subject).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Clear", bg="#6C757D", fg="white", width=10, command=clear_form).pack(side="left", padx=5)
    
    # Nút import riêng biệt
    tk.Button(btn_frame, text="📂 Import Câu Hỏi (Excel)", bg="#17A2B8", fg="white", width=25, command=import_excel).pack(side="left", padx=20)

    # ==========================================
    # 2. BẢNG DANH SÁCH MÔN HỌC
    # ==========================================
    list_frame = tk.LabelFrame(main_frame, text="Danh Sách Môn Học", bg="#FFFFFF")
    list_frame.pack(side="bottom", fill="both", expand=True, padx=10, pady=10)

    columns = ("ID", "Tên Môn Học", "Mô Tả")
    tree_subject = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
    for col in columns:
        tree_subject.heading(col, text=col)
    
    tree_subject.column("ID", width=50, anchor="center")
    tree_subject.column("Tên Môn Học", width=200)
    tree_subject.column("Mô Tả", width=400)
    
    tree_subject.pack(fill="both", expand=True, padx=5, pady=5)

    def on_subject_select(event):
        selected = tree_subject.selection()
        if selected:
            item = tree_subject.item(selected[0], "values")
            var_id.set(item[0])
            var_name.set(item[1])
            var_desc.set(item[2])

    tree_subject.bind("<<TreeviewSelect>>", on_subject_select)

    load_subjects()
