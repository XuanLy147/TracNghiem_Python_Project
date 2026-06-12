import tkinter as tk
from tkinter import ttk, messagebox
from shared.db import fetch_data, execute_query

def show_question_management(parent):
    for widget in parent.winfo_children():
        widget.destroy()

    main_frame = tk.Frame(parent, bg="#F8F9FB")
    main_frame.pack(fill="both", expand=True)

    # ==========================================
    # 1. KHUNG NHẬP LIỆU (Câu hỏi)
    # ==========================================
    form_frame = tk.LabelFrame(main_frame, text="Thông Tin Câu Hỏi", bg="#FFFFFF", font=("Arial", 10, "bold"), fg="#0D2340")
    form_frame.pack(side="top", fill="x", padx=10, pady=5)

    var_qid = tk.StringVar()
    var_subject = tk.StringVar() # Lưu ID môn học
    var_difficulty = tk.StringVar()
    var_content = tk.StringVar()
    var_opt_a = tk.StringVar()
    var_opt_b = tk.StringVar()
    var_opt_c = tk.StringVar()
    var_opt_d = tk.StringVar()
    var_correct = tk.StringVar()

    # Load subjects for combobox
    subjects_data = fetch_data("SELECT subject_id, subject_name FROM subjects")
    subject_map = {f"{s['subject_id']} - {s['subject_name']}": s['subject_id'] for s in subjects_data}
    subject_names = list(subject_map.keys())

    tk.Label(form_frame, text="ID:", bg="#FFFFFF").grid(row=0, column=0, padx=5, pady=2, sticky="e")
    tk.Entry(form_frame, textvariable=var_qid, state="readonly", width=5).grid(row=0, column=1, padx=5, pady=2, sticky="w")

    tk.Label(form_frame, text="Môn học:", bg="#FFFFFF").grid(row=0, column=2, padx=5, pady=2, sticky="e")
    cb_subject = ttk.Combobox(form_frame, values=subject_names, width=25, state="readonly")
    cb_subject.grid(row=0, column=3, padx=5, pady=2, sticky="w")
    
    tk.Label(form_frame, text="Độ khó:", bg="#FFFFFF").grid(row=0, column=4, padx=5, pady=2, sticky="e")
    cb_difficulty = ttk.Combobox(form_frame, values=["EASY", "MEDIUM", "HARD"], width=10, state="readonly")
    cb_difficulty.grid(row=0, column=5, padx=5, pady=2, sticky="w")

    tk.Label(form_frame, text="Câu hỏi:", bg="#FFFFFF").grid(row=1, column=0, padx=5, pady=2, sticky="e")
    tk.Entry(form_frame, textvariable=var_content, width=80).grid(row=1, column=1, columnspan=5, padx=5, pady=2, sticky="w")

    tk.Label(form_frame, text="Đáp án A:", bg="#FFFFFF").grid(row=2, column=0, padx=5, pady=2, sticky="e")
    tk.Entry(form_frame, textvariable=var_opt_a, width=30).grid(row=2, column=1, columnspan=2, padx=5, pady=2, sticky="w")

    tk.Label(form_frame, text="Đáp án B:", bg="#FFFFFF").grid(row=2, column=3, padx=5, pady=2, sticky="e")
    tk.Entry(form_frame, textvariable=var_opt_b, width=30).grid(row=2, column=4, columnspan=2, padx=5, pady=2, sticky="w")

    tk.Label(form_frame, text="Đáp án C:", bg="#FFFFFF").grid(row=3, column=0, padx=5, pady=2, sticky="e")
    tk.Entry(form_frame, textvariable=var_opt_c, width=30).grid(row=3, column=1, columnspan=2, padx=5, pady=2, sticky="w")

    tk.Label(form_frame, text="Đáp án D:", bg="#FFFFFF").grid(row=3, column=3, padx=5, pady=2, sticky="e")
    tk.Entry(form_frame, textvariable=var_opt_d, width=30).grid(row=3, column=4, columnspan=2, padx=5, pady=2, sticky="w")

    tk.Label(form_frame, text="Đáp án đúng:", bg="#FFFFFF").grid(row=4, column=0, padx=5, pady=2, sticky="e")
    cb_correct = ttk.Combobox(form_frame, values=["A", "B", "C", "D"], width=5, state="readonly")
    cb_correct.grid(row=4, column=1, padx=5, pady=2, sticky="w")

    btn_frame = tk.Frame(form_frame, bg="#FFFFFF")
    btn_frame.grid(row=5, column=0, columnspan=6, pady=5)

    def load_questions():
        for row in tree_q.get_children():
            tree_q.delete(row)
            
        sub_filter = cb_filter_subject.get()
        diff_filter = cb_filter_diff.get()
        
        query = "SELECT * FROM questions WHERE 1=1"
        params = []
        
        if sub_filter and sub_filter != "Tất cả":
            query += " AND subject_id = %s"
            params.append(subject_map[sub_filter])
        if diff_filter and diff_filter != "Tất cả":
            query += " AND difficulty_level = %s"
            params.append(diff_filter)
            
        questions = fetch_data(query, tuple(params))
        for q in questions:
            tree_q.insert("", "end", values=(
                q['question_id'], q['subject_id'], q['difficulty_level'], 
                q['question_content'], q['option_a'], q['option_b'], 
                q['option_c'], q['option_d'], q['correct_option']
            ))

    def clear_form():
        var_qid.set("")
        cb_subject.set("")
        cb_difficulty.set("")
        var_content.set("")
        var_opt_a.set("")
        var_opt_b.set("")
        var_opt_c.set("")
        var_opt_d.set("")
        cb_correct.set("")

    def get_form_data():
        sub_str = cb_subject.get()
        if not sub_str: return None
        return {
            'subject_id': subject_map[sub_str],
            'difficulty': cb_difficulty.get(),
            'content': var_content.get().strip(),
            'opt_a': var_opt_a.get().strip(),
            'opt_b': var_opt_b.get().strip(),
            'opt_c': var_opt_c.get().strip(),
            'opt_d': var_opt_d.get().strip(),
            'correct': cb_correct.get()
        }

    def add_question():
        data = get_form_data()
        if not data or not all(data.values()):
            messagebox.showwarning("Lỗi", "Vui lòng nhập đủ thông tin!")
            return
            
        success = execute_query(
            "INSERT INTO questions (subject_id, difficulty_level, question_content, option_a, option_b, option_c, option_d, correct_option) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (data['subject_id'], data['difficulty'], data['content'], data['opt_a'], data['opt_b'], data['opt_c'], data['opt_d'], data['correct'])
        )
        if success:
            messagebox.showinfo("Thành công", "Đã thêm câu hỏi!")
            clear_form()
            load_questions()
        else:
            messagebox.showerror("Lỗi", "Thêm câu hỏi thất bại! Vui lòng kiểm tra lại nội dung.")

    def update_question():
        q_id = var_qid.get()
        if not q_id:
            messagebox.showwarning("Lỗi", "Vui lòng chọn câu hỏi để sửa!")
            return
            
        data = get_form_data()
        if not data or not all(data.values()):
            messagebox.showwarning("Lỗi", "Vui lòng nhập đủ thông tin!")
            return
            
        success = execute_query(
            "UPDATE questions SET subject_id=%s, difficulty_level=%s, question_content=%s, option_a=%s, option_b=%s, option_c=%s, option_d=%s, correct_option=%s WHERE question_id=%s",
            (data['subject_id'], data['difficulty'], data['content'], data['opt_a'], data['opt_b'], data['opt_c'], data['opt_d'], data['correct'], q_id)
        )
        if success:
            messagebox.showinfo("Thành công", "Cập nhật thành công!")
            clear_form()
            load_questions()
        else:
            messagebox.showerror("Lỗi", "Cập nhật thất bại! Vui lòng kiểm tra lại thông tin.")

    def delete_question():
        q_id = var_qid.get()
        if not q_id:
            messagebox.showwarning("Lỗi", "Vui lòng chọn câu hỏi để xóa!")
            return
            
        if messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa câu hỏi ID={q_id}?"):
            success = execute_query("DELETE FROM questions WHERE question_id=%s", (q_id,))
            if success:
                messagebox.showinfo("Thành công", "Đã xóa câu hỏi!")
                clear_form()
                load_questions()
            else:
                messagebox.showerror("Lỗi", "Xóa thất bại! Vui lòng thử lại.")

    tk.Button(btn_frame, text="Thêm", bg="#28A745", fg="white", width=10, command=add_question).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Sửa", bg="#FFC107", fg="black", width=10, command=update_question).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Xóa", bg="#DC3545", fg="white", width=10, command=delete_question).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Clear", bg="#0D2340", fg="white", width=10, command=clear_form).pack(side="left", padx=5)

    # ==========================================
    # 2. BẢNG DANH SÁCH & LỌC
    # ==========================================
    filter_frame = tk.Frame(main_frame, bg="#F8F9FB")
    filter_frame.pack(fill="x", padx=10, pady=5)
    
    tk.Label(filter_frame, text="Lọc theo môn:", bg="#F8F9FB").pack(side="left", padx=5)
    cb_filter_subject = ttk.Combobox(filter_frame, values=["Tất cả"] + subject_names, state="readonly", width=20)
    cb_filter_subject.pack(side="left", padx=5)
    cb_filter_subject.current(0)
    
    tk.Label(filter_frame, text="Độ khó:", bg="#F8F9FB").pack(side="left", padx=5)
    cb_filter_diff = ttk.Combobox(filter_frame, values=["Tất cả", "EASY", "MEDIUM", "HARD"], state="readonly", width=10)
    cb_filter_diff.pack(side="left", padx=5)
    cb_filter_diff.current(0)
    
    tk.Button(filter_frame, text="Lọc", bg="#17A2B8", fg="white", command=load_questions).pack(side="left", padx=10)

    list_frame = tk.LabelFrame(main_frame, text="Danh Sách Câu Hỏi", bg="#FFFFFF")
    list_frame.pack(side="bottom", fill="both", expand=True, padx=10, pady=5)

    columns = ("ID", "Sub_ID", "Độ khó", "Câu hỏi", "A", "B", "C", "D", "Đáp án")
    tree_q = ttk.Treeview(list_frame, columns=columns, show="headings", height=10)
    for col in columns:
        tree_q.heading(col, text=col)
        
    tree_q.column("ID", width=30, anchor="center")
    tree_q.column("Sub_ID", width=50, anchor="center")
    tree_q.column("Độ khó", width=60, anchor="center")
    tree_q.column("Câu hỏi", width=250)
    tree_q.column("A", width=80)
    tree_q.column("B", width=80)
    tree_q.column("C", width=80)
    tree_q.column("D", width=80)
    tree_q.column("Đáp án", width=50, anchor="center")
    
    tree_q.pack(fill="both", expand=True, padx=5, pady=5)

    def on_q_select(event):
        selected = tree_q.selection()
        if selected:
            item = tree_q.item(selected[0], "values")
            var_qid.set(item[0])
            
            # Map sub_id back to string
            sub_id = int(item[1])
            for k, v in subject_map.items():
                if v == sub_id:
                    cb_subject.set(k)
                    break
                    
            cb_difficulty.set(item[2])
            var_content.set(item[3])
            var_opt_a.set(item[4])
            var_opt_b.set(item[5])
            var_opt_c.set(item[6])
            var_opt_d.set(item[7])
            cb_correct.set(item[8])

    tree_q.bind("<<TreeviewSelect>>", on_q_select)

    load_questions()
