import pandas as pd
import mysql.connector
import shared.db
import tkinter as tk
from mysql.connector import Error


def import_questions_from_excel(file_path):
    """
    Hàm đọc file Excel và chèn hàng loạt dữ liệu vào bảng questions trong MySQL.
    Trả về True nếu thành công, False nếu thất bại.
    """
    try:
        # 1. ĐỌC FILE EXCEL
        # print(f"⏳ Đang đọc file Excel: '{file_path}'...")
        df = pd.read_excel(file_path)
        
        # Chuyển đổi các ô trống (NaN trong Pandas) thành giá trị None để MySQL hiểu là NULL
        df = df.where(pd.notnull(df), None)

        # Kiểm tra xem file Excel có đủ cột không
        required_columns = [
            'subject_id', 'difficulty_level', 'question_content', 
            'option_a', 'option_b', 'option_c', 'option_d', 'correct_option'
        ]
        missing_cols = [col for col in required_columns if col not in df.columns]
        
        if missing_cols:
            print(f"❌ Lỗi: File Excel bị thiếu các cột: {', '.join(missing_cols)}")
            return False

        # Đóng gói dữ liệu thành List các Tuple để chuẩn bị chèn
        data_to_insert = []
        for index, row in df.iterrows():
            data_to_insert.append((
                row['subject_id'],
                str(row['difficulty_level']) if row['difficulty_level'] else None,
                str(row['question_content']) if row['question_content'] else None,
                str(row['option_a']) if row['option_a'] else None,
                str(row['option_b']) if row['option_b'] else None,
                str(row['option_c']) if row['option_c'] else None,
                str(row['option_d']) if row['option_d'] else None,
                str(row['correct_option']) if row['correct_option'] else None
            ))

        # 2. KẾT NỐI VÀ CHÈN VÀO MYSQL
        print("⏳ Đang kết nối MySQL và chèn dữ liệu...")
        connection = mysql.connector.connect(**shared.db.DB_CONFIG)
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Cú pháp %s là placeholder an toàn chống SQL Injection
            query = """
                INSERT INTO questions 
                (subject_id, difficulty_level, question_content, option_a, option_b, option_c, option_d, correct_option) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            # executemany giúp chạy 1 câu query cho toàn bộ list dữ liệu (tốc độ cực nhanh)
            cursor.executemany(query, data_to_insert)
            connection.commit()
            
            print(f"✅ THÀNH CÔNG! Đã thêm {cursor.rowcount} câu hỏi vào Database.")
            return True

    except FileNotFoundError:
        print(f"❌ Lỗi: Không tìm thấy file tại đường dẫn '{file_path}'")
        return False
    except Error as e:
        print(f"❌ Lỗi Database MySQL: {e}")
        return False
    except Exception as e:
        print(f"❌ Lỗi hệ thống: {e}")
        return False
    finally:
        # Luôn đảm bảo đóng kết nối dù thành công hay thất bại
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
    
