"""
Games module - 5 Python-themed games
- Memory Card: Match keyword with definition
- Pydle: Wordle with Python keywords
- 2048py: 2048 with Python concepts
- Minesweeper Debug: Find buggy code cells
- Bingo Solo: Python Bingo (single player)
"""
import streamlit as st
import random
import time
from database import update_code_progress
import sqlite3
from database import DB_PATH


# =============================================================================
# GAME DATA
# =============================================================================

# Python keywords & definitions for Memory Card
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

# Python keywords for Hangman (various lengths)
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


# Python keywords for Pydle (5-letter legacy, keep for compatibility)
PYDLE_WORDS = [
    "range", "while", "class", "break", "False",
    "input", "print", "float", "tuple", "yield",
    "raise", "super", "async", "await",
]

# Python keywords for 2048py (pairs that merge)
PY_MERGE_CHAIN = [
    "int", "float", "str", "list", "dict", "set", "tuple", "class"
]

# Buggy code snippets for Minesweeper
MINESWEEPER_CELLS = [
    {"code": "x = 5", "has_bug": False},
    {"code": "print('hello')", "has_bug": False},
    {"code": "if x = 5:", "has_bug": True, "bug": "Dùng = thay vì =="},
    {"code": "for i in range(10):", "has_bug": False},
    {"code": "def hello()\n    print('hi')", "has_bug": True, "bug": "Thiếu dấu : sau def"},
    {"code": "list = [1, 2, 3]", "has_bug": False},
    {"code": "print(hello)", "has_bug": True, "bug": "hello không phải string, thiếu dấu nháy"},
    {"code": "x == 5", "has_bug": False},
    {"code": "if x > 5\n    print(x)", "has_bug": True, "bug": "Thiếu dấu : sau điều kiện"},
    {"code": "my_list.append(5)", "has_bug": False},
    {"code": "for i range(5):", "has_bug": True, "bug": "Thiếu từ khóa 'in'"},
    {"code": "def add(a, b):\n    return a + b", "has_bug": False},
    {"code": "print('hi'", "has_bug": True, "bug": "Thiếu dấu đóng ngoặc"},
    {"code": "x = [1, 2, 3]\nprint(x[0])", "has_bug": False},
    {"code": "def func(:\n    pass", "has_bug": True, "bug": "Thiếu parameters hoặc dư dấu :"},
    {"code": "str(123)", "has_bug": False},
]

# Bingo keywords pool
BINGO_KEYWORDS = [
    "if", "else", "elif", "for", "while", "def", "class", "return",
    "import", "from", "as", "try", "except", "finally", "raise",
    "list", "dict", "set", "tuple", "str", "int", "float", "bool",
    "True", "False", "None", "and", "or", "not", "is", "in",
    "lambda", "yield", "pass", "break", "continue", "global",
]

# Bingo clues (definitions → keyword)
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
# HELPER - Award game points
# =============================================================================

def award_game_points(user_id, points, game_name):
    """Award points for playing games"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE users 
        SET total_points = total_points + ?,
            level = (total_points + ?) / 500 + 1
        WHERE id = ?
    """, (points, points, user_id))
    conn.commit()
    conn.close()
    return points


# =============================================================================
# GAME 1: MEMORY CARD
# =============================================================================

def game_memory_card():
    """Matching game - click to select and pair keyword with definition"""
    st.markdown("### Memory Card — Ghép cặp Keyword & Định nghĩa")
    st.caption("Click 1 keyword và 1 định nghĩa tương ứng để ghép cặp. Ghép hết để thắng!")
    
    # Initialize game state
    if 'memory_state' not in st.session_state:
        st.session_state.memory_state = None
    
    state = st.session_state.memory_state
    
    if state is None or st.button("Bắt đầu / Chơi lại", key="memory_new"):
        # Create 2 separate lists: keywords and definitions, shuffled
        keywords = [{'id': f'k{i}', 'text': kw, 'pair_id': i, 'type': 'keyword'} 
                    for i, (kw, _) in enumerate(MEMORY_PAIRS)]
        definitions = [{'id': f'd{i}', 'text': defn, 'pair_id': i, 'type': 'definition'} 
                       for i, (_, defn) in enumerate(MEMORY_PAIRS)]
        random.shuffle(keywords)
        random.shuffle(definitions)
        
        st.session_state.memory_state = {
            'keywords': keywords,
            'definitions': definitions,
            'selected_keyword': None,  # index in keywords list
            'selected_definition': None,  # index in definitions list
            'matched_pairs': [],  # list of pair_ids
            'attempts': 0,
            'start_time': time.time(),
            'completed': False,
            'last_result': None,  # 'correct' / 'wrong' / None
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
    if len(state['matched_pairs']) == len(MEMORY_PAIRS) and not state['completed']:
        state['completed'] = True
        time_taken = int(time.time() - state['start_time'])
        bonus = max(50, 200 - state['attempts'] * 5 - time_taken)
        
        award_game_points(
            st.session_state.user['id'], 
            bonus, 
            'memory_card'
        )
        st.balloons()
        st.success(f"Hoàn thành! +{bonus} điểm")
    
    # Show feedback from last attempt
    if state['last_result'] == 'correct':
        st.success("Ghép đúng!")
    elif state['last_result'] == 'wrong':
        st.error("Sai rồi, thử lại!")
    
    st.markdown("---")
    
    # Show 2 columns: Keywords (left) and Definitions (right)
    col_kw, col_def = st.columns(2)
    
    with col_kw:
        st.markdown("#### Keywords")
        for idx, kw in enumerate(state['keywords']):
            is_matched = kw['pair_id'] in state['matched_pairs']
            is_selected = (state['selected_keyword'] == idx)
            
            if is_matched:
                st.success(f"✓ {kw['text']}")
            elif is_selected:
                # Highlight selected
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
                    # If both selected → check match
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
                    # If both selected → check match
                    if state['selected_keyword'] is not None:
                        check_match(state)
                    st.rerun()


def check_match(state):
    """Helper to check if selected pair matches"""
    kw = state['keywords'][state['selected_keyword']]
    defn = state['definitions'][state['selected_definition']]
    state['attempts'] += 1
    
    if kw['pair_id'] == defn['pair_id']:
        # Match!
        state['matched_pairs'].append(kw['pair_id'])
        state['last_result'] = 'correct'
    else:
        state['last_result'] = 'wrong'
    
    # Reset selection
    state['selected_keyword'] = None
    state['selected_definition'] = None


# =============================================================================
# GAME 2: HANGMAN PYTHON
# =============================================================================

HANGMAN_STAGES = [
    # Stage 0 - chưa sai lần nào
    """
    ┌─────┐
    │     │
    │      
    │      
    │      
    │      
   ─┴─────
    """,
    # Stage 1 - sai 1 lần (đầu)
    """
    ┌─────┐
    │     │
    │     O
    │      
    │      
    │      
   ─┴─────
    """,
    # Stage 2 - sai 2 lần (thân)
    """
    ┌─────┐
    │     │
    │     O
    │     │
    │      
    │      
   ─┴─────
    """,
    # Stage 3 - sai 3 lần (tay trái)
    """
    ┌─────┐
    │     │
    │     O
    │    /│
    │      
    │      
   ─┴─────
    """,
    # Stage 4 - sai 4 lần (tay phải)
    """
    ┌─────┐
    │     │
    │     O
    │    /│\\
    │      
    │      
   ─┴─────
    """,
    # Stage 5 - sai 5 lần (chân trái)
    """
    ┌─────┐
    │     │
    │     O
    │    /│\\
    │    / 
    │      
   ─┴─────
    """,
    # Stage 6 - sai 6 lần (chân phải - GAME OVER)
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
    """Hangman - đoán từng chữ cái của keyword Python"""
    st.markdown("### Hangman Python — Đoán keyword qua từng chữ cái")
    st.caption("Đoán đúng chữ cái để hoàn thiện keyword. Sai 6 lần là thua!")
    
    if 'hangman_state' not in st.session_state:
        st.session_state.hangman_state = None
    
    state = st.session_state.hangman_state
    
    if state is None or st.button("Từ mới", key="hangman_new"):
        word, hint = random.choice(HANGMAN_WORDS)
        st.session_state.hangman_state = {
            'word': word.lower(),
            'hint': hint,
            'guessed_letters': set(),
            'wrong_count': 0,
            'won': False,
            'game_over': False,
        }
        st.rerun()
    
    if state is None:
        st.info("Click 'Từ mới' để bắt đầu!")
        return
    
    word = state['word']
    guessed = state['guessed_letters']
    wrong = state['wrong_count']
    MAX_WRONG = 6
    
    # Display hangman ASCII
    col_left, col_right = st.columns([1, 1])
    
    with col_left:
        st.code(HANGMAN_STAGES[min(wrong, 6)], language=None)
        st.caption(f"Số lần sai: {wrong}/{MAX_WRONG}")
    
    with col_right:
        # Show hint
        st.info(f"**Gợi ý:** {state['hint']}")
        st.caption(f"Độ dài: {len(word)} chữ cái")
        
        # Show word with blanks
        display = " ".join([c.upper() if c in guessed else "_" for c in word])
        st.markdown(
            f"<div style='font-size: 2rem; font-weight: bold; letter-spacing: 0.2rem; "
            f"text-align: center; padding: 1rem; border: 2px solid #667eea; "
            f"border-radius: 10px;'>{display}</div>",
            unsafe_allow_html=True
        )
    
    # Check win/lose
    if not state['game_over']:
        # Check win
        if all(c in guessed for c in word):
            state['won'] = True
            state['game_over'] = True
            points = max(30, 150 - wrong * 20)
            award_game_points(st.session_state.user['id'], points, 'hangman')
            st.balloons()
            st.success(f"Chính xác! Từ cần đoán là **{word.upper()}**. +{points} điểm")
        # Check lose
        elif wrong >= MAX_WRONG:
            state['game_over'] = True
            st.error(f"Thua rồi! Từ cần đoán là: **{word.upper()}**")
    else:
        if state['won']:
            st.success(f"Bạn đã đoán đúng: **{word.upper()}**!")
        else:
            st.error(f"Đáp án: **{word.upper()}**")
    
    # Alphabet buttons
    st.markdown("---")
    st.markdown("**Chọn chữ cái:**")
    
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    
    # Render in 2 rows of 13 letters each
    for row_start in [0, 13]:
        cols = st.columns(13)
        for i, letter in enumerate(alphabet[row_start:row_start + 13]):
            with cols[i]:
                is_guessed = letter in guessed
                is_in_word = letter in word
                
                if is_guessed:
                    # Already guessed - show disabled with color
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
                        disabled=state['game_over']
                    ):
                        state['guessed_letters'].add(letter)
                        if letter not in word:
                            state['wrong_count'] += 1
                        st.rerun()


# =============================================================================
# GAME 3: 2048py
# =============================================================================

def game_2048py():
    """2048 with Python type hierarchy"""
    st.markdown("### 2048py — Ghép kiểu dữ liệu Python")
    st.caption("Dùng các nút mũi tên để trượt. Ghép 2 ô giống nhau để tiến hóa!")
    st.caption(f"Thứ tự: {' → '.join(PY_MERGE_CHAIN)}")
    
    if 'game2048_state' not in st.session_state:
        st.session_state.game2048_state = None
    
    def new_game():
        board = [[None] * 4 for _ in range(4)]
        # Add 2 random tiles
        for _ in range(2):
            add_random_tile(board)
        return {
            'board': board,
            'score': 0,
            'game_over': False,
            'won': False,
        }
    
    def add_random_tile(board):
        empty = [(r, c) for r in range(4) for c in range(4) if board[r][c] is None]
        if empty:
            r, c = random.choice(empty)
            board[r][c] = 0  # Index in PY_MERGE_CHAIN
    
    def slide_left(board):
        """Returns new board, points earned, moved flag"""
        new_board = [[None] * 4 for _ in range(4)]
        points = 0
        moved = False
        
        for r in range(4):
            # Compact non-None values
            row = [v for v in board[r] if v is not None]
            # Merge
            merged_row = []
            skip = False
            for i in range(len(row)):
                if skip:
                    skip = False
                    continue
                if i + 1 < len(row) and row[i] == row[i + 1] and row[i] + 1 < len(PY_MERGE_CHAIN):
                    merged_row.append(row[i] + 1)
                    points += (row[i] + 1) * 10
                    skip = True
                else:
                    merged_row.append(row[i])
            # Pad with None
            while len(merged_row) < 4:
                merged_row.append(None)
            new_board[r] = merged_row
            
            if board[r] != merged_row:
                moved = True
        
        return new_board, points, moved
    
    def rotate_board(board):
        """Rotate board 90 degrees clockwise"""
        return [[board[3 - c][r] for c in range(4)] for r in range(4)]
    
    def move(board, direction):
        rotations = {'left': 0, 'up': 1, 'right': 2, 'down': 3}
        n = rotations[direction]
        
        for _ in range(n):
            board = rotate_board(board)
        
        board, points, moved = slide_left(board)
        
        for _ in range((4 - n) % 4):
            board = rotate_board(board)
        
        return board, points, moved
    
    def check_game_over(board):
        # Any empty cell?
        for r in range(4):
            for c in range(4):
                if board[r][c] is None:
                    return False
        # Any possible merge?
        for r in range(4):
            for c in range(4):
                if c + 1 < 4 and board[r][c] == board[r][c + 1]:
                    return False
                if r + 1 < 4 and board[r][c] == board[r + 1][c]:
                    return False
        return True
    
    if st.session_state.game2048_state is None or st.button("Ván mới", key="2048_new"):
        st.session_state.game2048_state = new_game()
        st.rerun()
    
    state = st.session_state.game2048_state
    board = state['board']
    
    # Score
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Điểm", state['score'])
    with col2:
        max_val = max((v for row in board for v in row if v is not None), default=0)
        st.metric("Cao nhất", PY_MERGE_CHAIN[max_val] if max_val < len(PY_MERGE_CHAIN) else "MAX")
    
    # Render board
    colors = ["#eee4da", "#ede0c8", "#f2b179", "#f59563", "#f67c5f",
              "#f65e3b", "#edcf72", "#edcc61"]
    
    for r in range(4):
        cols = st.columns(4)
        for c in range(4):
            val = board[r][c]
            with cols[c]:
                if val is None:
                    st.markdown(
                        """<div style='background:#cdc1b4; height:80px; 
                        border-radius:5px; display:flex; align-items:center; 
                        justify-content:center;'>&nbsp;</div>""",
                        unsafe_allow_html=True
                    )
                else:
                    color = colors[val % len(colors)]
                    st.markdown(
                        f"""<div style='background:{color}; height:80px; 
                        border-radius:5px; display:flex; align-items:center; 
                        justify-content:center; font-weight:bold; color:#333;'>
                        {PY_MERGE_CHAIN[val] if val < len(PY_MERGE_CHAIN) else 'MAX'}
                        </div>""",
                        unsafe_allow_html=True
                    )
    
    # Controls
    st.markdown("---")
    st.markdown("**Điều khiển:**")
    col1, col2, col3, col4 = st.columns(4)
    
    direction = None
    with col1:
        if st.button("← Trái", use_container_width=True, disabled=state['game_over']):
            direction = 'left'
    with col2:
        if st.button("↑ Lên", use_container_width=True, disabled=state['game_over']):
            direction = 'up'
    with col3:
        if st.button("↓ Xuống", use_container_width=True, disabled=state['game_over']):
            direction = 'down'
    with col4:
        if st.button("→ Phải", use_container_width=True, disabled=state['game_over']):
            direction = 'right'
    
    if direction:
        new_board, points, moved = move(board, direction)
        if moved:
            state['board'] = new_board
            state['score'] += points
            add_random_tile(state['board'])
            
            # Check win
            if not state['won']:
                for row in state['board']:
                    for v in row:
                        if v is not None and v >= len(PY_MERGE_CHAIN) - 1:
                            state['won'] = True
                            award_game_points(st.session_state.user['id'], 
                                            state['score'] // 10, '2048py')
                            st.success(f"Thắng! +{state['score'] // 10} điểm")
                            break
            
            # Check game over
            if check_game_over(state['board']):
                state['game_over'] = True
                if state['score'] > 0:
                    award_game_points(st.session_state.user['id'], 
                                    state['score'] // 20, '2048py')
            
            st.rerun()
    
    if state['game_over']:
        st.error(f"Game Over! Điểm cuối: {state['score']}")


# =============================================================================
# GAME 4: MINESWEEPER DEBUG
# =============================================================================

def game_minesweeper_debug():
    """Find the buggy code cells"""
    st.markdown("### Minesweeper Debug — Tìm code có bug")
    st.caption("Click vào ô để kiểm tra. Tìm ô KHÔNG có bug để an toàn. Click trúng bug = thua!")
    
    if 'minesweeper_state' not in st.session_state:
        st.session_state.minesweeper_state = None
    
    if st.session_state.minesweeper_state is None or st.button("Ván mới", key="mine_new"):
        cells = random.sample(MINESWEEPER_CELLS, 12)
        st.session_state.minesweeper_state = {
            'cells': cells,
            'revealed': [],
            'safe_clicked': 0,
            'game_over': False,
            'won': False,
            'start_time': time.time(),
        }
        st.rerun()
    
    state = st.session_state.minesweeper_state
    
    # Stats
    safe_total = sum(1 for c in state['cells'] if not c['has_bug'])
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Ô an toàn đã click", f"{state['safe_clicked']}/{safe_total}")
    with col2:
        st.metric("Tổng ô", len(state['cells']))
    with col3:
        elapsed = int(time.time() - state['start_time'])
        st.metric("Thời gian", f"{elapsed}s")
    
    # Check win
    if state['safe_clicked'] == safe_total and not state['won']:
        state['won'] = True
        state['game_over'] = True
        points = max(30, 150 - elapsed)
        award_game_points(st.session_state.user['id'], points, 'minesweeper')
        st.balloons()
        st.success(f"Bạn đã tìm hết ô an toàn! +{points} điểm")
    
    # Render 4x3 grid
    for row in range(3):
        cols = st.columns(4)
        for col_idx in range(4):
            cell_idx = row * 4 + col_idx
            if cell_idx >= len(state['cells']):
                continue
            
            cell = state['cells'][cell_idx]
            is_revealed = cell_idx in state['revealed']
            
            with cols[col_idx]:
                if is_revealed:
                    if cell['has_bug']:
                        st.error(f"BUG!\n```\n{cell['code']}\n```\n{cell.get('bug', '')}")
                    else:
                        st.success(f"OK\n```\n{cell['code']}\n```")
                else:
                    if st.button(f"Ô {cell_idx + 1}", 
                                key=f"mine_{cell_idx}",
                                use_container_width=True,
                                disabled=state['game_over']):
                        state['revealed'].append(cell_idx)
                        if cell['has_bug']:
                            state['game_over'] = True
                            st.error("Bạn đã click vào ô có bug!")
                        else:
                            state['safe_clicked'] += 1
                        st.rerun()
    
    if state['game_over'] and not state['won']:
        st.warning("Game Over. Click 'Ván mới' để thử lại.")


# =============================================================================
# GAME 5: BINGO SOLO
# =============================================================================

def game_bingo_solo():
    """Python Bingo - single player"""
    st.markdown("### Bingo Python — Đánh dấu ô theo định nghĩa")
    st.caption("Đọc định nghĩa bên dưới, tìm và click keyword tương ứng trên bảng. Hoàn thành 1 hàng/cột/chéo = BINGO!")
    
    if 'bingo_state' not in st.session_state:
        st.session_state.bingo_state = None
    
    if st.session_state.bingo_state is None or st.button("Ván mới", key="bingo_new"):
        # Create 5x5 board
        keywords = random.sample(BINGO_KEYWORDS, 25)
        board = [keywords[i*5:(i+1)*5] for i in range(5)]
        
        # Pick clues (same keywords from board)
        clue_queue = [kw for kw in keywords if kw in BINGO_CLUES]
        random.shuffle(clue_queue)
        
        st.session_state.bingo_state = {
            'board': board,
            'marked': set(),
            'clue_queue': clue_queue,
            'current_clue_idx': 0,
            'won': False,
            'mistakes': 0,
        }
        # Mark center as FREE
        st.session_state.bingo_state['marked'].add((2, 2))
        st.rerun()
    
    state = st.session_state.bingo_state
    
    # Check if we have clues left
    if state['current_clue_idx'] >= len(state['clue_queue']):
        if not state['won']:
            st.warning("Hết định nghĩa mà chưa Bingo. Click 'Ván mới'!")
        return
    
    current_keyword = state['clue_queue'][state['current_clue_idx']]
    current_clue = BINGO_CLUES.get(current_keyword, "")
    
    # Show clue
    st.info(f"**Định nghĩa {state['current_clue_idx'] + 1}/{len(state['clue_queue'])}:** {current_clue}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Đã đánh dấu", f"{len(state['marked'])}/25")
    with col2:
        st.metric("Sai", state['mistakes'])
    
    # Check win function
    def check_bingo(marked):
        # Rows
        for r in range(5):
            if all((r, c) in marked for c in range(5)):
                return True
        # Cols
        for c in range(5):
            if all((r, c) in marked for r in range(5)):
                return True
        # Diagonals
        if all((i, i) in marked for i in range(5)):
            return True
        if all((i, 4 - i) in marked for i in range(5)):
            return True
        return False
    
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
                                use_container_width=True,
                                disabled=state['won']):
                        if keyword == current_keyword:
                            state['marked'].add((r, c))
                            state['current_clue_idx'] += 1
                            
                            if check_bingo(state['marked']):
                                state['won'] = True
                                points = max(50, 200 - state['mistakes'] * 10)
                                award_game_points(
                                    st.session_state.user['id'], points, 'bingo'
                                )
                                st.balloons()
                                st.success(f"BINGO! +{points} điểm")
                        else:
                            state['mistakes'] += 1
                            st.error(f"Sai! '{keyword}' không phải đáp án. Đáp án là: {current_keyword}")
                            state['current_clue_idx'] += 1
                        st.rerun()
    
    # Skip button
    if not state['won']:
        if st.button("Bỏ qua định nghĩa này", key="bingo_skip"):
            state['current_clue_idx'] += 1
            st.rerun()


# =============================================================================
# MAIN GAME CENTER
# =============================================================================

def show_game_center():
    """Main game center hub"""
    st.markdown("## Game Center")
    st.caption("Học Python qua 5 mini games. Điểm tích lũy tính vào Leaderboard.")
    
    # Game selection
    if 'current_game' not in st.session_state:
        st.session_state.current_game = None
    
    if st.session_state.current_game is None:
        # Show all games
        st.markdown("### Chọn game:")
        
        games = [
            {
                'id': 'memory',
                'name': 'Memory Card',
                'desc': 'Ghép cặp keyword với định nghĩa',
                'difficulty': 'Dễ',
                'time': '3-5 phút',
            },
            {
                'id': 'hangman',
                'name': 'Hangman Python',
                'desc': 'Đoán keyword Python qua từng chữ cái',
                'difficulty': 'Trung bình',
                'time': '2-3 phút',
            },
            {
                'id': '2048py',
                'name': '2048py',
                'desc': 'Ghép kiểu dữ liệu Python',
                'difficulty': 'Trung bình',
                'time': '5-10 phút',
            },
            {
                'id': 'minesweeper',
                'name': 'Debug Minesweeper',
                'desc': 'Tìm code có bug và né tránh',
                'difficulty': 'Khó',
                'time': '3-5 phút',
            },
            {
                'id': 'bingo',
                'name': 'Python Bingo',
                'desc': 'Đánh dấu keyword theo định nghĩa',
                'difficulty': 'Trung bình',
                'time': '5-10 phút',
            },
        ]
        
        cols = st.columns(2)
        for idx, game in enumerate(games):
            with cols[idx % 2]:
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
        # Clear game-specific states
        for key in ['memory_state', 'hangman_state', 'pydle_state', 'game2048_state', 
                    'minesweeper_state', 'bingo_state']:
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
    elif game == '2048py':
        game_2048py()
    elif game == 'minesweeper':
        game_minesweeper_debug()
    elif game == 'bingo':
        game_bingo_solo()
