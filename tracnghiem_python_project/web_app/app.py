"""
app.py — Trang chính: Đăng nhập & Dashboard học sinh
Chạy bằng: streamlit run web_app/app.py
"""

import streamlit as st
import tempfile
import sys
import os

# Thêm thư mục gốc vào path để import shared
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from shared.db import fetch_data 

# ===================== CẤU HÌNH TRANG =====================
st.set_page_config(
    page_title="Hệ Thống Trắc Nghiệm",
    page_icon="📝",
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
                background-image: linear-gradient(rgba(255, 255, 255, 0.7), rgba(255, 255, 255, 0.7)), url(data:image/{ext};base64,{encoded_string});
                background-size: cover;
                background-position: center top;
                background-attachment: fixed;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    except:
        pass # Nếu không tìm thấy file ảnh thì bỏ qua

# Cài đặt hình nền từ file bg_image.jpg nằm trong thư mục 'img' (ngang cấp với web_app)
set_bg_hack(os.path.join(os.path.dirname(os.path.dirname(__file__)), "img", "background1.jpg"))

# ===================== CSS CUSTOM =====================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Be Vietnam Pro', sans-serif; }

/* Nền tảng trang web sáng sủa, hiện đại */
.stApp { background-color: #F8FAFC; }

/* Ẩn các thành phần mặc định không cần thiết */
#MainMenu, header, footer { visibility: hidden; }
header { background-color: transparent !important; }

/* === TRANG ĐĂNG NHẬP === */
.login-left-panel {
    background: linear-gradient(135deg, #a855f7 0%, #6366f1 100%);
    border-radius: 24px;
    padding: 3rem 2rem;
    color: white;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    box-shadow: 0 10px 25px rgba(99, 102, 241, 0.2);
}
.login-title { font-size: 2.8rem; font-weight: 800; line-height: 1.2; margin-bottom: 1rem; }
.login-subtitle { font-size: 1.1rem; opacity: 0.9; line-height: 1.5; }

/* === DASHBOARD === */
/* Topbar */
.topbar-container {
    display: flex; justify-content: space-between; align-items: center;
    padding-bottom: 1rem; border-bottom: 2px solid #E2E8F0; margin-bottom: 2rem;
}
.topbar-logo { font-size: 1.5rem; font-weight: 800; color: #4F46E5; margin: 0; }
.topbar-user { font-weight: 600; color: #475569; display: flex; align-items: center; gap: 0.5rem; }

/* Banner Chào mừng */
.welcome-banner {
    background: linear-gradient(to right, #4F46E5, #0EA5E9);
    border-radius: 16px; padding: 2rem; color: white; margin-bottom: 2rem;
    box-shadow: 0 4px 15px rgba(79, 70, 229, 0.2);
}
.welcome-name { font-size: 1.8rem; font-weight: 800; margin-bottom: 0.5rem; }
.welcome-sub { font-size: 1rem; opacity: 0.9; }

/* Thống kê */
.stat-container { background: rgba(255,255,255,0.2); border-radius: 12px; padding: 1rem; text-align: center; backdrop-filter: blur(4px); }
.stat-num { font-size: 1.8rem; font-weight: 800; }
.stat-label { font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; opacity: 0.9; }

/* Menu Cards (Đã được nâng cấp để làm nút bấm) */
.menu-card {
    background: #FFFFFF; border: 2px solid #E2E8F0; border-radius: 16px;
    padding: 2.5rem 1.5rem; text-align: center; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    transition: all 0.25s ease; height: 100%; cursor: pointer;
}
.menu-card:hover { 
    transform: translateY(-5px); 
    box-shadow: 0 15px 25px -5px rgba(79, 70, 229, 0.15); 
    border-color: #4F46E5; 
}
.menu-icon { font-size: 3rem; margin-bottom: 1rem; transition: transform 0.2s; }
.menu-card:hover .menu-icon { transform: scale(1.1); }
.menu-title { font-weight: 800; color: #1E293B; font-size: 1.2rem; margin-bottom: 0.5rem; transition: color 0.2s; }
.menu-card:hover .menu-title { color: #4F46E5; }
.menu-desc { color: #64748B; font-size: 0.95rem; }

/* Upload Vùng Nét Đứt */
.upload-zone {
    border: 2px dashed #94A3B8; border-radius: 16px; padding: 2rem;
    background-color: #F8FAFC; text-align: center; margin-top: 2rem;
}

/* Custom Inputs & Buttons */
.stTextInput > div > div > input {
    border: 2px solid #E2E8F0 !important; border-radius: 10px !important;
    padding: 0.75rem 1rem !important; transition: all 0.2s ease;
}
.stTextInput > div > div > input:focus { border-color: #4F46E5 !important; box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1) !important; }
.stButton > button {
    width: 100%; background: #4F46E5 !important; color: white !important;
    border: none !important; border-radius: 10px !important; font-weight: 600 !important;
    padding: 0.75rem 1rem !important; transition: all 0.2s !important;
}
.stButton > button:hover { background: #4338CA !important; transform: translateY(-2px) !important; }
.stButton.logout-btn > button { background: #F1F5F9 !important; color: #475569 !important; padding: 0.4rem 0.8rem !important; border-radius: 8px !important; }
.stButton.logout-btn > button:hover { background: #E2E8F0 !important; color: #EF4444 !important; }

/* ---- CUSTOM FOOTER STARTUP ---- */
.startup-footer {
    position: relative;
    background: #ffffff;
    border-top: 3px solid #2563eb;
    border-radius: 12px 12px 0 0;
    padding: 30px 20px 20px 20px;
    box-shadow: 0 -4px 12px rgba(0,0,0,0.05);
    text-align: center;
    margin-top: 25vh; /* Đẩy footer xuống xa một chút để người dùng phải lướt xuống mới thấy */
}
.footer-title {
    color: #2563eb; /* Màu Indigo nhấn -> ĐIỂM NHẤN */
    font-size: 1.1rem;
    font-weight: 700;
    margin-bottom: 5px;
}
.footer-tagline {
    color: #6b7280;
    font-size: 0.85rem;
    margin-bottom: 15px;
}
.footer-links {
    color: #9ca3af;
    font-size: 0.8rem;
    margin-bottom: 0;
}
.footer-highlight {
    color: #2563eb; /* Màu Indigo nhấn cho tên nhóm -> ĐIỂM NHẤN */
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)


# ===================== HELPER =====================
def do_login(username: str, password: str):
    """Xác thực học sinh. Trả về dict học sinh hoặc None."""
    rows = fetch_data("SELECT * FROM students WHERE username = %s", (username,))
    if not rows:
        return None
    
    student = rows[0]
    # So sánh trực tiếp mật khẩu
    if student["password_hash"] == password:
        return student
    return None


# ===================== SESSION STATE =====================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "student" not in st.session_state:
    st.session_state.student = None


# ===================== DASHBOARD (sau đăng nhập) =====================
# ===================== DASHBOARD (sau đăng nhập) =====================
def show_dashboard():
    student = st.session_state.student
    student_id = student['student_id']

    # --- 0. TRUY VẤN DỮ LIỆU THỐNG KÊ TỪ DATABASE ---
    total_attempts = 0
    avg_score = 0.0
    total_subjects = 0
    
    try:
        stats_query = """
            SELECT 
                COUNT(attempt_id) as total_attempts,
                AVG(score) as avg_score,
                COUNT(DISTINCT subject_id) as total_subjects
            FROM quiz_attempts
            WHERE student_id = %s
        """
        result = fetch_data(stats_query, (student_id,))
        
        if result and result[0]['total_attempts'] > 0:
            total_attempts = result[0]['total_attempts']
            raw_avg = result[0]['avg_score']
            if raw_avg is not None:
                avg = float(raw_avg)
                avg_score = round(avg, 1)
            total_subjects = result[0]['total_subjects']
    except Exception as e:
        # Bỏ qua lỗi nếu bảng quiz_attempts chưa tồn tại hoặc bị sai cấu trúc
        pass

    # --- 1. TOPBAR ---
    top1, top2, top3 = st.columns([5, 2, 1])
    with top1:
        st.markdown("<h2 class='topbar-logo'>Hệ Thống Trắc Nghiệm</h2>", unsafe_allow_html=True)
    with top2:
        st.markdown(f"<div class='topbar-user' style='justify-content: flex-end; margin-top: 10px;'>👤 {student['full_name']}</div>", unsafe_allow_html=True)
    with top3:
        st.markdown('<div class="logout-btn">', unsafe_allow_html=True)
        if st.button("Đăng xuất", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.student = None
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # Đưa nội dung vào khu vực hẹp hơn ở giữa
    main_col1, main_content, main_col3 = st.columns([1, 8, 1])
    
    with main_content:
        # --- 2. BANNER & THỐNG KÊ (Đã truyền biến dữ liệu thật) ---
        st.markdown(f"""
        <div class="welcome-banner">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;">
                <div>
                    <div class="welcome-name">👋 Xin chào, {student['full_name']}!</div>
                    <div class="welcome-sub">Chúc bạn có một phiên học tập hiệu quả hôm nay.</div>
                </div>
                <div style="display: flex; gap: 1rem;">
                    <div class="stat-container"><div class="stat-num">{total_attempts}</div><div class="stat-label">Lần thi</div></div>
                    <div class="stat-container"><div class="stat-num">{avg_score}</div><div class="stat-label">Điểm TB</div></div>
                    <div class="stat-container"><div class="stat-num">{total_subjects}</div><div class="stat-label">Môn học</div></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<h4 style='color: #1E293B; margin-bottom: 1rem;'>Góc Học Tập Của Bạn</h4>", unsafe_allow_html=True)

        # --- 3. MENU CHỨC NĂNG ---
        m1, m2, m3 = st.columns(3, gap="medium")
        
        with m1:
            st.markdown("""
                <div class="menu-card" style="margin-bottom: 15px; cursor: default;">
                    <div class="menu-icon">✍️</div>
                    <div class="menu-title">Làm Bài Thi</div>
                    <div class="menu-desc">Kiểm tra kiến thức với tính điểm</div>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Vào Thi", key="btn_thi", type="primary", use_container_width=True):
                st.switch_page("pages/Lam_Bai_Thi.py")
            
        with m2:
            st.markdown("""
                <div class="menu-card" style="margin-bottom: 15px; cursor: default;">
                    <div class="menu-icon">📇</div>
                    <div class="menu-title">Flashcard Ôn Tập</div>
                    <div class="menu-desc">Học nhanh qua thẻ nhớ lật</div>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Học Từ Vựng", key="btn_fc", type="primary", use_container_width=True):
                st.switch_page("pages/On_Tap_Flashcard.py")

        with m3:
            st.markdown("""
                <div class="menu-card" style="margin-bottom: 15px; cursor: default;">
                    <div class="menu-icon">📊</div>
                    <div class="menu-title">Lịch Sử Thi</div>
                    <div class="menu-desc">Xem lại điểm & đáp án cũ</div>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Xem Lịch Sử", key="btn_su", type="primary", use_container_width=True):
                st.switch_page("pages/Lich_Su_Lam_Bai.py")

        # (Đã di chuyển chức năng Thêm Excel sang Admin App)

        # ---- FOOTER ĐƯỢC DESIGN LẠI ( WOW-FACTOR ) ----
        st.markdown("""
            <div class="startup-footer">
                <div class="footer-title">EduQuest System</div>
                <div class="footer-tagline">Hệ thống Quản lý và Hỗ trợ luyện thi trắc nghiệm trực tuyến.</div>
                <div class="footer-links">
                    © 2026 | Thiết kế & Phát triển bởi nhóm <span class="footer-highlight">Rắn Độc</span>.<br>
                    <a href="https://youtu.be/dQw4w9WgXcQ?si=3smXtkiH5-f5ZdRd" target="_blank" style="color: #2563eb; text-decoration: underline; font-weight: 500; transition: color 0.2s;" onmouseover="this.style.color='#1d4ed8'" onmouseout="this.style.color='#2563eb'">Về chúng tôi</a> | 
                    <a href="https://youtu.be/dQw4w9WgXcQ?si=3smXtkiH5-f5ZdRd" target="_blank" style="color: #2563eb; text-decoration: underline; font-weight: 500; transition: color 0.2s;" onmouseover="this.style.color='#1d4ed8'" onmouseout="this.style.color='#2563eb'">Liên hệ</a>
                </div>
            </div>
        """, unsafe_allow_html=True)

# ===================== TRANG ĐĂNG NHẬP =====================
def show_login():
    st.markdown("<div style='margin-top: 5vh;'></div>", unsafe_allow_html=True)
    spacer1, col_left, col_right, spacer2 = st.columns([1, 4, 3, 1], gap="large")

    with col_left:
        st.markdown("""
        <div class="login-left-panel">
            <div class="login-title">Hệ Thống<br>Trắc Nghiệm</div>
            <div class="login-subtitle">Luyện tập thông minh, nâng cao kiến thức mỗi ngày. Đăng nhập để tiếp tục lộ trình học tập của bạn.</div>
        </div>
        """, unsafe_allow_html=True)

    with col_right:
        st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True) 
        st.markdown("<h3 style='color: #1E293B; font-weight: 800; margin-bottom: 1.5rem;'>Đăng nhập</h3>", unsafe_allow_html=True)
        
        with st.form("login_form", clear_on_submit=False):
            username = st.text_input("Tên đăng nhập", placeholder="Nhập tên đăng nhập của bạn...")
            password = st.text_input("Mật khẩu", type="password", placeholder="Nhập mật khẩu...")
            st.markdown("<br>", unsafe_allow_html=True)
            submitted = st.form_submit_button("Đăng nhập →")

        if submitted:
            if not username or not password:
                st.warning("⚠️ Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu.")
            else:
                with st.spinner("Đang xác thực..."):
                    student = do_login(username.strip(), password.strip())
                if student:
                    st.session_state.logged_in = True
                    st.session_state.student = student
                    st.rerun()
                else:
                    st.error("❌ Tên đăng nhập hoặc mật khẩu không đúng.")

        st.markdown("""
        <div style="text-align: center; margin-top: 1.5rem; font-size: 0.9rem; color: #64748B;">
            Chưa có tài khoản? <a href="/Dang_Ki" target="_self" style="color: #4F46E5; font-weight: 700; text-decoration: none;">Đăng ký ngay</a>
        </div>
        """, unsafe_allow_html=True)

# ===================== MAIN =====================
if st.session_state.logged_in:
    show_dashboard()
else:
    show_login()
