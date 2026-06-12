import streamlit as st
import pandas as pd
import altair as alt
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from shared.db import fetch_data
except ImportError:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    from shared.db import fetch_data

st.set_page_config(page_title="Lịch Sử Làm Bài", page_icon="🕒", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
[data-testid="collapsedControl"] {display: none;}
section[data-testid="stSidebar"] {display: none;}
</style>
""", unsafe_allow_html=True)

def color_score(val):
    try:
        score = float(val)
        if score >= 8.0: return 'color: #10b981; font-weight: bold;' 
        elif score >= 5.0: return 'color: #f59e0b; font-weight: bold;' 
        else: return 'color: #ef4444; font-weight: bold;' 
    except:
        return ''

def show_history():
    if 'logged_in' not in st.session_state or not st.session_state.logged_in:
        st.warning("⚠️ Vui lòng đăng nhập ở trang chủ để xem lịch sử làm bài!")
        return

    user_info = st.session_state.student
    student_id = user_info['student_id']

    if st.button("🏠 Quay về Trang chủ", type="secondary"):
        st.switch_page("app.py")

    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 style="font-family: 'Playfair Display', serif; color: #1d4ed8; font-size: 2.5rem; margin-bottom: 0;">Bảng Điểm Cá Nhân</h1>
        <p style="color: #475569; font-size: 1.1rem;">Học viên: <b>{}</b></p>
    </div>
    """.format(user_info['full_name']), unsafe_allow_html=True)

    # Lấy thêm cột attempt_id để truy xuất chi tiết
    query = """
        SELECT 
            qa.attempt_id,
            qa.started_at AS 'Thời gian nộp bài',
            s.subject_name AS 'Môn học',
            qa.difficulty_level AS 'Độ khó',
            CONCAT(qa.correct_answers, '/', qa.total_questions) AS 'Số câu đúng',
            qa.score AS 'Điểm số'
        FROM quiz_attempts qa
        JOIN subjects s ON qa.subject_id = s.subject_id
        WHERE qa.student_id = %s
        ORDER BY qa.started_at DESC
    """
    history_data = fetch_data(query, (student_id,))

    if not history_data:
        st.info("Tờ giấy trắng! Bạn chưa có lịch sử làm bài nào. Hãy ra ngoài làm thử một đề nhé!")
        return

    df = pd.DataFrame(history_data)
    df['Điểm số'] = pd.to_numeric(df['Điểm số'])
    df['Điểm số'] = df['Điểm số'].apply(lambda x: x / 10 if x > 10 else x)

    # --- METRICS ---
    total_exams = len(df)
    avg_score = round(df['Điểm số'].mean(), 2)
    max_score = df['Điểm số'].max()

    c1, c2, c3 = st.columns(3)
    with c1: st.info(f"📚 **Tổng Lần Thi:**\n### {total_exams} lần")
    with c2: st.warning(f"🎯 **Điểm Trung Bình:**\n### {avg_score} điểm")
    with c3: st.success(f"🏆 **Điểm Cao Nhất:**\n### {max_score} điểm")
    st.divider()

    # --- CHART ---
    st.markdown("<h3 style='color: #0f172a; font-size: 1.3rem;'>📈 Biểu đồ tiến độ học tập</h3>", unsafe_allow_html=True)
    
    # Chuẩn bị dữ liệu (Lưu ý: Không dùng set_index nữa)
    df_chart = df[['Thời gian nộp bài', 'Điểm số']].copy()
    df_chart['Thời gian nộp bài'] = pd.to_datetime(df_chart['Thời gian nộp bài']).dt.strftime('%H:%M:%S %d/%m')
    df_chart = df_chart.iloc[::-1] 
    
    # Vẽ biểu đồ bằng Altair
    chart = alt.Chart(df_chart).mark_line(
        point=alt.OverlayMarkDef(size=60, color="#FF0000") # Thêm chấm đỏ ở mỗi điểm cho nét
    ).encode(
        x=alt.X('Thời gian nộp bài:O', sort=None, title='Thời gian nộp bài'), # :O giữ nguyên thứ tự thời gian
        y=alt.Y('Điểm số:Q', 
                scale=alt.Scale(domain=[0, 10]), # Ép cứng trục Y từ 0 đến 10
                axis=alt.Axis(values=[0, 2, 4, 6, 8, 10]), # Chỉ hiện đúng các vạch số này
                title='Điểm số'
        )
    ).properties(
        height=350 # Chỉnh độ cao biểu đồ cho cân đối
    )

    st.altair_chart(chart, use_container_width=True)
    st.divider()
    # --- BẢNG ĐIỂM ---
    col_title, col_filter = st.columns([2, 1])
    with col_title:
        st.markdown("<h3 style='color: #0f172a; font-size: 1.3rem;'>📋 Chi tiết các lần thi</h3>", unsafe_allow_html=True)
    with col_filter:
        mon_hoc_list = ["Tất cả"] + df['Môn học'].unique().tolist()
        selected_mon = st.selectbox("Lọc theo môn học:", mon_hoc_list, label_visibility="collapsed")

    if selected_mon != "Tất cả":
        df_filtered = df[df['Môn học'] == selected_mon]
    else:
        df_filtered = df

    # Giấu cột attempt_id, chỉ hiện các cột còn lại
    display_df = df_filtered.drop(columns=['attempt_id'])
    
    # Ép chuẩn format: Bọc màu xanh đỏ + Làm tròn 2 chữ số + Thay dấu chấm thành dấu phẩy
    styled_df = display_df.style.map(color_score, subset=['Điểm số']).format({'Điểm số': lambda x: f"{x:.2f}"})
    
    st.dataframe(styled_df, use_container_width=True, hide_index=True)
    st.divider()

    # =========================================
    # TÍNH NĂNG: XEM LẠI CHI TIẾT BÀI LÀM
    # =========================================
    st.markdown("<h3 style='color: #0f172a; font-size: 1.5rem;'>🔍 Xem Lại Chi Tiết Đáp Án</h3>", unsafe_allow_html=True)
    
    # Tạo danh sách các lần thi để đưa vào hộp thoại chọn
    # Format: "Toán học - 14:38:35 (Điểm: 10.0)"
    attempt_options = {}
    for idx, row in df.iterrows():
        label = f"{row['Môn học']} - Ngày {row['Thời gian nộp bài']} (Đúng: {row['Số câu đúng']})"
        attempt_options[label] = row['attempt_id']

    selected_attempt_label = st.selectbox("Chọn một bài thi để xem chi tiết:", list(attempt_options.keys()))
    
    if selected_attempt_label:
        selected_attempt_id = attempt_options[selected_attempt_label]
        
        # Query lôi hết chi tiết từ DB lên
        detail_query = """
            SELECT 
                q.question_content AS question_text,
                ad.student_choice AS selected_option,
                q.correct_option,
                q.option_a, q.option_b, q.option_c, q.option_d,
                ad.is_correct
            FROM attempt_details ad
            JOIN questions q ON ad.question_id = q.question_id
            WHERE ad.attempt_id = %s
        """
        details_data = fetch_data(detail_query, (selected_attempt_id,))

        if details_data:
            # Bọc chi tiết vào một khung Expander (Mở ra đóng vào cho gọn)
            with st.expander("📝 Bấm vào đây để xem toàn bộ câu hỏi và đáp án", expanded=True):
                for i, row in enumerate(details_data):
                    is_correct = row['is_correct'] == 1
                    status_icon = "✅" if is_correct else "❌"
                    color = "#10b981" if is_correct else "#ef4444"
                    
                    # Ánh xạ đáp án A, B, C, D từ DB ra Text gốc
                    correct_letter = row['correct_option']
                    mapping = {
                        'A': row['option_a'],
                        'B': row['option_b'],
                        'C': row['option_c'],
                        'D': row['option_d']
                    }
                    correct_text = mapping.get(correct_letter, "Không xác định")

                    st.markdown(f"""
                    <div style="border-left: 4px solid {color}; padding-left: 15px; margin-bottom: 20px; background-color: #f8fafc; padding: 15px; border-radius: 5px;">
                        <p style="font-weight: bold; margin-bottom: 5px; color: #0f172a;">Câu {i+1}: {row['question_text']} {status_icon}</p>
                        <p style="margin: 0; font-size: 0.95rem;"><b>Bạn chọn:</b> <span style="color: {color};">{row['selected_option']}</span></p>
                        <p style="margin: 0; font-size: 0.95rem;"><b>Đáp án đúng:</b> <span style="color: #10b981;">{correct_text}</span></p>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("Bài thi này không lưu chi tiết câu hỏi.")

if __name__ == "__main__":
    show_history()