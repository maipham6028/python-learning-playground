"""
Quiz questions for all 10 chapters
Each chapter has 10-15 questions
"""

QUIZ_QUESTIONS = {
    1: {  # Introduction to Python
        "title": "Chapter 1: Introduction to Python",
        "questions": [
            {
                "question": "Python là ngôn ngữ lập trình kiểu gì?",
                "options": ["Compiled", "Interpreted", "Assembly", "Machine code"],
                "correct": 1,
                "explanation": "Python là ngôn ngữ thông dịch (interpreted), code được thực thi từng dòng."
            },
            {
                "question": "Ai là người tạo ra Python?",
                "options": ["James Gosling", "Guido van Rossum", "Bjarne Stroustrup", "Dennis Ritchie"],
                "correct": 1,
                "explanation": "Guido van Rossum tạo ra Python vào năm 1991."
            },
            {
                "question": "Câu lệnh nào in ra màn hình?",
                "options": ["echo()", "print()", "console.log()", "printf()"],
                "correct": 1,
                "explanation": "print() là hàm dùng để in output ra màn hình trong Python."
            },
            {
                "question": "Comment một dòng trong Python dùng ký tự gì?",
                "options": ["//", "/*", "#", "--"],
                "correct": 2,
                "explanation": "Python dùng dấu # để comment một dòng."
            },
            {
                "question": "Cách khai báo biến đúng trong Python?",
                "options": ["var x = 5", "x = 5", "int x = 5", "let x = 5"],
                "correct": 1,
                "explanation": "Python không cần khai báo kiểu, chỉ cần x = 5."
            },
            {
                "question": "Python phân biệt chữ hoa chữ thường (case-sensitive)?",
                "options": ["Có", "Không", "Tùy trường hợp", "Chỉ với hàm"],
                "correct": 0,
                "explanation": "Python là case-sensitive: 'name' và 'Name' là 2 biến khác nhau."
            },
            {
                "question": "Kết quả của `print(\"Hello\" + \" \" + \"World\")` là?",
                "options": ["HelloWorld", "Hello World", "Hello+World", "Error"],
                "correct": 1,
                "explanation": "Toán tử + nối các string lại, tạo ra 'Hello World'."
            },
            {
                "question": "Câu lệnh nào nhận input từ người dùng?",
                "options": ["read()", "scan()", "input()", "get()"],
                "correct": 2,
                "explanation": "input() dùng để nhận dữ liệu từ người dùng."
            },
            {
                "question": "Input() trả về kiểu dữ liệu gì?",
                "options": ["int", "float", "str", "bool"],
                "correct": 2,
                "explanation": "input() luôn trả về string, cần convert nếu muốn dùng số."
            },
            {
                "question": "Extension file Python là gì?",
                "options": [".py", ".python", ".pt", ".pyt"],
                "correct": 0,
                "explanation": "File Python có đuôi .py"
            }
        ]
    },
    2: {  # Operations & Syntax
        "title": "Chapter 2: Operations & Syntax",
        "questions": [
            {
                "question": "Kết quả của `7 // 2`?",
                "options": ["3.5", "3", "4", "2"],
                "correct": 1,
                "explanation": "// là floor division, 7 // 2 = 3 (phần nguyên)."
            },
            {
                "question": "Kết quả của `7 % 2`?",
                "options": ["3", "0", "1", "3.5"],
                "correct": 2,
                "explanation": "% là modulo (lấy phần dư), 7 % 2 = 1."
            },
            {
                "question": "Kết quả của `2 ** 3`?",
                "options": ["6", "8", "9", "5"],
                "correct": 1,
                "explanation": "** là lũy thừa, 2 ** 3 = 2³ = 8."
            },
            {
                "question": "Kiểu dữ liệu của `3.14`?",
                "options": ["int", "float", "str", "double"],
                "correct": 1,
                "explanation": "Số thập phân trong Python là kiểu float."
            },
            {
                "question": "Kết quả của `0.1 + 0.2 == 0.3`?",
                "options": ["True", "False", "Error", "None"],
                "correct": 1,
                "explanation": "Do lỗi làm tròn float, 0.1 + 0.2 = 0.30000000000000004, không bằng 0.3."
            },
            {
                "question": "Chuyển '42' sang int dùng hàm nào?",
                "options": ["str()", "int()", "float()", "number()"],
                "correct": 1,
                "explanation": "int('42') chuyển string thành integer."
            },
            {
                "question": "Thứ tự ưu tiên: `2 + 3 * 4`?",
                "options": ["20", "14", "24", "11"],
                "correct": 1,
                "explanation": "Nhân trước cộng: 3*4=12, sau đó 2+12=14."
            },
            {
                "question": "Toán tử nào KHÔNG phải comparison?",
                "options": ["==", "!=", "=", ">="],
                "correct": 2,
                "explanation": "= là gán giá trị, không phải so sánh. == mới là so sánh."
            },
            {
                "question": "f-string đúng cú pháp?",
                "options": ["f\"Hello {name}\"", "\"Hello {name}\"", "f'Hello $name'", "\"Hello \" + name"],
                "correct": 0,
                "explanation": "f-string dùng f\"\" với biến trong {}."
            },
            {
                "question": "Kết quả của `'Ha' * 3`?",
                "options": ["Ha3", "HaHaHa", "Error", "Ha Ha Ha"],
                "correct": 1,
                "explanation": "Toán tử * với string là repetition: 'Ha' * 3 = 'HaHaHa'."
            }
        ]
    },
    3: {  # Conditionals
        "title": "Chapter 3: Conditionals",
        "questions": [
            {
                "question": "Câu lệnh điều kiện trong Python?",
                "options": ["switch", "if-else", "case", "when"],
                "correct": 1,
                "explanation": "Python dùng if-elif-else cho điều kiện."
            },
            {
                "question": "Kết quả của `True and False`?",
                "options": ["True", "False", "None", "Error"],
                "correct": 1,
                "explanation": "AND chỉ True khi cả hai đều True."
            },
            {
                "question": "Kết quả của `True or False`?",
                "options": ["True", "False", "None", "Error"],
                "correct": 0,
                "explanation": "OR True khi ít nhất một vế True."
            },
            {
                "question": "Cú pháp if đúng?",
                "options": ["if (x > 5) {}", "if x > 5:", "if x > 5 then", "if [x > 5]"],
                "correct": 1,
                "explanation": "Python dùng if condition: và indentation."
            },
            {
                "question": "elif là viết tắt của?",
                "options": ["else if", "end if", "elif", "exit if"],
                "correct": 0,
                "explanation": "elif = else if, dùng cho nhiều điều kiện."
            },
            {
                "question": "Output của `x = 5; print('big' if x > 3 else 'small')`?",
                "options": ["big", "small", "Error", "5"],
                "correct": 0,
                "explanation": "Ternary operator: x > 3 là True nên in 'big'."
            },
            {
                "question": "Kết quả của `not True`?",
                "options": ["True", "False", "None", "Error"],
                "correct": 1,
                "explanation": "not đảo ngược giá trị: not True = False."
            },
            {
                "question": "Indentation trong Python dùng để?",
                "options": ["Trang trí", "Định nghĩa code block", "Comment", "Không bắt buộc"],
                "correct": 1,
                "explanation": "Python dùng indentation để xác định code block, bắt buộc!"
            },
            {
                "question": "Kết quả của `bool(0)`?",
                "options": ["True", "False", "0", "None"],
                "correct": 1,
                "explanation": "Số 0 được coi là False trong Python."
            },
            {
                "question": "Short-circuit evaluation của `False and any_func()`?",
                "options": ["Chạy any_func()", "Không chạy any_func()", "Error", "True"],
                "correct": 1,
                "explanation": "AND với False đầu tiên → không cần đánh giá phần còn lại."
            }
        ]
    },
    4: {  # Loops
        "title": "Chapter 4: Loops",
        "questions": [
            {
                "question": "Vòng lặp nào dùng khi biết trước số lần lặp?",
                "options": ["while", "for", "do-while", "repeat"],
                "correct": 1,
                "explanation": "for loop dùng khi biết trước số lần lặp."
            },
            {
                "question": "`range(5)` tạo ra các số?",
                "options": ["1,2,3,4,5", "0,1,2,3,4", "0,1,2,3,4,5", "1,2,3,4"],
                "correct": 1,
                "explanation": "range(5) tạo 0,1,2,3,4 (không bao gồm 5)."
            },
            {
                "question": "`range(2, 8, 2)` tạo ra?",
                "options": ["2,3,4,5,6,7", "2,4,6", "2,4,6,8", "2,8"],
                "correct": 1,
                "explanation": "range(start=2, stop=8, step=2) = 2, 4, 6."
            },
            {
                "question": "Từ khóa nào thoát khỏi vòng lặp?",
                "options": ["exit", "stop", "break", "end"],
                "correct": 2,
                "explanation": "break thoát khỏi vòng lặp ngay lập tức."
            },
            {
                "question": "Từ khóa nào bỏ qua iteration hiện tại?",
                "options": ["skip", "continue", "pass", "next"],
                "correct": 1,
                "explanation": "continue bỏ qua iteration hiện tại, tiếp tục lần tiếp theo."
            },
            {
                "question": "Vòng lặp vô hạn xảy ra khi?",
                "options": ["Điều kiện luôn True", "Điều kiện luôn False", "Không có điều kiện", "Dùng for"],
                "correct": 0,
                "explanation": "While với điều kiện luôn True sẽ chạy mãi mãi."
            },
            {
                "question": "Số lần lặp của `for i in range(3): for j in range(2):`?",
                "options": ["3", "5", "6", "2"],
                "correct": 2,
                "explanation": "Nested loop: 3 × 2 = 6 lần."
            },
            {
                "question": "`for char in 'abc':` lặp qua?",
                "options": ["Toàn bộ string", "Từng ký tự", "Chỉ 'a'", "Error"],
                "correct": 1,
                "explanation": "For loop với string lặp qua từng ký tự."
            },
            {
                "question": "`else` với for loop chạy khi?",
                "options": ["Luôn chạy", "Khi loop kết thúc bình thường", "Khi có break", "Không bao giờ"],
                "correct": 1,
                "explanation": "else chạy khi for loop kết thúc mà không có break."
            },
            {
                "question": "Output của `for i in range(3): print(i, end=' ')`?",
                "options": ["1 2 3", "0 1 2", "0 1 2 3", "1 2 3 4"],
                "correct": 1,
                "explanation": "range(3) = 0,1,2. end=' ' in cùng dòng với space."
            }
        ]
    },
    5: {  # Functions
        "title": "Chapter 5: Functions",
        "questions": [
            {
                "question": "Từ khóa định nghĩa function?",
                "options": ["function", "def", "func", "define"],
                "correct": 1,
                "explanation": "Python dùng def để định nghĩa function."
            },
            {
                "question": "Câu lệnh trả về giá trị từ function?",
                "options": ["send", "return", "output", "yield"],
                "correct": 1,
                "explanation": "return trả về giá trị và kết thúc function."
            },
            {
                "question": "Function không có return sẽ trả về?",
                "options": ["0", "None", "False", "Error"],
                "correct": 1,
                "explanation": "Function không có return tự động trả về None."
            },
            {
                "question": "`def f(x, y=10):` - y là?",
                "options": ["Required parameter", "Optional parameter", "Keyword argument", "Error"],
                "correct": 1,
                "explanation": "y=10 là default value, nên y là optional parameter."
            },
            {
                "question": "`*args` trong function nghĩa là?",
                "options": ["Một argument", "Nhiều positional args", "Keyword args", "Error"],
                "correct": 1,
                "explanation": "*args cho phép nhận nhiều positional arguments."
            },
            {
                "question": "`**kwargs` nhận?",
                "options": ["Positional args", "Keyword args", "Một dict", "Error"],
                "correct": 1,
                "explanation": "**kwargs nhận nhiều keyword arguments dưới dạng dict."
            },
            {
                "question": "Lambda function đúng cú pháp?",
                "options": ["lambda x: x*2", "lambda(x): x*2", "lambda x -> x*2", "(x) => x*2"],
                "correct": 0,
                "explanation": "Lambda: `lambda parameters: expression`"
            },
            {
                "question": "Scope của biến bên trong function?",
                "options": ["Global", "Local", "Tùy", "Không có"],
                "correct": 1,
                "explanation": "Biến khai báo trong function có local scope."
            },
            {
                "question": "Từ khóa nào làm biến thành global bên trong function?",
                "options": ["public", "global", "extern", "static"],
                "correct": 1,
                "explanation": "Dùng global keyword để access biến global."
            },
            {
                "question": "Docstring của function được đặt ở đâu?",
                "options": ["Trước def", "Dòng đầu sau def", "Cuối function", "Bất kỳ"],
                "correct": 1,
                "explanation": "Docstring là string ở dòng đầu tiên trong function body."
            }
        ]
    },
    6: {  # Data Structures
        "title": "Chapter 6: Data Structures",
        "questions": [
            {
                "question": "List trong Python mutable hay immutable?",
                "options": ["Mutable", "Immutable", "Tùy", "Không xác định"],
                "correct": 0,
                "explanation": "List là mutable - có thể thay đổi sau khi tạo."
            },
            {
                "question": "Tuple mutable hay immutable?",
                "options": ["Mutable", "Immutable", "Tùy", "Không xác định"],
                "correct": 1,
                "explanation": "Tuple là immutable - không thể thay đổi."
            },
            {
                "question": "Cú pháp tạo dictionary?",
                "options": ["[]", "()", "{}", "<>"],
                "correct": 2,
                "explanation": "Dictionary dùng {key: value}."
            },
            {
                "question": "`my_list[-1]` trả về?",
                "options": ["Phần tử đầu", "Phần tử cuối", "Error", "None"],
                "correct": 1,
                "explanation": "Index âm đếm từ cuối: -1 là phần tử cuối cùng."
            },
            {
                "question": "Method thêm phần tử vào cuối list?",
                "options": ["add()", "push()", "append()", "insert()"],
                "correct": 2,
                "explanation": "append() thêm element vào cuối list."
            },
            {
                "question": "Set có phần tử trùng lặp không?",
                "options": ["Có", "Không", "Tùy", "1 phần tử trùng"],
                "correct": 1,
                "explanation": "Set không cho phép phần tử trùng lặp."
            },
            {
                "question": "Truy cập value của dict theo key?",
                "options": ["dict.key", "dict[key]", "dict(key)", "dict->key"],
                "correct": 1,
                "explanation": "Dùng dict[key] để lấy value."
            },
            {
                "question": "Slicing `my_list[1:4]` lấy?",
                "options": ["Index 1,2,3", "Index 1,2,3,4", "Index 0,1,2,3", "Error"],
                "correct": 0,
                "explanation": "Slicing [1:4] lấy index 1, 2, 3 (không bao gồm 4)."
            },
            {
                "question": "Method xóa phần tử cuối list?",
                "options": ["remove()", "pop()", "delete()", "del()"],
                "correct": 1,
                "explanation": "pop() mặc định xóa và trả về phần tử cuối."
            },
            {
                "question": "List comprehension `[x*2 for x in range(3)]` trả về?",
                "options": ["[0,2,4]", "[1,2,3]", "[2,4,6]", "Error"],
                "correct": 0,
                "explanation": "range(3) = 0,1,2. Mỗi x*2 = 0,2,4."
            }
        ]
    },
    7: {  # OOP
        "title": "Chapter 7: Object-Oriented Programming",
        "questions": [
            {
                "question": "Từ khóa định nghĩa class?",
                "options": ["class", "Class", "struct", "object"],
                "correct": 0,
                "explanation": "Dùng class (chữ thường) để định nghĩa class."
            },
            {
                "question": "Method khởi tạo trong class?",
                "options": ["__start__", "__init__", "__new__", "constructor"],
                "correct": 1,
                "explanation": "__init__ là constructor trong Python."
            },
            {
                "question": "`self` trong class là?",
                "options": ["Từ khóa", "Tham chiếu đến instance", "Class name", "Biến toàn cục"],
                "correct": 1,
                "explanation": "self tham chiếu đến instance hiện tại của class."
            },
            {
                "question": "Tạo object từ class `Dog`?",
                "options": ["Dog()", "new Dog()", "Dog.new()", "create Dog"],
                "correct": 0,
                "explanation": "Python tạo object bằng cách gọi class như function: Dog()."
            },
            {
                "question": "Kế thừa class trong Python?",
                "options": ["class B extends A", "class B(A)", "class B : A", "class B inherits A"],
                "correct": 1,
                "explanation": "Python dùng class B(A): để kế thừa."
            },
            {
                "question": "Đặc trưng nào KHÔNG phải OOP?",
                "options": ["Encapsulation", "Inheritance", "Polymorphism", "Recursion"],
                "correct": 3,
                "explanation": "Recursion không phải đặc trưng OOP. OOP: Encapsulation, Inheritance, Polymorphism, Abstraction."
            },
            {
                "question": "Method ghi đè (override) từ class cha?",
                "options": ["@override", "Định nghĩa lại với cùng tên", "super()", "extends"],
                "correct": 1,
                "explanation": "Chỉ cần định nghĩa lại method cùng tên ở class con."
            },
            {
                "question": "`super()` dùng để?",
                "options": ["Tạo class cha", "Gọi method class cha", "Xóa class cha", "Kiểm tra class cha"],
                "correct": 1,
                "explanation": "super() dùng để gọi methods từ class cha."
            },
            {
                "question": "Attribute có dấu `_` đầu là?",
                "options": ["Public", "Private", "Protected convention", "Static"],
                "correct": 2,
                "explanation": "_attribute là convention cho protected (Python không có private thực sự)."
            },
            {
                "question": "Class method vs Instance method khác nhau?",
                "options": ["Không khác", "Instance method dùng self, class method dùng cls", "Class method không dùng được", "Instance method static"],
                "correct": 1,
                "explanation": "Instance method dùng self, class method dùng cls với @classmethod."
            }
        ]
    },
    8: {  # Exception Handling
        "title": "Chapter 8: Exception Handling",
        "questions": [
            {
                "question": "Khối xử lý exception trong Python?",
                "options": ["try-catch", "try-except", "try-handle", "catch-throw"],
                "correct": 1,
                "explanation": "Python dùng try-except (không phải try-catch)."
            },
            {
                "question": "Khối chạy dù có exception hay không?",
                "options": ["finally", "always", "end", "last"],
                "correct": 0,
                "explanation": "finally luôn chạy, dù có exception hay không."
            },
            {
                "question": "Chia cho 0 gây ra exception nào?",
                "options": ["ValueError", "TypeError", "ZeroDivisionError", "ArithmeticError"],
                "correct": 2,
                "explanation": "10/0 → ZeroDivisionError."
            },
            {
                "question": "Truy cập index vượt quá list?",
                "options": ["ValueError", "IndexError", "KeyError", "TypeError"],
                "correct": 1,
                "explanation": "list[100] khi list có 3 phần tử → IndexError."
            },
            {
                "question": "Truy cập key không tồn tại trong dict?",
                "options": ["IndexError", "KeyError", "ValueError", "LookupError"],
                "correct": 1,
                "explanation": "dict['missing'] → KeyError."
            },
            {
                "question": "Chủ động raise exception?",
                "options": ["throw", "raise", "error", "except"],
                "correct": 1,
                "explanation": "Python dùng raise để throw exception."
            },
            {
                "question": "Chuyển string không hợp lệ sang int?",
                "options": ["ValueError", "TypeError", "SyntaxError", "ConvertError"],
                "correct": 0,
                "explanation": "int('hello') → ValueError."
            },
            {
                "question": "Bắt tất cả exception?",
                "options": ["except:", "except Exception:", "Cả hai đúng", "except all:"],
                "correct": 2,
                "explanation": "Cả `except:` và `except Exception:` đều bắt mọi exception (Exception là base class)."
            },
            {
                "question": "`else` trong try-except chạy khi?",
                "options": ["Có exception", "Không có exception", "Luôn chạy", "Không bao giờ"],
                "correct": 1,
                "explanation": "else trong try-except chỉ chạy khi KHÔNG có exception."
            },
            {
                "question": "Tạo custom exception?",
                "options": ["Extend Error", "Inherit từ Exception", "@exception", "def exception"],
                "correct": 1,
                "explanation": "Custom exception: class MyError(Exception): pass"
            }
        ]
    },
    9: {  # NumPy
        "title": "Chapter 9: NumPy",
        "questions": [
            {
                "question": "Import NumPy đúng convention?",
                "options": ["import numpy", "import numpy as np", "from numpy import *", "import np"],
                "correct": 1,
                "explanation": "Convention chuẩn: import numpy as np"
            },
            {
                "question": "Tạo array NumPy từ list?",
                "options": ["np.array([1,2,3])", "np.list([1,2,3])", "np.create([1,2,3])", "numpy([1,2,3])"],
                "correct": 0,
                "explanation": "np.array() tạo array từ list."
            },
            {
                "question": "Tạo array toàn số 0, shape (3,3)?",
                "options": ["np.zero(3,3)", "np.zeros((3,3))", "np.empty(3,3)", "np.null(3,3)"],
                "correct": 1,
                "explanation": "np.zeros() với tuple shape."
            },
            {
                "question": "`arr.shape` trả về?",
                "options": ["Số phần tử", "Hình dạng array", "Kiểu dữ liệu", "Dimension"],
                "correct": 1,
                "explanation": "shape trả về tuple mô tả kích thước array."
            },
            {
                "question": "`np.arange(0, 10, 2)` tạo?",
                "options": ["[0,2,4,6,8,10]", "[0,2,4,6,8]", "[2,4,6,8]", "[0,1,2,...,10]"],
                "correct": 1,
                "explanation": "arange(start=0, stop=10, step=2) = [0,2,4,6,8]."
            },
            {
                "question": "Ưu điểm NumPy so với Python list?",
                "options": ["Dễ code hơn", "Nhanh hơn với dữ liệu số", "Nhiều tính năng", "Miễn phí"],
                "correct": 1,
                "explanation": "NumPy nhanh hơn list cho operations số học nhờ C implementation."
            },
            {
                "question": "Broadcasting trong NumPy?",
                "options": ["Copy array", "Phép toán trên arrays khác shape", "Gửi data", "Parallel computing"],
                "correct": 1,
                "explanation": "Broadcasting cho phép thực hiện phép toán trên arrays có shape khác nhau."
            },
            {
                "question": "`np.dot(a, b)` là?",
                "options": ["Cộng", "Nhân element-wise", "Nhân ma trận", "Chia"],
                "correct": 2,
                "explanation": "np.dot() là phép nhân ma trận (dot product)."
            },
            {
                "question": "`arr.reshape(2,3)` làm gì?",
                "options": ["Copy array", "Đổi shape thành (2,3)", "Sort array", "Delete elements"],
                "correct": 1,
                "explanation": "reshape() thay đổi hình dạng array."
            },
            {
                "question": "Số phần tử trong np.zeros((2,3,4))?",
                "options": ["9", "12", "24", "6"],
                "correct": 2,
                "explanation": "2 × 3 × 4 = 24 phần tử."
            }
        ]
    },
    10: {  # Pandas & Matplotlib
        "title": "Chapter 10: Pandas & Matplotlib",
        "questions": [
            {
                "question": "Import Pandas theo convention?",
                "options": ["import pandas", "import pandas as pd", "import pd", "from pandas import *"],
                "correct": 1,
                "explanation": "Convention: import pandas as pd"
            },
            {
                "question": "Cấu trúc dữ liệu 2D trong Pandas?",
                "options": ["Series", "DataFrame", "Array", "List"],
                "correct": 1,
                "explanation": "DataFrame là bảng 2D, Series là 1D."
            },
            {
                "question": "Đọc file CSV?",
                "options": ["pd.read_csv()", "pd.open_csv()", "pd.load_csv()", "pd.csv()"],
                "correct": 0,
                "explanation": "pd.read_csv() đọc file CSV thành DataFrame."
            },
            {
                "question": "Xem 5 dòng đầu DataFrame?",
                "options": ["df.top()", "df.head()", "df.first()", "df.show()"],
                "correct": 1,
                "explanation": "df.head() mặc định hiển thị 5 dòng đầu."
            },
            {
                "question": "Thông tin tổng quan DataFrame?",
                "options": ["df.info()", "df.describe()", "Cả hai", "df.summary()"],
                "correct": 2,
                "explanation": "info() cho cấu trúc, describe() cho thống kê. Cả hai đều hữu ích."
            },
            {
                "question": "Import Matplotlib?",
                "options": ["import matplotlib", "import matplotlib.pyplot as plt", "import plt", "from matplotlib import *"],
                "correct": 1,
                "explanation": "Convention: import matplotlib.pyplot as plt"
            },
            {
                "question": "Vẽ biểu đồ đường?",
                "options": ["plt.line()", "plt.plot()", "plt.draw()", "plt.graph()"],
                "correct": 1,
                "explanation": "plt.plot() là hàm cơ bản vẽ line chart."
            },
            {
                "question": "Hiển thị biểu đồ?",
                "options": ["plt.display()", "plt.show()", "plt.render()", "plt.view()"],
                "correct": 1,
                "explanation": "plt.show() hiển thị biểu đồ."
            },
            {
                "question": "Vẽ biểu đồ cột?",
                "options": ["plt.plot()", "plt.bar()", "plt.col()", "plt.chart()"],
                "correct": 1,
                "explanation": "plt.bar() vẽ bar chart."
            },
            {
                "question": "Lọc DataFrame theo điều kiện?",
                "options": ["df.filter()", "df[df['col'] > 5]", "df.where()", "Cả hai đều được"],
                "correct": 1,
                "explanation": "Boolean indexing: df[df['col'] > 5] là cách phổ biến nhất."
            }
        ]
    }
}


def get_quiz(chapter_id):
    """Get quiz for a specific chapter"""
    return QUIZ_QUESTIONS.get(chapter_id, None)


def get_all_chapters():
    """Get list of all chapter titles"""
    return [(i, QUIZ_QUESTIONS[i]["title"]) for i in sorted(QUIZ_QUESTIONS.keys())]
