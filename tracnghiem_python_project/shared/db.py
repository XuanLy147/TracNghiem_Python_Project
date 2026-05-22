import mysql.connector
from mysql.connector import Error

# Cấu hình Database (Bạn hãy sửa lại 'user' và 'password' cho khớp với máy của bạn)
DB_CONFIG = {
    'host': 'localhost',
    'database': 'tracnghiem_python',
    'user': 'root',      # Thường mặc định trên XAMPP/WAMP là 'root'
    'password': ''       # Thường mặc định trên XAMPP/WAMP là rỗng ('')
}

def get_connection():
    """Tạo và trả về đối tượng kết nối đến MySQL."""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Lỗi kết nối MySQL: {e}")
        return None

def fetch_data(query, params=None):
    """
    Dùng cho các lệnh SELECT. 
    Trả về danh sách các dòng dữ liệu dưới dạng Dictionary.
    """
    connection = get_connection()
    if connection is None:
        return []

    try:
        # dictionary=True giúp kết quả trả về dạng {'cột': 'giá trị'} cực kỳ dễ đọc
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params or ())
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"Lỗi khi thực thi SELECT: {e}")
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def execute_query(query, params=None):
    """
    Dùng cho các lệnh INSERT, UPDATE, DELETE.
    Trả về True nếu thành công, False nếu thất bại.
    """
    connection = get_connection()
    if connection is None:
        return False

    try:
        cursor = connection.cursor()
        cursor.execute(query, params or ())
        connection.commit() # Bắt buộc phải commit thì dữ liệu mới lưu vào DB
        return True
    except Error as e:
        print(f"Lỗi khi thực thi thao tác dữ liệu (Thêm/Sửa/Xóa): {e}")
        return False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# ==========================================
# KHU VỰC TEST CODE ĐỘC LẬP
# ==========================================
if __name__ == "__main__":
    print("Đang kiểm tra kết nối Database...")
    conn = get_connection()
    
    if conn:
        print("=> KẾT NỐI THÀNH CÔNG!")
        conn.close()
    else:
        print("=> KẾT NỐI THẤT BẠI. Vui lòng kiểm tra lại DB_CONFIG hoặc xem MySQL đã bật chưa.")