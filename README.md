# 🐍 Python Learning Playground

Ứng dụng web tương tác giúp học Python qua trực quan hóa các khái niệm cơ bản.

## ✨ Tính năng

### 📚 7 Modules chính:

1. **🔢 Operations & Data Types**
   - So sánh `/`, `//`, `%`
   - Operator precedence
   - Type conversion
   - Float precision demo

2. **🔄 Loops Animator**
   - For loop visualization
   - While loop simulator
   - Nested loops patterns

3. **📦 Data Structures**
   - Interactive List operations
   - Dictionary playground
   - Set operations với Venn diagram
   - Tuple immutability demo

4. **🎯 Functions Visualizer**
   - Function execution tracker
   - Recursion tree (Fibonacci)

5. **🧮 NumPy Arrays**
   - Array creation methods
   - Array operations
   - Broadcasting visualization

6. **📊 Matplotlib Plotter**
   - Interactive line plots
   - Bar charts
   - Scatter plots

7. **🎓 Quiz & Challenges**
   - Multiple choice quiz
   - Coding challenges

## 🚀 Chạy Local

### Cách 1: Trực tiếp với Python

```bash
# Clone hoặc download code
cd python-learning-playground

# Cài đặt dependencies
pip install -r requirements.txt

# Chạy ứng dụng
streamlit run app.py
```

Mở trình duyệt tại: `http://localhost:8501`

### Cách 2: Với Virtual Environment (Khuyến nghị)

```bash
# Tạo virtual environment
python -m venv venv

# Kích hoạt
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Cài đặt dependencies
pip install -r requirements.txt

# Chạy
streamlit run app.py
```

## 🌐 Deploy lên Cloud

### Option 1: Streamlit Community Cloud (Khuyến nghị - MIỄN PHÍ)

1. Push code lên GitHub repository
2. Truy cập [share.streamlit.io](https://share.streamlit.io)
3. Đăng nhập bằng GitHub
4. Click "New app"
5. Chọn repository, branch, và file `app.py`
6. Click "Deploy"

**✅ Ưu điểm:**
- Hoàn toàn miễn phí
- Deploy cực nhanh (< 5 phút)
- Auto-update khi push code
- Có sẵn URL public

### Option 2: Heroku

```bash
# Cần thêm 2 files:

# 1. Procfile
echo "web: streamlit run app.py --server.port=$PORT" > Procfile

# 2. setup.sh
cat > setup.sh << 'EOF'
mkdir -p ~/.streamlit/
echo "[server]
headless = true
port = $PORT
enableCORS = false
" > ~/.streamlit/config.toml
EOF

# Deploy
heroku create your-app-name
git push heroku main
```

### Option 3: Render (MIỄN PHÍ)

1. Push code lên GitHub
2. Truy cập [render.com](https://render.com)
3. Tạo "New Web Service"
4. Connect GitHub repo
5. Build Command: `pip install -r requirements.txt`
6. Start Command: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`

## ⚠️ Lưu ý về Netlify

**Netlify KHÔNG hỗ trợ Streamlit!** 

Netlify chỉ host static sites (HTML/CSS/JS), không chạy Python server.

**Các nền tảng phù hợp:**
- ✅ **Streamlit Cloud** (Tốt nhất, miễn phí)
- ✅ Heroku (Có free tier)
- ✅ Render (Miễn phí)
- ✅ Railway
- ✅ Google Cloud Run
- ❌ Netlify (Không hỗ trợ)
- ❌ Vercel (Giới hạn cho Python)

## 📁 Cấu trúc Project

```
python-learning-playground/
│
├── app.py                 # Main Streamlit app
├── requirements.txt       # Python dependencies
├── README.md             # Documentation
└── .gitignore           # Git ignore file
```

## 🛠️ Customization

### Thêm Module mới:

```python
elif module == "🆕 Module X: New Topic":
    st.header("🆕 Module X: New Topic")
    # Your code here
```

### Thêm Quiz questions:

Tìm section `questions = [...]` trong Module 7 và thêm:

```python
{
    "question": "Câu hỏi của bạn?",
    "options": ["A", "B", "C", "D"],
    "correct": 0,  # Index of correct answer
    "explanation": "Giải thích..."
}
```

## 🐛 Troubleshooting

### Lỗi: ModuleNotFoundError

```bash
pip install -r requirements.txt
```

### Lỗi: Port already in use

```bash
streamlit run app.py --server.port 8502
```

### Matplotlib không hiển thị

```bash
pip install --upgrade matplotlib
```

## 📖 Tài liệu tham khảo

- [Streamlit Documentation](https://docs.streamlit.io)
- [NumPy Documentation](https://numpy.org/doc/)
- [Matplotlib Documentation](https://matplotlib.org/stable/index.html)
- [Plotly Documentation](https://plotly.com/python/)

## 🤝 Contributing

Contributions are welcome! 

1. Fork repository
2. Tạo feature branch
3. Commit changes
4. Push to branch
5. Tạo Pull Request

## 📝 License

MIT License - Feel free to use for educational purposes!

## 💡 Tips

- Sử dụng sidebar để navigate giữa các modules
- Mỗi module có nhiều tabs để explore
- Thử thay đổi parameters và xem kết quả real-time
- Làm quiz để test kiến thức
- Try coding challenges!

## 📧 Contact

Có câu hỏi? Tạo issue trên GitHub!

---

**Made with ❤️ for Python learners**
