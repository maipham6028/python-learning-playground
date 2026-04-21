# 🐍 Python Learning Playground v2.0

Ứng dụng học Python với **Login, Quiz, Code Grader, Leaderboard**!

## ✨ Tính năng

### 🔐 **Authentication System**
- Đăng ký tài khoản (Email + Password)
- Đăng nhập bảo mật (SHA-256 hashing)
- Session management

### 📚 **10 Chapters học Python**
1. Introduction to Python
2. Operations & Syntax
3. Conditionals
4. Loops
5. Functions
6. Data Structures
7. OOP
8. Exception Handling
9. NumPy
10. Pandas & Matplotlib

### 📝 **Quiz System (Quizizz-style)**
- 100+ câu hỏi trắc nghiệm (10 câu/chương)
- Timer cho mỗi câu
- Điểm & bảng xếp hạng
- Giải thích chi tiết sau mỗi câu
- Lưu điểm cao nhất

### 💻 **Code Challenges với Auto-Grader**
- 25+ bài tập code (2-3 bài/chương)
- Độ khó: Easy / Medium / Hard
- **Auto-grading** với test cases
- Hints khi stuck
- Không cần AI - test cases chính xác!

### 🏆 **Gamification**
- **Leaderboard** toàn cục
- **Achievements/Badges** (9 loại)
- **Level system** (500 points/level)
- **Streak tracking**

### 👤 **Profile & Progress**
- Dashboard cá nhân
- Theo dõi tiến độ 10 chương
- Xem lịch sử quiz
- Thống kê chi tiết

## 🚀 Cấu trúc Project

```
python-learning-playground/
│
├── app.py                  # Main Streamlit app
├── database.py             # SQLite database operations
├── quiz_data.py            # 100+ quiz questions
├── code_challenges.py      # Code challenges + grader
├── requirements.txt        # Dependencies
└── python_playground.db    # SQLite DB (auto-created)
```

## 💾 Dependencies

```
streamlit
pandas
numpy
```

Chỉ 3 thư viện! Siêu nhẹ và nhanh!

## 🚀 Chạy Local

```bash
# Cài đặt
pip install -r requirements.txt

# Chạy
streamlit run app.py
```

Mở: `http://localhost:8501`

## 🌐 Deploy lên Streamlit Cloud

### **Bước 1: Push code lên GitHub**

```bash
git add .
git commit -m "v2.0: Add authentication, quiz, code grader"
git push
```

### **Bước 2: Streamlit tự động rebuild**

App của bạn sẽ được cập nhật tự động!

## 🎯 Cách sử dụng

### **Lần đầu:**
1. Truy cập app
2. Click tab **"Đăng ký"**
3. Tạo tài khoản (username + email + password)
4. Đăng nhập

### **Học tập:**
1. **Dashboard**: Xem tiến độ tổng thể
2. **Quiz**: Làm trắc nghiệm 10 câu/chương
3. **Code Challenges**: Code thử, auto-grading
4. **Leaderboard**: Xem top học viên
5. **Profile**: Xem achievements

## 🏆 Hệ thống điểm

| Hoạt động | Điểm |
|-----------|------|
| Trả lời đúng 1 câu quiz | +10 points |
| Hoàn thành 1 code challenge | +20 points |
| Level up | Mỗi 500 points |

## 🎨 Tính năng sắp có (v3.0)

- [ ] AI Code Review (khi có budget)
- [ ] Friends system
- [ ] Study groups
- [ ] Daily challenges
- [ ] Certificates

## 🐛 Troubleshooting

### Database lỗi:
```bash
rm python_playground.db
# Chạy lại app, DB sẽ được tạo mới
```

### Package lỗi:
```bash
pip install --upgrade streamlit pandas numpy
```

## 📝 License

MIT License - Free for educational use!

---

**Made with ❤️ for Python learners**
