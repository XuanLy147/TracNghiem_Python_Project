-- 1. Tạo Database
CREATE DATABASE IF NOT EXISTS tracnghiem_python
CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE tracnghiem_python;

-- 2. Tạo các bảng (Giữ nguyên cấu trúc đã chốt)
CREATE TABLE admins (
    admin_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL
);

CREATE TABLE students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL
);

CREATE TABLE subjects (
    subject_id INT AUTO_INCREMENT PRIMARY KEY,
    subject_name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT
);

CREATE TABLE questions (
    question_id INT AUTO_INCREMENT PRIMARY KEY,
    subject_id INT NOT NULL,
    difficulty_level ENUM('EASY', 'MEDIUM', 'HARD') NOT NULL,
    question_content TEXT NOT NULL,
    option_a TEXT NOT NULL,
    option_b TEXT NOT NULL,
    option_c TEXT NOT NULL,
    option_d TEXT NOT NULL,
    correct_option ENUM('A', 'B', 'C', 'D') NOT NULL,
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id) ON DELETE CASCADE
);

CREATE TABLE quiz_attempts (
    attempt_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    subject_id INT NOT NULL,
    difficulty_level ENUM('EASY', 'MEDIUM', 'HARD') NOT NULL,
    total_questions INT NOT NULL,
    correct_answers INT DEFAULT 0,
    score DECIMAL(5,2) DEFAULT 0.00,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP NULL,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id) ON DELETE CASCADE
);

CREATE TABLE attempt_details (
    detail_id INT AUTO_INCREMENT PRIMARY KEY,
    attempt_id INT NOT NULL,
    question_id INT NOT NULL,
    student_choice ENUM('A', 'B', 'C', 'D', 'UNANSWERED') DEFAULT 'UNANSWERED',
    is_correct BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (attempt_id) REFERENCES quiz_attempts(attempt_id) ON DELETE CASCADE,
    FOREIGN KEY (question_id) REFERENCES questions(question_id) ON DELETE CASCADE
);

-- ==========================================
-- 3. INSERT DỮ LIỆU MẪU (SEED DATA MỚI ĐÃ CHIA FOLDER)
-- ==========================================

-- Thêm tài khoản Admin
INSERT INTO admins (username, password_hash) VALUES 
('admin', '123456');

-- Thêm tài khoản Học sinh
INSERT INTO students (username, password_hash, full_name) VALUES 
('hocsinh01', 'hashed_hs01', 'Nguyễn Văn A'),
('hocsinh02', 'hashed_hs02', 'Trần Thị B');

-- Thêm các Môn học (Đã đóng vai trò như các "Folder" riêng biệt)
INSERT INTO subjects (subject_id, subject_name, description) VALUES 
(1, 'Toán lớp 2', 'Các phép tính cơ bản cộng, trừ, nhân, chia'),
(2, 'Toán lớp 9', 'Đại số, phương trình và hình học cấp THCS'),
(3, 'Toán lớp 12', 'Giải tích, đạo hàm, tích phân và số phức'),
(4, 'Ngữ pháp Tiếng Anh', 'Ngân hàng câu hỏi ngữ pháp từ cơ bản đến nâng cao'),
(5, 'Từ vựng Tiếng Anh', 'Ngân hàng từ vựng flashcard'),
(6, 'Vật Lý THPT', 'Ngân hàng câu hỏi môn Vật Lý'),
(7, 'Hóa Học THPT', 'Ngân hàng câu hỏi môn Hóa Học'),
(8, 'Sinh Học THPT', 'Ngân hàng câu hỏi môn Sinh Học'),
(9, 'Địa Lý lớp 6', 'Kiến thức địa lý tự nhiên cơ bản');

-- ==========================================
-- INSERT CÂU HỎI VÀO CÁC "FOLDER" TƯƠNG ỨNG
-- ==========================================
INSERT INTO questions (subject_id, difficulty_level, question_content, option_a, option_b, option_c, option_d, correct_option) VALUES 

-- >>> TOÁN LỚP 2 (subject_id = 1) - Tận dụng bộ câu hỏi Toán mức Dễ cũ
(1, 'EASY', 'Kết quả của phép tính 15 + 27 là bao nhiêu?', '32', '42', '52', '40', 'B'),
(1, 'EASY', '50 trừ đi 18 còn lại bao nhiêu?', '32', '22', '42', '28', 'A'),
(1, 'EASY', 'Kết quả của 7 x 8 là?', '54', '56', '64', '48', 'B'),
(1, 'MEDIUM', 'Tính: 10 + 2 x 5 = ?', '60', '20', '17', '15', 'B'),
(1, 'MEDIUM', 'Tính chu vi hình chữ nhật có chiều dài 4cm, chiều rộng 3cm?', '7 cm', '12 cm', '14 cm', '24 cm', 'C'),
(1, 'HARD', 'Kết quả của 100 - (20 + 30) là?', '110', '50', '60', '40', 'B'),
(1, 'HARD', '1 giờ rưỡi bằng bao nhiêu phút?', '60', '80', '90', '120', 'C'),

-- >>> TOÁN LỚP 9 (subject_id = 2) - Tận dụng bộ câu hỏi Toán mức Trung Bình cũ
(2, 'EASY', 'Nghiệm của phương trình 2x - 6 = 0 là?', 'x = 2', 'x = 3', 'x = 4', 'x = -3', 'B'),
(2, 'EASY', 'Trung bình cộng của 10, 15, và 20 là?', '10', '12', '15', '20', 'C'),
(2, 'MEDIUM', 'Giải phương trình: x + 15 = 3x - 5', 'x = 10', 'x = -10', 'x = 5', 'x = 20', 'A'),
(2, 'MEDIUM', 'Phương trình x^2 - 4x + 4 = 0 có nghiệm là?', 'x = -2', 'x = 2', 'x = 4', 'Vô nghiệm', 'B'),
(2, 'HARD', 'Tìm x biết: 5/x = 1/2', 'x = 2', 'x = 5', 'x = 10', 'x = 2.5', 'C'),
(2, 'HARD', 'Tổng các góc trong một tam giác bằng bao nhiêu độ?', '90', '180', '270', '360', 'B'),

-- >>> TOÁN LỚP 12 (subject_id = 3) - Tận dụng bộ câu hỏi Toán mức Khó cũ
(3, 'EASY', 'Đạo hàm của hàm số y = sin(x) là?', 'cos(x)', '-cos(x)', 'tan(x)', '-sin(x)', 'A'),
(3, 'EASY', 'Tích phân từ 0 đến 1 của x^2 dx bằng?', '1/2', '1/3', '1', '2/3', 'B'),
(3, 'MEDIUM', 'Giới hạn lim(x->0) của (sin x / x) bằng?', '0', '1', 'Vô cực', 'Không tồn tại', 'B'),
(3, 'MEDIUM', 'Số phức liên hợp của z = 3 - 4i là?', '-3 + 4i', '3 + 4i', '-3 - 4i', '4 - 3i', 'B'),
(3, 'HARD', 'Đạo hàm cấp 2 của y = x^3 là?', '3x^2', '6x', '6', 'x', 'B'),
(3, 'HARD', 'Nghiệm của phương trình 2^x = 8 là?', 'x = 2', 'x = 3', 'x = 4', 'x = 8', 'B'),

-- >>> NGỮ PHÁP TIẾNG ANH (subject_id = 4) - Tích hợp đủ 3 level trong cùng 1 chủ đề
(4, 'EASY', 'Hello, what _____ your name?', 'am', 'is', 'are', 'be', 'B'),
(4, 'EASY', 'I _____ from Vietnam.', 'is', 'am', 'are', 'has', 'B'),
(4, 'MEDIUM', 'If it rains, we _____ at home.', 'stay', 'will stay', 'stayed', 'would stay', 'B'),
(4, 'MEDIUM', 'She told me she _____ tired.', 'is', 'were', 'was', 'has been', 'C'),
(4, 'HARD', 'Hardly had I arrived _____ it started to rain.', 'when', 'than', 'that', 'then', 'A'),
(4, 'HARD', 'If she had studied harder, she _____ the exam.', 'would pass', 'will pass', 'would have passed', 'passed', 'C'),

-- >>> TỪ VỰNG TIẾNG ANH (subject_id = 5)
(5, 'EASY', 'Apple', 'Quả táo', 'Quả chuối', 'Quả cam', 'Quả lê', 'A'),
(5, 'EASY', 'Dog', 'Con mèo', 'Con chó', 'Con cá', 'Con chim', 'B'),
(5, 'MEDIUM', 'Environment', 'Giáo dục', 'Kinh tế', 'Môi trường', 'Xã hội', 'C'),
(5, 'MEDIUM', 'Opportunity', 'Thử thách', 'Cơ hội', 'Khó khăn', 'Sự kiện', 'B'),
(5, 'HARD', 'Ubiquitous', 'Hiếm hoi', 'Có mặt khắp nơi', 'Độc đáo', 'Bí ẩn', 'B'),
(5, 'HARD', 'Ephemeral', 'Vĩnh cửu', 'Phù du / Chóng tàn', 'Mạnh mẽ', 'Rực rỡ', 'B'),

-- >>> VẬT LÝ THPT (subject_id = 6)
(6, 'EASY', 'Đơn vị đo lực trong hệ SI là gì?', 'Joule', 'Newton', 'Watt', 'Pascal', 'B'),
(6, 'MEDIUM', 'Công thức tính động năng là gì?', 'Wd = mv^2/2', 'Wd = mgh', 'Wd = 1/2 kx^2', 'Wd = F.s', 'A'),
(6, 'HARD', 'Theo thuyết tương đối hẹp, năng lượng nghỉ của một vật khối lượng m là?', 'E = m/c^2', 'E = 1/2 mv^2', 'E = mc^2', 'E = mgh', 'C'),

-- >>> HÓA HỌC THPT (subject_id = 7)
(7, 'EASY', 'Ký hiệu hóa học của nguyên tố Oxi là gì?', 'Ox', 'O', 'O2', 'Om', 'B'),
(7, 'MEDIUM', 'Liên kết hóa học trong phân tử NaCl là liên kết gì?', 'Cộng hóa trị', 'Ion', 'Kim loại', 'Hydro', 'B'),
(7, 'HARD', 'Số oxi hóa của Lưu huỳnh trong H2SO4 là?', '+2', '+4', '+6', '-2', 'C'),

-- >>> SINH HỌC THPT (subject_id = 8)
(8, 'EASY', 'Quang hợp ở thực vật diễn ra chủ yếu ở bộ phận nào?', 'Rễ', 'Thân', 'Lá', 'Hoa', 'C'),
(8, 'MEDIUM', 'Ở tế bào nhân thực, vật chất di truyền (ADN) nằm chủ yếu ở đâu?', 'Tế bào chất', 'Ribosome', 'Nhân tế bào', 'Màng tế bào', 'C'),
(8, 'HARD', 'Thuyết nội cộng sinh giải thích nguồn gốc của các bào quan nào?', 'Nhân và Ribosome', 'Ty thể và Lục lạp', 'Lưới nội chất và Bộ máy Golgi', 'Không bào', 'B'),

-- >>> ĐỊA LÝ LỚP 6 (subject_id = 9) - Đã thêm mới theo đúng yêu cầu
(9, 'EASY', 'Trái Đất là hành tinh thứ mấy tính từ Mặt Trời?', 'Thứ 2', 'Thứ 3', 'Thứ 4', 'Thứ 5', 'B'),
(9, 'EASY', 'Đại dương nào có diện tích lớn nhất trên Trái Đất?', 'Đại Tây Dương', 'Ấn Độ Dương', 'Bắc Băng Dương', 'Thái Bình Dương', 'D'),
(9, 'MEDIUM', 'Hiện tượng ngày và đêm luân phiên nhau là do đâu?', 'Trái Đất quay quanh Mặt Trời', 'Trái Đất tự quay quanh trục', 'Mặt Trăng quay quanh Trái Đất', 'Sự chênh lệch nhiệt độ', 'B'),
(9, 'HARD', 'Tỷ lệ bản đồ 1:100.000 có nghĩa là 1cm trên bản đồ tương ứng với bao nhiêu km ngoài thực tế?', '1 km', '10 km', '100 km', '1000 km', 'A');


-- ==========================================
-- BỔ SUNG LƯỢNG LỚN CÂU HỎI CHO 9 CHỦ ĐỀ
-- ==========================================
INSERT INTO questions (subject_id, difficulty_level, question_content, option_a, option_b, option_c, option_d, correct_option) VALUES 

-- >>> TOÁN LỚP 2 (subject_id = 1)
(1, 'EASY', '10 + 15 = ?', '20', '25', '30', '35', 'B'),
(1, 'EASY', '20 - 8 = ?', '10', '12', '14', '16', 'B'),
(1, 'EASY', 'Hình tam giác có mấy cạnh?', '2', '3', '4', '5', 'B'),
(1, 'MEDIUM', '5 x 4 = ?', '15', '20', '25', '30', 'B'),
(1, 'MEDIUM', 'Đoạn thẳng dài 10cm, cắt đi 3cm còn lại bao nhiêu?', '5cm', '6cm', '7cm', '8cm', 'C'),
(1, 'MEDIUM', 'Một tuần có 7 ngày, 2 tuần có bao nhiêu ngày?', '10 ngày', '12 ngày', '14 ngày', '16 ngày', 'C'),
(1, 'HARD', 'Nhà Lan có 12 con gà, mẹ mua thêm 8 con. Hỏi nhà Lan có tất cả bao nhiêu con gà?', '18', '19', '20', '21', 'C'),
(1, 'HARD', 'Số liền trước của 100 là?', '98', '99', '101', '100', 'B'),

-- >>> TOÁN LỚP 9 (subject_id = 2)
(2, 'EASY', 'Căn bậc hai số học của 81 là?', '8', '9', '-9', '81', 'B'),
(2, 'EASY', 'Hàm số y = 2x + 1 là hàm số gì?', 'Bậc nhất', 'Bậc hai', 'Bậc ba', 'Hằng số', 'A'),
(2, 'MEDIUM', 'Hệ số góc của đường thẳng y = 3x - 5 là?', '-5', '3', 'x', '0', 'B'),
(2, 'MEDIUM', 'Đồ thị hàm số y = ax^2 (a khác 0) là đường gì?', 'Đường thẳng', 'Đường tròn', 'Parabol', 'Đường elip', 'C'),
(2, 'HARD', 'Điều kiện để phương trình bậc 2 có nghiệm kép là?', 'Delta < 0', 'Delta > 0', 'Delta = 0', 'Delta khác 0', 'C'),
(2, 'HARD', 'Cho đường tròn (O;R), góc nội tiếp chắn nửa đường tròn có số đo bằng?', '45 độ', '60 độ', '90 độ', '180 độ', 'C'),

-- >>> TOÁN LỚP 12 (subject_id = 3)
(3, 'EASY', 'Họ nguyên hàm của hàm số f(x) = 2x là?', 'x^2 + C', '2x^2 + C', 'x + C', 'x^2', 'A'),
(3, 'EASY', 'Số phức z = 3 + 4i có phần thực là?', '3', '4', '4i', '7', 'A'),
(3, 'MEDIUM', 'Thể tích khối chóp có diện tích đáy B và chiều cao h là?', 'V = B.h', 'V = 1/3 B.h', 'V = 1/2 B.h', 'V = 3 B.h', 'B'),
(3, 'MEDIUM', 'Mô-đun của số phức z = 3 + 4i là?', '5', '7', '25', '1', 'A'),
(3, 'HARD', 'Tập xác định của hàm số y = log_2(x-2) là?', 'R', '(0, +vô cực)', '(2, +vô cực)', '[2, +vô cực)', 'C'),
(3, 'HARD', 'Thể tích mặt cầu có bán kính R là?', '4/3.pi.R^3', '4.pi.R^2', '1/3.pi.R^3', 'pi.R^2', 'A'),

-- >>> NGỮ PHÁP TIẾNG ANH (subject_id = 4)
(4, 'EASY', 'He ___ a student.', 'is', 'am', 'are', 'be', 'A'),
(4, 'EASY', 'They ___ playing football now.', 'is', 'are', 'do', 'does', 'B'),
(4, 'MEDIUM', 'I ___ my homework when the phone rang.', 'did', 'was doing', 'am doing', 'have done', 'B'),
(4, 'MEDIUM', 'If I had a lot of money, I ___ travel the world.', 'will', 'can', 'would', 'shall', 'C'),
(4, 'HARD', 'By next month, I ___ in this city for 5 years.', 'will live', 'am living', 'will have lived', 'lived', 'C'),
(4, 'HARD', 'She suggested ___ to the cinema tonight.', 'to go', 'going', 'go', 'went', 'B'),

-- >>> TỪ VỰNG TIẾNG ANH (subject_id = 5)
(5, 'EASY', 'Màu xanh lá cây trong tiếng Anh là?', 'Red', 'Blue', 'Green', 'Yellow', 'C'),
(5, 'EASY', 'Con mèo trong tiếng Anh là?', 'Dog', 'Cat', 'Bird', 'Fish', 'B'),
(5, 'MEDIUM', 'Từ nào đồng nghĩa với "Beautiful"?', 'Ugly', 'Pretty', 'Bad', 'Sad', 'B'),
(5, 'MEDIUM', 'Trái nghĩa với "Happy" là?', 'Glad', 'Joyful', 'Sad', 'Excited', 'C'),
(5, 'HARD', 'Nghĩa của từ "Meticulous" là gì?', 'Cẩu thả', 'Tỉ mỉ', 'Nhanh nhẹn', 'Lười biếng', 'B'),
(5, 'HARD', 'Nghĩa của từ "Ambiguous" là gì?', 'Rõ ràng', 'Mơ hồ', 'Thông minh', 'Ngốc nghếch', 'B'),

-- >>> VẬT LÝ THPT (subject_id = 6)
(6, 'EASY', 'Đơn vị đo cường độ dòng điện là?', 'Volt', 'Ohm', 'Ampere', 'Joule', 'C'),
(6, 'EASY', 'Công thức tính vận tốc của chuyển động thẳng đều?', 'v = s/t', 'v = s.t', 'v = t/s', 'v = s+t', 'A'),
(6, 'MEDIUM', 'Sóng cơ không truyền được trong môi trường nào?', 'Chất rắn', 'Chất lỏng', 'Chất khí', 'Chân không', 'D'),
(6, 'MEDIUM', 'Công thức tính chu kì con lắc lò xo là?', 'T = 2pi.sqrt(k/m)', 'T = 2pi.sqrt(m/k)', 'T = 1/2pi.sqrt(k/m)', 'T = pi.sqrt(m/k)', 'B'),
(6, 'HARD', 'Hiện tượng quang điện ngoài là hiện tượng electron bứt ra khỏi kim loại khi?', 'Bị nung nóng', 'Bị chiếu sáng thích hợp', 'Đặt trong điện trường', 'Đặt trong từ trường', 'B'),
(6, 'HARD', 'Theo thuyết tương đối, vận tốc ánh sáng trong chân không là?', '3.10^5 m/s', '3.10^8 km/s', '3.10^8 m/s', '3.10^5 km/h', 'C'),

-- >>> HÓA HỌC THPT (subject_id = 7)
(7, 'EASY', 'Khí nào làm đục nước vôi trong?', 'O2', 'H2', 'CO2', 'N2', 'C'),
(7, 'EASY', 'Công thức hóa học của muối ăn là?', 'NaCl', 'HCl', 'NaOH', 'KCl', 'A'),
(7, 'MEDIUM', 'Kim loại nào sau đây có tính khử mạnh nhất?', 'Cu', 'Fe', 'Al', 'Na', 'D'),
(7, 'MEDIUM', 'Độ pH của dung dịch axit là?', 'pH < 7', 'pH = 7', 'pH > 7', 'pH = 14', 'A'),
(7, 'HARD', 'Chất nào sau đây là este?', 'CH3COOH', 'C2H5OH', 'CH3COOC2H5', 'CH3CHO', 'C'),
(7, 'HARD', 'Liên kết trong phân tử N2 là liên kết gì?', 'Cộng hóa trị không cực', 'Cộng hóa trị có cực', 'Ion', 'Kim loại', 'A'),

-- >>> SINH HỌC THPT (subject_id = 8)
(8, 'EASY', 'Bộ NST lưỡng bội của người là?', '46', '23', '48', '24', 'A'),
(8, 'EASY', 'Cơ quan hô hấp chính của cá là?', 'Phổi', 'Da', 'Mang', 'Hệ thống ống khí', 'C'),
(8, 'MEDIUM', 'Quá trình phiên mã diễn ra ở đâu trong tế bào nhân thực?', 'Tế bào chất', 'Ribosome', 'Nhân tế bào', 'Ti thể', 'C'),
(8, 'MEDIUM', 'Nhóm máu nào là nhóm máu chuyên cho?', 'A', 'B', 'AB', 'O', 'D'),
(8, 'HARD', 'Hiện tượng một kiểu gen có thể thay đổi kiểu hình trước các điều kiện môi trường khác nhau gọi là?', 'Đột biến', 'Thường biến', 'Hoán vị gen', 'Tương tác gen', 'B'),
(8, 'HARD', 'Mã di truyền có tính thoái hóa nghĩa là gì?', '1 mã quy định nhiều axit amin', 'Nhiều bộ ba cùng mã hóa 1 axit amin', 'Mã di truyền thay đổi', 'Không có ý nghĩa', 'B'),

-- >>> ĐỊA LÝ LỚP 6 (subject_id = 9)
(9, 'EASY', 'Dạng địa hình nào cao nhất?', 'Đồng bằng', 'Cao nguyên', 'Đồi', 'Núi', 'D'),
(9, 'EASY', 'Trái Đất có hình dạng gì?', 'Hình tròn', 'Hình vuông', 'Hình cầu', 'Hình elip', 'C'),
(9, 'MEDIUM', 'Lớp vỏ Trái Đất dày khoảng bao nhiêu km?', '5 - 70 km', '100 - 200 km', '1000 - 2000 km', '3000 km', 'A'),
(9, 'MEDIUM', 'Đỉnh núi Phan Xi Păng nằm ở dãy núi nào?', 'Trường Sơn', 'Hoàng Liên Sơn', 'Bạch Mã', 'Con Voi', 'B'),
(9, 'HARD', 'Khí quyển có bao nhiêu tầng chính?', '3', '4', '5', '6', 'C'),
(9, 'HARD', 'Độ muối trung bình của nước biển và đại dương là bao nhiêu?', '25 phần nghìn', '30 phần nghìn', '35 phần nghìn', '40 phần nghìn', 'C');

-- ==========================================
-- BỔ SUNG 180 CÂU HỎI CHO 9 CHỦ ĐỀ (MỖI CHỦ ĐỀ 20 CÂU)
-- ==========================================
INSERT INTO questions (subject_id, difficulty_level, question_content, option_a, option_b, option_c, option_d, correct_option) VALUES 

-- ==========================================
-- >>> 1. TOÁN LỚP 2 (20 câu)
-- ==========================================
(1, 'EASY', '12 + 5 = ?', '16', '17', '18', '19', 'B'),
(1, 'EASY', '25 - 10 = ?', '10', '15', '20', '5', 'B'),
(1, 'EASY', 'Số chẵn liền sau số 10 là?', '11', '12', '14', '8', 'B'),
(1, 'EASY', 'Hình chữ nhật có bao nhiêu góc vuông?', '2', '3', '4', '5', 'C'),
(1, 'EASY', '1 gang tay dài khoảng bao nhiêu?', '15 cm', '1 cm', '1 m', '5 m', 'A'),
(1, 'EASY', 'Số lớn nhất có 1 chữ số là?', '8', '9', '10', '1', 'B'),
(1, 'EASY', '30 + 40 = ?', '60', '70', '80', '90', 'B'),
(1, 'MEDIUM', 'Mẹ có 15 quả táo, mẹ cho em 6 quả. Mẹ còn mấy quả?', '8', '9', '10', '11', 'B'),
(1, 'MEDIUM', 'Đồng hồ chỉ 3 giờ chiều. Kim dài chỉ số mấy?', '12', '3', '6', '9', 'A'),
(1, 'MEDIUM', 'Tìm x biết: x + 12 = 20', '8', '9', '10', '12', 'A'),
(1, 'MEDIUM', '1 dm bằng bao nhiêu cm?', '1', '10', '100', '1000', 'B'),
(1, 'MEDIUM', '3 x 6 = ?', '15', '18', '21', '24', 'B'),
(1, 'MEDIUM', 'Số 54 đọc là gì?', 'Năm bốn', 'Năm mươi tư', 'Năm mươi bốn', 'Năm mươi', 'C'),
(1, 'MEDIUM', 'Lớp 2A có 30 bạn, lớp 2B có 25 bạn. Cả hai lớp có bao nhiêu bạn?', '50', '55', '60', '65', 'B'),
(1, 'HARD', 'Thứ hai tuần này là ngày 5. Thứ hai tuần sau là ngày mấy?', '10', '11', '12', '13', 'C'),
(1, 'HARD', 'Tìm số lớn nhất trong các số: 34, 43, 29, 41', '34', '43', '29', '41', 'B'),
(1, 'HARD', 'Một sợi dây dài 20cm, cắt thành các đoạn 5cm. Được mấy đoạn?', '3', '4', '5', '6', 'B'),
(1, 'HARD', 'Con heo nặng 50kg, con chó nặng 15kg. Con heo nặng hơn con chó bao nhiêu kg?', '30kg', '35kg', '40kg', '45kg', 'B'),
(1, 'HARD', 'Có bao nhiêu số có hai chữ số mà chữ số hàng chục là 2?', '9', '10', '11', '12', 'B'),
(1, 'HARD', 'Trong bến có 14 ô tô. Lúc sau có 5 xe rời đi và 3 xe đi vào. Bến còn lại mấy xe?', '10', '11', '12', '13', 'C'),

-- ==========================================
-- >>> 2. TOÁN LỚP 9 (20 câu)
-- ==========================================
(2, 'EASY', 'Căn bậc hai của 16 là?', '4', '-4', '4 và -4', '256', 'C'),
(2, 'EASY', 'Hệ số a của phương trình 2x^2 - 3x + 1 = 0 là?', '2', '-3', '1', '0', 'A'),
(2, 'EASY', 'Đồ thị hàm số y = 3x - 2 cắt trục tung tại điểm có tung độ bằng?', '2', '-2', '3', '-3', 'B'),
(2, 'EASY', 'sin(30 độ) bằng bao nhiêu?', '1/2', 'sqrt(3)/2', '1', '0', 'A'),
(2, 'EASY', 'Góc nội tiếp chắn nửa đường tròn là góc gì?', 'Góc nhọn', 'Góc vuông', 'Góc tù', 'Góc bẹt', 'B'),
(2, 'EASY', 'Đường kính là dây cung... của đường tròn?', 'Nhỏ nhất', 'Lớn nhất', 'Bằng bán kính', 'Tùy ý', 'B'),
(2, 'EASY', 'Phương trình x^2 = 9 có nghiệm là?', '3', '-3', '3 và -3', 'Vô nghiệm', 'C'),
(2, 'MEDIUM', 'Điều kiện xác định của biểu thức sqrt(x - 2) là?', 'x > 2', 'x >= 2', 'x < 2', 'x <= 2', 'B'),
(2, 'MEDIUM', 'Nghiệm của hệ: x + y = 5 và x - y = 1 là?', '(2; 3)', '(3; 2)', '(1; 4)', '(4; 1)', 'B'),
(2, 'MEDIUM', 'Tam giác ABC vuông tại A, AB=3, AC=4. Kẻ đường cao AH. Độ dài BC là?', '5', '6', '7', '8', 'A'),
(2, 'MEDIUM', 'Hàm số y = (m-1)x + 3 đồng biến khi nào?', 'm > 0', 'm < 1', 'm > 1', 'm < 0', 'C'),
(2, 'MEDIUM', 'Tổng 2 nghiệm của phương trình x^2 - 5x + 6 = 0 là?', '5', '-5', '6', '-6', 'A'),
(2, 'MEDIUM', 'Hai đường thẳng y = 2x + 1 và y = ax - 3 song song khi a bằng?', '1', '-2', '2', '-1', 'C'),
(2, 'MEDIUM', 'Tứ giác nội tiếp đường tròn có tổng hai góc đối bằng?', '90 độ', '180 độ', '270 độ', '360 độ', 'B'),
(2, 'HARD', 'Rút gọn biểu thức sqrt( (1-sqrt(2))^2 ) ta được?', '1 - sqrt(2)', 'sqrt(2) - 1', '1', 'sqrt(2)', 'B'),
(2, 'HARD', 'Tìm m để pt x^2 - 2mx + m^2 - 1 = 0 có 2 nghiệm phân biệt?', 'm > 1', 'm < 1', 'Với mọi m', 'Không có m', 'C'),
(2, 'HARD', 'Cho đường tròn (O; 5cm) và dây AB = 8cm. Khoảng cách từ O đến AB là?', '2cm', '3cm', '4cm', '5cm', 'B'),
(2, 'HARD', 'Giá trị lớn nhất của biểu thức A = -x^2 + 4x + 5 là?', '5', '7', '9', '11', 'C'),
(2, 'HARD', 'Chu vi đường tròn ngoại tiếp tam giác đều cạnh a là?', 'pi.a', 'pi.a.sqrt(3)/3', '2.pi.a.sqrt(3)/3', 'pi.a^2', 'C'),
(2, 'HARD', 'Một ô tô dự định đi 120km trong thời gian nhất định. Nếu tăng vận tốc thêm 10km/h thì đến sớm hơn 1h. Vận tốc dự định là?', '30 km/h', '40 km/h', '50 km/h', '60 km/h', 'A'),

-- ==========================================
-- >>> 3. TOÁN LỚP 12 (20 câu)
-- ==========================================
(3, 'EASY', 'Đạo hàm của y = x^4 là?', '4x^3', 'x^3', '3x^4', '4x', 'A'),
(3, 'EASY', 'Nguyên hàm của cos(x) là?', 'sin(x) + C', '-sin(x) + C', '-cos(x) + C', 'tan(x) + C', 'A'),
(3, 'EASY', 'Tập xác định của hàm số y = a^x (a>0, a!=1) là?', 'R', '(0; +vô cực)', '[0; +vô cực)', 'R \\ {0}', 'A'),
(3, 'EASY', 'Số phức z = 5 - 2i có phần ảo là?', '5', '-2i', '-2', '2', 'C'),
(3, 'EASY', 'Thể tích khối lăng trụ có diện tích đáy B, chiều cao h là?', 'B.h', '1/3 B.h', '1/2 B.h', '3 B.h', 'A'),
(3, 'EASY', 'Điểm M(1; 2; 3) thuộc mặt phẳng nào dưới đây?', 'x=0', 'y=0', 'z=0', 'Không thuộc các mặt phẳng tọa độ', 'D'),
(3, 'EASY', 'log_2(8) bằng bao nhiêu?', '2', '3', '4', '8', 'B'),
(3, 'MEDIUM', 'Hàm số y = x^3 - 3x^2 nghịch biến trên khoảng nào?', '(0; 2)', '(-vô cực; 0)', '(2; +vô cực)', 'R', 'A'),
(3, 'MEDIUM', 'Tiệm cận ngang của đồ thị hàm số y = (2x-1)/(x+1) là?', 'y = 1', 'y = -1', 'y = 2', 'x = -1', 'C'),
(3, 'MEDIUM', 'Tích phân từ 0 đến 1 của e^x dx là?', 'e', 'e - 1', 'e + 1', '1', 'B'),
(3, 'MEDIUM', 'Diện tích hình phẳng giới hạn bởi y = x^2, y = 0, x = 1, x = 2 là?', '7/3', '8/3', '1', '3/7', 'A'),
(3, 'MEDIUM', 'Mô-đun của số phức z = 1 + i.sqrt(3) là?', '2', '4', 'sqrt(2)', '1', 'A'),
(3, 'MEDIUM', 'Tọa độ tâm mặt cầu (S): x^2 + y^2 + z^2 - 2x + 4y - 6z = 0 là?', 'I(-1; 2; -3)', 'I(1; -2; 3)', 'I(2; -4; 6)', 'I(-2; 4; -6)', 'B'),
(3, 'MEDIUM', 'Khoảng cách từ điểm A(1;1;1) đến mặt phẳng (P): x + 2y - 2z + 1 = 0 là?', '1/3', '2/3', '1', '4/3', 'B'),
(3, 'HARD', 'Số giao điểm của đồ thị y = x^3 - 3x và đường thẳng y = x là?', '0', '1', '2', '3', 'D'),
(3, 'HARD', 'Tìm m để hàm số y = x^3/3 - mx^2 + x đồng biến trên R?', 'm >= 1', 'm <= -1', '-1 <= m <= 1', 'm = 1', 'C'),
(3, 'HARD', 'Nghiệm của phương trình 4^x - 3.2^x + 2 = 0 là?', 'x=0; x=1', 'x=1; x=2', 'x=-1; x=0', 'Vô nghiệm', 'A'),
(3, 'HARD', 'Tính mô-đun của số phức z thỏa mãn (1+i)z = 3 - i', 'sqrt(5)', 'sqrt(10)', '5', '10', 'A'),
(3, 'HARD', 'Trong không gian Oxyz, phương trình mặt phẳng qua A(1;0;0), B(0;2;0), C(0;0;3) là?', 'x/1 + y/2 + z/3 = 1', 'x + 2y + 3z = 1', 'x/1 + y/2 + z/3 = 0', '6x + 3y + 2z = 0', 'A'),
(3, 'HARD', 'Thể tích khối nón có bán kính đáy r=3, độ dài đường sinh l=5 là?', '12.pi', '15.pi', '36.pi', '45.pi', 'A'),

-- ==========================================
-- >>> 4. NGỮ PHÁP TIẾNG ANH (20 câu)
-- ==========================================
(4, 'EASY', 'She ___ a book every night.', 'read', 'reads', 'reading', 'is reading', 'B'),
(4, 'EASY', 'We ___ to the zoo yesterday.', 'go', 'goes', 'went', 'gone', 'C'),
(4, 'EASY', '___ you like some coffee?', 'Do', 'Does', 'Are', 'Would', 'D'),
(4, 'EASY', 'This pen belongs ___ me.', 'at', 'in', 'to', 'for', 'C'),
(4, 'EASY', 'My sister is ___ than me.', 'tall', 'taller', 'tallest', 'the tallest', 'B'),
(4, 'EASY', 'They ___ playing tennis right now.', 'is', 'are', 'was', 'were', 'B'),
(4, 'EASY', 'I have lived here ___ 2015.', 'for', 'since', 'in', 'at', 'B'),
(4, 'MEDIUM', 'If it rains tomorrow, we ___ at home.', 'will stay', 'would stay', 'stayed', 'stay', 'A'),
(4, 'MEDIUM', 'The book ___ was written by J.K. Rowling is very famous.', 'who', 'whom', 'which', 'whose', 'C'),
(4, 'MEDIUM', 'She asked me what my name ___.', 'is', 'was', 'were', 'has been', 'B'),
(4, 'MEDIUM', 'I am used ___ up early in the morning.', 'to getting', 'to get', 'getting', 'get', 'A'),
(4, 'MEDIUM', 'By the time we arrived, the movie ___.', 'started', 'has started', 'had started', 'was starting', 'C'),
(4, 'MEDIUM', 'He is the man ___ car was stolen yesterday.', 'who', 'whom', 'which', 'whose', 'D'),
(4, 'MEDIUM', 'Despite ___ tired, he finished the work.', 'be', 'being', 'was', 'is', 'B'),
(4, 'HARD', 'Had I known you were in hospital, I ___ you.', 'will visit', 'would visit', 'would have visited', 'visited', 'C'),
(4, 'HARD', 'Not until yesterday ___ the truth.', 'I knew', 'did I know', 'I had known', 'had I known', 'B'),
(4, 'HARD', 'It is imperative that the letter ___ sent immediately.', 'be', 'is', 'was', 'has been', 'A'),
(4, 'HARD', 'Scarcely had she finished reading ___ the phone rang.', 'than', 'when', 'then', 'that', 'B'),
(4, 'HARD', 'I would rather you ___ smoking in here.', 'stop', 'stopped', 'had stopped', 'stopping', 'B'),
(4, 'HARD', 'No sooner ___ the door than the dog rushed out.', 'he had opened', 'had he opened', 'he opened', 'did he open', 'B'),

-- ==========================================
-- >>> 5. TỪ VỰNG TIẾNG ANH (20 câu)
-- ==========================================
(5, 'EASY', 'Trường học trong tiếng Anh là?', 'Hospital', 'School', 'Market', 'Bank', 'B'),
(5, 'EASY', 'Gia đình trong tiếng Anh là?', 'Friend', 'Family', 'Team', 'Group', 'B'),
(5, 'EASY', 'Màu vàng trong tiếng Anh là?', 'Red', 'Blue', 'Yellow', 'Black', 'C'),
(5, 'EASY', 'Bữa sáng trong tiếng Anh là?', 'Lunch', 'Dinner', 'Breakfast', 'Snack', 'C'),
(5, 'EASY', 'Đồng nghĩa với "Big" là?', 'Small', 'Large', 'Tiny', 'Short', 'B'),
(5, 'EASY', 'Trái nghĩa với "Hot" là?', 'Warm', 'Cool', 'Cold', 'Boiling', 'C'),
(5, 'EASY', 'Giáo viên trong tiếng Anh là?', 'Student', 'Doctor', 'Teacher', 'Farmer', 'C'),
(5, 'MEDIUM', 'Từ nào đồng nghĩa với "Important"?', 'Trivial', 'Crucial', 'Minor', 'Optional', 'B'),
(5, 'MEDIUM', 'Trái nghĩa với "Success" là?', 'Victory', 'Achievement', 'Failure', 'Goal', 'C'),
(5, 'MEDIUM', 'Từ "Environment" nghĩa là gì?', 'Kinh tế', 'Môi trường', 'Chính trị', 'Xã hội', 'B'),
(5, 'MEDIUM', 'Từ nào miêu tả một người "thông minh"?', 'Stupid', 'Intelligent', 'Lazy', 'Boring', 'B'),
(5, 'MEDIUM', 'Từ "Colleague" nghĩa là gì?', 'Khách hàng', 'Đồng nghiệp', 'Giám đốc', 'Nhân viên', 'B'),
(5, 'MEDIUM', 'Đồng nghĩa với "Difficult" là?', 'Easy', 'Simple', 'Hard', 'Clear', 'C'),
(5, 'MEDIUM', 'Từ "Celebrate" thường dùng trong dịp nào?', 'Đám tang', 'Lễ hội / Tiệc tùng', 'Họp hành', 'Đi ngủ', 'B'),
(5, 'HARD', 'Nghĩa của từ "Eloquent" là?', 'Lắp bắp', 'Có tài hùng biện', 'Im lặng', 'Thô lỗ', 'B'),
(5, 'HARD', 'Đồng nghĩa với "Ephemeral" là?', 'Permanent', 'Short-lived', 'Endless', 'Eternal', 'B'),
(5, 'HARD', 'Trái nghĩa với "Gregarious" (hòa đồng) là?', 'Sociable', 'Friendly', 'Introverted / Reclusive', 'Outgoing', 'C'),
(5, 'HARD', 'Từ "Mitigate" có nghĩa là gì?', 'Làm trầm trọng thêm', 'Làm giảm nhẹ', 'Khởi xướng', 'Chấm dứt', 'B'),
(5, 'HARD', 'Một người "Fastidious" là người như thế nào?', 'Cẩu thả', 'Dễ tính', 'Khó tính / Khắt khe', 'Hào phóng', 'C'),
(5, 'HARD', 'Từ "Ubiquitous" nghĩa là gì?', 'Hiếm có', 'Tàng hình', 'Có mặt ở khắp nơi', 'Đắt tiền', 'C'),

-- ==========================================
-- >>> 6. VẬT LÝ THPT (20 câu)
-- ==========================================
(6, 'EASY', 'Gia tốc rơi tự do g xấp xỉ bằng?', '9.8 m/s', '9.8 m/s^2', '10 km/h', '9.8 cm/s^2', 'B'),
(6, 'EASY', 'Đơn vị của tần số là?', 'Joule', 'Hertz (Hz)', 'Newton', 'Watt', 'B'),
(6, 'EASY', 'Dòng điện một chiều được kí hiệu là?', 'AC', 'DC', 'Hz', 'V', 'B'),
(6, 'EASY', 'Thấu kính hội tụ có đặc điểm cơ bản là?', 'Rìa dày hơn giữa', 'Rìa mỏng hơn giữa', 'Phẳng', 'Gồ ghề', 'B'),
(6, 'EASY', 'Lực hút giữa Trái Đất và Mặt Trăng là?', 'Lực đàn hồi', 'Lực ma sát', 'Lực hấp dẫn', 'Lực điện từ', 'C'),
(6, 'EASY', 'Đơn vị của công cơ học là?', 'Newton', 'Joule', 'Watt', 'Pascal', 'B'),
(6, 'EASY', 'Vận tốc âm thanh truyền nhanh nhất trong môi trường nào?', 'Chân không', 'Chất khí', 'Chất lỏng', 'Chất rắn', 'D'),
(6, 'MEDIUM', 'Công suất tiêu thụ của đoạn mạch xoay chiều là?', 'P = U.I', 'P = U.I.cos(phi)', 'P = U.I.sin(phi)', 'P = U^2/R', 'B'),
(6, 'MEDIUM', 'Chu kì dao động của con lắc đơn phụ thuộc vào?', 'Khối lượng', 'Biên độ', 'Chiều dài dây và gia tốc g', 'Góc lệch', 'C'),
(6, 'MEDIUM', 'Hiện tượng giao thoa ánh sáng chứng tỏ ánh sáng có tính chất gì?', 'Hạt', 'Sóng', 'Điện', 'Từ', 'B'),
(6, 'MEDIUM', 'Máy biến áp là thiết bị có chức năng gì?', 'Đổi điện AC thành DC', 'Làm tăng hoặc giảm điện áp AC', 'Phát điện', 'Tích điện', 'B'),
(6, 'MEDIUM', 'Trong chân không, các bức xạ được sắp xếp theo thứ tự bước sóng giảm dần là?', 'Hồng ngoại, Ánh sáng nhìn thấy, Tử ngoại, Tia X', 'Tia X, Tử ngoại, Ánh sáng nhìn thấy, Hồng ngoại', 'Ánh sáng nhìn thấy, Hồng ngoại, Tử ngoại, Tia X', 'Tử ngoại, Hồng ngoại, Tia X, Ánh sáng', 'A'),
(6, 'MEDIUM', 'Cường độ dòng điện hiệu dụng được tính bằng?', 'I_max / 2', 'I_max / sqrt(2)', 'I_max * sqrt(2)', 'I_max * 2', 'B'),
(6, 'MEDIUM', 'Lực Lo-ren-xơ tác dụng lên?', 'Điện tích đứng yên', 'Điện tích chuyển động trong từ trường', 'Nam châm', 'Sợi dây có dòng điện', 'B'),
(6, 'HARD', 'Năng lượng liên kết riêng của hạt nhân lớn nhất ở khu vực có số khối A bằng bao nhiêu?', '50 - 90', '10 - 20', '200 - 238', '1 - 10', 'A'),
(6, 'HARD', 'Theo mẫu nguyên tử Bo, bán kính quỹ đạo dừng thứ n tỉ lệ với?', 'n', 'n^2', '1/n', '1/n^2', 'B'),
(6, 'HARD', 'Độ hụt khối của hạt nhân là?', 'Sự giảm khối lượng theo thời gian', 'Sự chênh lệch giữa tổng khối lượng các nucleon và khối lượng hạt nhân', 'Khối lượng bị mất khi va chạm', 'Sự phân rã của neutron', 'B'),
(6, 'HARD', 'Mạch dao động LC lí tưởng có tần số góc là?', '1/(L.C)', 'sqrt(L.C)', '1/sqrt(L.C)', 'L.C', 'C'),
(6, 'HARD', 'Trong thí nghiệm Y-âng, khoảng vân i được tính bằng công thức?', 'i = (lambda.D)/a', 'i = (lambda.a)/D', 'i = (a.D)/lambda', 'i = lambda.D.a', 'A'),
(6, 'HARD', 'Sự phóng xạ là quá trình?', 'Thu nhiệt', 'Hấp thụ nơtron', 'Tự phát phân rã của hạt nhân không bền', 'Phản ứng hạt nhân nhân tạo', 'C'),

-- ==========================================
-- >>> 7. HÓA HỌC THPT (20 câu)
-- ==========================================
(7, 'EASY', 'Kí hiệu hóa học của Sắt là?', 'Sa', 'Fe', 'Cu', 'Ag', 'B'),
(7, 'EASY', 'Công thức của khí Oxi là?', 'O', 'O2', 'O3', 'H2O', 'B'),
(7, 'EASY', 'Chất nào sau đây làm quỳ tím chuyển đỏ?', 'NaOH', 'NaCl', 'HCl', 'H2O', 'C'),
(7, 'EASY', 'Nước có độ pH bằng bao nhiêu?', '5', '7', '9', '14', 'B'),
(7, 'EASY', 'Khí CO2 có tên gọi là gì?', 'Cacbon oxit', 'Cacbon đioxit', 'Cacbonic', 'Cả B và C đều đúng', 'D'),
(7, 'EASY', 'Kim loại nào ở thể lỏng ở điều kiện thường?', 'Sắt', 'Thủy ngân', 'Chì', 'Nhôm', 'B'),
(7, 'EASY', 'Muối ăn có công thức hóa học là?', 'KCl', 'MgCl2', 'NaCl', 'CaCl2', 'C'),
(7, 'MEDIUM', 'Liên kết trong phân tử HCl là liên kết gì?', 'Cộng hóa trị phân cực', 'Cộng hóa trị không cực', 'Ion', 'Kim loại', 'A'),
(7, 'MEDIUM', 'Cho Cu vào dung dịch AgNO3, hiện tượng xảy ra là?', 'Không có hiện tượng', 'Cu tan, có bạc bám vào, dung dịch chuyển màu xanh', 'Có khí thoát ra', 'Kết tủa trắng', 'B'),
(7, 'MEDIUM', 'Công thức chung của Ankan là?', 'CnH2n', 'CnH2n-2', 'CnH2n+2', 'CnH2n-6', 'C'),
(7, 'MEDIUM', 'Axit axetic có trong chất nào trong đời sống?', 'Rượu', 'Nước chanh', 'Giấm ăn', 'Sữa chua', 'C'),
(7, 'MEDIUM', 'Dung dịch làm hồng phenolphtalein là?', 'HCl', 'NaCl', 'NaOH', 'H2SO4', 'C'),
(7, 'MEDIUM', 'Nhôm không tác dụng với dung dịch nào sau đây?', 'HCl loãng', 'H2SO4 loãng', 'HNO3 đặc nguội', 'NaOH', 'C'),
(7, 'MEDIUM', 'Thành phần chính của khí thiên nhiên là?', 'Metan (CH4)', 'Etan (C2H6)', 'Propan', 'Butan', 'A'),
(7, 'HARD', 'Phản ứng tráng gương là phản ứng đặc trưng của nhóm chức nào?', 'Ancol (-OH)', 'Andehit (-CHO)', 'Cacboxylic (-COOH)', 'Este (-COO-)', 'B'),
(7, 'HARD', 'Amino axit đơn giản nhất là?', 'Alanin', 'Glyxin', 'Valin', 'Lysin', 'B'),
(7, 'HARD', 'Polime nào sau đây được dùng để chế tạo tơ nilon-6,6?', 'Poli vinyl clorua', 'Poli etylen', 'Poli hexametylen ađipamit', 'Poli stiren', 'C'),
(7, 'HARD', 'Sắt có số oxi hóa +3 trong hợp chất nào?', 'FeO', 'FeCl2', 'Fe2O3', 'FeSO4', 'C'),
(7, 'HARD', 'Tính bazơ của các amin được sắp xếp tăng dần như sau?', 'NH3 < C6H5NH2 < CH3NH2', 'C6H5NH2 < NH3 < CH3NH2', 'CH3NH2 < NH3 < C6H5NH2', 'C6H5NH2 < CH3NH2 < NH3', 'B'),
(7, 'HARD', 'Đồng phân quang học xuất hiện khi phân tử có chứa?', 'Liên kết đôi', 'Vòng benzen', 'Nguyên tử Cacbon bất đối (C gắn 4 nhóm khác nhau)', 'Nhóm -OH', 'C'),

-- ==========================================
-- >>> 8. SINH HỌC THPT (20 câu)
-- ==========================================
(8, 'EASY', 'Tế bào là đơn vị tổ chức cơ bản của?', 'Vật chất vô cơ', 'Sự sống', 'Khoáng sản', 'Năng lượng', 'B'),
(8, 'EASY', 'Cơ quan hô hấp của con người là?', 'Tim', 'Gan', 'Phổi', 'Thận', 'C'),
(8, 'EASY', 'Quang hợp xảy ra ở bào quan nào của tế bào thực vật?', 'Nhân', 'Ty thể', 'Lục lạp', 'Ribosome', 'C'),
(8, 'EASY', 'Ruồi giấm có bao nhiêu nhiễm sắc thể (2n)?', '8', '46', '24', '14', 'A'),
(8, 'EASY', 'Cây xanh nhả khí gì vào ban ngày?', 'Cacbonic', 'Oxi', 'Nito', 'Hidro', 'B'),
(8, 'EASY', 'Nhóm máu nào là nhóm máu chuyên nhận?', 'O', 'A', 'B', 'AB', 'D'),
(8, 'EASY', 'Con người có bao nhiêu cặp nhiễm sắc thể?', '22', '23', '24', '46', 'B'),
(8, 'MEDIUM', 'ADN được cấu tạo từ các đơn phân nào?', 'Axit amin', 'Nuclêôtit', 'Đường đơn', 'Axit béo', 'B'),
(8, 'MEDIUM', 'Quá trình tổng hợp ARN trên mạch khuôn ADN gọi là?', 'Nhân đôi', 'Phiên mã', 'Dịch mã', 'Đột biến', 'B'),
(8, 'MEDIUM', 'Nơi diễn ra quá trình dịch mã trong tế bào là?', 'Nhân', 'Ti thể', 'Tế bào chất (tại Ribosome)', 'Màng tế bào', 'C'),
(8, 'MEDIUM', 'Sự trao đổi chéo giữa các NST tương đồng xảy ra ở kỳ nào của giảm phân?', 'Kỳ đầu I', 'Kỳ giữa I', 'Kỳ sau II', 'Kỳ cuối I', 'A'),
(8, 'MEDIUM', 'Ông tổ của di truyền học là ai?', 'Darwin', 'Mendel', 'Morgan', 'Watson', 'B'),
(8, 'MEDIUM', 'Trong chuỗi thức ăn, sinh vật sản xuất thường là?', 'Động vật ăn cỏ', 'Thực vật xanh', 'Động vật ăn thịt', 'Vi khuẩn phân giải', 'B'),
(8, 'MEDIUM', 'Bệnh Đao (Down) ở người do đột biến dạng nào?', 'Mất đoạn NST 21', 'Thể ba (3 NST) ở cặp số 21', 'Đột biến gen lặn', 'Lệch bội NST giới tính', 'B'),
(8, 'HARD', 'Hiện tượng một gen chi phối sự biểu hiện của nhiều tính trạng gọi là?', 'Tương tác gen', 'Gen đa hiệu', 'Di truyền liên kết', 'Hoán vị gen', 'B'),
(8, 'HARD', 'Enzym xúc tác cho quá trình nhân đôi ADN là?', 'ARN polymerase', 'ADN polymerase', 'Ligase', 'Restrictaza', 'B'),
(8, 'HARD', 'Trong mô hình Operon Lac, chất cảm ứng (Lactose) liên kết với thành phần nào?', 'Vùng khởi động', 'Vùng vận hành', 'Protein ức chế', 'Gen cấu trúc', 'C'),
(8, 'HARD', 'Sự tiến hóa hình thành loài mới thường trải qua mấy giai đoạn?', '1', '2', '3 (Đột biến, Giao phối, Chọn lọc)', 'Rất nhiều bước phức tạp khó chia', 'D'),
(8, 'HARD', 'Cơ quan tương đồng là những cơ quan có?', 'Cùng chức năng, khác nguồn gốc', 'Cùng nguồn gốc, có thể khác chức năng', 'Hình thái giống nhau', 'Kích thước giống nhau', 'B'),
(8, 'HARD', 'Theo định luật Hardy-Weinberg, quần thể cân bằng khi?', 'Tần số alen và thành phần kiểu gen không đổi qua các thế hệ', 'Tần số đột biến cao', 'Có chọn lọc tự nhiên mạnh', 'Kích thước quần thể nhỏ', 'A'),

-- ==========================================
-- >>> 9. ĐỊA LÝ LỚP 6 (20 câu)
-- ==========================================
(9, 'EASY', 'Trái Đất là hành tinh thứ mấy tính từ Mặt Trời?', 'Thứ 2', 'Thứ 3', 'Thứ 4', 'Thứ 5', 'B'),
(9, 'EASY', 'Trái Đất có hình gì?', 'Hình tròn', 'Hình vuông', 'Hình cầu', 'Hình elip', 'C'),
(9, 'EASY', 'Châu lục nào có diện tích lớn nhất?', 'Châu Phi', 'Châu Mỹ', 'Châu Á', 'Châu Âu', 'C'),
(9, 'EASY', 'Đại dương nào lớn nhất?', 'Đại Tây Dương', 'Ấn Độ Dương', 'Bắc Băng Dương', 'Thái Bình Dương', 'D'),
(9, 'EASY', 'Việt Nam nằm ở châu lục nào?', 'Châu Á', 'Châu Âu', 'Châu Phi', 'Châu Mỹ', 'A'),
(9, 'EASY', 'Sự luân phiên ngày và đêm do đâu?', 'Mặt Trời di chuyển', 'Trái Đất tự quay quanh trục', 'Trái Đất quay quanh Mặt Trời', 'Trái Đất quay quanh Mặt Trăng', 'B'),
(9, 'EASY', 'Bản đồ là gì?', 'Ảnh chụp từ vệ tinh', 'Hình vẽ thu nhỏ tương đối chính xác của bề mặt Trái Đất', 'Tranh vẽ phong cảnh', 'Mô hình quả địa cầu', 'B'),
(9, 'MEDIUM', 'Kinh tuyến gốc đi qua đài thiên văn Greenwich thuộc quốc gia nào?', 'Mỹ', 'Pháp', 'Anh', 'Nga', 'C'),
(9, 'MEDIUM', 'Vĩ tuyến lớn nhất trên quả địa cầu là?', 'Vòng cực', 'Chí tuyến Bắc', 'Chí tuyến Nam', 'Xích đạo', 'D'),
(9, 'MEDIUM', 'Một vòng quay của Trái Đất quanh trục mất bao lâu?', '12 giờ', '24 giờ', '30 ngày', '365 ngày', 'B'),
(9, 'MEDIUM', 'Trái Đất quay quanh Mặt Trời theo quỹ đạo hình gì?', 'Hình tròn', 'Hình elip gần tròn', 'Hình vuông', 'Hình xoắn ốc', 'B'),
(9, 'MEDIUM', 'Cấu tạo bên trong của Trái Đất gồm mấy lớp?', '2', '3 (Lớp vỏ, Lớp trung gian, Lõi)', '4', '5', 'B'),
(9, 'MEDIUM', 'Lớp vỏ Trái Đất có độ dày khoảng bao nhiêu?', '5 - 70 km', '100 - 200 km', '1000 - 2000 km', '3000 km', 'A'),
(9, 'MEDIUM', 'Dạng địa hình có đỉnh nhọn, sườn dốc, độ cao trên 500m là?', 'Đồng bằng', 'Cao nguyên', 'Đồi', 'Núi', 'D'),
(9, 'HARD', 'Hiện tượng các mùa trong năm do nguyên nhân nào?', 'Trái Đất tự quay quanh trục', 'Trái Đất quay quanh Mặt Trời với trục nghiêng không đổi', 'Mặt Trời thay đổi nhiệt độ', 'Khoảng cách Trái Đất và Mặt Trời thay đổi', 'B'),
(9, 'HARD', 'Ở nửa cầu Bắc, ngày 22/6 (Hạ chí) có hiện tượng gì?', 'Ngày dài hơn đêm', 'Ngày ngắn hơn đêm', 'Ngày dài bằng đêm', 'Không có Mặt Trời', 'A'),
(9, 'HARD', 'Độ cao tuyệt đối của một ngọn núi được tính từ đâu?', 'Từ chân núi', 'Từ mực nước biển trung bình', 'Từ đáy đại dương', 'Từ vùng đồng bằng gần nhất', 'B'),
(9, 'HARD', 'Khí quyển Trái Đất có lớp khí nào chiếm tỉ lệ lớn nhất?', 'Oxi', 'Cacbonic', 'Nitơ (78%)', 'Hơi nước', 'C'),
(9, 'HARD', 'Sự phong hóa đá là quá trình gì?', 'Đá biến thành magma', 'Đá bị phá hủy, tơi xốp do nhiệt độ, nước, sinh vật', 'Đá bị nén chặt', 'Đá dịch chuyển', 'B'),
(9, 'HARD', 'Sông và hồ khác nhau cơ bản ở điểm nào?', 'Sông có nước ngọt, hồ nước mặn', 'Sông là dòng chảy thường xuyên, hồ là khoảng nước đọng', 'Sông do con người đào, hồ tự nhiên', 'Sông ở trên núi, hồ ở đồng bằng', 'B');
