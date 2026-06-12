"""
pages/Lam_Bai_Thi.py — Trang làm bài thi trắc nghiệm
- Bước 5.1: Form chọn Môn học & Độ khó
- Bước 5.2: Query lấy N câu hỏi ngẫu nhiên
- Bước 5.3: Hiển thị câu hỏi & xáo trộn đáp án
- Bước 5.4: Nút Nộp bài -> So sánh đáp án
- Bước 5.5: Hiển thị kết quả (success/error)
- Bước 5.6: Lưu vào quiz_attempts & attempt_details
"""

import random
import streamlit as st
import sys
import os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from shared.db import fetch_data, execute_query

# TEST MODE
if os.environ.get("TEST_MODE") == "1":
    if "student_id" not in st.session_state:
        st.session_state.student_id = 1
    try:
        rows = fetch_data("SELECT * FROM students WHERE student_id = %s", (1,))
        if rows:
            st.session_state.student = rows[0]
        else:
            st.session_state.student = {"full_name": "Test User"}
    except Exception:
        st.session_state.student = {"full_name": "Test User"}


st.set_page_config(
    page_title="Làm Bài Thi — Hệ Thống Trắc Nghiệm",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@300;400;500;600;700;800&family=Playfair+Display:wght@700&display=swap');

html, body, [class*="css"] { font-family: 'Be Vietnam Pro', sans-serif; color: #000000; font-size: 1rem; }

.stApp { background: #ffffff; min-height: 100vh; color: #000000; }

#MainMenu, header, footer { visibility: hidden; }
[data-testid="collapsedControl"] {display: none;}
section[data-testid="stSidebar"] {display: none;}
.block-container { padding-top: 2rem !important; }
.hero-header { text-align: center; padding: 2rem 1rem 1.2rem; animation: fadeInDown 0.7s ease; }
.hero-icon { font-size: 3rem; display: block; margin-bottom: 0.4rem; }

.hero-title { font-family: 'Playfair Display', serif; font-size: 2.2rem; font-weight: 700; color: #FF0000; margin: 0; text-shadow: 1px 1px 3px rgba(255,255,255,0.7); }
.hero-subtitle { font-size: 1rem; color: #0f172a; margin-top: 0.4rem; }

.stSelectbox > div > div > input,
.stTextInput > div > div > input { 
    background: #FFFFFF !important; 
    border: 2px solid #1d4ed8 !important; 
    border-radius: 10px !important; 
    color: #000000 !important; 
    font-family: 'Be Vietnam Pro', sans-serif !important; 
    font-size: 1.05rem !important; 
    padding: 0.7rem 0.9rem !important; 
    transition: border 0.25s, box-shadow 0.25s; 
}
.stSelectbox > div > div > input:focus,
.stTextInput > div > div > input:focus { 
    border-color: #1d4ed8 !important; 
    box-shadow: 0 0 0 3px rgba(29,78,216,0.2) !important; 
}
.stSelectbox > label,
.stTextInput > label { 
    color: #000000 !important; 
    font-size: 0.95rem !important; 
    font-weight: 600 !important; 
    letter-spacing: 0.05em !important; 
    text-transform: uppercase !important; 
}
.stSlider > div > div > input,
.stSlider [role="slider"] {
    height: 22px !important;
}
.stSlider > label {
    color: #000000 !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
}

.stRadio label, .stRadio span, .stRadio div {
    color: #000000 !important;
}
.stRadio label { font-weight: 600 !important; font-size: 1rem !important; }

/* FIX 2: Bỏ ép buộc màu xanh ở mọi nút để type primary/secondary có tác dụng */
.stButton > button { 
    width: 100%; 
    border-radius: 10px !important; 
    font-family: 'Be Vietnam Pro', sans-serif !important; 
    font-weight: 700 !important; 
    font-size: 0.95rem !important; 
    padding: 0.7rem 1.5rem !important; 
    cursor: pointer !important; 
    transition: opacity 0.2s, transform 0.15s !important; 
    letter-spacing: 0.03em; 
    box-shadow: 0 4px 6px rgba(0,0,0,0.1); 
}
.stButton > button:hover { 
    opacity: 0.9 !important; 
    transform: translateY(-2px) !important; 
    box-shadow: 0 6px 12px rgba(0,0,0,0.15); 
}

.question-card { 
    background: #f8fafc; 
    border: 2px solid #1d4ed8; 
    border-radius: 15px; 
    padding: 1.5rem; 
    margin: 1.5rem 0; 
    box-shadow: 0 8px 20px rgba(0,0,0,0.06);
}
.question-text { 
    color: #0f172a; 
    font-size: 1rem; 
    font-weight: 700; 
    margin-bottom: 1rem; 
    line-height: 1.6;
}
.question-counter { 
    font-size: 0.9rem; 
    color: #475569; 
    margin-bottom: 0.5rem; 
}

.progress-container { 
    background: rgba(255,255,255,0.1); 
    border-radius: 10px; 
    height: 8px; 
    margin: 1rem 0; 
    overflow: hidden;
}
.progress-bar { 
    background: linear-gradient(90deg, #10b981, #0ea5e9); 
    height: 100%; 
    transition: width 0.3s ease;
}

@keyframes fadeInDown { from { opacity: 0; transform: translateY(-20px); } to { opacity: 1; transform: translateY(0); } }
@keyframes fadeInUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
</style>    
""", unsafe_allow_html=True)

# FIX 1: Dùng get() để lấy an toàn, tránh lỗi AttributeError khi refresh trang
is_logged_in = st.session_state.get("logged_in", False)
current_student = st.session_state.get("student", None)

if not is_logged_in or current_student is None:
    st.warning("⚠️ Vui lòng đăng nhập trước khi làm bài thi.")
    if st.button("🔐 Quay lại Đăng nhập"):
        st.switch_page("app.py")
    st.stop()


def get_subjects():
    result = fetch_data("SELECT subject_id, subject_name FROM subjects ORDER BY subject_name", ())
    return result if result else []

def get_difficulty_levels():
    return ["Dễ", "Trung bình", "Khó"]

def get_questions(subject_id: int, difficulty: str, num_questions: int = 10):
    diff_map = {"Dễ": "EASY", "Trung bình": "MEDIUM", "Khó": "HARD"}
    db_diff = diff_map.get(difficulty, difficulty)
    query = f"""
    SELECT question_id, question_content, option_a, option_b, option_c, option_d, correct_option
    FROM questions
    WHERE subject_id = %s AND difficulty_level = %s
    ORDER BY RAND()
    LIMIT {int(num_questions)}
    """
    result = fetch_data(query, (subject_id, db_diff))
    return result if result else []

def shuffle_options(options: dict):
    option_list = [
        ("A", options["option_a"]),
        ("B", options["option_b"]),
        ("C", options["option_c"]),
        ("D", options["option_d"]),
    ]
    random.shuffle(option_list)
    return option_list

def save_quiz_attempt(student_id: int, subject_id: int, difficulty: str, score: int, total: int):
    try:
        percent = round((score / total) * 10, 2) if total > 0 else 0.0
    except Exception:
        percent = 0.0
    diff_map = {"Dễ": "EASY", "Trung bình": "MEDIUM", "Khó": "HARD"}
    db_diff = diff_map.get(difficulty, difficulty)
    query = """
    INSERT INTO quiz_attempts (student_id, subject_id, difficulty_level, total_questions, correct_answers, score, started_at)
    VALUES (%s, %s, %s, %s, %s, %s, NOW())
    """
    return execute_query(query, (student_id, subject_id, db_diff, total, score, percent), return_lastrowid=True)

def save_attempt_detail(attempt_id: int, question_id: int, selected_option: str, is_correct: bool):
    query = """
    INSERT INTO attempt_details (attempt_id, question_id, student_choice, is_correct)
    VALUES (%s, %s, %s, %s)
    """
    return execute_query(query, (attempt_id, question_id, selected_option, 1 if is_correct else 0))


if "quiz_phase" not in st.session_state:
    st.session_state.quiz_phase = "setup"
if "selected_subject" not in st.session_state:
    st.session_state.selected_subject = None
if "selected_difficulty" not in st.session_state:
    st.session_state.selected_difficulty = None
if "questions_list" not in st.session_state:
    st.session_state.questions_list = []
if "question_shuffled_map" not in st.session_state:
    st.session_state.question_shuffled_map = {}
if "current_question_index" not in st.session_state:
    st.session_state.current_question_index = 0
if "bookmarked_questions" not in st.session_state:
    st.session_state.bookmarked_questions = []
if "user_answers" not in st.session_state:
    st.session_state.user_answers = {}
if "quiz_results" not in st.session_state:
    st.session_state.quiz_results = []


if st.session_state.quiz_phase == "setup":
    st.markdown("""
    <div class="hero-header">
        <span class="hero-icon">📝</span>
        <h1 class="hero-title">Làm Bài Thi</h1>
    </div>
    """, unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown('<div style="font-size: 1.2rem; font-weight: 700; color: #0f172a; margin-bottom: 1rem;">⚙️ Chọn Môn Học & Độ Khó</div>', unsafe_allow_html=True)

        subjects = get_subjects()
        if not subjects:
            st.error("❌ Không có môn học nào trong hệ thống.")
            st.stop()

        subject_names = [s['subject_name'] for s in subjects]
        subject_dict = {s['subject_name']: s['subject_id'] for s in subjects}

        selected_subject_name = st.selectbox("Chọn Môn Học", subject_names, key="setup_subject")
        selected_difficulty = st.selectbox("Chọn Độ Khó", get_difficulty_levels(), key="setup_difficulty")
        num_questions = st.slider("Số câu hỏi", min_value=5, max_value=30, value=10, step=5)

        st.markdown("<br>", unsafe_allow_html=True)

        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("🏠 Quay về Trang chủ", type="secondary", use_container_width=True):
                st.switch_page("app.py")
        with col_btn2:
            if st.button("🚀 Bắt Đầu Làm Bài", type="primary", use_container_width=True):
                subject_id = subject_dict[selected_subject_name]
                questions = get_questions(subject_id, selected_difficulty, num_questions)

                if not questions:
                    st.error(f"❌ Không có câu hỏi nào cho môn '{selected_subject_name}' độ khó '{selected_difficulty}'.")
                else:
                    st.session_state.selected_subject = (subject_id, selected_subject_name)
                    st.session_state.selected_difficulty = selected_difficulty
                    st.session_state.questions_list = questions
                    st.session_state.user_answers = {}
                    st.session_state.question_shuffled_map = {}
                    st.session_state.current_question_index = 0
                    st.session_state.bookmarked_questions = []
                    st.session_state.quiz_phase = "taking"
                    st.session_state.has_saved = False
                    st.rerun()


elif st.session_state.quiz_phase == "taking":
    subject_id, subject_name = st.session_state.selected_subject
    difficulty = st.session_state.selected_difficulty
    questions = st.session_state.questions_list
    total_q = len(questions)
    current_idx = st.session_state.current_question_index
    current_idx = max(0, min(current_idx, total_q - 1))
    st.session_state.current_question_index = current_idx

    # HEADER với title, subject, submit button
    header_col1, header_col2, header_col3 = st.columns([2, 2, 1])
    with header_col1:
        st.markdown(f"""
        <div style="padding: 1rem 0;">
            <h1 style="font-family: 'Playfair Display', serif; color: #FF0000; font-size: 2rem; margin: 0; font-weight: 700;">Làm Bài Trắc Nghiệm</h1>
        </div>
        """, unsafe_allow_html=True)
    
    with header_col2:
        st.markdown(f"""
        <div style="padding: 1.3rem 0;">
            <div style="color: #0f172a; font-size: 1.05rem; font-weight: 600;">📚 {subject_name}</div>
            <div style="color: #475569; font-size: 0.9rem; margin-top: 0.3rem;">Độ khó: {difficulty}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with header_col3:
        if st.button("📤 Nộp Bài", key="header_submit", type="primary", use_container_width=True):
            st.session_state.quiz_phase = "results"
            st.rerun()

    current_question = questions[current_idx]
    question_id = current_question['question_id']
    question_text = current_question['question_content']
    options_dict = {
        "option_a": current_question['option_a'],
        "option_b": current_question['option_b'],
        "option_c": current_question['option_c'],
        "option_d": current_question['option_d'],
    }

    if question_id not in st.session_state.question_shuffled_map:
        st.session_state.question_shuffled_map[question_id] = shuffle_options(options_dict)
    shuffled_options = st.session_state.question_shuffled_map[question_id]

    st.markdown("<hr style='border: 1px solid #e2e8f0; margin: 1rem 0;'>", unsafe_allow_html=True)

    # 2-PANEL LAYOUT
    left_col, right_col = st.columns([2.5, 1])

    # ===== LEFT PANEL (LỚN) - QUESTION & ANSWERS & PIN =====
    with left_col:
        with st.container(border=True):
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 1rem; margin-bottom: 1rem;">
                <div>
                    <div class="question-counter">Câu {current_idx + 1}/{total_q}</div>
                    <div class="question-text">{question_text}</div>
                </div>
                <div style="color: #475569; font-size: 0.9rem; font-weight: 600;">{subject_name}</div>
            </div>
            """, unsafe_allow_html=True)

            current_answer = st.session_state.user_answers.get(question_id)

            # FIX 2: Tự động đổi type của nút thành primary nếu đáp án đó đang được chọn
            for opt_key, opt_text in shuffled_options:
                btn_text = f"{opt_key}: {opt_text}"
                btn_type = "primary" if current_answer == opt_key else "secondary"
                
                if st.button(btn_text, key=f"ans_{question_id}_{opt_key}", type=btn_type, use_container_width=True):
                    st.session_state.user_answers[question_id] = opt_key
                    st.rerun()

            is_bookmarked = question_id in st.session_state.bookmarked_questions
            pin_label = "📌 Bỏ Ghim" if is_bookmarked else "📍 Ghim Câu Hỏi"

            if st.button(pin_label, key=f"pin_{question_id}", type="secondary", use_container_width=True):
                if is_bookmarked:
                    st.session_state.bookmarked_questions.remove(question_id)
                else:
                    st.session_state.bookmarked_questions.append(question_id)
                st.rerun()

    # ===== RIGHT PANEL (NHỎ) - QUESTION GRID + STATS + NAV BUTTONS =====
    answered_count = len([v for v in st.session_state.user_answers.values() if v])
    with right_col:
        with st.container(border=True):
            st.markdown("<div style='font-size: 1rem; font-weight: 700; color: #0f172a; margin-bottom: 1rem;'>Bảng câu hỏi</div>", unsafe_allow_html=True)

        # FIX 3: Hiển thị bảng câu hỏi chuẩn với Streamlit type và thêm dấu tick ✅
        for row_start in range(0, total_q, 5):
            cols = st.columns(5)
            for col_index in range(5):
                idx = row_start + col_index
                if idx >= total_q:
                    cols[col_index].write("")
                    continue
                qid = questions[idx]['question_id']
                is_current = (idx == current_idx)
                is_pinned = qid in st.session_state.bookmarked_questions
                is_answered = qid in st.session_state.user_answers
                
                btn_type = "primary" if is_current else "secondary"
                btn_label = f"{idx + 1} ✅" if is_answered and not is_current else str(idx + 1)

                button_label = f"{idx + 1}"
                if is_pinned:
                    button_label += " 📌"
                
                if cols[col_index].button(btn_label, key=f"q_nav_{idx}", type=btn_type, use_container_width=True):
                    st.session_state.current_question_index = idx
                    st.rerun()

        st.markdown(f"""
        <div style="background: #f8fafc; border-radius: 16px; padding: 1rem; display: flex; justify-content: space-between; align-items: center; margin: 1rem 0;">
            <div>
                <div style="color: #475569; font-size: 0.9rem;">Đã trả lời</div>
            </div>
            <div style="color: #1d4ed8; font-size: 1.75rem; font-weight: 800;">{answered_count}/{total_q}</div>
        </div>
        """, unsafe_allow_html=True)

        nav_col1, nav_col2 = st.columns(2)
        with nav_col1:
            if st.button("Trước", key="prev_q", type="secondary", disabled=(current_idx == 0), use_container_width=True):
                st.session_state.current_question_index = current_idx - 1
                st.rerun()
        with nav_col2:
            if st.button("Tiếp", key="next_q", type="secondary", disabled=(current_idx == total_q - 1), use_container_width=True):
                st.session_state.current_question_index = current_idx + 1
                st.rerun()


elif st.session_state.quiz_phase == "results":
    subject_id, subject_name = st.session_state.selected_subject
    difficulty = st.session_state.selected_difficulty
    questions = st.session_state.questions_list
    user_answers = st.session_state.user_answers
    total_q = len(questions)

    st.markdown("""
    <div class="hero-header">
        <span class="hero-icon">📊</span>
        <h1 class="hero-title">Kết Quả Bài Thi</h1>
    </div>
    """, unsafe_allow_html=True)

    score = 0
    results_list = []

    for question in questions:
        question_id = question['question_id']
        question_text = question['question_content']
        correct_option = question['correct_option']

        if question_id in user_answers:
            selected = user_answers[question_id]
            is_correct = (selected == correct_option)
            if is_correct:
                score += 1
            results_list.append({
                "question_id": question_id,
                "question_text": question_text,
                "selected": selected,
                "correct": correct_option,
                "is_correct": is_correct
            })
        else:
            results_list.append({
                "question_id": question_id,
                "question_text": question_text,
                "selected": "—",
                "correct": correct_option,
                "is_correct": False
            })

    st.markdown(f"""
    <div style="background: #ffffff; border: 2px solid #1d4ed8; border-radius: 15px; padding: 1.5rem; text-align: center;">
        <div style="font-size: 2.5rem;">🎯</div>
        <div style="color: #0f172a; font-size: 1.8rem; font-weight: 800; margin: 0.8rem 0;">{score}/{total_q}</div>
        <div style="color: #0f172a; font-weight: 700; font-size: 1.1rem; margin-top: 0.5rem;">Bạn trả lời đúng {score} trên {total_q} câu</div>
    </div>
    """, unsafe_allow_html=True)

    with st.spinner("Đang lưu kết quả..."):
        student_id = st.session_state.student['student_id']
        # KIỂM TRA Ổ KHÓA: Nếu chưa lưu (False) thì mới cho lưu
        if st.session_state.get('has_saved', False) == False:
            attempt_id = save_quiz_attempt(student_id, subject_id, difficulty, score, total_q)
            if attempt_id:
                for result in results_list:
                    short_selected = str(result["selected"])[:250]
                    save_attempt_detail(attempt_id, result["question_id"], short_selected, result["is_correct"])
                
                # KHÓA LẠI: Đánh dấu là đã lưu rồi, cấm lưu thêm!
                st.session_state.has_saved = True
                st.success("✅ Kết quả đã được lưu thành công vào Sổ Điểm!")
        else:
            # Nếu đã lưu rồi thì web chỉ cần hiện thông báo xanh thôi, không đụng vào Database nữa
            st.success("✅ Kết quả đã được lưu thành công vào Sổ Điểm!")

    st.markdown("<h3 style='color: #0f172a; text-align: center; margin-top: 1.5rem;'>📋 Chi Tiết Bài Làm</h3>", unsafe_allow_html=True)

    for idx, result in enumerate(results_list):
        status_icon = "✅" if result["is_correct"] else "❌"
        status_text = "Đúng" if result["is_correct"] else "Sai"
        border_color = "#34d399" if result["is_correct"] else "#ef4444"
        is_pinned = result["question_id"] in st.session_state.bookmarked_questions
        pinned_label = "<span style='color: #b45309; font-weight: 700;'>📌 Đã ghim</span>" if is_pinned else ""

        st.markdown(f"""
        <div style="background: #ffffff; border: 2px solid #1d4ed8; border-left: 4px solid {border_color}; border-radius: 15px; padding: 1.5rem; margin: 1rem 0;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <div style="color: #475569; font-size: 0.85rem;">Câu {idx + 1}</div>
                <div style="color: #0f172a; font-weight: 700;">{status_icon} {status_text}</div>
            </div>
            <div style="color: #0f172a; margin: 0.8rem 0; line-height: 1.5;">
                <strong>Câu hỏi:</strong> {result['question_text']}
            </div>
            <div style="color: #0f172a; margin-bottom: 0.5rem;">
                <strong>Bạn chọn:</strong> {result['selected']}
            </div>
            <div style="color: #0f172a; font-weight: 600;">
                <strong>Đáp án đúng:</strong> {result['correct']}
            </div>
        </div>
        """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🏠 Quay lại Trang chủ", type="secondary", use_container_width=True):
            st.session_state.quiz_phase = "setup"
            st.session_state.user_answers = {}
            st.switch_page("app.py")
    with col2:
        if st.button("📚 Làm bài khác", type="primary", use_container_width=True):
            st.session_state.quiz_phase = "setup"
            st.session_state.user_answers = {}
            st.rerun()
