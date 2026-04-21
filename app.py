import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from io import StringIO
import sys
import time

# Page config
st.set_page_config(
    page_title="Python Learning Playground",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 1rem;
    }
    .module-card {
        background: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .code-output {
        background: #1e1e1e;
        color: #d4d4d4;
        padding: 1rem;
        border-radius: 5px;
        font-family: 'Courier New', monospace;
    }
    .highlight {
        background-color: yellow;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-header"> Python Learning Playground</h1>', unsafe_allow_html=True)
st.markdown("### Trực quan hóa các khái niệm Python cơ bản")

# Sidebar
with st.sidebar:
    st.image("https://www.python.org/static/community_logos/python-logo-master-v3-TM.png", width=200)
    st.markdown("##  Chọn Module")
    
    module = st.radio(
        "Chọn chủ đề:",
        [
            "🏠 Trang chủ",
            "🔢 Module 1: Operations & Data Types",
            "🔄 Module 2: Loops Animator",
            "📦 Module 3: Data Structures",
            "🎯 Module 4: Functions Visualizer",
            "🧮 Module 5: NumPy Arrays",
            "📊 Module 6: Matplotlib Plotter",
            "🎓 Module 7: Quiz & Challenges"
        ]
    )
    
    st.markdown("---")
    st.markdown("### 💡 Về ứng dụng")
    st.info("Ứng dụng giúp học Python qua trực quan hóa các khái niệm cơ bản.")

# =============================================================================
# HOME PAGE
# =============================================================================
if module == "🏠 Trang chủ":
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("###  Tính năng chính")
        st.markdown("""
        -  Trực quan hóa các phép toán Python
        -  Mô phỏng vòng lặp từng bước
        -  Thao tác với Data Structures
        -  Visualize NumPy arrays
        -  Vẽ đồ thị tương tác
        -  Quiz và thử thách code
        """)
    
    with col2:
        st.markdown("### Nội dung học")
        st.markdown("""
        1. **Operations & Types**: int, float, str, bool
        2. **Loops**: for, while, nested loops
        3. **Data Structures**: List, Dict, Set, Tuple
        4. **Functions**: def, parameters, return
        5. **NumPy**: Arrays, slicing, operations
        6. **Matplotlib**: Plotting và visualization
        """)
    
    st.markdown("---")
    st.success(" Chọn một module từ sidebar để bắt đầu!")
    
    # Statistics
    st.markdown("###  Thống kê nhanh")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Modules", "7", "+2")
    col2.metric("Bài tập", "25+", "+5")
    col3.metric("Ví dụ", "50+", "+10")
    col4.metric("Quiz", "20+", "+3")

# =============================================================================
# MODULE 1: OPERATIONS & DATA TYPES
# =============================================================================
elif module == "🔢 Module 1: Operations & Data Types":
    st.header("🔢 Module 1: Operations & Data Types")
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "Division Types", 
        "Operator Precedence", 
        "Type Conversion",
        "Float Precision"
    ])
    
    # TAB 1: Division Types
    with tab1:
        st.subheader("So sánh các loại phép chia: `/` vs `//` vs `%`")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            dividend = st.number_input("Số bị chia", value=7, step=1)
            divisor = st.number_input("Số chia", value=2, step=1, min_value=1)
            
            if st.button("Tính toán", key="division"):
                regular_div = dividend / divisor
                floor_div = dividend // divisor
                modulus = dividend % divisor
                
                st.markdown("### Kết quả:")
                st.code(f"""
{dividend} / {divisor}  = {regular_div}    (Chia thông thường - luôn trả về float)
{dividend} // {divisor} = {floor_div}      (Chia lấy phần nguyên)
{dividend} % {divisor}  = {modulus}       (Chia lấy phần dư)
                """)
                
                # Verification
                st.info(f"✅ Kiểm tra: {divisor} × {floor_div} + {modulus} = {divisor * floor_div + modulus} = {dividend}")
        
        with col2:
            # Visualization
            if divisor > 0:
                fig = go.Figure()
                
                # Full bars
                num_full_bars = int(dividend // divisor)
                remainder = dividend % divisor
                
                for i in range(num_full_bars):
                    fig.add_trace(go.Bar(
                        x=[i],
                        y=[divisor],
                        name=f"Nhóm {i+1}",
                        marker_color='#667eea',
                        text=f"{divisor}",
                        textposition='inside'
                    ))
                
                if remainder > 0:
                    fig.add_trace(go.Bar(
                        x=[num_full_bars],
                        y=[remainder],
                        name="Phần dư",
                        marker_color='#f093fb',
                        text=f"{remainder}",
                        textposition='inside'
                    ))
                
                fig.update_layout(
                    title=f"Visualize: {dividend} chia cho {divisor}",
                    xaxis_title="Nhóm",
                    yaxis_title="Giá trị",
                    showlegend=True,
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
    
    # TAB 2: Operator Precedence
    with tab2:
        st.subheader("🔢 Thứ tự ưu tiên của toán tử")
        
        st.markdown("""
        **Thứ tự ưu tiên (từ cao xuống thấp):**
        1. `**` (Lũy thừa)
        2. `*, /, //, %` (Nhân, chia)
        3. `+, -` (Cộng, trừ)
        4. `==, !=, <, >, <=, >=` (So sánh)
        5. `not, and, or` (Logic)
        """)
        
        expression = st.text_input(
            "Nhập biểu thức (ví dụ: 2 + 3 * 4, 2 ** 3 ** 2):",
            value="2 + 3 * 4"
        )
        
        if st.button("Tính toán từng bước", key="precedence"):
            try:
                result = eval(expression)
                st.success(f"### Kết quả: `{expression}` = **{result}**")
                
                # Show step by step
                st.markdown("#### 📝 Giải thích:")
                
                if "**" in expression:
                    st.markdown("1. ✅ **Lũy thừa** (`**`) được tính trước")
                if "*" in expression or "/" in expression:
                    st.markdown("2. ✅ **Nhân/Chia** (`*`, `/`, `//`, `%`) được tính tiếp")
                if "+" in expression or "-" in expression:
                    st.markdown("3. ✅ **Cộng/Trừ** (`+`, `-`) được tính sau cùng")
                
                # Example visualization
                col1, col2 = st.columns(2)
                with col1:
                    st.code(f"""
# Không có ngoặc:
{expression} = {result}
                    """)
                
                with col2:
                    # Suggest with parentheses
                    st.markdown("**💡 Khuyến nghị: Dùng ngoặc để rõ ràng hơn**")
                    if "+" in expression and "*" in expression:
                        parts = expression.split("+")
                        if len(parts) == 2:
                            suggested = f"({parts[0].strip()}) + ({parts[1].strip()})"
                            st.code(f"{suggested}")
                
            except Exception as e:
                st.error(f"❌ Lỗi: {e}")
    
    # TAB 3: Type Conversion
    with tab3:
        st.subheader(" Chuyển đổi kiểu dữ liệu")
        
        col1, col2 = st.columns(2)
        
        with col1:
            input_value = st.text_input("Nhập giá trị:", value="42")
            conversion_type = st.selectbox(
                "Chuyển sang kiểu:",
                ["int()", "float()", "str()", "bool()"]
            )
            
            if st.button("Chuyển đổi", key="convert"):
                try:
                    original_type = type(eval(input_value)).__name__
                    
                    if conversion_type == "int()":
                        result = int(eval(input_value))
                    elif conversion_type == "float()":
                        result = float(eval(input_value))
                    elif conversion_type == "str()":
                        result = str(eval(input_value))
                    elif conversion_type == "bool()":
                        result = bool(eval(input_value))
                    
                    st.success(f"✅ Kết quả: `{result}` (type: {type(result).__name__})")
                    
                    # Show conversion flow
                    st.markdown("### Quá trình chuyển đổi:")
                    st.code(f"""
Giá trị gốc: {input_value} ({original_type})
      ↓
{conversion_type}
      ↓
Kết quả: {result} ({type(result).__name__})
                    """)
                    
                except Exception as e:
                    st.error(f"❌ Không thể chuyển đổi: {e}")
        
        with col2:
            st.markdown("###  Bảng chuyển đổi phổ biến")
            
            conversion_table = pd.DataFrame({
                'Từ': ['int', 'float', 'str', 'bool'],
                'int()': ['✓', '✓ (làm tròn)', '✓ (nếu là số)', '1 hoặc 0'],
                'float()': ['✓', '✓', '✓ (nếu là số)', '1.0 hoặc 0.0'],
                'str()': ['✓', '✓', '✓', '"True" / "False"'],
                'bool()': ['False nếu 0', 'False nếu 0.0', 'False nếu ""', '✓']
            })
            
            st.dataframe(conversion_table, use_container_width=True)
            
            st.warning("""
            ⚠️ **Lưu ý:**
            - `int("3.14")` → ❌ Lỗi! Phải dùng `int(float("3.14"))`
            - `int("hello")` → ❌ Lỗi!
            - `bool(0)` → False, `bool(1)` → True
            - `bool("")` → False, `bool("any string")` → True
            """)
    
    # TAB 4: Float Precision
    with tab4:
        st.subheader("🔬 Vấn đề độ chính xác Float")
        
        st.markdown("""
        ### Tại sao `0.1 + 0.2 ≠ 0.3` trong Python?
        
        Máy tính lưu trữ số thập phân dưới dạng **nhị phân (binary)**. 
        Một số số thập phân không thể biểu diễn chính xác trong hệ nhị phân.
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            num1 = st.number_input("Số thứ nhất:", value=0.1, format="%.10f")
            num2 = st.number_input("Số thứ hai:", value=0.2, format="%.10f")
            
            if st.button("Tính tổng", key="float_precision"):
                result = num1 + num2
                expected = 0.3
                
                st.code(f"""
{num1} + {num2} = {result}

Giá trị thật sự: {result:.20f}
Giá trị mong đợi: {expected:.20f}
                """)
                
                if abs(result - expected) < 1e-10:
                    st.success("✅ Kết quả gần đúng!")
                else:
                    st.warning(f"⚠️ Có sai số: {result - expected:.20e}")
        
        with col2:
            st.markdown("### 💡 Giải pháp:")
            
            st.code("""
# 1. Dùng round()
result = round(0.1 + 0.2, 2)  # 0.3

# 2. Dùng decimal module (chính xác hơn)
from decimal import Decimal

a = Decimal('0.1')
b = Decimal('0.2')
result = a + b  # Exactly 0.3

# 3. So sánh với tolerance
import math
math.isclose(0.1 + 0.2, 0.3)  # True
            """)
            
            st.info("""
            **Khi nào cần cẩn thận:**
            - Tính toán tài chính (tiền)
            - So sánh số thực
            - Tính toán khoa học chính xác
            """)

# =============================================================================
# MODULE 2: LOOPS ANIMATOR
# =============================================================================
elif module == "🔄 Module 2: Loops Animator":
    st.header("🔄 Module 2: Loops Animator")
    
    tab1, tab2, tab3 = st.tabs(["For Loop", "While Loop", "Nested Loops"])
    
    # TAB 1: For Loop
    with tab1:
        st.subheader("🔁 For Loop Animator")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            loop_type = st.radio(
                "Chọn kiểu for loop:",
                ["range()", "List iteration", "String iteration"]
            )
            
            if loop_type == "range()":
                start = st.number_input("Start:", value=0, step=1)
                end = st.number_input("End:", value=5, step=1)
                step = st.number_input("Step:", value=1, step=1, min_value=1)
                
                code = f"for i in range({start}, {end}, {step}):\n    print(i)"
                items = list(range(start, end, step))
                
            elif loop_type == "List iteration":
                list_input = st.text_input("Nhập list (cách nhau bởi dấu phẩy):", value="apple, banana, cherry")
                items = [x.strip() for x in list_input.split(",")]
                code = f"items = {items}\nfor item in items:\n    print(item)"
                
            else:  # String iteration
                string_input = st.text_input("Nhập chuỗi:", value="Python")
                items = list(string_input)
                code = f"text = '{string_input}'\nfor char in text:\n    print(char)"
            
            st.code(code, language="python")
            
            if st.button("▶️ Chạy Animation", key="for_loop"):
                progress_bar = st.progress(0)
                status_text = st.empty()
                result_container = st.empty()
                
                results = []
                for i, item in enumerate(items):
                    progress = (i + 1) / len(items)
                    progress_bar.progress(progress)
                    status_text.text(f"Iteration {i+1}/{len(items)}: {item}")
                    results.append(str(item))
                    time.sleep(0.5)
                
                result_container.success(f"✅ Hoàn thành! Output: {results}")
        
        with col2:
            st.markdown("### 📊 Visualization")
            
            if 'items' in locals():
                # Create visualization
                fig = go.Figure()
                
                for i, item in enumerate(items):
                    fig.add_trace(go.Bar(
                        x=[i],
                        y=[1],
                        text=str(item),
                        textposition='inside',
                        name=f"Iteration {i}",
                        marker_color=px.colors.qualitative.Plotly[i % len(px.colors.qualitative.Plotly)]
                    ))
                
                fig.update_layout(
                    title="Các phần tử được lặp qua",
                    xaxis_title="Index",
                    yaxis_title="",
                    showlegend=False,
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Show iterations table
                st.markdown("### 📋 Bảng iterations")
                iterations_df = pd.DataFrame({
                    'Iteration': range(len(items)),
                    'Value': items,
                    'Type': [type(x).__name__ for x in items]
                })
                st.dataframe(iterations_df, use_container_width=True)
    
    # TAB 2: While Loop
    with tab2:
        st.subheader("🔄 While Loop Simulator")
        
        col1, col2 = st.columns(2)
        
        with col1:
            initial_value = st.number_input("Giá trị khởi tạo:", value=0, step=1)
            condition_type = st.selectbox("Điều kiện:", ["< (nhỏ hơn)", "<= (nhỏ hơn hoặc bằng)", "!= (khác)"])
            target_value = st.number_input("Giá trị đích:", value=5, step=1)
            increment = st.number_input("Bước nhảy (increment):", value=1, step=1)
            
            operator = condition_type.split()[0]
            
            code = f"""
counter = {initial_value}
while counter {operator} {target_value}:
    print(counter)
    counter += {increment}
            """
            
            st.code(code, language="python")
            
            if st.button("▶️ Chạy While Loop", key="while_loop"):
                counter = initial_value
                iterations = []
                
                max_iterations = 100  # Safety limit
                iteration_count = 0
                
                while iteration_count < max_iterations:
                    if operator == "<" and counter >= target_value:
                        break
                    elif operator == "<=" and counter > target_value:
                        break
                    elif operator == "!=" and counter == target_value:
                        break
                    
                    iterations.append(counter)
                    counter += increment
                    iteration_count += 1
                
                st.success(f"✅ Loop chạy {len(iterations)} lần")
                st.code(f"Output: {iterations}")
                
                # Show counter progression
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=list(range(len(iterations))),
                    y=iterations,
                    mode='lines+markers',
                    name='Counter value',
                    line=dict(color='#667eea', width=3),
                    marker=dict(size=10)
                ))
                
                fig.add_hline(y=target_value, line_dash="dash", line_color="red", 
                             annotation_text=f"Target: {target_value}")
                
                fig.update_layout(
                    title="Counter progression",
                    xaxis_title="Iteration",
                    yaxis_title="Counter value",
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### ⚠️ Chú ý về While Loop")
            
            st.warning("""
            **Infinite Loop (Vòng lặp vô hạn):**
            
            While loop có thể chạy mãi nếu điều kiện luôn đúng!
            
            ```python
            # ❌ NGUY HIỂM - Vòng lặp vô hạn
            x = 0
            while x < 10:
                print(x)
                # Quên không tăng x!
            
            # ✅ ĐÚNG
            x = 0
            while x < 10:
                print(x)
                x += 1  # Nhớ cập nhật biến!
            ```
            """)
            
            st.info("""
            **Khi nào dùng While vs For?**
            
            - **For**: Khi biết trước số lần lặp
            - **While**: Khi lặp cho đến khi điều kiện sai
            
            Ví dụ While loop thực tế:
            ```python
            # Đọc input cho đến khi hợp lệ
            password = ""
            while len(password) < 8:
                password = input("Enter password: ")
            ```
            """)
    
    # TAB 3: Nested Loops
    with tab3:
        st.subheader("🔲 Nested Loops (Vòng lặp lồng nhau)")
        
        rows = st.slider("Số hàng:", 1, 10, 5)
        cols = st.slider("Số cột:", 1, 10, 5)
        
        pattern_type = st.selectbox(
            "Chọn pattern:",
            ["Số thứ tự", "Ký tự *", "Bảng nhân", "Chess board"]
        )
        
        code = f"""
for i in range({rows}):
    for j in range({cols}):
        # Pattern logic here
        """
        
        st.code(code, language="python")
        
        if st.button("🎨 Tạo Pattern", key="nested"):
            # Create pattern
            pattern = []
            
            for i in range(rows):
                row = []
                for j in range(cols):
                    if pattern_type == "Số thứ tự":
                        row.append(i * cols + j)
                    elif pattern_type == "Ký tự *":
                        row.append("*")
                    elif pattern_type == "Bảng nhân":
                        row.append((i + 1) * (j + 1))
                    elif pattern_type == "Chess board":
                        row.append("⬛" if (i + j) % 2 == 0 else "⬜")
                pattern.append(row)
            
            # Display as dataframe
            df = pd.DataFrame(pattern)
            st.dataframe(df, use_container_width=True)
            
            # Iteration counter
            total_iterations = rows * cols
            st.info(f"📊 Tổng số iterations: **{rows}** × **{cols}** = **{total_iterations}**")
            
            # Show code with actual values
            st.markdown("### 📝 Code thực tế:")
            if pattern_type == "Bảng nhân":
                actual_code = f"""
for i in range(1, {rows + 1}):
    for j in range(1, {cols + 1}):
        print(f"{{i}} × {{j}} = {{i * j}}", end="\\t")
    print()  # Xuống dòng
                """
                st.code(actual_code, language="python")

# =============================================================================
# MODULE 3: DATA STRUCTURES
# =============================================================================
elif module == "📦 Module 3: Data Structures":
    st.header("📦 Module 3: Data Structures")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Lists", "Dictionaries", "Sets", "Tuples"])
    
    # TAB 1: Lists
    with tab1:
        st.subheader("📝 List Operations")
        
        # Initialize session state for list
        if 'my_list' not in st.session_state:
            st.session_state.my_list = [1, 2, 3, 4, 5]
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown(f"### Current List: `{st.session_state.my_list}`")
            
            operation = st.selectbox(
                "Chọn thao tác:",
                ["append()", "insert()", "remove()", "pop()", "sort()", "reverse()"]
            )
            
            if operation == "append()":
                value = st.text_input("Giá trị cần thêm:", value="6")
                if st.button("Thực hiện"):
                    try:
                        st.session_state.my_list.append(eval(value))
                        st.success(f"✅ Đã thêm {value} vào cuối list")
                    except:
                        st.error("Lỗi!")
            
            elif operation == "insert()":
                index = st.number_input("Vị trí (index):", value=0, step=1)
                value = st.text_input("Giá trị:", value="0")
                if st.button("Thực hiện"):
                    try:
                        st.session_state.my_list.insert(int(index), eval(value))
                        st.success(f"✅ Đã chèn {value} tại vị trí {index}")
                    except:
                        st.error("Lỗi!")
            
            elif operation == "remove()":
                value = st.text_input("Giá trị cần xóa:", value="1")
                if st.button("Thực hiện"):
                    try:
                        st.session_state.my_list.remove(eval(value))
                        st.success(f"✅ Đã xóa {value} khỏi list")
                    except:
                        st.error(f"{value} không có trong list!")
            
            elif operation == "pop()":
                index = st.number_input("Vị trí cần xóa (-1 = cuối):", value=-1, step=1)
                if st.button("Thực hiện"):
                    try:
                        removed = st.session_state.my_list.pop(int(index))
                        st.success(f"✅ Đã xóa {removed}")
                    except:
                        st.error("Index out of range!")
            
            elif operation == "sort()":
                if st.button("Sắp xếp tăng dần"):
                    st.session_state.my_list.sort()
                    st.success("✅ Đã sắp xếp")
            
            elif operation == "reverse()":
                if st.button("Đảo ngược"):
                    st.session_state.my_list.reverse()
                    st.success("✅ Đã đảo ngược")
            
            if st.button("🔄 Reset List"):
                st.session_state.my_list = [1, 2, 3, 4, 5]
                st.rerun()
        
        with col2:
            # Visualize list
            if len(st.session_state.my_list) > 0:
                fig = go.Figure()
                
                fig.add_trace(go.Bar(
                    x=[f"[{i}]" for i in range(len(st.session_state.my_list))],
                    y=st.session_state.my_list,
                    text=st.session_state.my_list,
                    textposition='outside',
                    marker_color='#667eea'
                ))
                
                fig.update_layout(
                    title="List Visualization",
                    xaxis_title="Index",
                    yaxis_title="Value",
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            # List info
            st.markdown("### 📊 Thông tin List:")
            st.code(f"""
Length: {len(st.session_state.my_list)}
Min: {min(st.session_state.my_list) if st.session_state.my_list else 'N/A'}
Max: {max(st.session_state.my_list) if st.session_state.my_list else 'N/A'}
Sum: {sum(st.session_state.my_list) if st.session_state.my_list else 'N/A'}
            """)
    
    # TAB 2: Dictionaries
    with tab2:
        st.subheader("📖 Dictionary Operations")
        
        # Initialize session state
        if 'my_dict' not in st.session_state:
            st.session_state.my_dict = {
                "name": "Alice",
                "age": 25,
                "city": "Hanoi"
            }
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("### Current Dictionary:")
            st.json(st.session_state.my_dict)
            
            dict_operation = st.selectbox(
                "Thao tác:",
                ["Thêm/Sửa key", "Xóa key", "Get value", "Check key exists"]
            )
            
            if dict_operation == "Thêm/Sửa key":
                key = st.text_input("Key:", value="email")
                value = st.text_input("Value:", value="alice@example.com")
                if st.button("Thực hiện", key="dict_add"):
                    st.session_state.my_dict[key] = value
                    st.success(f"✅ Đã thêm/cập nhật '{key}': '{value}'")
                    st.rerun()
            
            elif dict_operation == "Xóa key":
                key = st.text_input("Key cần xóa:", value="age")
                if st.button("Xóa", key="dict_remove"):
                    if key in st.session_state.my_dict:
                        del st.session_state.my_dict[key]
                        st.success(f"✅ Đã xóa '{key}'")
                        st.rerun()
                    else:
                        st.error(f"Key '{key}' không tồn tại!")
            
            elif dict_operation == "Get value":
                key = st.text_input("Key:", value="name")
                if st.button("Lấy giá trị", key="dict_get"):
                    value = st.session_state.my_dict.get(key, "Key not found")
                    st.info(f"Value: **{value}**")
            
            elif dict_operation == "Check key exists":
                key = st.text_input("Key:", value="city")
                if st.button("Kiểm tra", key="dict_check"):
                    exists = key in st.session_state.my_dict
                    if exists:
                        st.success(f"✅ Key '{key}' tồn tại!")
                    else:
                        st.error(f"❌ Key '{key}' không tồn tại!")
            
            if st.button("🔄 Reset Dictionary"):
                st.session_state.my_dict = {
                    "name": "Alice",
                    "age": 25,
                    "city": "Hanoi"
                }
                st.rerun()
        
        with col2:
            # Visualize dictionary as table
            st.markdown("### 📊 Dictionary Table View")
            
            dict_df = pd.DataFrame({
                'Key': list(st.session_state.my_dict.keys()),
                'Value': list(st.session_state.my_dict.values()),
                'Type': [type(v).__name__ for v in st.session_state.my_dict.values()]
            })
            
            st.dataframe(dict_df, use_container_width=True)
            
            # Dictionary methods
            st.markdown("### 🔧 Dictionary Methods")
            st.code("""
# Lấy tất cả keys
keys = my_dict.keys()

# Lấy tất cả values
values = my_dict.values()

# Lấy tất cả items (key-value pairs)
items = my_dict.items()

# Get với default value
value = my_dict.get('key', 'default')
            """, language="python")
    
    # TAB 3: Sets
    with tab3:
        st.subheader("🎯 Set Operations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            set_a_input = st.text_input("Set A (cách nhau bởi dấu phẩy):", value="1, 2, 3, 4, 5")
            set_b_input = st.text_input("Set B (cách nhau bởi dấu phẩy):", value="4, 5, 6, 7, 8")
            
            try:
                set_a = set(eval(f"[{set_a_input}]"))
                set_b = set(eval(f"[{set_b_input}]"))
                
                st.markdown(f"**Set A:** `{set_a}`")
                st.markdown(f"**Set B:** `{set_b}`")
                
            except:
                st.error("Invalid input!")
                set_a = {1, 2, 3}
                set_b = {3, 4, 5}
        
        with col2:
            st.markdown("### 🔢 Set Operations Results:")
            
            union = set_a | set_b
            intersection = set_a & set_b
            difference_ab = set_a - set_b
            difference_ba = set_b - set_a
            symmetric_diff = set_a ^ set_b
            
            st.code(f"""
Union (A ∪ B):           {union}
Intersection (A ∩ B):    {intersection}
Difference (A - B):      {difference_ab}
Difference (B - A):      {difference_ba}
Symmetric Diff (A △ B):  {symmetric_diff}
            """)
        
        # Visualize with Venn diagram
        st.markdown("### 📊 Venn Diagram Visualization")
        
        from matplotlib_venn import venn2
        import matplotlib.pyplot as plt
        
        fig, ax = plt.subplots(figsize=(10, 6))
        venn2([set_a, set_b], set_labels=('Set A', 'Set B'), ax=ax)
        plt.title("Venn Diagram: Set A vs Set B")
        st.pyplot(fig)
        
        st.info("""
        **Set đặc điểm:**
        - ✅ Không có phần tử trùng lặp
        - ✅ Không có thứ tự (unordered)
        - ✅ Thao tác nhanh cho membership test
        - ❌ Không thể truy cập qua index
        """)
    
    # TAB 4: Tuples
    with tab4:
        st.subheader("🔒 Tuple - Immutable Sequences")
        
        st.markdown("""
        ### Tuple vs List
        
        | Feature | List | Tuple |
        |---------|------|-------|
        | Syntax | `[1, 2, 3]` | `(1, 2, 3)` |
        | Mutable | ✅ Yes | ❌ No |
        | Speed | Slower | Faster |
        | Use case | Data thay đổi | Data cố định |
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### ❌ Không thể sửa Tuple:")
            
            st.code("""
# Tạo tuple
my_tuple = (1, 2, 3, 4, 5)

# ❌ SẼ BỊ LỖI
my_tuple[0] = 10  # TypeError!
my_tuple.append(6)  # AttributeError!
            """, language="python")
            
            if st.button("Thử sửa tuple (sẽ lỗi!)"):
                try:
                    my_tuple = (1, 2, 3)
                    my_tuple[0] = 10
                except TypeError as e:
                    st.error(f"❌ TypeError: {e}")
        
        with col2:
            st.markdown("### ✅ Có thể làm với Tuple:")
            
            st.code("""
my_tuple = (1, 2, 3, 4, 5)

# ✅ Truy cập elements
first = my_tuple[0]  # 1

# ✅ Slicing
subset = my_tuple[1:3]  # (2, 3)

# ✅ Unpacking
a, b, c, d, e = my_tuple

# ✅ Count và index
count = my_tuple.count(3)
idx = my_tuple.index(3)
            """, language="python")
        
        st.markdown("### 🎯 Khi nào dùng Tuple?")
        st.success("""
        1. **Dữ liệu không đổi**: Tọa độ GPS (lat, lon), ngày tháng
        2. **Return nhiều giá trị**: `return (status, message, data)`
        3. **Dictionary keys**: Tuple có thể làm key, List không được
        4. **Performance**: Tuple nhanh hơn List một chút
        """)

# =============================================================================
# MODULE 4: FUNCTIONS VISUALIZER
# =============================================================================
elif module == "🎯 Module 4: Functions Visualizer":
    st.header("🎯 Module 4: Functions Visualizer")
    
    tab1, tab2 = st.tabs(["Function Execution", "Recursion Tree"])
    
    with tab1:
        st.subheader("📞 Function Call Visualizer")
        
        st.markdown("### Tạo function của bạn:")
        
        function_code = st.text_area(
            "Nhập code function:",
            value="""def calculate_total(price, quantity, tax_rate=0.1):
    subtotal = price * quantity
    tax = subtotal * tax_rate
    total = subtotal + tax
    return total""",
            height=150
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Input Parameters:")
            price = st.number_input("price:", value=100.0)
            quantity = st.number_input("quantity:", value=2, step=1)
            tax_rate = st.number_input("tax_rate:", value=0.1)
            
            if st.button("▶️ Execute Function"):
                try:
                    # Execute function
                    exec(function_code, globals())
                    result = calculate_total(price, quantity, tax_rate)
                    
                    st.success(f"### 🎯 Result: {result:.2f}")
                    
                    # Show execution steps
                    st.markdown("### 📝 Execution Steps:")
                    subtotal = price * quantity
                    tax = subtotal * tax_rate
                    
                    st.code(f"""
Step 1: subtotal = price × quantity
        subtotal = {price} × {quantity} = {subtotal}

Step 2: tax = subtotal × tax_rate
        tax = {subtotal} × {tax_rate} = {tax}

Step 3: total = subtotal + tax
        total = {subtotal} + {tax} = {result}

Step 4: return {result}
                    """)
                    
                except Exception as e:
                    st.error(f"❌ Error: {e}")
        
        with col2:
            st.markdown("### 🔍 Function Anatomy")
            
            st.code("""
def function_name(param1, param2, param3=default):
    │         │        │        │         │
    │         │        │        │         └─ Default value
    │         │        │        └─────────── Optional param
    │         │        └──────────────────── Required param
    │         └───────────────────────────── Required param
    └─────────────────────────────────────── Function name
    
    # Function body
    result = param1 + param2
    
    return result  # Return value
            """, language="python")
            
            st.info("""
            **Components:**
            - `def`: Keyword để định nghĩa function
            - Parameters: Input của function
            - Default values: Giá trị mặc định (optional)
            - Return: Output của function
            """)
    
    with tab2:
        st.subheader("🌳 Recursion Tree Visualizer")
        
        st.markdown("### Fibonacci Recursion")
        
        n = st.slider("Tính Fibonacci(n):", 1, 8, 5)
        
        if st.button("🌳 Visualize Recursion Tree"):
            # Calculate fibonacci
            call_count = [0]
            
            def fibonacci(n, depth=0):
                call_count[0] += 1
                if n <= 1:
                    return n
                return fibonacci(n-1, depth+1) + fibonacci(n-2, depth+1)
            
            result = fibonacci(n)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.success(f"### Fibonacci({n}) = {result}")
                st.warning(f"⚠️ Số lần gọi hàm: **{call_count[0]}** lần!")
                
                st.code(f"""
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

fibonacci({n}) = {result}
Total calls: {call_count[0]}
                """, language="python")
            
            with col2:
                st.markdown("### 📊 Call Tree Structure")
                
                # Generate tree structure
                tree_text = f"""
Fibonacci({n})
├─ Fibonacci({n-1})
│  ├─ Fibonacci({n-2})
│  └─ Fibonacci({n-3})
└─ Fibonacci({n-2})
   ├─ Fibonacci({n-3})
   └─ Fibonacci({n-4})
...
                """
                st.code(tree_text)
        
        st.markdown("---")
        st.markdown("### 💡 So sánh: Recursion vs Iteration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**❌ Recursion (Chậm)**")
            st.code("""
def fibonacci_recursive(n):
    if n <= 1:
        return n
    return fibonacci_recursive(n-1) + \\
           fibonacci_recursive(n-2)

# O(2^n) - Very slow!
            """, language="python")
        
        with col2:
            st.markdown("**✅ Iteration (Nhanh)**")
            st.code("""
def fibonacci_iterative(n):
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(n-1):
        a, b = b, a + b
    return b

# O(n) - Much faster!
            """, language="python")

# =============================================================================
# MODULE 5: NUMPY ARRAYS
# =============================================================================
elif module == "🧮 Module 5: NumPy Arrays":
    st.header("🧮 Module 5: NumPy Arrays Visualizer")
    
    tab1, tab2, tab3 = st.tabs(["Array Creation", "Array Operations", "Broadcasting"])
    
    with tab1:
        st.subheader("📐 NumPy Array Creation")
        
        col1, col2 = st.columns(2)
        
        with col1:
            array_type = st.selectbox(
                "Chọn cách tạo array:",
                ["np.array()", "np.zeros()", "np.ones()", "np.arange()", "np.linspace()", "np.random.rand()"]
            )
            
            if array_type == "np.array()":
                array_input = st.text_input("Nhập array (ví dụ: [[1,2,3],[4,5,6]]):", value="[[1,2,3],[4,5,6]]")
                if st.button("Tạo Array"):
                    try:
                        arr = np.array(eval(array_input))
                        st.session_state.numpy_arr = arr
                    except:
                        st.error("Invalid input!")
            
            elif array_type in ["np.zeros()", "np.ones()"]:
                shape_input = st.text_input("Shape (rows, cols):", value="3, 4")
                if st.button("Tạo Array"):
                    try:
                        shape = tuple(map(int, shape_input.split(',')))
                        if array_type == "np.zeros()":
                            arr = np.zeros(shape)
                        else:
                            arr = np.ones(shape)
                        st.session_state.numpy_arr = arr
                    except:
                        st.error("Invalid shape!")
            
            elif array_type == "np.arange()":
                start = st.number_input("Start:", value=0)
                stop = st.number_input("Stop:", value=10)
                step = st.number_input("Step:", value=1)
                if st.button("Tạo Array"):
                    arr = np.arange(start, stop, step)
                    st.session_state.numpy_arr = arr
            
            elif array_type == "np.linspace()":
                start = st.number_input("Start:", value=0.0)
                stop = st.number_input("Stop:", value=1.0)
                num = st.number_input("Number of points:", value=10, step=1)
                if st.button("Tạo Array"):
                    arr = np.linspace(start, stop, int(num))
                    st.session_state.numpy_arr = arr
            
            elif array_type == "np.random.rand()":
                rows = st.number_input("Rows:", value=3, step=1)
                cols = st.number_input("Cols:", value=4, step=1)
                if st.button("Tạo Array"):
                    arr = np.random.rand(int(rows), int(cols))
                    st.session_state.numpy_arr = arr
        
        with col2:
            if 'numpy_arr' in st.session_state:
                st.markdown("### 🔍 Array Info:")
                arr = st.session_state.numpy_arr
                
                st.code(f"""
Shape: {arr.shape}
Dimensions: {arr.ndim}
Size: {arr.size}
Data type: {arr.dtype}
                """)
                
                st.markdown("### 📊 Array Values:")
                st.write(arr)
                
                # Visualize if 2D
                if arr.ndim == 2:
                    fig = go.Figure(data=go.Heatmap(
                        z=arr,
                        colorscale='Viridis',
                        text=np.round(arr, 2),
                        texttemplate='%{text}',
                        textfont={"size": 10}
                    ))
                    fig.update_layout(title="Array Heatmap", height=400)
                    st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("🔧 NumPy Array Operations")
        
        # Sample arrays
        arr1 = np.array([[1, 2, 3], [4, 5, 6]])
        arr2 = np.array([[10, 20, 30], [40, 50, 60]])
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Array 1:")
            st.write(arr1)
            
            st.markdown("### Array 2:")
            st.write(arr2)
        
        with col2:
            operation = st.selectbox(
                "Chọn phép toán:",
                ["Addition (+)", "Subtraction (-)", "Multiplication (*)", 
                 "Division (/)", "Matrix Multiplication (@)", "Transpose"]
            )
            
            if operation == "Addition (+)":
                result = arr1 + arr2
                st.markdown("### arr1 + arr2 =")
                st.write(result)
            
            elif operation == "Subtraction (-)":
                result = arr1 - arr2
                st.markdown("### arr1 - arr2 =")
                st.write(result)
            
            elif operation == "Multiplication (*)":
                result = arr1 * arr2
                st.markdown("### arr1 * arr2 (element-wise) =")
                st.write(result)
            
            elif operation == "Division (/)":
                result = arr1 / arr2
                st.markdown("### arr1 / arr2 =")
                st.write(result)
            
            elif operation == "Matrix Multiplication (@)":
                # Need compatible shapes
                arr2_t = arr2.T
                result = arr1 @ arr2_t
                st.markdown("### arr1 @ arr2.T =")
                st.write(result)
            
            elif operation == "Transpose":
                result = arr1.T
                st.markdown("### arr1.T =")
                st.write(result)
        
        st.markdown("---")
        st.markdown("### 📚 Common NumPy Operations:")
        
        st.code("""
# Statistical operations
arr.mean()      # Trung bình
arr.sum()       # Tổng
arr.min()       # Min
arr.max()       # Max
arr.std()       # Độ lệch chuẩn

# Reshaping
arr.reshape(2, 3)  # Đổi shape
arr.flatten()      # Flatten to 1D

# Indexing & Slicing
arr[0, 1]       # Element at row 0, col 1
arr[0, :]       # First row
arr[:, 1]       # Second column
arr[arr > 5]    # Boolean indexing
        """, language="python")
    
    with tab3:
        st.subheader("📡 NumPy Broadcasting")
        
        st.markdown("""
        ### Broadcasting là gì?
        
        Broadcasting cho phép NumPy thực hiện phép toán trên các array có **shape khác nhau**.
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Ví dụ 1: Array + Scalar")
            
            arr = np.array([[1, 2, 3], [4, 5, 6]])
            scalar = 10
            
            st.write("Array:", arr)
            st.write("Scalar:", scalar)
            st.write("Result (arr + scalar):", arr + scalar)
            
            st.code("""
# Scalar được "broadcast" thành array cùng shape
[[1, 2, 3],     [[10, 10, 10],     [[11, 12, 13],
 [4, 5, 6]]  +   [10, 10, 10]]  =   [14, 15, 16]]
            """)
        
        with col2:
            st.markdown("### Ví dụ 2: Array + 1D Array")
            
            arr = np.array([[1, 2, 3], [4, 5, 6]])
            row = np.array([10, 20, 30])
            
            st.write("Array (2×3):", arr)
            st.write("Row (3,):", row)
            st.write("Result (arr + row):", arr + row)
            
            st.code("""
# Row được broadcast thành (2×3)
[[1, 2, 3],     [[10, 20, 30],     [[11, 22, 33],
 [4, 5, 6]]  +   [10, 20, 30]]  =   [14, 25, 36]]
            """)
        
        st.markdown("### 🎯 Broadcasting Rules:")
        st.info("""
        1. Nếu arrays có **số chiều khác nhau**, thêm chiều 1 vào bên trái array nhỏ hơn
        2. Hai arrays tương thích nếu mỗi chiều:
           - Bằng nhau, HOẶC
           - Một trong hai là 1
        3. Sau khi broadcast, mỗi array có cùng shape
        
        **Ví dụ:**
        - (3, 1) + (1, 4) → (3, 4) ✅
        - (3, 4) + (3, 1) → (3, 4) ✅
        - (3, 4) + (2, 4) → ❌ Không tương thích!
        """)

# =============================================================================
# MODULE 6: MATPLOTLIB PLOTTER
# =============================================================================
elif module == "📊 Module 6: Matplotlib Plotter":
    st.header("📊 Module 6: Matplotlib Interactive Plotter")
    
    tab1, tab2, tab3 = st.tabs(["Line Plot", "Bar Chart", "Scatter Plot"])
    
    with tab1:
        st.subheader("📈 Line Plot Creator")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("### Settings:")
            
            x_function = st.text_input("X values (Python expression):", value="np.linspace(0, 10, 100)")
            y_function = st.text_input("Y = f(X):", value="np.sin(x)")
            
            title = st.text_input("Title:", value="Sine Wave")
            xlabel = st.text_input("X Label:", value="X")
            ylabel = st.text_input("Y Label:", value="Y")
            
            color = st.color_picker("Line Color:", value="#667eea")
            linewidth = st.slider("Line Width:", 1, 5, 2)
            
            if st.button("🎨 Generate Plot"):
                try:
                    x = eval(x_function)
                    y = eval(y_function)
                    
                    fig, ax = plt.subplots(figsize=(10, 6))
                    ax.plot(x, y, color=color, linewidth=linewidth)
                    ax.set_title(title, fontsize=16, fontweight='bold')
                    ax.set_xlabel(xlabel, fontsize=12)
                    ax.set_ylabel(ylabel, fontsize=12)
                    ax.grid(True, alpha=0.3)
                    
                    st.session_state.current_plot = fig
                    
                except Exception as e:
                    st.error(f"Error: {e}")
        
        with col2:
            if 'current_plot' in st.session_state:
                st.pyplot(st.session_state.current_plot)
            else:
                st.info("👈 Configure settings and click 'Generate Plot'")
        
        st.markdown("---")
        st.markdown("### 💡 Common Functions to Try:")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.code("""
# Sin Wave
X: np.linspace(0, 10, 100)
Y: np.sin(x)
            """)
        
        with col2:
            st.code("""
# Quadratic
X: np.linspace(-5, 5, 100)
Y: x**2
            """)
        
        with col3:
            st.code("""
# Exponential
X: np.linspace(0, 5, 100)
Y: np.exp(x)
            """)
    
    with tab2:
        st.subheader("📊 Bar Chart Creator")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            categories = st.text_input("Categories (comma-separated):", value="Python, Java, JavaScript, C++, C#")
            values = st.text_input("Values (comma-separated):", value="45, 30, 25, 20, 15")
            
            title = st.text_input("Chart Title:", value="Programming Languages Popularity")
            
            if st.button("📊 Create Bar Chart"):
                try:
                    cats = [c.strip() for c in categories.split(',')]
                    vals = [float(v.strip()) for v in values.split(',')]
                    
                    fig, ax = plt.subplots(figsize=(10, 6))
                    bars = ax.bar(cats, vals, color=['#667eea', '#764ba2', '#f093fb', '#4facfe', '#00f2fe'])
                    ax.set_title(title, fontsize=16, fontweight='bold')
                    ax.set_ylabel("Popularity (%)", fontsize=12)
                    plt.xticks(rotation=45, ha='right')
                    
                    # Add value labels on bars
                    for bar in bars:
                        height = bar.get_height()
                        ax.text(bar.get_x() + bar.get_width()/2., height,
                               f'{height:.1f}%',
                               ha='center', va='bottom')
                    
                    plt.tight_layout()
                    st.session_state.bar_chart = fig
                    
                except Exception as e:
                    st.error(f"Error: {e}")
        
        with col2:
            if 'bar_chart' in st.session_state:
                st.pyplot(st.session_state.bar_chart)
            else:
                st.info("👈 Enter data and create chart")
    
    with tab3:
        st.subheader("🎯 Scatter Plot Creator")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            n_points = st.slider("Number of points:", 10, 200, 50)
            
            distribution = st.selectbox(
                "Distribution:",
                ["Random", "Linear", "Quadratic", "Circular"]
            )
            
            if st.button("🎯 Generate Scatter Plot"):
                if distribution == "Random":
                    x = np.random.rand(n_points) * 10
                    y = np.random.rand(n_points) * 10
                
                elif distribution == "Linear":
                    x = np.linspace(0, 10, n_points)
                    y = 2 * x + 3 + np.random.randn(n_points) * 2
                
                elif distribution == "Quadratic":
                    x = np.linspace(-5, 5, n_points)
                    y = x**2 + np.random.randn(n_points) * 3
                
                elif distribution == "Circular":
                    theta = np.linspace(0, 2*np.pi, n_points)
                    r = 5 + np.random.randn(n_points) * 0.5
                    x = r * np.cos(theta)
                    y = r * np.sin(theta)
                
                fig, ax = plt.subplots(figsize=(10, 6))
                scatter = ax.scatter(x, y, c=np.arange(n_points), 
                                   cmap='viridis', s=100, alpha=0.6)
                ax.set_title(f"Scatter Plot - {distribution} Distribution", 
                           fontsize=16, fontweight='bold')
                ax.set_xlabel("X", fontsize=12)
                ax.set_ylabel("Y", fontsize=12)
                ax.grid(True, alpha=0.3)
                plt.colorbar(scatter, ax=ax, label='Point Index')
                
                st.session_state.scatter_plot = fig
        
        with col2:
            if 'scatter_plot' in st.session_state:
                st.pyplot(st.session_state.scatter_plot)
            else:
                st.info("👈 Configure and generate plot")

# =============================================================================
# MODULE 7: QUIZ & CHALLENGES
# =============================================================================
elif module == "🎓 Module 7: Quiz & Challenges":
    st.header("🎓 Module 7: Quiz & Challenges")
    
    tab1, tab2 = st.tabs(["Multiple Choice Quiz", "Coding Challenges"])
    
    with tab1:
        st.subheader("📝 Python Quiz")
        
        # Quiz questions
        questions = [
            {
                "question": "Kết quả của `7 // 2` là gì?",
                "options": ["3.5", "3", "4", "2"],
                "correct": 1,
                "explanation": "// là floor division, trả về phần nguyên: 7 // 2 = 3"
            },
            {
                "question": "Kiểu dữ liệu nào là immutable (không thể thay đổi)?",
                "options": ["List", "Dictionary", "Tuple", "Set"],
                "correct": 2,
                "explanation": "Tuple là immutable, không thể sửa đổi sau khi tạo"
            },
            {
                "question": "Output của `print(type(5.0))` là gì?",
                "options": ["<class 'int'>", "<class 'float'>", "<class 'str'>", "<class 'number'>"],
                "correct": 1,
                "explanation": "5.0 là số thực (float), không phải số nguyên"
            },
            {
                "question": "`'Hello' + 'World'` kết quả là?",
                "options": ["HelloWorld", "Hello World", "Error", "Hello+World"],
                "correct": 0,
                "explanation": "Toán tử + với strings là concatenation (nối chuỗi)"
            },
            {
                "question": "Kết quả của `bool('')` (chuỗi rỗng)?",
                "options": ["True", "False", "Error", "None"],
                "correct": 1,
                "explanation": "Chuỗi rỗng được coi là False trong Python"
            }
        ]
        
        # Initialize score
        if 'quiz_score' not in st.session_state:
            st.session_state.quiz_score = 0
            st.session_state.quiz_answers = {}
        
        # Display questions
        for i, q in enumerate(questions):
            st.markdown(f"### Câu {i+1}: {q['question']}")
            
            answer = st.radio(
                f"Chọn đáp án:",
                q['options'],
                key=f"q{i}"
            )
            
            if st.button(f"Kiểm tra", key=f"check{i}"):
                selected_idx = q['options'].index(answer)
                
                if selected_idx == q['correct']:
                    st.success(f"✅ Chính xác! {q['explanation']}")
                    st.session_state.quiz_answers[i] = True
                else:
                    st.error(f"❌ Sai rồi. Đáp án đúng: {q['options'][q['correct']]}")
                    st.info(f"💡 {q['explanation']}")
                    st.session_state.quiz_answers[i] = False
            
            st.markdown("---")
        
        # Show score
        if st.button("📊 Xem Kết Quả"):
            correct = sum(st.session_state.quiz_answers.values())
            total = len(questions)
            percentage = (correct / total) * 100
            
            st.markdown(f"## 🎯 Điểm của bạn: {correct}/{total} ({percentage:.1f}%)")
            
            if percentage >= 80:
                st.balloons()
                st.success("🎉 Xuất sắc! Bạn đã nắm vững kiến thức!")
            elif percentage >= 60:
                st.info("👍 Khá tốt! Ôn thêm một chút nữa nhé!")
            else:
                st.warning("💪 Cố gắng thêm! Hãy xem lại các module trước.")
    
    with tab2:
        st.subheader("💻 Coding Challenges")
        
        challenge = st.selectbox(
            "Chọn thử thách:",
            [
                "Challenge 1: FizzBuzz",
                "Challenge 2: Palindrome Checker",
                "Challenge 3: Sum of Evens",
                "Challenge 4: Reverse String"
            ]
        )
        
        if challenge == "Challenge 1: FizzBuzz":
            st.markdown("""
            ### 🎯 Challenge: FizzBuzz
            
            **Yêu cầu:**
            - In các số từ 1 đến n
            - Nếu số chia hết cho 3: in "Fizz"
            - Nếu số chia hết cho 5: in "Buzz"
            - Nếu chia hết cho cả 3 và 5: in "FizzBuzz"
            - Các số khác: in số đó
            
            **Ví dụ:** n = 15
            ```
            1, 2, Fizz, 4, Buzz, Fizz, 7, 8, Fizz, Buzz, 11, Fizz, 13, 14, FizzBuzz
            ```
            """)
            
            n = st.number_input("Nhập n:", value=15, step=1, min_value=1)
            
            user_code = st.text_area(
                "Viết code của bạn:",
                value="""# Viết code ở đây
for i in range(1, n+1):
    # Your code here
    pass
""",
                height=200
            )
            
            if st.button("▶️ Run Code"):
                try:
                    # Capture output
                    output = StringIO()
                    sys.stdout = output
                    
                    exec(user_code, {'n': n})
                    
                    sys.stdout = sys.__stdout__
                    result = output.getvalue()
                    
                    st.code(result)
                    
                    # Expected answer
                    expected = []
                    for i in range(1, n+1):
                        if i % 15 == 0:
                            expected.append("FizzBuzz")
                        elif i % 3 == 0:
                            expected.append("Fizz")
                        elif i % 5 == 0:
                            expected.append("Buzz")
                        else:
                            expected.append(str(i))
                    
                    st.markdown("### ✅ Expected Output:")
                    st.code(", ".join(expected))
                    
                except Exception as e:
                    st.error(f"Error: {e}")
                    sys.stdout = sys.__stdout__
        
        elif challenge == "Challenge 2: Palindrome Checker":
            st.markdown("""
            ### 🎯 Challenge: Kiểm tra Palindrome
            
            **Yêu cầu:**
            Viết function kiểm tra một chuỗi có phải là palindrome không.
            
            **Palindrome:** Chuỗi đọc xuôi và ngược giống nhau
            
            **Ví dụ:**
            - "racecar" → True
            - "hello" → False
            - "A man a plan a canal Panama" → True (ignore spaces & case)
            """)
            
            user_code = st.text_area(
                "Viết function:",
                value="""def is_palindrome(s):
    # Your code here
    pass
""",
                height=150
            )
            
            test_string = st.text_input("Test string:", value="racecar")
            
            if st.button("🧪 Test"):
                try:
                    exec(user_code, globals())
                    result = is_palindrome(test_string)
                    
                    # Check answer
                    cleaned = ''.join(test_string.lower().split())
                    expected = cleaned == cleaned[::-1]
                    
                    if result == expected:
                        st.success(f"✅ Correct! '{test_string}' is {'' if result else 'not '}a palindrome")
                    else:
                        st.error(f"❌ Wrong answer. Expected: {expected}, Got: {result}")
                    
                except Exception as e:
                    st.error(f"Error: {e}")

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p>Made with ❤️ for Python learners | © 2024 Python Learning Playground</p>
    <p>📚 Keep Learning | 💻 Keep Coding | 🚀 Keep Growing</p>
</div>
""", unsafe_allow_html=True)
