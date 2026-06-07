"""
app.py — Trang chính: Đăng nhập & Dashboard học sinh
Chạy bằng: streamlit run web_app/app.py
"""

import streamlit as st
import sys
import os

# Thêm thư mục gốc vào path để import shared
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from shared.db import fetch_data 

# ===================== CẤU HÌNH TRANG =====================
st.set_page_config(
    page_title="Hệ Thống Trắc Nghiệm",
    page_icon="📝",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ===================== CSS CUSTOM =====================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@300;400;500;600;700;800&family=Playfair+Display:wght@700&display=swap');

html, body, [class*="css"] { font-family: 'Be Vietnam Pro', sans-serif; }

/* MÀU NỀN TRANG WEB #4ECDC4 */
.stApp { background: #4ECDC4; min-height: 100vh; }

#MainMenu, footer { visibility: hidden; }
header { background-color: transparent !important; }
.block-container { padding-top: 2rem !important; }
.hero-header { text-align: center; padding: 2.5rem 1rem 1.5rem; animation: fadeInDown 0.7s ease; }

/* MÀU CHỮ TIÊU ĐỀ #FF0000 */
.hero-title { font-family: 'Playfair Display', serif; font-size: 2.4rem; font-weight: 700; color: #FF0000; margin: 0; line-height: 1.2; text-shadow: 1px 1px 3px rgba(255,255,255,0.7); }
.hero-subtitle { font-size: 0.95rem; color: #e0f2fe; margin-top: 0.5rem; letter-spacing: 0.04em; }

/* 1. LÀM ĐẬM BO VIỀN FORM ĐĂNG NHẬP (Lên 2px và đậm hơn) */
.login-card { background: rgba(255,255,255,0.15); border: 2px solid rgba(255,255,255,0.7); border-radius: 20px; padding: 2.2rem 2rem; backdrop-filter: blur(12px); box-shadow: 0 10px 25px rgba(0,0,0,0.15); animation: fadeInUp 0.7s ease 0.15s both; max-width: 440px; margin: 0 auto; }
.card-title { font-size: 1.15rem; font-weight: 700; color: #ffffff; margin-bottom: 1.4rem; display: flex; align-items: center; gap: 0.5rem; }

/* 2. LÀM ĐẬM BO VIỀN Ô NHẬP LIỆU (Đổi sang xám đậm #94A3B8, dày 2px) */
.stTextInput > div > div > input { background: #FFFFFF !important; border: 2px solid #94A3B8 !important; border-radius: 10px !important; color: #000000 !important; font-family: 'Be Vietnam Pro', sans-serif !important; font-size: 0.92rem !important; padding: 0.65rem 0.9rem !important; transition: border 0.25s, box-shadow 0.25s; }
.stTextInput > div > div > input:focus { border-color: #0ea5e9 !important; box-shadow: 0 0 0 3px rgba(14,165,233,0.3) !important; outline: none !important; }
.stTextInput > label { color: #f8fafc !important; font-size: 0.82rem !important; font-weight: 600 !important; letter-spacing: 0.05em !important; text-shadow: 0px 1px 2px rgba(0,0,0,0.2); }

.stButton > button { width: 100%; background: linear-gradient(135deg, #0ea5e9, #6366f1) !important; color: white !important; border: none !important; border-radius: 10px !important; font-family: 'Be Vietnam Pro', sans-serif !important; font-weight: 700 !important; font-size: 0.95rem !important; padding: 0.7rem 1.5rem !important; cursor: pointer !important; transition: opacity 0.2s, transform 0.15s !important; letter-spacing: 0.03em; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
.stButton > button:hover { opacity: 0.9 !important; transform: translateY(-2px) !important; box-shadow: 0 6px 12px rgba(0,0,0,0.15); }
.stButton > button:active { transform: translateY(0px) !important; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
.stAlert { border-radius: 10px !important; font-family: 'Be Vietnam Pro', sans-serif !important; }
.divider { display: flex; align-items: center; gap: 0.8rem; margin: 1rem 0; color: #e0f2fe; font-size: 0.8rem; }
.divider::before, .divider::after { content: ''; flex: 1; height: 1px; background: rgba(255,255,255,0.4); }
.nav-link { text-align: center; margin-top: 1rem; font-size: 0.88rem; color: #f1f5f9; }
.nav-link a { color: #0f172a; text-decoration: none; font-weight: 800; background: #ffffff; padding: 2px 8px; border-radius: 4px; }

/* CHỈNH LẠI BO VIỀN CHO CÁC THẺ Ở TRANG DASHBOARD */
.welcome-banner { background: rgba(255,255,255,0.15); border: 2px solid rgba(255,255,255,0.6); border-radius: 16px; padding: 1.5rem 2rem; margin-bottom: 1.5rem; animation: fadeInDown 0.5s ease; backdrop-filter: blur(10px); }
.welcome-name { font-size: 1.5rem; font-weight: 800; color: #ffffff; }
.welcome-sub { color: #e0f2fe; font-size: 0.9rem; margin-top: 0.2rem; }
.stat-card { background: rgba(255,255,255,0.15); border: 2px solid rgba(255,255,255,0.5); border-radius: 14px; padding: 1.2rem 1rem; text-align: center; backdrop-filter: blur(5px); }
.stat-num { font-size: 2rem; font-weight: 800; color: #ffffff; text-shadow: 0 2px 4px rgba(0,0,0,0.1); }
.stat-label { font-size: 0.8rem; color: #e0f2fe; margin-top: 0.2rem; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600;}
.menu-card { background: rgba(255,255,255,0.15); border: 2px solid rgba(255,255,255,0.5); border-radius: 14px; padding: 1.5rem 1.2rem; text-align: center; transition: background 0.2s, transform 0.2s; cursor: pointer; backdrop-filter: blur(5px); }
.menu-card:hover { background: rgba(255,255,255,0.25); transform: translateY(-3px); }
.menu-icon { font-size: 2rem; margin-bottom: 0.5rem; }
.menu-title { font-weight: 700; color: #ffffff; font-size: 0.95rem; }
.menu-desc { color: #e0f2fe; font-size: 0.8rem; margin-top: 0.25rem; }
@keyframes fadeInDown { from { opacity: 0; transform: translateY(-20px); } to { opacity: 1; transform: translateY(0); } }
@keyframes fadeInUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
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
def show_dashboard():
    student = st.session_state.student

    st.markdown(f"""
    <div class="welcome-banner">
        <div class="welcome-name">👋 Xin chào, {student['full_name']}!</div>
        <div class="welcome-sub">Chào mừng bạn quay lại hệ thống trắc nghiệm.</div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1: st.markdown('<div class="stat-card"><div class="stat-num">—</div><div class="stat-label">Lần thi</div></div>', unsafe_allow_html=True)
    with c2: st.markdown('<div class="stat-card"><div class="stat-num">—</div><div class="stat-label">Điểm TB</div></div>', unsafe_allow_html=True)
    with c3: st.markdown('<div class="stat-card"><div class="stat-num">—</div><div class="stat-label">Môn học</div></div>', unsafe_allow_html=True)

    st.markdown("<br><strong style='color:white;'>📌 Chức năng</strong>", unsafe_allow_html=True)

    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown('<div class="menu-card"><div class="menu-icon">✍️</div><div class="menu-title">Làm Bài Thi</div><div class="menu-desc">Chọn môn & độ khó</div></div>', unsafe_allow_html=True)
        if st.button("Vào Thi", key="btn_thi", use_container_width=True):
            st.switch_page("pages/Lam_Bai_Thi.py")
    with m2:
        st.markdown('<div class="menu-card" style="margin-bottom: 10px;"><div class="menu-icon">📊</div><div class="menu-title">Lịch Sử Thi</div><div class="menu-desc">Xem kết quả các lần thi</div></div>', unsafe_allow_html=True)
        if st.button("Xem Lịch Sử 🕒", key="btn_su", use_container_width=True):
            st.switch_page("pages/Lich_Su_Lam_Bai.py")
    with m3: st.markdown('<div class="menu-card"><div class="menu-icon">👤</div><div class="menu-title">Tài Khoản</div><div class="menu-desc">Thông tin cá nhân</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.info("💡 Dùng thanh menu bên trái để điều hướng đến các trang.", icon="ℹ️")

    if st.button("🚪 Đăng xuất"):
        st.session_state.logged_in = False
        st.session_state.student = None
        st.rerun()


# ===================== TRANG ĐĂNG NHẬP =====================
def show_login():
    st.markdown("""
    <div class="hero-header">
        <h1 class="hero-title">Hệ Thống Trắc Nghiệm</h1>
    </div>
    """, unsafe_allow_html=True)

    
    with st.form("login_form", clear_on_submit=False):
        username = st.text_input("Tên đăng nhập", placeholder="Nhập tên đăng nhập...")
        password = st.text_input("Mật khẩu", type="password", placeholder="Nhập mật khẩu...")
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
                st.success(f"✅ Chào mừng, {student['full_name']}!")
                st.rerun()
            else:
                st.error("❌ Tên đăng nhập hoặc mật khẩu không đúng.")

    st.markdown('<div class="divider">hoặc</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="nav-link">
        Chưa có tài khoản? <a href="/Dang_Ki" target="_self">Đăng ký ngay</a>
    </div>
    </div>
    """, unsafe_allow_html=True)

# ===================== MAIN =====================
if st.session_state.logged_in:
    show_dashboard()
else:
    show_login()