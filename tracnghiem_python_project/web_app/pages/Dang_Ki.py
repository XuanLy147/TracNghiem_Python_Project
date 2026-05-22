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
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ===================== CSS ĐỒNG BỘ VỚI APP.PY =====================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@300;400;500;600;700;800&family=Playfair+Display:wght@700&display=swap');

html, body, [class*="css"] { font-family: 'Be Vietnam Pro', sans-serif; }

/* 1. MÀU NỀN ĐỒNG BỘ #4ECDC4 */
.stApp { background: #4ECDC4; min-height: 100vh; }

#MainMenu, header, footer { visibility: hidden; }
.block-container { padding-top: 2rem !important; }
.hero-header { text-align: center; padding: 2rem 1rem 1.2rem; animation: fadeInDown 0.7s ease; }
.hero-icon { font-size: 3rem; display: block; margin-bottom: 0.4rem; }

/* 2. MÀU TIÊU ĐỀ ĐỎ #FF0000 */
.hero-title { font-family: 'Playfair Display', serif; font-size: 2.2rem; font-weight: 700; color: #FF0000; margin: 0; text-shadow: 1px 1px 3px rgba(255,255,255,0.7); }
.hero-subtitle { font-size: 0.9rem; color: #e0f2fe; margin-top: 0.4rem; }

/* 3. LÀM ĐẬM BO VIỀN CARD ĐĂNG KÝ (Dày 2px, viền trắng rõ nét) */
.register-card { background: rgba(255,255,255,0.15); border: 2px solid rgba(255,255,255,0.7); border-radius: 20px; padding: 2rem 2rem; backdrop-filter: blur(12px); box-shadow: 0 10px 25px rgba(0,0,0,0.15); animation: fadeInUp 0.7s ease 0.1s both; max-width: 460px; margin: 0 auto; }
.card-title { font-size: 1.1rem; font-weight: 700; color: #ffffff; margin-bottom: 1.2rem; display: flex; align-items: center; gap: 0.5rem; }

/* 4. SỬA Ô NHẬP LIỆU: NỀN TRẮNG (#FFFFFF), CHỮ ĐEN (#000000), VIỀN ĐẬM (#94A3B8) */
.stTextInput > div > div > input { background: #FFFFFF !important; border: 2px solid #94A3B8 !important; border-radius: 10px !important; color: #000000 !important; font-family: 'Be Vietnam Pro', sans-serif !important; font-size: 0.92rem !important; padding: 0.65rem 0.9rem !important; transition: border 0.25s, box-shadow 0.25s; }
.stTextInput > div > div > input:focus { border-color: #0ea5e9 !important; box-shadow: 0 0 0 3px rgba(14,165,233,0.3) !important; }
.stTextInput > label { color: #f8fafc !important; font-size: 0.82rem !important; font-weight: 600 !important; letter-spacing: 0.05em !important; text-transform: uppercase !important; text-shadow: 0px 1px 2px rgba(0,0,0,0.2); }

/* Button Đăng ký */
.stButton > button { width: 100%; background: linear-gradient(135deg, #10b981, #0ea5e9) !important; color: white !important; border: none !important; border-radius: 10px !important; font-family: 'Be Vietnam Pro', sans-serif !important; font-weight: 700 !important; font-size: 0.95rem !important; padding: 0.7rem 1.5rem !important; cursor: pointer !important; transition: opacity 0.2s, transform 0.15s !important; letter-spacing: 0.03em; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
.stButton > button:hover { opacity: 0.9 !important; transform: translateY(-2px) !important; box-shadow: 0 6px 12px rgba(0,0,0,0.15); }

.divider { display: flex; align-items: center; gap: 0.8rem; margin: 1rem 0; color: #e0f2fe; font-size: 0.8rem; }
.divider::before, .divider::after { content: ''; flex: 1; height: 1px; background: rgba(255,255,255,0.4); }

.nav-link { text-align: center; margin-top: 1rem; font-size: 0.88rem; color: #f1f5f9; }
.nav-link a { color: #0f172a; text-decoration: none; font-weight: 800; background: #ffffff; padding: 2px 8px; border-radius: 4px; }

.rule-list { font-size: 0.8rem; color: #e0f2fe; line-height: 1.7; margin: 0; padding-left: 1.1rem; }
.rule-list li { list-style: disc; }

.success-box { background: rgba(52,211,153,0.2); border: 2px solid #34d399; border-radius: 12px; padding: 1.5rem; text-align: center; animation: fadeInUp 0.5s ease; }
.success-icon { font-size: 2.5rem; }
.success-text { color: #34d399; font-weight: 700; font-size: 1.1rem; margin-top: 0.5rem; text-shadow: 0px 1px 2px rgba(0,0,0,0.3); }
.success-sub { color: #ffffff; font-size: 0.85rem; margin-top: 0.3rem; }

@keyframes fadeInDown { from { opacity: 0; transform: translateY(-20px); } to { opacity: 1; transform: translateY(0); } }
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


# ===================== UI =====================
st.markdown("""
<div class="hero-header">
    <span class="hero-icon">📋</span>
    <h1 class="hero-title">Tạo Tài Khoản</h1>
</div>
""", unsafe_allow_html=True)

if st.session_state.register_success:
    st.markdown(f"""
    <div class="success-box">
        <div class="success-icon">🎉</div>
        <div class="success-text">Đăng ký thành công!</div>
        <div class="success-sub">Chào mừng <strong>{st.session_state.new_student_name}</strong> đến với hệ thống.</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔐 Đến trang Đăng nhập"):
        st.session_state.register_success = False
        st.switch_page("app.py")
else:
    st.markdown('<div class="card-title">✏️ Thông tin đăng ký</div>', unsafe_allow_html=True)

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
            <div style="margin-bottom:6px;font-size:0.78rem;color:{color};font-weight:600;">
                Độ mạnh mật khẩu: {label}
            </div>
            <div style="background:rgba(255,255,255,0.08);border-radius:3px;height:5px;margin-bottom:14px;">
                <div style="width:{bar_width}%;height:5px;border-radius:3px;background:{color};transition:all 0.3s;"></div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <ul class="rule-list">
            <li>Tên đăng nhập: 4–20 ký tự, chỉ gồm chữ, số, gạch dưới</li>
            <li>Mật khẩu: ít nhất 6 ký tự</li>
        </ul>
        <br>
        """, unsafe_allow_html=True)

        submitted = st.form_submit_button("Đăng ký tài khoản →")

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

    st.markdown('<div class="divider">hoặc</div>', unsafe_allow_html=True)
    st.markdown('<div class="nav-link">Đã có tài khoản? <a href="/" target="_self">Đăng nhập ngay</a></div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)