"""
pages/1_Đăng_Ký.py — Trang đăng ký tài khoản học sinh
"""

import re
import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from shared.db import fetch_data, execute_query

# ===================== CẤU HÌNH TRANG =====================
st.set_page_config(
    page_title="Đăng Ký — Hệ Thống Trắc Nghiệm",
    page_icon="📋",
    layout="wide", # Sử dụng layout wide để chia 2 cột giống trang Đăng nhập
    initial_sidebar_state="collapsed",
)

# ===================== CSS ĐỒNG BỘ VỚI TRANG ĐĂNG NHẬP =====================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Be Vietnam Pro', sans-serif; }

/* Nền tảng trang web sáng sủa, hiện đại */
.stApp { background-color: #F8FAFC; }

/* Ẩn các thành phần mặc định không cần thiết */
#MainMenu, header, footer { visibility: hidden; }

/* Bảng điều khiển bên trái (Gradient) */
.register-left-panel {
    background: linear-gradient(135deg, #10b981 0%, #0ea5e9 100%); /* Màu xanh ngọc/biển tạo cảm giác mới mẻ cho trang đăng ký */
    border-radius: 24px;
    padding: 3rem 2rem;
    color: white;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    box-shadow: 0 10px 25px rgba(14, 165, 233, 0.2);
}
.register-title { font-size: 2.8rem; font-weight: 800; line-height: 1.2; margin-bottom: 1rem; }
.register-subtitle { font-size: 1.1rem; opacity: 0.9; line-height: 1.5; }

/* Custom Inputs & Buttons */
.stTextInput > div > div > input {
    border: 2px solid #E2E8F0 !important; border-radius: 10px !important;
    padding: 0.75rem 1rem !important; transition: all 0.2s ease; background: #FFFFFF !important;
}
.stTextInput > div > div > input:focus { border-color: #0EA5E9 !important; box-shadow: 0 0 0 3px rgba(14, 165, 233, 0.1) !important; }
.stTextInput > label { color: #475569 !important; font-size: 0.85rem !important; font-weight: 600 !important; }

/* Nút Đăng ký */
.stButton > button {
    width: 100%; background: #0EA5E9 !important; color: white !important;
    border: none !important; border-radius: 10px !important; font-weight: 600 !important;
    padding: 0.75rem 1rem !important; transition: all 0.2s !important;
}
.stButton > button:hover { background: #0284C7 !important; transform: translateY(-2px) !important; }

/* Nút Chuyển về Đăng nhập (nút phụ) */
.btn-secondary > .stButton > button { background: #F1F5F9 !important; color: #475569 !important; }
.btn-secondary > .stButton > button:hover { background: #E2E8F0 !important; color: #1E293B !important; }

.rule-list { font-size: 0.85rem; color: #64748B; line-height: 1.6; margin-top: 0.5rem; padding-left: 1.2rem; }
.rule-list li { list-style: disc; }

/* Hộp thông báo thành công */
.success-box { 
    background: #DCFCE7; border: 2px solid #22C55E; border-radius: 16px; 
    padding: 2rem; text-align: center; animation: fadeInUp 0.5s ease; 
}
.success-icon { font-size: 3rem; margin-bottom: 0.5rem;}
.success-text { color: #15803D; font-weight: 800; font-size: 1.3rem; }
.success-sub { color: #166534; font-size: 0.95rem; margin-top: 0.5rem; }

@keyframes fadeInUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
</style>
""", unsafe_allow_html=True)


# ===================== HELPER =====================
def validate_username(u: str) -> str | None:
    if len(u) < 4: return "Tên đăng nhập phải có ít nhất 4 ký tự."
    if not re.match(r'^[a-zA-Z0-9_]+$', u): return "Tên đăng nhập chỉ gồm chữ cái, số và dấu gạch dưới (_)."
    return None

def validate_password(pw: str) -> str | None:
    if len(pw) < 6: return "Mật khẩu phải có ít nhất 6 ký tự."
    return None

def password_strength(pw: str) -> tuple[int, str, str]:
    score = 0
    if len(pw) >= 8: score += 1
    if re.search(r'[A-Z]', pw): score += 1
    if re.search(r'[0-9!@#$%^&*]', pw): score += 1
    labels = ["Yếu", "Trung bình", "Khá", "Mạnh"]
    colors = ["#ef4444", "#f59e0b", "#3b82f6", "#10b981"]
    return score, labels[score], colors[score]


# ===================== STATE =====================
if "register_success" not in st.session_state:
    st.session_state.register_success = False
if "new_student_name" not in st.session_state:
    st.session_state.new_student_name = ""


# ===================== UI LAYOUT 2 CỘT =====================
st.markdown("<div style='margin-top: 5vh;'></div>", unsafe_allow_html=True)
spacer1, col_left, col_right, spacer2 = st.columns([1, 4, 3, 1], gap="large")

# --- CỘT TRÁI: THÔNG ĐIỆP CHÀO MỪNG ---
with col_left:
    st.markdown("""
    <div class="register-left-panel">
        <div class="register-title">Bắt Đầu<br>Hành Trình Mới</div>
        <div class="register-subtitle">Tạo tài khoản ngay hôm nay để tham gia vào hệ thống ôn luyện và làm bài trắc nghiệm hiệu quả.</div>
    </div>
    """, unsafe_allow_html=True)

# --- CỘT PHẢI: KHU VỰC FORM ---
with col_right:
    st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
    
    # 1. NẾU ĐĂNG KÝ THÀNH CÔNG
    if st.session_state.register_success:
        st.markdown(f"""
        <div class="success-box">
            <div class="success-icon">🎉</div>
            <div class="success-text">Đăng ký thành công!</div>
            <div class="success-sub">Chào mừng <strong>{st.session_state.new_student_name}</strong> đến với hệ thống.</div>
        </div>
        <br>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="btn-secondary">', unsafe_allow_html=True)
        if st.button("🔐 Quay về trang Đăng nhập", use_container_width=True):
            st.session_state.register_success = False
            st.switch_page("app.py")
        st.markdown('</div>', unsafe_allow_html=True)

    # 2. NẾU ĐANG Ở TRẠNG THÁI NHẬP FORM
    else:
        st.markdown("<h3 style='color: #1E293B; font-weight: 800; margin-bottom: 1rem;'>Tạo Tài Khoản</h3>", unsafe_allow_html=True)

        with st.form("register_form", clear_on_submit=False):
            full_name = st.text_input("Họ và tên *", placeholder="Nguyễn Văn A")
            username  = st.text_input("Tên đăng nhập *", placeholder="vd: hocsinh01")
            email     = st.text_input("Email (không bắt buộc)", placeholder="email@example.com")
            password  = st.text_input("Mật khẩu *", type="password", placeholder="Tối thiểu 6 ký tự")
            password2 = st.text_input("Xác nhận mật khẩu *", type="password", placeholder="Nhập lại mật khẩu")

            if password:
                score, label, color = password_strength(password)
                bar_width = [25, 50, 75, 100][score]
                st.markdown(f"""
                <div style="margin-bottom:6px;font-size:0.8rem;color:{color};font-weight:600;">
                    Độ mạnh mật khẩu: {label}
                </div>
                <div style="background:#E2E8F0;border-radius:3px;height:5px;margin-bottom:14px;">
                    <div style="width:{bar_width}%;height:5px;border-radius:3px;background:{color};transition:all 0.3s;"></div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("""
            <ul class="rule-list">
                <li>Tên đăng nhập: 4–20 ký tự (chữ, số, dấu gạch dưới).</li>
                <li>Mật khẩu: Ít nhất 6 ký tự.</li>
            </ul>
            <br>
            """, unsafe_allow_html=True)

            submitted = st.form_submit_button("Đăng ký tài khoản →")

        # Xử lý Logic Submit
        if submitted:
            errors = []
            if not full_name.strip(): errors.append("Vui lòng nhập họ và tên.")
            err_u = validate_username(username.strip())
            if err_u: errors.append(err_u)
            err_p = validate_password(password)
            if err_p: errors.append(err_p)
            if password != password2: errors.append("Hai mật khẩu không khớp nhau.")

            if errors:
                for e in errors: st.error(f"❌ {e}")
            else:
                with st.spinner("Đang xử lý..."):
                    check_user = fetch_data("SELECT student_id FROM students WHERE username = %s", (username.strip(),))
                    if len(check_user) > 0:
                        st.error("❌ Tên đăng nhập này đã được sử dụng. Vui lòng chọn tên khác.")
                    else:
                        query = "INSERT INTO students (username, password_hash, full_name) VALUES (%s, %s, %s)"
                        success = execute_query(query, (username.strip(), password, full_name.strip()))
                        
                        if success:
                            st.session_state.register_success = True
                            st.session_state.new_student_name = full_name.strip()
                            st.rerun()
                        else:
                            st.error("❌ Đã xảy ra lỗi khi tạo tài khoản. Vui lòng thử lại.")

        st.markdown("""
        <div style="text-align: center; margin-top: 1.5rem; font-size: 0.9rem; color: #64748B;">
            Đã có tài khoản? <a href="/" target="_self" style="color: #0EA5E9; font-weight: 700; text-decoration: none;">Đăng nhập ngay</a>
        </div>
        """, unsafe_allow_html=True)
