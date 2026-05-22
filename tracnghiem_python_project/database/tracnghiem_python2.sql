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
-- 3. INSERT DỮ LIỆU MẪU (SEED DATA)
-- ==========================================

-- Thêm tài khoản Admin
INSERT INTO admins (username, password_hash) VALUES 
('admin', '123456');

-- Thêm tài khoản Học sinh
INSERT INTO students (username, password_hash, full_name) VALUES 
('hocsinh01', 'hashed_hs01', 'Nguyễn Văn A'),
('hocsinh02', 'hashed_hs02', 'Trần Thị B');

-- Thêm Môn học
INSERT INTO subjects (subject_name, description) VALUES 
('Toán học', 'Ngân hàng câu hỏi môn Toán'),
('Tiếng Anh', 'Ngân hàng câu hỏi môn Tiếng Anh');
INSERT INTO questions (subject_id, difficulty_level, question_content, option_a, option_b, option_c, option_d, correct_option) VALUES 
-- ==========================================
-- MÔN TOÁN (subject_id = 1) - MỨC ĐỘ DỄ (20 câu)
-- ==========================================
(1, 'EASY', 'Kết quả của phép tính 15 + 27 là bao nhiêu?', '32', '42', '52', '40', 'B'),
(1, 'EASY', '50 trừ đi 18 còn lại bao nhiêu?', '32', '22', '42', '28', 'A'),
(1, 'EASY', 'Kết quả của 7 x 8 là?', '54', '56', '64', '48', 'B'),
(1, 'EASY', 'Thương của phép chia 81 / 9 là?', '7', '8', '9', '10', 'C'),
(1, 'EASY', 'Một tuần có bao nhiêu giờ?', '168', '144', '120', '156', 'A'),
(1, 'EASY', 'Số tự nhiên liền sau số 999 là?', '998', '1000', '1001', '100', 'B'),
(1, 'EASY', 'Tính: 10 + 2 x 5 = ?', '60', '20', '17', '15', 'B'),
(1, 'EASY', 'Số nào sau đây là số chẵn?', '13', '27', '88', '91', 'C'),
(1, 'EASY', 'Hình vuông có cạnh 5cm thì diện tích là?', '20 cm2', '25 cm2', '10 cm2', '15 cm2', 'B'),
(1, 'EASY', '1 kilomet bằng bao nhiêu mét?', '10', '100', '1000', '10000', 'C'),
(1, 'EASY', 'Số lớn nhất có 2 chữ số là?', '90', '98', '99', '100', 'C'),
(1, 'EASY', 'Tính chu vi hình chữ nhật có chiều dài 4cm, chiều rộng 3cm?', '7 cm', '12 cm', '14 cm', '24 cm', 'C'),
(1, 'EASY', 'Căn bậc hai của 25 là?', '4', '5', '6', '25', 'B'),
(1, 'EASY', 'Số 0 có phải là số tự nhiên không?', 'Có', 'Không', 'Chỉ khi tính tổng', 'Tùy trường hợp', 'A'),
(1, 'EASY', 'Kết quả của 100 - (20 + 30) là?', '110', '50', '60', '40', 'B'),
(1, 'EASY', 'Số chục của số 345 là?', '3', '4', '5', '34', 'B'),
(1, 'EASY', 'Phân số rút gọn của 10/20 là?', '1/2', '2/4', '5/10', '1/3', 'A'),
(1, 'EASY', '1 giờ rưỡi bằng bao nhiêu phút?', '60', '80', '90', '120', 'C'),
(1, 'EASY', 'Gấp 3 lần số 12 ta được số nào?', '36', '24', '15', '48', 'A'),
(1, 'EASY', 'Nửa tá là bao nhiêu cái?', '5', '6', '10', '12', 'B'),

-- ==========================================
-- MÔN TOÁN (subject_id = 1) - MỨC ĐỘ TRUNG BÌNH (20 câu)
-- ==========================================
(1, 'MEDIUM', 'Nghiệm của phương trình 2x - 6 = 0 là?', 'x = 2', 'x = 3', 'x = 4', 'x = -3', 'B'),
(1, 'MEDIUM', 'Giải phương trình: x + 15 = 3x - 5', 'x = 10', 'x = -10', 'x = 5', 'x = 20', 'A'),
(1, 'MEDIUM', 'Trung bình cộng của 10, 15, và 20 là?', '10', '12', '15', '20', 'C'),
(1, 'MEDIUM', 'Tính 20% của 250?', '20', '25', '50', '100', 'C'),
(1, 'MEDIUM', 'Diện tích hình tam giác có đáy 10cm, chiều cao 5cm là?', '50 cm2', '25 cm2', '15 cm2', '30 cm2', 'B'),
(1, 'MEDIUM', 'Một chiếc áo giá 200.000đ giảm giá 10% còn bao nhiêu tiền?', '180.000đ', '190.000đ', '150.000đ', '100.000đ', 'A'),
(1, 'MEDIUM', 'Thể tích khối lập phương cạnh 3cm là?', '9 cm3', '18 cm3', '27 cm3', '81 cm3', 'C'),
(1, 'MEDIUM', 'Số nguyên tố nhỏ nhất là?', '0', '1', '2', '3', 'C'),
(1, 'MEDIUM', 'Đổi 2.5 giờ ra phút ta được?', '120 phút', '150 phút', '130 phút', '140 phút', 'B'),
(1, 'MEDIUM', 'Tìm x biết: 5/x = 1/2', 'x = 2', 'x = 5', 'x = 10', 'x = 2.5', 'C'),
(1, 'MEDIUM', 'Tam giác vuông có hai cạnh góc vuông là 3 và 4. Cạnh huyền bằng?', '5', '6', '7', '25', 'A'),
(1, 'MEDIUM', 'Tổng các góc trong một tam giác bằng bao nhiêu độ?', '90', '180', '270', '360', 'B'),
(1, 'MEDIUM', 'Nếu x^2 = 64 thì x bằng?', '8', '-8', '8 hoặc -8', 'Chỉ 64', 'C'),
(1, 'MEDIUM', 'Tập hợp các ước tự nhiên của 6 là?', '{1, 2, 3}', '{1, 2, 3, 6}', '{2, 3}', '{1, 6}', 'B'),
(1, 'MEDIUM', 'Phương trình x^2 - 4x + 4 = 0 có nghiệm là?', 'x = -2', 'x = 2', 'x = 4', 'Vô nghiệm', 'B'),
(1, 'MEDIUM', 'Tính tổng 1 + 2 + 3 + ... + 10?', '50', '55', '60', '45', 'B'),
(1, 'MEDIUM', 'Tỉ lệ bản đồ 1:1000, 5cm trên bản đồ tương ứng bao nhiêu ngoài thực tế?', '5m', '50m', '500m', '5km', 'B'),
(1, 'MEDIUM', 'Nếu tung một con xúc xắc, xác suất ra mặt chẵn là?', '1/6', '1/3', '1/2', '2/3', 'C'),
(1, 'MEDIUM', 'Một hình tròn có bán kính R=5. Chu vi là? (Pi ~ 3.14)', '15.7', '31.4', '78.5', '3.14', 'B'),
(1, 'MEDIUM', 'Phân số 3/4 viết dưới dạng số thập phân là?', '0.34', '3.4', '0.75', '7.5', 'C'),

-- ==========================================
-- MÔN TOÁN (subject_id = 1) - MỨC ĐỘ KHÓ (20 câu)
-- ==========================================
(1, 'HARD', 'Đạo hàm của hàm số y = sin(x) là?', 'cos(x)', '-cos(x)', 'tan(x)', '-sin(x)', 'A'),
(1, 'HARD', 'Tích phân từ 0 đến 1 của x^2 dx bằng?', '1/2', '1/3', '1', '2/3', 'B'),
(1, 'HARD', 'Giới hạn lim(x->0) của (sin x / x) bằng?', '0', '1', 'Vô cực', 'Không tồn tại', 'B'),
(1, 'HARD', 'Nghiệm của hệ phương trình x+y=5 và x-y=1 là?', '(2,3)', '(3,2)', '(4,1)', '(1,4)', 'B'),
(1, 'HARD', 'Tập xác định của hàm số y = log_2(x-1) là?', 'x > 0', 'x > 1', 'x >= 1', 'Mọi x', 'B'),
(1, 'HARD', 'Phương trình tiếp tuyến của y = x^2 tại điểm x=1 là?', 'y = 2x - 1', 'y = 2x + 1', 'y = x - 1', 'y = x + 1', 'A'),
(1, 'HARD', 'Cấp số cộng có u1=2, công sai d=3. Số hạng thứ 5 là?', '11', '14', '17', '15', 'B'),
(1, 'HARD', 'Đạo hàm cấp 2 của y = x^3 là?', '3x^2', '6x', '6', 'x', 'B'),
(1, 'HARD', 'Số phức liên hợp của z = 3 - 4i là?', '-3 + 4i', '3 + 4i', '-3 - 4i', '4 - 3i', 'B'),
(1, 'HARD', 'Thể tích khối chóp có diện tích đáy B=6, chiều cao h=4 là?', '24', '12', '8', '10', 'C'),
(1, 'HARD', 'Khoảng cách từ điểm M(1,2) đến đường thẳng x - y + 3 = 0 là?', 'sqrt(2)', '2', '3', '2*sqrt(2)', 'A'),
(1, 'HARD', 'Giải bất phương trình: x^2 - 5x + 6 < 0', 'x < 2', 'x > 3', '2 < x < 3', 'x < 2 hoặc x > 3', 'C'),
(1, 'HARD', 'Hàm số y = x^3 - 3x có cực tiểu tại x bằng?', '-1', '1', '0', '3', 'B'),
(1, 'HARD', 'Có bao nhiêu cách xếp 5 học sinh vào 5 ghế trống?', '120', '25', '5', '24', 'A'),
(1, 'HARD', 'Giá trị lớn nhất của hàm số y = -x^2 + 4x trên R là?', '2', '4', '0', 'Vô cực', 'B'),
(1, 'HARD', 'Đồ thị hàm số y = (x+1)/(x-1) có tiệm cận đứng là?', 'x = 1', 'y = 1', 'x = -1', 'y = -1', 'A'),
(1, 'HARD', 'Mô-đun của số phức z = 3 + 4i bằng?', '5', '7', '25', '1', 'A'),
(1, 'HARD', 'Nghiệm của phương trình 2^x = 8 là?', 'x = 2', 'x = 3', 'x = 4', 'x = 8', 'B'),
(1, 'HARD', 'Diện tích mặt cầu có bán kính R=2 là?', '8*pi', '16*pi', '32*pi/3', '4*pi', 'B'),
(1, 'HARD', 'Cho tam giác ABC có a=5, b=6, c=7. Tính cosA?', '1/5', '5/7', '2/3', '1/2', 'C'),

-- ==========================================
-- MÔN TIẾNG ANH (subject_id = 2) - MỨC ĐỘ DỄ (20 câu)
-- ==========================================
(2, 'EASY', 'Hello, what _____ your name?', 'am', 'is', 'are', 'be', 'B'),
(2, 'EASY', 'I _____ from Vietnam.', 'is', 'am', 'are', 'has', 'B'),
(2, 'EASY', '_____ you like apples?', 'Do', 'Does', 'Are', 'Is', 'A'),
(2, 'EASY', 'She _____ to school every day.', 'go', 'goes', 'going', 'went', 'B'),
(2, 'EASY', 'They _____ playing soccer now.', 'is', 'am', 'are', 'be', 'C'),
(2, 'EASY', 'My mother _____ a teacher.', 'are', 'is', 'am', 'be', 'B'),
(2, 'EASY', 'We have two _____.', 'cat', 'cats', 'cates', 'caties', 'B'),
(2, 'EASY', 'This is _____ apple.', 'a', 'an', 'the', 'some', 'B'),
(2, 'EASY', '_____ is your favorite color? - Red.', 'Who', 'Where', 'What', 'When', 'C'),
(2, 'EASY', 'I don’t have _____ money.', 'some', 'any', 'many', 'a', 'B'),
(2, 'EASY', 'The book is _____ the table.', 'on', 'in', 'under', 'at', 'A'),
(2, 'EASY', 'He _____ television yesterday.', 'watch', 'watches', 'watched', 'watching', 'C'),
(2, 'EASY', 'Can you _____ English?', 'speak', 'speaks', 'spoke', 'speaking', 'A'),
(2, 'EASY', 'I will _____ you tomorrow.', 'see', 'saw', 'seen', 'seeing', 'A'),
(2, 'EASY', 'There _____ three chairs in the room.', 'is', 'are', 'am', 'be', 'B'),
(2, 'EASY', 'What time _____ it?', 'am', 'are', 'is', 'has', 'C'),
(2, 'EASY', 'Please open _____ door.', 'a', 'an', 'the', 'some', 'C'),
(2, 'EASY', 'My birthday is _____ May.', 'on', 'in', 'at', 'of', 'B'),
(2, 'EASY', 'He is _____ doctor.', 'a', 'an', 'the', 'some', 'A'),
(2, 'EASY', '_____ old are you?', 'What', 'Where', 'How', 'Who', 'C'),

-- ==========================================
-- MÔN TIẾNG ANH (subject_id = 2) - MỨC ĐỘ TRUNG BÌNH (20 câu)
-- ==========================================
(2, 'MEDIUM', 'If it rains, we _____ at home.', 'stay', 'will stay', 'stayed', 'would stay', 'B'),
(2, 'MEDIUM', 'She is taller _____ her sister.', 'as', 'than', 'to', 'then', 'B'),
(2, 'MEDIUM', 'I have lived here _____ 2010.', 'since', 'for', 'in', 'from', 'A'),
(2, 'MEDIUM', 'They haven’t finished their homework _____.', 'already', 'just', 'yet', 'still', 'C'),
(2, 'MEDIUM', 'The window was broken _____ the boy.', 'with', 'by', 'from', 'in', 'B'),
(2, 'MEDIUM', 'You should _____ smoking.', 'give up', 'take off', 'look for', 'put on', 'A'),
(2, 'MEDIUM', 'I look forward to _____ you soon.', 'see', 'seeing', 'saw', 'be seeing', 'B'),
(2, 'MEDIUM', 'She told me she _____ tired.', 'is', 'were', 'was', 'has been', 'C'),
(2, 'MEDIUM', 'He _____ working here for 5 years.', 'has been', 'is', 'was', 'have been', 'A'),
(2, 'MEDIUM', 'Do you mind _____ the window?', 'open', 'to open', 'opening', 'opened', 'C'),
(2, 'MEDIUM', 'If I had money, I _____ a new car.', 'will buy', 'buy', 'would buy', 'bought', 'C'),
(2, 'MEDIUM', 'This is the most _____ book I have ever read.', 'interest', 'interested', 'interesting', 'interests', 'C'),
(2, 'MEDIUM', 'He is used to _____ up early.', 'get', 'getting', 'got', 'gets', 'B'),
(2, 'MEDIUM', 'I wish I _____ speak French fluently.', 'can', 'will', 'could', 'shall', 'C'),
(2, 'MEDIUM', 'The movie was boring, _____ we left early.', 'because', 'but', 'so', 'although', 'C'),
(2, 'MEDIUM', 'She asked me where I _____.', 'live', 'lived', 'am living', 'have lived', 'B'),
(2, 'MEDIUM', 'We had to cancel the match _____ the bad weather.', 'because', 'because of', 'despite', 'although', 'B'),
(2, 'MEDIUM', 'It’s important _____ on time.', 'to be', 'being', 'be', 'been', 'A'),
(2, 'MEDIUM', 'He let me _____ his laptop.', 'to use', 'using', 'use', 'used', 'C'),
(2, 'MEDIUM', 'I didn’t go to the party _____ I was sick.', 'because', 'so', 'but', 'and', 'A'),

-- ==========================================
-- MÔN TIẾNG ANH (subject_id = 2) - MỨC ĐỘ KHÓ (20 câu)
-- ==========================================
(2, 'HARD', 'Hardly had I arrived _____ it started to rain.', 'when', 'than', 'that', 'then', 'A'),
(2, 'HARD', 'Not only _____ late, but he also forgot his books.', 'did he come', 'he came', 'comes he', 'he did come', 'A'),
(2, 'HARD', 'If she had studied harder, she _____ the exam.', 'would pass', 'will pass', 'would have passed', 'passed', 'C'),
(2, 'HARD', 'It is imperative that everyone _____ the meeting.', 'attends', 'attend', 'attended', 'attending', 'B'),
(2, 'HARD', 'By this time next year, I _____ my degree.', 'will finish', 'finish', 'will have finished', 'have finished', 'C'),
(2, 'HARD', 'The manager objected _____ the new proposal.', 'to accept', 'accepting', 'to accepting', 'accept', 'C'),
(2, 'HARD', '_____ all his wealth, he is not happy.', 'Despite', 'Although', 'In spite', 'Even though', 'A'),
(2, 'HARD', 'We regret _____ you that your application has been rejected.', 'to inform', 'informing', 'inform', 'informed', 'A'),
(2, 'HARD', 'No sooner had they left the building _____ the bomb exploded.', 'than', 'when', 'before', 'that', 'A'),
(2, 'HARD', 'The man _____ car was stolen called the police.', 'who', 'whom', 'whose', 'which', 'C'),
(2, 'HARD', 'He speaks English as if he _____ a native speaker.', 'is', 'were', 'has been', 'had been', 'B'),
(2, 'HARD', 'Little _____ about his true intentions.', 'I knew', 'did I know', 'I did know', 'knew I', 'B'),
(2, 'HARD', 'The project was successful, _____ our expectations.', 'beyond', 'over', 'above', 'exceeding', 'A'),
(2, 'HARD', 'It’s high time you _____ looking for a job.', 'start', 'started', 'have started', 'had started', 'B'),
(2, 'HARD', 'But for his help, I _____ the project.', 'couldn’t finish', 'didn’t finish', 'wouldn’t have finished', 'won’t finish', 'C'),
(2, 'HARD', 'She denied _____ the money.', 'to steal', 'stealing', 'steal', 'stolen', 'B'),
(2, 'HARD', 'The longer you wait, _____ it gets.', 'the harder', 'harder', 'the hardest', 'hardest', 'A'),
(2, 'HARD', 'Make sure you _____ the form correctly.', 'fill in', 'fill up', 'fill on', 'fill with', 'A'),
(2, 'HARD', 'Rarely _____ such a beautiful sunset.', 'I have seen', 'have I seen', 'did I see', 'I see', 'B'),
(2, 'HARD', 'He is considered _____ the greatest artist of his time.', 'being', 'to be', 'as being', 'be', 'B');