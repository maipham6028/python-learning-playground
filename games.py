"""
Games module - 3 Python-themed games with knowledge reminders
- Memory Card: Match keyword with definition
- Hangman: Guess Python keyword letter by letter
- Bingo: Mark keywords from definitions
"""
import streamlit as st
import random
import time
from database import get_supabase


# =============================================================================
# KNOWLEDGE BASE - Chi tiết giải thích cho mỗi keyword
# =============================================================================

PYTHON_KNOWLEDGE = {
    "def": {
        "title": "def - Định nghĩa hàm",
        "explanation": "`def` là từ khóa dùng để định nghĩa một hàm trong Python. Sau `def` là tên hàm, dấu ngoặc chứa tham số, và dấu `:` ở cuối.",
        "example": "def greet(name):\n    return f'Hello, {name}!'",
        "chapter": "Chương 5: Functions"
    },
    "if": {
        "title": "if - Câu điều kiện",
        "explanation": "`if` dùng để thực thi code khi điều kiện đúng. Có thể kết hợp với `elif` và `else`.",
        "example": "if x > 0:\n    print('Positive')\nelif x < 0:\n    print('Negative')\nelse:\n    print('Zero')",
        "chapter": "Chương 3: Conditionals"
    },
    "else": {
        "title": "else - Trường hợp còn lại",
        "explanation": "`else` chạy khi điều kiện `if` sai. Không có điều kiện riêng.",
        "example": "if x > 0:\n    print('Dương')\nelse:\n    print('Không dương')",
        "chapter": "Chương 3: Conditionals"
    },
    "elif": {
        "title": "elif - Else if",
        "explanation": "`elif` là viết tắt của 'else if', dùng để kiểm tra thêm điều kiện sau `if`.",
        "example": "if x > 10:\n    print('Lớn')\nelif x > 5:\n    print('Trung bình')\nelse:\n    print('Nhỏ')",
        "chapter": "Chương 3: Conditionals"
    },
    "for": {
        "title": "for - Vòng lặp for",
        "explanation": "`for` dùng để lặp qua các phần tử của một sequence (list, tuple, string, range...). Biết trước số lần lặp.",
        "example": "for i in range(5):\n    print(i)  # In 0, 1, 2, 3, 4",
        "chapter": "Chương 4: Loops"
    },
    "while": {
        "title": "while - Vòng lặp while",
        "explanation": "`while` lặp khi điều kiện còn đúng. Cần cẩn thận để tránh vòng lặp vô hạn.",
        "example": "count = 0\nwhile count < 5:\n    print(count)\n    count += 1",
        "chapter": "Chương 4: Loops"
    },
    "class": {
        "title": "class - Định nghĩa lớp",
        "explanation": "`class` dùng để định nghĩa một lớp trong lập trình hướng đối tượng (OOP).",
        "example": "class Dog:\n    def __init__(self, name):\n        self.name = name\n    def bark(self):\n        return 'Woof!'",
        "chapter": "Chương 7: OOP"
    },
    "return": {
        "title": "return - Trả về giá trị",
        "explanation": "`return` dùng để trả về giá trị từ hàm và kết thúc hàm. Hàm không có `return` sẽ trả về `None`.",
        "example": "def add(a, b):\n    return a + b\n\nresult = add(3, 5)  # result = 8",
        "chapter": "Chương 5: Functions"
    },
    "import": {
        "title": "import - Nhập thư viện",
        "explanation": "`import` dùng để nhập module hoặc thư viện vào code. Có thể dùng với `from` và `as`.",
        "example": "import math\nimport numpy as np\nfrom datetime import datetime",
        "chapter": "Chương 1: Introduction"
    },
    "from": {
        "title": "from - Import cụ thể",
        "explanation": "`from` kết hợp với `import` để lấy cụ thể function/class từ module, không import toàn bộ.",
        "example": "from math import pi, sqrt\nfrom typing import List",
        "chapter": "Chương 1: Introduction"
    },
    "as": {
        "title": "as - Đặt tên thay thế",
        "explanation": "`as` dùng để đặt tên thay thế (alias) khi import, giúp code ngắn gọn hơn.",
        "example": "import numpy as np\nimport pandas as pd",
        "chapter": "Chương 9: NumPy"
    },
    "try": {
        "title": "try - Thử chạy code",
        "explanation": "`try` dùng với `except` để bắt và xử lý exception (lỗi runtime).",
        "example": "try:\n    result = 10 / 0\nexcept ZeroDivisionError:\n    print('Không chia được cho 0')",
        "chapter": "Chương 8: Exception Handling"
    },
    "except": {
        "title": "except - Bắt exception",
        "explanation": "`except` bắt và xử lý exception được ném ra từ khối `try`.",
        "example": "try:\n    x = int('abc')\nexcept ValueError as e:\n    print(f'Lỗi: {e}')",
        "chapter": "Chương 8: Exception Handling"
    },
    "finally": {
        "title": "finally - Luôn chạy",
        "explanation": "`finally` luôn chạy dù có exception hay không. Thường dùng để cleanup (đóng file, kết nối...).",
        "example": "try:\n    file = open('data.txt')\nexcept FileNotFoundError:\n    print('Không tìm thấy')\nfinally:\n    print('Done')",
        "chapter": "Chương 8: Exception Handling"
    },
    "raise": {
        "title": "raise - Ném exception",
        "explanation": "`raise` dùng để chủ động ném ra một exception.",
        "example": "def divide(a, b):\n    if b == 0:\n        raise ValueError('b không được bằng 0')\n    return a / b",
        "chapter": "Chương 8: Exception Handling"
    },
    "list": {
        "title": "list - Danh sách",
        "explanation": "`list` là cấu trúc dữ liệu có thứ tự, **mutable** (thay đổi được), cho phép trùng lặp. Dùng dấu `[]`.",
        "example": "fruits = ['apple', 'banana', 'cherry']\nfruits.append('date')\nprint(fruits[0])  # 'apple'",
        "chapter": "Chương 6: Data Structures"
    },
    "dict": {
        "title": "dict - Từ điển",
        "explanation": "`dict` là cấu trúc key-value, không có thứ tự (Python 3.7+ giữ thứ tự insert). Dùng dấu `{}`.",
        "example": "person = {'name': 'Alice', 'age': 25}\nprint(person['name'])  # 'Alice'",
        "chapter": "Chương 6: Data Structures"
    },
    "set": {
        "title": "set - Tập hợp",
        "explanation": "`set` là tập hợp không có thứ tự, không trùng lặp. Dùng dấu `{}` (khác dict vì không có key-value).",
        "example": "numbers = {1, 2, 3, 2, 1}\nprint(numbers)  # {1, 2, 3}",
        "chapter": "Chương 6: Data Structures"
    },
    "tuple": {
        "title": "tuple - Bộ",
        "explanation": "`tuple` là sequence **immutable** (không đổi được). Dùng dấu `()`.",
        "example": "point = (3, 5)\nx, y = point  # Unpacking",
        "chapter": "Chương 6: Data Structures"
    },
    "str": {
        "title": "str - Chuỗi",
        "explanation": "`str` là kiểu chuỗi ký tự, immutable. Dùng dấu nháy đơn `'` hoặc nháy kép `\"`.",
        "example": "name = 'Python'\nprint(name.upper())  # 'PYTHON'",
        "chapter": "Chương 2: Operations & Syntax"
    },
    "int": {
        "title": "int - Số nguyên",
        "explanation": "`int` là kiểu số nguyên trong Python. Python tự động xử lý số lớn (big integer).",
        "example": "age = 25\nbig_num = 10**100  # Số rất lớn",
        "chapter": "Chương 2: Operations & Syntax"
    },
    "float": {
        "title": "float - Số thực",
        "explanation": "`float` là số thập phân. Chú ý vấn đề độ chính xác: 0.1 + 0.2 ≠ 0.3.",
        "example": "pi = 3.14\nprint(0.1 + 0.2)  # 0.30000000000000004",
        "chapter": "Chương 2: Operations & Syntax"
    },
    "bool": {
        "title": "bool - True/False",
        "explanation": "`bool` chỉ có 2 giá trị: `True` và `False`. Dùng cho điều kiện logic.",
        "example": "is_student = True\nprint(bool(0))   # False\nprint(bool(''))  # False",
        "chapter": "Chương 2: Operations & Syntax"
    },
    "True": {
        "title": "True - Giá trị đúng",
        "explanation": "`True` là giá trị Boolean biểu thị 'đúng'. Viết hoa chữ T.",
        "example": "is_valid = True\nif is_valid:\n    print('Valid!')",
        "chapter": "Chương 2: Operations & Syntax"
    },
    "False": {
        "title": "False - Giá trị sai",
        "explanation": "`False` là giá trị Boolean biểu thị 'sai'. Viết hoa chữ F. Các giá trị được coi là False: 0, '', [], {}, None.",
        "example": "is_empty = False\nprint(bool([]))  # False",
        "chapter": "Chương 2: Operations & Syntax"
    },
    "None": {
        "title": "None - Giá trị rỗng",
        "explanation": "`None` là giá trị đặc biệt biểu thị 'không có gì' (tương đương null). Hàm không `return` sẽ trả về `None`.",
        "example": "x = None\nif x is None:\n    print('x chưa có giá trị')",
        "chapter": "Chương 3: Conditionals"
    },
    "and": {
        "title": "and - VÀ logic",
        "explanation": "`and` trả về True khi CẢ HAI điều kiện đều True. Short-circuit: dừng khi gặp False.",
        "example": "age = 20\nif age >= 18 and age < 60:\n    print('Người lớn')",
        "chapter": "Chương 3: Conditionals"
    },
    "or": {
        "title": "or - HOẶC logic",
        "explanation": "`or` trả về True khi ÍT NHẤT MỘT điều kiện True. Short-circuit: dừng khi gặp True.",
        "example": "is_weekend = day == 'Sat' or day == 'Sun'",
        "chapter": "Chương 3: Conditionals"
    },
    "not": {
        "title": "not - Phủ định logic",
        "explanation": "`not` đảo ngược giá trị Boolean: `not True` = False, `not False` = True.",
        "example": "is_empty = not my_list  # True nếu list rỗng",
        "chapter": "Chương 3: Conditionals"
    },
    "is": {
        "title": "is - So sánh identity",
        "explanation": "`is` so sánh xem 2 biến có trỏ đến CÙNG object không (khác với `==` so sánh giá trị).",
        "example": "x = None\nif x is None:  # Đúng cách check None\n    print('Empty')",
        "chapter": "Chương 3: Conditionals"
    },
    "in": {
        "title": "in - Kiểm tra thành viên",
        "explanation": "`in` kiểm tra xem phần tử có trong sequence/collection không. Dùng nhiều trong for loop.",
        "example": "if 'a' in 'apple':\n    print('Có chữ a')\n\nfor i in range(5):\n    print(i)",
        "chapter": "Chương 4: Loops"
    },
    "lambda": {
        "title": "lambda - Hàm ẩn danh",
        "explanation": "`lambda` tạo hàm một dòng, không có tên. Thường dùng với `map`, `filter`, `sorted`.",
        "example": "square = lambda x: x ** 2\nnums = sorted([3, 1, 2], key=lambda x: -x)",
        "chapter": "Chương 5: Functions"
    },
    "yield": {
        "title": "yield - Generator",
        "explanation": "`yield` biến hàm thành generator - trả về từng giá trị mỗi khi được gọi, tiết kiệm bộ nhớ.",
        "example": "def count_up(n):\n    for i in range(n):\n        yield i",
        "chapter": "Chương 5: Functions"
    },
    "pass": {
        "title": "pass - Không làm gì",
        "explanation": "`pass` là placeholder - không làm gì cả, dùng khi syntax yêu cầu có lệnh nhưng chưa viết code.",
        "example": "def future_function():\n    pass  # Sẽ viết sau\n\nclass EmptyClass:\n    pass",
        "chapter": "Chương 5: Functions"
    },
    "break": {
        "title": "break - Thoát vòng lặp",
        "explanation": "`break` thoát ngay lập tức khỏi vòng lặp gần nhất (for hoặc while).",
        "example": "for i in range(10):\n    if i == 5:\n        break\n    print(i)  # In 0, 1, 2, 3, 4",
        "chapter": "Chương 4: Loops"
    },
    "continue": {
        "title": "continue - Bỏ qua iteration",
        "explanation": "`continue` bỏ qua iteration hiện tại và tiếp tục iteration tiếp theo.",
        "example": "for i in range(5):\n    if i == 2:\n        continue\n    print(i)  # In 0, 1, 3, 4",
        "chapter": "Chương 4: Loops"
    },
    "global": {
        "title": "global - Biến toàn cục",
        "explanation": "`global` khai báo rằng biến trong hàm là biến global (ngoài hàm), không phải local.",
        "example": "count = 0\ndef increment():\n    global count\n    count += 1",
        "chapter": "Chương 5: Functions"
    },
    "super": {
        "title": "super - Class cha",
        "explanation": "`super()` dùng để gọi method của class cha từ class con trong OOP.",
        "example": "class Dog(Animal):\n    def __init__(self, name):\n        super().__init__(name)",
        "chapter": "Chương 7: OOP"
    },
    "input": {
        "title": "input - Nhận input",
        "explanation": "`input()` nhận dữ liệu từ người dùng. LUÔN trả về string, cần convert nếu muốn số.",
        "example": "name = input('Tên bạn: ')\nage = int(input('Tuổi: '))",
        "chapter": "Chương 1: Introduction"
    },
    "print": {
        "title": "print - In ra màn hình",
        "explanation": "`print()` in giá trị ra màn hình. Có thể in nhiều thứ cùng lúc, tùy chỉnh separator và ending.",
        "example": "print('Hello', 'World', sep=', ')\nprint('No newline', end='')",
        "chapter": "Chương 1: Introduction"
    },
    "range": {
        "title": "range - Dãy số",
        "explanation": "`range(start, stop, step)` tạo dãy số. `range(5)` = 0,1,2,3,4. Thường dùng với for loop.",
        "example": "for i in range(1, 10, 2):\n    print(i)  # 1, 3, 5, 7, 9",
        "chapter": "Chương 4: Loops"
    },
    "function": {
        "title": "function - Hàm",
        "explanation": "Function (hàm) là khối code có thể tái sử dụng, nhận input (parameters) và trả về output.",
        "example": "def square(x):\n    return x ** 2",
        "chapter": "Chương 5: Functions"
    },
    "iterator": {
        "title": "iterator - Đối tượng lặp",
        "explanation": "Iterator là đối tượng có thể lặp qua (iterate). List, tuple, dict, string đều là iterables.",
        "example": "my_iter = iter([1, 2, 3])\nprint(next(my_iter))  # 1",
        "chapter": "Chương 6: Data Structures"
    },
    "variable": {
        "title": "variable - Biến",
        "explanation": "Biến là tên gán cho một giá trị. Python không cần khai báo kiểu trước, tự động xác định.",
        "example": "name = 'Alice'  # str\nage = 25        # int\nheight = 1.65   # float",
        "chapter": "Chương 2: Operations & Syntax"
    },
    "operator": {
        "title": "operator - Toán tử",
        "explanation": "Toán tử: số học (+, -, *, /), so sánh (==, !=, <, >), logic (and, or, not), gán (=, +=).",
        "example": "x = 10 + 5       # Số học\ny = (x > 5)      # So sánh\nz = True and False  # Logic",
        "chapter": "Chương 2: Operations & Syntax"
    },
    "parameter": {
        "title": "parameter - Tham số",
        "explanation": "Parameter là biến trong định nghĩa hàm. Argument là giá trị truyền vào khi gọi hàm.",
        "example": "def greet(name, greeting='Hi'):  # params\n    return f'{greeting}, {name}'\n\ngreet('Alice')  # argument",
        "chapter": "Chương 5: Functions"
    },
    "recursion": {
        "title": "recursion - Đệ quy",
        "explanation": "Đệ quy là khi hàm tự gọi chính nó. Phải có base case để không lặp vô hạn.",
        "example": "def factorial(n):\n    if n <= 1:  # Base case\n        return 1\n    return n * factorial(n-1)",
        "chapter": "Chương 5: Functions"
    },
    "exception": {
        "title": "exception - Lỗi runtime",
        "explanation": "Exception là lỗi xảy ra khi chạy code. Dùng try-except để xử lý mà không crash chương trình.",
        "example": "try:\n    int('abc')\nexcept ValueError:\n    print('Không phải số')",
        "chapter": "Chương 8: Exception Handling"
    },
    "await": {
        "title": "await - Async/Await",
        "explanation": "`await` dùng trong async function để đợi một coroutine hoàn thành (lập trình bất đồng bộ).",
        "example": "async def fetch_data():\n    result = await api_call()\n    return result",
        "chapter": "Nâng cao: Async Programming"
    },
    "async": {
        "title": "async - Hàm bất đồng bộ",
        "explanation": "`async def` định nghĩa coroutine - hàm có thể chạy bất đồng bộ.",
        "example": "async def main():\n    await asyncio.sleep(1)\n    print('Done')",
        "chapter": "Nâng cao: Async Programming"
    },
}


# =============================================================================
# GAME DATA
# =============================================================================

MEMORY_PAIRS = [
    ("def", "Định nghĩa hàm"),
    ("if", "Câu điều kiện"),
    ("for", "Vòng lặp có số lần xác định"),
    ("while", "Vòng lặp có điều kiện"),
    ("class", "Định nghĩa lớp"),
    ("return", "Trả về giá trị từ hàm"),
    ("import", "Nhập thư viện"),
    ("list", "Cấu trúc dữ liệu có thứ tự, mutable"),
]

HANGMAN_WORDS = [
    # Short (3-4 letters)
    ("def", "Từ khóa định nghĩa hàm"),
    ("for", "Vòng lặp có số lần xác định"),
    ("int", "Kiểu số nguyên"),
    ("str", "Kiểu chuỗi ký tự"),
    ("try", "Khối xử lý exception"),
    ("not", "Toán tử phủ định logic"),
    ("and", "Toán tử logic VÀ"),
    ("pass", "Lệnh không làm gì"),
    ("list", "Cấu trúc dữ liệu có thứ tự, mutable"),
    ("dict", "Cấu trúc key-value"),
    ("None", "Giá trị rỗng"),
    ("True", "Giá trị Boolean đúng"),
    # Medium (5-6 letters)
    ("range", "Hàm tạo dãy số"),
    ("while", "Vòng lặp có điều kiện"),
    ("class", "Từ khóa định nghĩa lớp"),
    ("break", "Thoát khỏi vòng lặp"),
    ("False", "Giá trị Boolean sai"),
    ("input", "Hàm nhận dữ liệu từ người dùng"),
    ("print", "Hàm in ra màn hình"),
    ("float", "Kiểu số thực"),
    ("tuple", "Sequence immutable"),
    ("yield", "Tạo generator"),
    ("raise", "Chủ động ném exception"),
    ("super", "Gọi method class cha"),
    ("lambda", "Hàm ẩn danh một dòng"),
    ("import", "Nhập thư viện"),
    ("return", "Trả về giá trị từ hàm"),
    ("global", "Khai báo biến global"),
    ("except", "Bắt exception"),
    # Long (7-10 letters)
    ("finally", "Khối luôn chạy dù có lỗi hay không"),
    ("continue", "Bỏ qua iteration hiện tại"),
    ("function", "Khối code có thể tái sử dụng"),
    ("iterator", "Đối tượng có thể lặp qua"),
    ("variable", "Biến lưu giá trị"),
    ("operator", "Toán tử như +, -, *, /"),
    ("parameter", "Tham số truyền vào hàm"),
    ("recursion", "Hàm tự gọi chính nó"),
    ("exception", "Lỗi phát sinh khi chạy"),
]

BINGO_KEYWORDS = [
    "if", "else", "elif", "for", "while", "def", "class", "return",
    "import", "from", "as", "try", "except", "finally", "raise",
    "list", "dict", "set", "tuple", "str", "int", "float", "bool",
    "True", "False", "None", "and", "or", "not", "is", "in",
    "lambda", "yield", "pass", "break", "continue", "global",
]

BINGO_CLUES = {
    "if": "Từ khóa bắt đầu câu điều kiện",
    "else": "Khối chạy khi điều kiện if sai",
    "elif": "Viết tắt của 'else if'",
    "for": "Vòng lặp qua sequence",
    "while": "Vòng lặp khi điều kiện còn đúng",
    "def": "Từ khóa định nghĩa hàm",
    "class": "Từ khóa định nghĩa lớp",
    "return": "Trả về giá trị từ hàm",
    "import": "Nhập module vào code",
    "from": "Dùng với import để lấy cụ thể",
    "as": "Đặt tên thay thế khi import",
    "try": "Khối thử chạy code có thể lỗi",
    "except": "Bắt exception",
    "finally": "Luôn chạy dù có lỗi hay không",
    "raise": "Chủ động ném exception",
    "list": "Cấu trúc dữ liệu mutable có thứ tự []",
    "dict": "Cấu trúc key-value {}",
    "set": "Tập hợp không trùng lặp",
    "tuple": "Sequence immutable ()",
    "str": "Kiểu chuỗi ký tự",
    "int": "Kiểu số nguyên",
    "float": "Kiểu số thực",
    "bool": "Kiểu True/False",
    "True": "Giá trị Boolean đúng",
    "False": "Giá trị Boolean sai",
    "None": "Giá trị rỗng / null",
    "and": "Toán tử logic VÀ",
    "or": "Toán tử logic HOẶC",
    "not": "Toán tử phủ định",
    "is": "So sánh identity (cùng object)",
    "in": "Kiểm tra phần tử có trong sequence",
    "lambda": "Hàm ẩn danh một dòng",
    "yield": "Tạo generator",
    "pass": "Lệnh không làm gì",
    "break": "Thoát khỏi vòng lặp",
    "continue": "Bỏ qua iteration hiện tại",
    "global": "Khai báo biến global trong function",
}


# =============================================================================
# HELPERS
# =============================================================================

def award_game_points(user_id, points, game_name):
    """Award points for playing games"""
    try:
        supabase = get_supabase()
        user = supabase.table("users").select("total_points").eq("id", user_id).execute()
        if user.data:
            new_points = (user.data[0]['total_points'] or 0) + points
            supabase.table("users").update({
                "total_points": new_points,
                "level": new_points // 500 + 1,
            }).eq("id", user_id).execute()
    except Exception as e:
        pass
    return points


def show_knowledge_box(keywords, title="Kiến thức đã ôn trong game này"):
    """Display knowledge reminder after game"""
    if not keywords:
        return
    
    st.markdown("---")
    st.markdown(f"### 📚 {title}")
    st.caption("Ôn lại kiến thức về các từ khóa đã xuất hiện trong game:")
    
    unique_kws = list(dict.fromkeys(keywords))  # Remove duplicates, keep order
    
    for kw in unique_kws:
        if kw in PYTHON_KNOWLEDGE:
            info = PYTHON_KNOWLEDGE[kw]
            with st.expander(f"**{info['title']}** · {info['chapter']}"):
                st.markdown(info['explanation'])
                st.markdown("**Ví dụ:**")
                st.code(info['example'], language='python')


# =============================================================================
# GAME 1: MEMORY CARD
# =============================================================================

def check_match(state):
    """Helper to check if selected pair matches"""
    kw = state['keywords'][state['selected_keyword']]
    defn = state['definitions'][state['selected_definition']]
    state['attempts'] += 1
    
    # Track this keyword for knowledge review
    if kw['text'] not in state['seen_keywords']:
        state['seen_keywords'].append(kw['text'])
    
    if kw['pair_id'] == defn['pair_id']:
        state['matched_pairs'].append(kw['pair_id'])
        state['last_result'] = 'correct'
    else:
        state['last_result'] = 'wrong'
    
    state['selected_keyword'] = None
    state['selected_definition'] = None


def game_memory_card():
    """Matching game - click to select and pair keyword with definition"""
    st.markdown("### Memory Card — Ghép cặp Keyword & Định nghĩa")
    st.caption("Click 1 keyword và 1 định nghĩa tương ứng để ghép cặp. Ghép hết để thắng!")
    
    if 'memory_state' not in st.session_state:
        st.session_state.memory_state = None
    
    state = st.session_state.memory_state
    
    if state is None or st.button("Bắt đầu / Chơi lại", key="memory_new"):
        keywords = [{'id': f'k{i}', 'text': kw, 'pair_id': i} 
                    for i, (kw, _) in enumerate(MEMORY_PAIRS)]
        definitions = [{'id': f'd{i}', 'text': defn, 'pair_id': i} 
                       for i, (_, defn) in enumerate(MEMORY_PAIRS)]
        random.shuffle(keywords)
        random.shuffle(definitions)
        
        st.session_state.memory_state = {
            'keywords': keywords,
            'definitions': definitions,
            'selected_keyword': None,
            'selected_definition': None,
            'matched_pairs': [],
            'attempts': 0,
            'start_time': time.time(),
            'completed': False,
            'last_result': None,
            'seen_keywords': [],
        }
        st.rerun()
    
    if state is None:
        st.info("Click 'Bắt đầu / Chơi lại' để chơi!")
        return
    
    # Stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Số lượt thử", state['attempts'])
    with col2:
        st.metric("Đã ghép", f"{len(state['matched_pairs'])}/{len(MEMORY_PAIRS)}")
    with col3:
        elapsed = int(time.time() - state['start_time'])
        st.metric("Thời gian", f"{elapsed}s")
    
    # Check completion
    just_completed = False
    if len(state['matched_pairs']) == len(MEMORY_PAIRS) and not state['completed']:
        state['completed'] = True
        just_completed = True
        time_taken = int(time.time() - state['start_time'])
        bonus = max(50, 200 - state['attempts'] * 5 - time_taken)
        award_game_points(st.session_state.user['id'], bonus, 'memory_card')
        st.balloons()
        st.success(f"Hoàn thành tất cả cặp! +{bonus} điểm")
    elif state['completed']:
        st.success("Bạn đã hoàn thành game này!")
    
    # Feedback
    if state['last_result'] == 'correct':
        st.success("Ghép đúng!")
    elif state['last_result'] == 'wrong':
        st.error("Sai rồi, thử lại!")
    
    # If completed, show knowledge review
    if state['completed']:
        # All keywords in the game
        all_kws = [kw for kw, _ in MEMORY_PAIRS]
        show_knowledge_box(all_kws, "Ôn lại kiến thức")
        return
    
    st.markdown("---")
    
    # 2 columns
    col_kw, col_def = st.columns(2)
    
    with col_kw:
        st.markdown("#### Keywords")
        for idx, kw in enumerate(state['keywords']):
            is_matched = kw['pair_id'] in state['matched_pairs']
            is_selected = (state['selected_keyword'] == idx)
            
            if is_matched:
                st.success(f"✓ {kw['text']}")
            elif is_selected:
                if st.button(f"▶ {kw['text']}", key=f"kw_{idx}", 
                           use_container_width=True, type="primary"):
                    state['selected_keyword'] = None
                    state['last_result'] = None
                    st.rerun()
            else:
                if st.button(kw['text'], key=f"kw_{idx}", 
                           use_container_width=True):
                    state['selected_keyword'] = idx
                    state['last_result'] = None
                    if state['selected_definition'] is not None:
                        check_match(state)
                    st.rerun()
    
    with col_def:
        st.markdown("#### Định nghĩa")
        for idx, defn in enumerate(state['definitions']):
            is_matched = defn['pair_id'] in state['matched_pairs']
            is_selected = (state['selected_definition'] == idx)
            
            if is_matched:
                st.success(f"✓ {defn['text']}")
            elif is_selected:
                if st.button(f"▶ {defn['text']}", key=f"def_{idx}", 
                           use_container_width=True, type="primary"):
                    state['selected_definition'] = None
                    state['last_result'] = None
                    st.rerun()
            else:
                if st.button(defn['text'], key=f"def_{idx}", 
                           use_container_width=True):
                    state['selected_definition'] = idx
                    state['last_result'] = None
                    if state['selected_keyword'] is not None:
                        check_match(state)
                    st.rerun()


# =============================================================================
# GAME 2: HANGMAN PYTHON
# =============================================================================

HANGMAN_STAGES = [
    """
    ┌─────┐
    │     │
    │      
    │      
    │      
    │      
   ─┴─────
    """,
    """
    ┌─────┐
    │     │
    │     O
    │      
    │      
    │      
   ─┴─────
    """,
    """
    ┌─────┐
    │     │
    │     O
    │     │
    │      
    │      
   ─┴─────
    """,
    """
    ┌─────┐
    │     │
    │     O
    │    /│
    │      
    │      
   ─┴─────
    """,
    """
    ┌─────┐
    │     │
    │     O
    │    /│\\
    │      
    │      
   ─┴─────
    """,
    """
    ┌─────┐
    │     │
    │     O
    │    /│\\
    │    / 
    │      
   ─┴─────
    """,
    """
    ┌─────┐
    │     │
    │     X
    │    /│\\
    │    / \\
    │      
   ─┴─────
    """,
]


def game_hangman():
    """Hangman - đoán keyword Python qua từng chữ cái"""
    st.markdown("### Hangman Python — Đoán keyword qua từng chữ cái")
    st.caption("Đoán đúng chữ cái để hoàn thiện keyword. Sai 6 lần là thua!")
    
    if 'hangman_state' not in st.session_state:
        st.session_state.hangman_state = None
    
    state = st.session_state.hangman_state
    
    if state is None or st.button("Từ mới", key="hangman_new"):
        word, hint = random.choice(HANGMAN_WORDS)
        st.session_state.hangman_state = {
            'word': word.lower(),
            'original_word': word,
            'hint': hint,
            'guessed_letters': set(),
            'wrong_count': 0,
            'won': False,
            'game_over': False,
            'points_awarded': False,
        }
        st.rerun()
    
    if state is None:
        st.info("Click 'Từ mới' để bắt đầu!")
        return
    
    word = state['word']
    guessed = state['guessed_letters']
    wrong = state['wrong_count']
    MAX_WRONG = 6
    
    # Hangman + word display
    col_left, col_right = st.columns([1, 1])
    
    with col_left:
        st.code(HANGMAN_STAGES[min(wrong, 6)], language=None)
        st.caption(f"Số lần sai: {wrong}/{MAX_WRONG}")
    
    with col_right:
        st.info(f"**Gợi ý:** {state['hint']}")
        st.caption(f"Độ dài: {len(word)} chữ cái")
        
        display = " ".join([c.upper() if c in guessed else "_" for c in word])
        st.markdown(
            f"<div style='font-size: 2rem; font-weight: bold; letter-spacing: 0.2rem; "
            f"text-align: center; padding: 1rem; border: 2px solid #667eea; "
            f"border-radius: 10px;'>{display}</div>",
            unsafe_allow_html=True
        )
    
    # Check win/lose
    if not state['game_over']:
        if all(c in guessed for c in word):
            state['won'] = True
            state['game_over'] = True
            if not state['points_awarded']:
                points = max(30, 150 - wrong * 20)
                award_game_points(st.session_state.user['id'], points, 'hangman')
                state['points_awarded'] = True
                state['points'] = points
                st.balloons()
        elif wrong >= MAX_WRONG:
            state['game_over'] = True
    
    if state['game_over']:
        if state['won']:
            st.success(f"Chính xác! Từ cần đoán là **{state['original_word'].upper()}**. +{state.get('points', 0)} điểm")
        else:
            st.error(f"Thua rồi! Đáp án: **{state['original_word'].upper()}**")
        
        # Show knowledge about this word
        show_knowledge_box([state['original_word']], "Ôn lại kiến thức về từ này")
        return
    
    # Alphabet buttons
    st.markdown("---")
    st.markdown("**Chọn chữ cái:**")
    
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    
    for row_start in [0, 13]:
        cols = st.columns(13)
        for i, letter in enumerate(alphabet[row_start:row_start + 13]):
            with cols[i]:
                is_guessed = letter in guessed
                is_in_word = letter in word
                
                if is_guessed:
                    if is_in_word:
                        st.markdown(
                            f"<div style='background:#10b981; color:white; "
                            f"text-align:center; padding:0.5rem; border-radius:5px; "
                            f"font-weight:bold;'>{letter.upper()}</div>",
                            unsafe_allow_html=True
                        )
                    else:
                        st.markdown(
                            f"<div style='background:#6b7280; color:white; "
                            f"text-align:center; padding:0.5rem; border-radius:5px; "
                            f"font-weight:bold; opacity:0.5;'>{letter.upper()}</div>",
                            unsafe_allow_html=True
                        )
                else:
                    if st.button(
                        letter.upper(),
                        key=f"hangman_{letter}",
                        use_container_width=True,
                    ):
                        state['guessed_letters'].add(letter)
                        if letter not in word:
                            state['wrong_count'] += 1
                        st.rerun()


# =============================================================================
# GAME 3: BINGO SOLO
# =============================================================================

def game_bingo_solo():
    """Python Bingo - single player"""
    st.markdown("### Bingo Python — Đánh dấu ô theo định nghĩa")
    st.caption("Đọc định nghĩa, tìm và click keyword tương ứng trên bảng. Hoàn thành 1 hàng/cột/chéo = BINGO!")
    
    if 'bingo_state' not in st.session_state:
        st.session_state.bingo_state = None
    
    if st.session_state.bingo_state is None or st.button("Ván mới", key="bingo_new"):
        keywords = random.sample(BINGO_KEYWORDS, 25)
        board = [keywords[i*5:(i+1)*5] for i in range(5)]
        
        clue_queue = [kw for kw in keywords if kw in BINGO_CLUES]
        random.shuffle(clue_queue)
        
        st.session_state.bingo_state = {
            'board': board,
            'marked': set(),
            'clue_queue': clue_queue,
            'current_clue_idx': 0,
            'won': False,
            'mistakes': 0,
            'points_awarded': False,
            'seen_keywords': [],
        }
        st.session_state.bingo_state['marked'].add((2, 2))
        st.rerun()
    
    state = st.session_state.bingo_state
    
    # Check win
    def check_bingo(marked):
        for r in range(5):
            if all((r, c) in marked for c in range(5)):
                return True
        for c in range(5):
            if all((r, c) in marked for r in range(5)):
                return True
        if all((i, i) in marked for i in range(5)):
            return True
        if all((i, 4 - i) in marked for i in range(5)):
            return True
        return False
    
    # If won - show results + knowledge
    if state['won']:
        if not state['points_awarded']:
            points = max(50, 200 - state['mistakes'] * 10)
            award_game_points(st.session_state.user['id'], points, 'bingo')
            state['points_awarded'] = True
            state['points'] = points
        
        st.success(f"BINGO! +{state.get('points', 0)} điểm")
        
        # Show board final state
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Đã đánh dấu", f"{len(state['marked'])}/25")
        with col2:
            st.metric("Số lần sai", state['mistakes'])
        
        # Knowledge review
        show_knowledge_box(state['seen_keywords'], "Ôn lại keyword đã gặp")
        return
    
    # If ran out of clues without winning
    if state['current_clue_idx'] >= len(state['clue_queue']):
        st.warning("Đã hết định nghĩa mà chưa đạt Bingo. Click 'Ván mới' để chơi lại!")
        show_knowledge_box(state['seen_keywords'], "Ôn lại keyword đã gặp")
        return
    
    current_keyword = state['clue_queue'][state['current_clue_idx']]
    current_clue = BINGO_CLUES.get(current_keyword, "")
    
    st.info(f"**Định nghĩa {state['current_clue_idx'] + 1}/{len(state['clue_queue'])}:** {current_clue}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Đã đánh dấu", f"{len(state['marked'])}/25")
    with col2:
        st.metric("Số lần sai", state['mistakes'])
    
    # Render 5x5 board
    for r in range(5):
        cols = st.columns(5)
        for c in range(5):
            keyword = state['board'][r][c]
            is_marked = (r, c) in state['marked']
            is_center = (r == 2 and c == 2)
            
            with cols[c]:
                if is_marked:
                    label = "FREE" if is_center else keyword
                    st.success(label)
                else:
                    if st.button(keyword, key=f"bingo_{r}_{c}",
                                use_container_width=True):
                        # Track seen keywords
                        if keyword not in state['seen_keywords']:
                            state['seen_keywords'].append(keyword)
                        if current_keyword not in state['seen_keywords']:
                            state['seen_keywords'].append(current_keyword)
                        
                        if keyword == current_keyword:
                            state['marked'].add((r, c))
                            state['current_clue_idx'] += 1
                            
                            if check_bingo(state['marked']):
                                state['won'] = True
                                st.balloons()
                        else:
                            state['mistakes'] += 1
                            st.error(f"Sai! Đáp án đúng là: **{current_keyword}**")
                            state['current_clue_idx'] += 1
                        st.rerun()
    
    if st.button("Bỏ qua định nghĩa này", key="bingo_skip"):
        state['current_clue_idx'] += 1
        st.rerun()


# =============================================================================
# MAIN GAME CENTER
# =============================================================================

def show_game_center():
    """Main game center hub"""
    st.markdown("## Game Center")
    st.caption("Học Python qua các mini games. Điểm tích lũy tính vào Leaderboard.")
    
    if 'current_game' not in st.session_state:
        st.session_state.current_game = None
    
    if st.session_state.current_game is None:
        st.markdown("### Chọn game:")
        
        games = [
            {
                'id': 'memory',
                'name': 'Memory Card',
                'desc': 'Ghép cặp keyword với định nghĩa. Ôn vocabulary Python cơ bản.',
                'difficulty': 'Dễ',
                'time': '3-5 phút',
            },
            {
                'id': 'hangman',
                'name': 'Hangman Python',
                'desc': 'Đoán keyword Python qua từng chữ cái, có gợi ý định nghĩa.',
                'difficulty': 'Trung bình',
                'time': '2-3 phút',
            },
            {
                'id': 'bingo',
                'name': 'Python Bingo',
                'desc': 'Đọc định nghĩa, tìm keyword trên bảng 5x5, hoàn thành hàng/cột để BINGO!',
                'difficulty': 'Trung bình',
                'time': '5-10 phút',
            },
        ]
        
        cols = st.columns(3)
        for idx, game in enumerate(games):
            with cols[idx]:
                with st.container(border=True):
                    st.markdown(f"#### {game['name']}")
                    st.caption(game['desc'])
                    st.caption(f"Độ khó: {game['difficulty']} · {game['time']}")
                    if st.button("Chơi", key=f"play_{game['id']}", 
                                use_container_width=True, type="primary"):
                        st.session_state.current_game = game['id']
                        st.rerun()
        return
    
    # Back button
    if st.button("← Quay lại danh sách game"):
        for key in ['memory_state', 'hangman_state', 'bingo_state']:
            if key in st.session_state:
                del st.session_state[key]
        st.session_state.current_game = None
        st.rerun()
    
    st.markdown("---")
    
    # Route to game
    game = st.session_state.current_game
    if game == 'memory':
        game_memory_card()
    elif game == 'hangman':
        game_hangman()
    elif game == 'bingo':
        game_bingo_solo()
