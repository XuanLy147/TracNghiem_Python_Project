"""
Module: pages/On_Tap_Flashcard.py
Mô tả: Trang hỗ trợ người dùng ôn tập câu hỏi theo phương pháp Flashcard (lật thẻ ghi nhớ).
Chức năng: Lọc bộ câu hỏi ngẫu nhiên theo môn học, độ khó, lật thẻ xem đáp án.
"""

import streamlit as st
import sys
import os
import random

# Thêm đường dẫn để import từ thư mục shared
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from shared.db import fetch_data

# ===================== CẤU HÌNH TRANG =====================
st.set_page_config(
    page_title="Ôn Tập Flashcard — Hệ Thống Trắc Nghiệm",
    page_icon="📇",
    layout="wide",
    initial_sidebar_state="collapsed",
)

import base64
def set_bg_hack(main_bg):
    try:
        ext = 'png' if main_bg.lower().endswith('.png') else 'jpeg'
        with open(main_bg, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: linear-gradient(rgba(255, 255, 255, 0.85), rgba(255, 255, 255, 0.85)), url(data:image/{ext};base64,{encoded_string});
                background-size: cover;
                background-position: center top;
                background-attachment: fixed;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    except:
        pass

# Cài đặt hình nền từ thư mục img
img_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "img", "background2.jpg")
set_bg_hack(img_path)

if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("⚠️ Vui lòng đăng nhập ở trang chủ để truy cập tính năng ôn tập!")
    if st.button("🏠 Quay về Trang chủ", type="primary"):
        st.switch_page("app.py")
    st.stop()

# ===================== CSS ĐỊNH DẠNG FLASHCARD =====================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Be Vietnam Pro', sans-serif; color: #000000; }
#MainMenu, header, footer { visibility: hidden; }
[data-testid="collapsedControl"] {display: none;}
section[data-testid="stSidebar"] {display: none;}

/* Thẻ Flashcard */
.flashcard-container {
    perspective: 1000px;
    width: 100%;
    max-width: 700px;
    margin: 0 auto 2rem auto;
}

.flashcard {
    background: #ffffff;
    border: 3px solid #1d4ed8;
    border-radius: 20px;
    box-shadow: 0 10px 25px rgba(29, 78, 216, 0.15);
    min-height: 350px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 2.5rem;
    text-align: center;
    transition: transform 0.6s, background-color 0.3s;
    cursor: default;
}

.flashcard.flipped {
    background: #f0fdf4;
    border-color: #16a34a;
}

.card-title {
    font-size: 0.9rem;
    color: #64748b;
    text-transform: uppercase;
    font-weight: 700;
    letter-spacing: 1px;
    margin-bottom: 1.5rem;
}

.card-content {
    font-size: 1.4rem;
    font-weight: 600;
    color: #0f172a;
    line-height: 1.6;
}

.card-content-answer {
    font-size: 1.5rem;
    font-weight: 700;
    color: #16a34a;
    margin-top: 1rem;
}

.card-options {
    margin-top: 2rem;
    text-align: left;
    width: 100%;
    font-size: 1.1rem;
    color: #475569;
}

.stButton > button {
    border-radius: 10px !important;
    font-weight: 600 !important;
}

.hero-header { text-align: center; padding: 2rem 1rem 1.2rem; }
.hero-title { font-size: 2.5rem; font-weight: 800; color: #1d4ed8; margin: 0; }
.hero-subtitle { font-size: 1.1rem; color: #475569; margin-top: 0.5rem; }
</style>
""", unsafe_allow_html=True)

# ===================== TRUY XUẤT DỮ LIỆU (DATABASE ACCESS) =====================
def get_subjects():
    result = fetch_data("SELECT subject_id, subject_name FROM subjects ORDER BY subject_name")
    return result if result else []

def get_questions(subject_id: int, difficulty: str, limit: int = 20):
    diff_map = {"Dễ": "EASY", "Trung bình": "MEDIUM", "Khó": "HARD"}
    db_diff = diff_map.get(difficulty, difficulty)
    
    query = """
    SELECT question_id, question_content, option_a, option_b, option_c, option_d, correct_option
    FROM questions
    WHERE subject_id = %s AND difficulty_level = %s
    ORDER BY RAND()
    LIMIT %s
    """
    result = fetch_data(query, (subject_id, db_diff, limit))
    return result if result else []

# ===================== QUẢN LÝ TRẠNG THÁI (SESSION STATE) =====================
if "fc_phase" not in st.session_state:
    st.session_state.fc_phase = "setup"
if "fc_questions" not in st.session_state:
    st.session_state.fc_questions = []
if "fc_index" not in st.session_state:
    st.session_state.fc_index = 0
if "fc_flipped" not in st.session_state:
    st.session_state.fc_flipped = False

# ===================== GIAO DIỆN CẤU HÌNH BÀI ÔN TẬP =====================
if st.session_state.fc_phase == "setup":
    st.markdown("""
    <div class="hero-header">
        <h1 class="hero-title">Chế Độ Ôn Tập Flashcard</h1>
        <div class="hero-subtitle">Lật thẻ để xem đáp án - Học nhanh, nhớ lâu!</div>
    </div>
    """, unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown('<h4>Tùy Chỉnh Bộ Thẻ</h4>', unsafe_allow_html=True)

        subjects = get_subjects()
        if not subjects:
            st.error("❌ Không có môn học nào trong hệ thống.")
            st.stop()

        subject_names = [s['subject_name'] for s in subjects]
        subject_dict = {s['subject_name']: s['subject_id'] for s in subjects}
        
        # Cấu hình bộ lọc tìm kiếm môn học
        search_query = st.text_input("Tìm kiếm môn học", placeholder="Ví dụ: Toán lớp 2, Ngữ pháp...")
        
        if search_query:
            filtered_subject_names = [name for name in subject_names if search_query.lower() in name.lower()]
        else:
            filtered_subject_names = subject_names
            
        if not filtered_subject_names:
            st.warning("Không tìm thấy môn học nào phù hợp với từ khóa.")
            selected_subject_name = st.selectbox("Chọn Môn Học", ["Không có kết quả"], disabled=True, key="setup_subject")
        else:
            selected_subject_name = st.selectbox("Chọn Môn Học", filtered_subject_names, key="setup_subject")
        # Kết thúc cấu hình bộ lọc

        sel_diff = st.selectbox("Chọn Độ Khó", ["Dễ", "Trung bình", "Khó"])
        num_cards = st.slider("Số lượng thẻ ôn tập", min_value=5, max_value=50, value=20, step=5)

        st.markdown("<br>", unsafe_allow_html=True)

        col_b1, col_b2 = st.columns(2)
        with col_b1:
            if st.button("Quay về Trang chủ", type="secondary", use_container_width=True):
                st.switch_page("app.py")
        with col_b2:
            if st.button("Bắt Đầu Ôn Tập", type="primary", use_container_width=True):
                if not filtered_subject_names:
                    st.error("❌ Vui lòng chọn một môn học hợp lệ trước khi bắt đầu.")
                else:
                    subject_id = subject_dict[selected_subject_name]
                    questions = get_questions(subject_id, sel_diff, num_cards)

                    if not questions:
                        st.error(f"❌ Không tìm thấy câu hỏi nào cho độ khó '{sel_diff}'.")
                    else:
                        st.session_state.fc_questions = questions
                        st.session_state.fc_index = 0
                        st.session_state.fc_flipped = False
                        st.session_state.fc_phase = "study"
                        st.rerun()

# ===================== GIAO DIỆN HỌC TẬP (FLASHCARD VIEW) =====================
elif st.session_state.fc_phase == "study":
    questions = st.session_state.fc_questions
    total_q = len(questions)
    curr_idx = st.session_state.fc_index

    if curr_idx >= total_q or curr_idx < 0:
        st.session_state.fc_index = 0
        curr_idx = 0

    current_q = questions[curr_idx]
    is_flipped = st.session_state.fc_flipped

    # Thanh điều hướng và hiển thị tiến độ
    top1, top2, top3 = st.columns([1, 2, 1])
    with top1:
        if st.button("Thoát", use_container_width=True):
            st.session_state.fc_phase = "setup"
            st.rerun()
    with top2:
        st.markdown(f"<div style='text-align: center; font-size: 1.2rem; font-weight: 700; color: #1d4ed8; padding-top: 5px;'>Thẻ {curr_idx + 1} / {total_q}</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Khối hiển thị nội dung thẻ Flashcard
    options_html = ""
    if not is_flipped:
        # Giao diện mặt trước (Câu hỏi)
        st.markdown(f'<div class="flashcard-container">'
                    f'<div class="flashcard">'
                    f'<div class="card-content" style="font-size: 1.8rem;">{current_q["question_content"]}</div>'
                    f'</div></div>', unsafe_allow_html=True)
    else:
        # Giao diện mặt sau (Đáp án)
        correct_letter = current_q['correct_option']
        mapping = {
            'A': current_q['option_a'],
            'B': current_q['option_b'],
            'C': current_q['option_c'],
            'D': current_q['option_d']
        }
        correct_text = mapping.get(correct_letter, "Không xác định")

        st.markdown(f'<div class="flashcard-container">'
                    f'<div class="flashcard flipped">'
                    f'<div class="card-content" style="font-size: 1.2rem; opacity: 0.8;">{current_q["question_content"]}</div>'
                    f'<div class="card-content-answer" style="font-size: 1.8rem;">{correct_text}</div>'
                    f'</div></div>', unsafe_allow_html=True)

    # Cụm phím điều khiển tương tác thẻ
    c1, c2, c3, c4, c5 = st.columns([1.5, 1, 2, 1, 1.5])
    
    with c2:
        if st.button("⬅️", disabled=(curr_idx == 0), use_container_width=True):
            st.session_state.fc_index -= 1
            st.session_state.fc_flipped = False
            st.rerun()

    with c3:
        flip_label = "Úp thẻ lại" if is_flipped else "Lật thẻ"
        btn_type = "secondary" if is_flipped else "primary"
        if st.button(flip_label, type=btn_type, use_container_width=True):
            st.session_state.fc_flipped = not st.session_state.fc_flipped
            st.rerun()

    with c4:
        if st.button("➡️", disabled=(curr_idx == total_q - 1), use_container_width=True):
            st.session_state.fc_index += 1
            st.session_state.fc_flipped = False
            st.rerun()
