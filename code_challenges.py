"""
Code challenges for all 10 chapters
Each challenge has test cases for auto-grading
"""

CODE_CHALLENGES = {
    1: [  # Chapter 1: Introduction
        {
            "id": "ch1_1",
            "title": "Hello World",
            "difficulty": "Easy",
            "description": "Viết chương trình in ra 'Hello, Python!'",
            "starter_code": "# In ra 'Hello, Python!'\n",
            "function_name": None,  # Direct execution
            "test_cases": [
                {"input": None, "expected_output": "Hello, Python!"}
            ],
            "hints": ["Dùng hàm print()", "Chú ý dấu phẩy và chấm than"],
            "solution": "print('Hello, Python!')"
        },
        {
            "id": "ch1_2",
            "title": "Tính tổng 2 số",
            "difficulty": "Easy",
            "description": "Viết function `add(a, b)` trả về tổng của a và b",
            "starter_code": "def add(a, b):\n    # Viết code ở đây\n    pass",
            "function_name": "add",
            "test_cases": [
                {"input": [1, 2], "expected": 3},
                {"input": [10, 20], "expected": 30},
                {"input": [-5, 5], "expected": 0},
                {"input": [100, 200], "expected": 300}
            ],
            "hints": ["Dùng toán tử +", "Return a + b"],
            "solution": "def add(a, b):\n    return a + b"
        }
    ],
    2: [  # Chapter 2: Operations
        {
            "id": "ch2_1",
            "title": "Kiểm tra số chẵn lẻ",
            "difficulty": "Easy",
            "description": "Viết function `is_even(n)` trả về True nếu n chẵn, False nếu lẻ",
            "starter_code": "def is_even(n):\n    # Viết code ở đây\n    pass",
            "function_name": "is_even",
            "test_cases": [
                {"input": [2], "expected": True},
                {"input": [3], "expected": False},
                {"input": [0], "expected": True},
                {"input": [100], "expected": True},
                {"input": [-5], "expected": False}
            ],
            "hints": ["Dùng toán tử % (modulo)", "n % 2 == 0 là chẵn"],
            "solution": "def is_even(n):\n    return n % 2 == 0"
        },
        {
            "id": "ch2_2",
            "title": "Tính diện tích hình chữ nhật",
            "difficulty": "Easy",
            "description": "Viết function `rectangle_area(width, height)` tính diện tích",
            "starter_code": "def rectangle_area(width, height):\n    # Viết code ở đây\n    pass",
            "function_name": "rectangle_area",
            "test_cases": [
                {"input": [3, 4], "expected": 12},
                {"input": [5, 10], "expected": 50},
                {"input": [1, 1], "expected": 1},
                {"input": [0, 100], "expected": 0}
            ],
            "hints": ["Diện tích = dài × rộng", "Return width * height"],
            "solution": "def rectangle_area(width, height):\n    return width * height"
        }
    ],
    3: [  # Chapter 3: Conditionals
        {
            "id": "ch3_1",
            "title": "Phân loại điểm",
            "difficulty": "Easy",
            "description": "Viết function `grade(score)`:\n- score >= 90: 'A'\n- score >= 80: 'B'\n- score >= 70: 'C'\n- score >= 60: 'D'\n- còn lại: 'F'",
            "starter_code": "def grade(score):\n    # Viết code ở đây\n    pass",
            "function_name": "grade",
            "test_cases": [
                {"input": [95], "expected": "A"},
                {"input": [85], "expected": "B"},
                {"input": [75], "expected": "C"},
                {"input": [65], "expected": "D"},
                {"input": [50], "expected": "F"},
                {"input": [90], "expected": "A"}
            ],
            "hints": ["Dùng if-elif-else", "Kiểm tra từ cao xuống thấp"],
            "solution": "def grade(score):\n    if score >= 90:\n        return \"A\"\n    elif score >= 80:\n        return \"B\"\n    elif score >= 70:\n        return \"C\"\n    elif score >= 60:\n        return \"D\"\n    else:\n        return \"F\""
        },
        {
            "id": "ch3_2",
            "title": "Số lớn nhất trong 3 số",
            "difficulty": "Medium",
            "description": "Viết function `max_of_three(a, b, c)` trả về số lớn nhất",
            "starter_code": "def max_of_three(a, b, c):\n    # Viết code ở đây\n    pass",
            "function_name": "max_of_three",
            "test_cases": [
                {"input": [1, 2, 3], "expected": 3},
                {"input": [10, 5, 7], "expected": 10},
                {"input": [-1, -5, -3], "expected": -1},
                {"input": [5, 5, 5], "expected": 5}
            ],
            "hints": ["Dùng if-elif", "Hoặc dùng hàm max()"],
            "solution": "def max_of_three(a, b, c):\n    return max(a, b, c)"
        }
    ],
    4: [  # Chapter 4: Loops
        {
            "id": "ch4_1",
            "title": "Tính tổng từ 1 đến n",
            "difficulty": "Easy",
            "description": "Viết function `sum_to_n(n)` tính tổng từ 1 đến n",
            "starter_code": "def sum_to_n(n):\n    # Viết code ở đây\n    pass",
            "function_name": "sum_to_n",
            "test_cases": [
                {"input": [5], "expected": 15},
                {"input": [10], "expected": 55},
                {"input": [1], "expected": 1},
                {"input": [100], "expected": 5050}
            ],
            "hints": ["Dùng for loop với range(1, n+1)", "Tích lũy vào biến total"],
            "solution": "def sum_to_n(n):\n    total = 0\n    for i in range(1, n+1):\n        total += i\n    return total"
        },
        {
            "id": "ch4_2",
            "title": "FizzBuzz",
            "difficulty": "Medium",
            "description": "Viết function `fizzbuzz(n)` trả về list từ 1 đến n:\n- Chia hết 3: 'Fizz'\n- Chia hết 5: 'Buzz'\n- Chia hết cả 3 và 5: 'FizzBuzz'\n- Còn lại: số đó (dạng string)",
            "starter_code": "def fizzbuzz(n):\n    # Viết code ở đây\n    pass",
            "function_name": "fizzbuzz",
            "test_cases": [
                {"input": [5], "expected": ["1", "2", "Fizz", "4", "Buzz"]},
                {"input": [15], "expected": ["1", "2", "Fizz", "4", "Buzz", "Fizz", "7", "8", "Fizz", "Buzz", "11", "Fizz", "13", "14", "FizzBuzz"]},
                {"input": [3], "expected": ["1", "2", "Fizz"]}
            ],
            "hints": ["Kiểm tra chia hết 15 TRƯỚC", "str(i) để convert số thành string"],
            "solution": "def fizzbuzz(n):\n    result = []\n    for i in range(1, n+1):\n        if i % 15 == 0:\n            result.append(\"FizzBuzz\")\n        elif i % 3 == 0:\n            result.append(\"Fizz\")\n        elif i % 5 == 0:\n            result.append(\"Buzz\")\n        else:\n            result.append(str(i))\n    return result"
        },
        {
            "id": "ch4_3",
            "title": "Đếm nguyên âm",
            "difficulty": "Medium",
            "description": "Viết function `count_vowels(s)` đếm số nguyên âm (a, e, i, o, u) trong string",
            "starter_code": "def count_vowels(s):\n    # Viết code ở đây\n    pass",
            "function_name": "count_vowels",
            "test_cases": [
                {"input": ["hello"], "expected": 2},
                {"input": ["python"], "expected": 1},
                {"input": ["aeiou"], "expected": 5},
                {"input": [""], "expected": 0},
                {"input": ["HELLO"], "expected": 2}
            ],
            "hints": ["Dùng for loop", "Chuyển về chữ thường với .lower()", "Kiểm tra char in 'aeiou'"],
            "solution": "def count_vowels(s):\n    count = 0\n    for char in s.lower():\n        if char in \"aeiou\":\n            count += 1\n    return count"
        }
    ],
    5: [  # Chapter 5: Functions
        {
            "id": "ch5_1",
            "title": "Giai thừa",
            "difficulty": "Medium",
            "description": "Viết function `factorial(n)` tính n! (n giai thừa)",
            "starter_code": "def factorial(n):\n    # Viết code ở đây\n    pass",
            "function_name": "factorial",
            "test_cases": [
                {"input": [0], "expected": 1},
                {"input": [1], "expected": 1},
                {"input": [5], "expected": 120},
                {"input": [7], "expected": 5040},
                {"input": [10], "expected": 3628800}
            ],
            "hints": ["n! = n * (n-1) * ... * 1", "0! = 1 (đặc biệt)", "Có thể dùng loop hoặc recursion"],
            "solution": "def factorial(n):\n    if n == 0:\n        return 1\n    result = 1\n    for i in range(1, n+1):\n        result *= i\n    return result"
        },
        {
            "id": "ch5_2",
            "title": "Kiểm tra số nguyên tố",
            "difficulty": "Medium",
            "description": "Viết function `is_prime(n)` kiểm tra n có phải số nguyên tố không",
            "starter_code": "def is_prime(n):\n    # Viết code ở đây\n    pass",
            "function_name": "is_prime",
            "test_cases": [
                {"input": [2], "expected": True},
                {"input": [3], "expected": True},
                {"input": [4], "expected": False},
                {"input": [17], "expected": True},
                {"input": [1], "expected": False},
                {"input": [100], "expected": False}
            ],
            "hints": ["Số nguyên tố > 1", "Chỉ chia hết cho 1 và chính nó", "Kiểm tra từ 2 đến sqrt(n)"],
            "solution": "def is_prime(n):\n    if n < 2:\n        return False\n    for i in range(2, int(n**0.5)+1):\n        if n % i == 0:\n            return False\n    return True"
        }
    ],
    6: [  # Chapter 6: Data Structures
        {
            "id": "ch6_1",
            "title": "Đảo ngược list",
            "difficulty": "Easy",
            "description": "Viết function `reverse_list(lst)` đảo ngược list",
            "starter_code": "def reverse_list(lst):\n    # Viết code ở đây\n    pass",
            "function_name": "reverse_list",
            "test_cases": [
                {"input": [[1, 2, 3]], "expected": [3, 2, 1]},
                {"input": [[]], "expected": []},
                {"input": [[1]], "expected": [1]},
                {"input": [["a", "b", "c"]], "expected": ["c", "b", "a"]}
            ],
            "hints": ["Dùng slicing lst[::-1]", "Hoặc dùng method reverse()", "Hoặc dùng reversed()"],
            "solution": "def reverse_list(lst):\n    return lst[::-1]"
        },
        {
            "id": "ch6_2",
            "title": "Đếm phần tử xuất hiện",
            "difficulty": "Medium",
            "description": "Viết function `count_items(lst)` trả về dict đếm số lần xuất hiện",
            "starter_code": "def count_items(lst):\n    # Viết code ở đây\n    pass",
            "function_name": "count_items",
            "test_cases": [
                {"input": [[1, 2, 2, 3, 3, 3]], "expected": {1: 1, 2: 2, 3: 3}},
                {"input": [["a", "b", "a"]], "expected": {"a": 2, "b": 1}},
                {"input": [[]], "expected": {}}
            ],
            "hints": ["Tạo dict rỗng", "Loop qua list, tăng count", "Hoặc dùng Counter từ collections"],
            "solution": "def count_items(lst):\n    result = {}\n    for item in lst:\n        result[item] = result.get(item, 0) + 1\n    return result"
        },
        {
            "id": "ch6_3",
            "title": "Union 2 list (không trùng)",
            "difficulty": "Medium",
            "description": "Viết function `union(list1, list2)` trả về list các phần tử duy nhất từ cả 2, đã sort",
            "starter_code": "def union(list1, list2):\n    # Viết code ở đây\n    pass",
            "function_name": "union",
            "test_cases": [
                {"input": [[1,2,3], [2,3,4]], "expected": [1,2,3,4]},
                {"input": [[1,2,3], []], "expected": [1,2,3]},
                {"input": [[], []], "expected": []}
            ],
            "hints": ["Dùng set để loại trùng", "sorted() để sort", "list(sorted(set(...)))"],
            "solution": "def union(list1, list2):\n    return list(sorted(set(list1) | set(list2)))"
        }
    ],
    7: [  # Chapter 7: OOP
        {
            "id": "ch7_1",
            "title": "Tạo class Rectangle",
            "difficulty": "Medium",
            "description": "Tạo class `Rectangle` với:\n- __init__(width, height)\n- method area() trả về diện tích\n- method perimeter() trả về chu vi",
            "starter_code": "class Rectangle:\n    # Viết code ở đây\n    pass\n\n# Test:\n# r = Rectangle(3, 4)\n# r.area() → 12\n# r.perimeter() → 14",
            "function_name": "Rectangle",
            "is_class": True,
            "test_cases": [
                {"code": "r = Rectangle(3, 4)\nresult = r.area()", "expected": 12},
                {"code": "r = Rectangle(5, 10)\nresult = r.perimeter()", "expected": 30},
                {"code": "r = Rectangle(1, 1)\nresult = r.area()", "expected": 1}
            ],
            "hints": ["Dùng __init__(self, width, height)", "self.width = width", "area = width * height"],
            "solution": "class Rectangle:\n    def __init__(self, width, height):\n        self.width = width\n        self.height = height\n    def area(self):\n        return self.width * self.height\n    def perimeter(self):\n        return 2 * (self.width + self.height)"
        },
        {
            "id": "ch7_2",
            "title": "Class BankAccount",
            "difficulty": "Hard",
            "description": "Tạo class `BankAccount`:\n- __init__(balance=0)\n- deposit(amount): tăng balance\n- withdraw(amount): giảm balance (không cho âm)\n- get_balance(): trả về balance",
            "starter_code": "class BankAccount:\n    # Viết code ở đây\n    pass",
            "function_name": "BankAccount",
            "is_class": True,
            "test_cases": [
                {"code": "acc = BankAccount(100)\nacc.deposit(50)\nresult = acc.get_balance()", "expected": 150},
                {"code": "acc = BankAccount(100)\nacc.withdraw(30)\nresult = acc.get_balance()", "expected": 70},
                {"code": "acc = BankAccount()\nresult = acc.get_balance()", "expected": 0}
            ],
            "hints": ["Default param: balance=0", "Check balance >= amount trong withdraw", "self.balance += amount"],
            "solution": "class BankAccount:\n    def __init__(self, balance=0):\n        self.balance = balance\n    def deposit(self, amount):\n        self.balance += amount\n    def withdraw(self, amount):\n        if amount <= self.balance:\n            self.balance -= amount\n    def get_balance(self):\n        return self.balance"
        }
    ],
    8: [  # Chapter 8: Exception
        {
            "id": "ch8_1",
            "title": "Chia an toàn",
            "difficulty": "Medium",
            "description": "Viết function `safe_divide(a, b)`:\n- Trả về a/b nếu b != 0\n- Trả về None nếu b == 0 (bắt exception)",
            "starter_code": "def safe_divide(a, b):\n    # Viết code ở đây\n    pass",
            "function_name": "safe_divide",
            "test_cases": [
                {"input": [10, 2], "expected": 5},
                {"input": [10, 0], "expected": None},
                {"input": [100, 4], "expected": 25},
                {"input": [0, 5], "expected": 0}
            ],
            "hints": ["Dùng try-except", "except ZeroDivisionError", "return None trong except"],
            "solution": "def safe_divide(a, b):\n    try:\n        return a / b\n    except ZeroDivisionError:\n        return None"
        },
        {
            "id": "ch8_2",
            "title": "Parse số an toàn",
            "difficulty": "Medium",
            "description": "Viết function `parse_int(s)`:\n- Trả về int(s) nếu convert được\n- Trả về -1 nếu không được",
            "starter_code": "def parse_int(s):\n    # Viết code ở đây\n    pass",
            "function_name": "parse_int",
            "test_cases": [
                {"input": ["42"], "expected": 42},
                {"input": ["hello"], "expected": -1},
                {"input": ["0"], "expected": 0},
                {"input": ["-10"], "expected": -10},
                {"input": ["3.14"], "expected": -1}
            ],
            "hints": ["try: return int(s)", "except ValueError: return -1"],
            "solution": "def parse_int(s):\n    try:\n        return int(s)\n    except ValueError:\n        return -1"
        }
    ],
    9: [  # Chapter 9: NumPy
        {
            "id": "ch9_1",
            "title": "Tổng các phần tử",
            "difficulty": "Easy",
            "description": "Viết function `array_sum(arr)` dùng NumPy tính tổng các phần tử",
            "starter_code": "import numpy as np\n\ndef array_sum(arr):\n    # Viết code ở đây\n    pass",
            "function_name": "array_sum",
            "needs_numpy": True,
            "test_cases": [
                {"input": [[1, 2, 3, 4, 5]], "expected": 15},
                {"input": [[10, 20, 30]], "expected": 60},
                {"input": [[0]], "expected": 0}
            ],
            "hints": ["np.array(arr)", "np.sum()", "Hoặc arr.sum()"],
            "solution": "import numpy as np\ndef array_sum(arr):\n    return int(np.sum(arr))"
        },
        {
            "id": "ch9_2",
            "title": "Trung bình cộng",
            "difficulty": "Easy",
            "description": "Viết function `array_mean(arr)` tính trung bình cộng dùng NumPy",
            "starter_code": "import numpy as np\n\ndef array_mean(arr):\n    # Viết code ở đây\n    pass",
            "function_name": "array_mean",
            "needs_numpy": True,
            "test_cases": [
                {"input": [[1, 2, 3, 4, 5]], "expected": 3.0},
                {"input": [[10, 20]], "expected": 15.0},
                {"input": [[5, 5, 5]], "expected": 5.0}
            ],
            "hints": ["np.mean()", "Hoặc arr.mean()"],
            "solution": "import numpy as np\ndef array_mean(arr):\n    return float(np.mean(arr))"
        }
    ],
    10: [  # Chapter 10: Pandas
        {
            "id": "ch10_1",
            "title": "Tạo DataFrame",
            "difficulty": "Medium",
            "description": "Viết function `create_df(names, ages)` tạo DataFrame từ 2 list\n- Columns: 'Name', 'Age'\n- Trả về số rows",
            "starter_code": "import pandas as pd\n\ndef create_df(names, ages):\n    # Tạo DataFrame và trả về số rows\n    pass",
            "function_name": "create_df",
            "needs_pandas": True,
            "test_cases": [
                {"input": [["Alice", "Bob"], [25, 30]], "expected": 2},
                {"input": [["A"], [10]], "expected": 1},
                {"input": [["A", "B", "C", "D"], [1, 2, 3, 4]], "expected": 4}
            ],
            "hints": ["pd.DataFrame({'Name': names, 'Age': ages})", "len(df) trả về số rows"],
            "solution": "import pandas as pd\ndef create_df(names, ages):\n    df = pd.DataFrame({\"Name\": names, \"Age\": ages})\n    return len(df)"
        }
    ]
}


def get_challenges(chapter_id):
    """Get challenges for a specific chapter"""
    return CODE_CHALLENGES.get(chapter_id, [])


def get_challenge_by_id(challenge_id):
    """Get a specific challenge by id"""
    for chapter_id, challenges in CODE_CHALLENGES.items():
        for challenge in challenges:
            if challenge["id"] == challenge_id:
                return challenge, chapter_id
    return None, None


def run_code_tests(user_code, challenge):
    """
    Run user code against test cases
    Returns: (passed, results, error_message)
    """
    results = []
    all_passed = True
    error_msg = None
    
    try:
        # Create safe execution environment
        safe_globals = {
            '__builtins__': __builtins__,
        }
        
        # Import numpy/pandas if needed
        if challenge.get('needs_numpy'):
            import numpy as np
            safe_globals['np'] = np
        if challenge.get('needs_pandas'):
            import pandas as pd
            safe_globals['pd'] = pd
        
        # Execute user code
        exec(user_code, safe_globals)
        
        # Run test cases
        for i, test in enumerate(challenge['test_cases'], 1):
            try:
                if challenge.get('is_class'):
                    # For class challenges
                    test_code = test['code']
                    local_vars = {}
                    exec(test_code, safe_globals, local_vars)
                    actual = local_vars.get('result')
                    expected = test['expected']
                    passed = actual == expected
                    
                elif challenge.get('function_name'):
                    # For function challenges
                    func_name = challenge['function_name']
                    if func_name not in safe_globals:
                        results.append({
                            'test_num': i,
                            'passed': False,
                            'message': f"Function '{func_name}' not found"
                        })
                        all_passed = False
                        continue
                    
                    func = safe_globals[func_name]
                    inputs = test['input']
                    expected = test['expected']
                    actual = func(*inputs)
                    passed = actual == expected
                    
                else:
                    # Direct execution (like print)
                    from io import StringIO
                    import sys
                    old_stdout = sys.stdout
                    sys.stdout = captured = StringIO()
                    exec(user_code, safe_globals)
                    sys.stdout = old_stdout
                    actual = captured.getvalue().strip()
                    expected = test['expected_output']
                    passed = actual == expected
                
                results.append({
                    'test_num': i,
                    'passed': passed,
                    'input': test.get('input', test.get('code', 'N/A')),
                    'expected': test.get('expected', test.get('expected_output')),
                    'actual': actual
                })
                
                if not passed:
                    all_passed = False
                    
            except Exception as e:
                results.append({
                    'test_num': i,
                    'passed': False,
                    'error': str(e),
                    'input': test.get('input', test.get('code', 'N/A'))
                })
                all_passed = False
    
    except SyntaxError as e:
        error_msg = f"Syntax Error: {str(e)}"
        all_passed = False
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        all_passed = False
    
    return all_passed, results, error_msg
