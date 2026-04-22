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

# 5-letter Python keywords for Pydle
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
    """Memory matching game - pair Python keyword with definition"""
    st.markdown("### Memory Card — Ghép cặp Keyword & Định nghĩa")
    st.caption("Lật 2 thẻ, ghép đúng keyword với định nghĩa của nó. Ghép hết để thắng!")
    
    # Initialize game state
    if 'memory_state' not in st.session_state:
        st.session_state.memory_state = None
    
    state = st.session_state.memory_state
    
    if state is None or st.button("Bắt đầu / Chơi lại", key="memory_new"):
        # Create shuffled cards
        cards = []
        for i, (kw, defn) in enumerate(MEMORY_PAIRS):
            cards.append({'id': f'k{i}', 'text': kw, 'pair_id': i, 'type': 'keyword'})
            cards.append({'id': f'd{i}', 'text': defn, 'pair_id': i, 'type': 'definition'})
        random.shuffle(cards)
        
        st.session_state.memory_state = {
            'cards': cards,
            'flipped': [],
            'matched': [],
            'moves': 0,
            'start_time': time.time(),
            'completed': False,
        }
        st.rerun()
    
    if state is None:
        st.info("Click 'Bắt đầu' để chơi!")
        return
    
    # Stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Số lượt", state['moves'])
    with col2:
        matched_count = len(state['matched']) // 2
        st.metric("Đã ghép", f"{matched_count}/{len(MEMORY_PAIRS)}")
    with col3:
        elapsed = int(time.time() - state['start_time'])
        st.metric("Thời gian", f"{elapsed}s")
    
    # Check completion
    if len(state['matched']) == len(state['cards']) and not state['completed']:
        state['completed'] = True
        time_taken = int(time.time() - state['start_time'])
        bonus = max(50, 200 - state['moves'] * 5 - time_taken)
        
        award_game_points(
            st.session_state.user['id'], 
            bonus, 
            'memory_card'
        )
        st.balloons()
        st.success(f"Hoàn thành! +{bonus} điểm")
        st.rerun()
    
    # Auto-hide unmatched flipped cards after 1.5s
    if len(state['flipped']) == 2:
        c1_idx, c2_idx = state['flipped']
        c1 = state['cards'][c1_idx]
        c2 = state['cards'][c2_idx]
        
        if c1['pair_id'] == c2['pair_id'] and c1['type'] != c2['type']:
            # Match!
            state['matched'].extend([c1_idx, c2_idx])
            state['flipped'] = []
        else:
            # No match - show briefly then hide
            time.sleep(1.2)
            state['flipped'] = []
            st.rerun()
    
    # Render 4x4 grid
    cols_per_row = 4
    for row in range(len(state['cards']) // cols_per_row):
        cols = st.columns(cols_per_row)
        for col_idx in range(cols_per_row):
            card_idx = row * cols_per_row + col_idx
            if card_idx >= len(state['cards']):
                continue
            
            card = state['cards'][card_idx]
            is_flipped = card_idx in state['flipped']
            is_matched = card_idx in state['matched']
            
            with cols[col_idx]:
                if is_matched:
                    st.success(card['text'])
                elif is_flipped:
                    st.info(card['text'])
                else:
                    if st.button("?", key=f"mem_card_{card_idx}", use_container_width=True):
                        if len(state['flipped']) < 2:
                            state['flipped'].append(card_idx)
                            if len(state['flipped']) == 2:
                                state['moves'] += 1
                            st.rerun()


# =============================================================================
# GAME 2: PYDLE (Wordle Python)
# =============================================================================

def game_pydle():
    """Wordle with 5-letter Python keywords"""
    st.markdown("### Pydle — Đoán keyword Python 5 chữ cái")
    st.caption("Bạn có 6 lần đoán. Xanh = đúng vị trí, Vàng = sai vị trí, Xám = không có.")
    
    if 'pydle_state' not in st.session_state:
        st.session_state.pydle_state = None
    
    state = st.session_state.pydle_state
    
    if state is None or st.button("Từ mới", key="pydle_new"):
        target = random.choice(PYDLE_WORDS).lower()
        st.session_state.pydle_state = {
            'target': target,
            'guesses': [],
            'won': False,
            'game_over': False,
        }
        st.rerun()
    
    if state is None:
        st.info("Click 'Từ mới' để bắt đầu!")
        return
    
    target = state['target']
    
    # Render previous guesses
    for guess in state['guesses']:
        cols = st.columns(5)
        for i, char in enumerate(guess):
            with cols[i]:
                if char == target[i]:
                    color = "#538d4e"  # green
                elif char in target:
                    color = "#b59f3b"  # yellow
                else:
                    color = "#3a3a3c"  # gray
                st.markdown(
                    f"""<div style='background:{color}; color:white; 
                    text-align:center; padding:1rem; border-radius:5px;
                    font-size:1.5rem; font-weight:bold;'>{char.upper()}</div>""",
                    unsafe_allow_html=True
                )
    
    # Input guess
    if not state['game_over']:
        with st.form("pydle_form", clear_on_submit=True):
            guess_input = st.text_input(
                f"Lần đoán {len(state['guesses']) + 1}/6 (5 chữ cái):",
                max_chars=5
            )
            submit = st.form_submit_button("Đoán")
            
            if submit:
                guess = guess_input.lower().strip()
                if len(guess) != 5:
                    st.error("Phải nhập đúng 5 chữ cái!")
                elif not guess.isalpha():
                    st.error("Chỉ dùng chữ cái!")
                else:
                    state['guesses'].append(guess)
                    
                    if guess == target:
                        state['won'] = True
                        state['game_over'] = True
                        points = 100 - (len(state['guesses']) - 1) * 15
                        award_game_points(st.session_state.user['id'], points, 'pydle')
                        st.balloons()
                        st.success(f"Chính xác! +{points} điểm")
                    elif len(state['guesses']) >= 6:
                        state['game_over'] = True
                        st.error(f"Hết lượt! Đáp án: **{target.upper()}**")
                    
                    st.rerun()
    else:
        if state['won']:
            st.success(f"Đã đoán đúng sau {len(state['guesses'])} lần!")
        else:
            st.error(f"Đáp án là: **{target.upper()}**")


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
                'id': 'pydle',
                'name': 'Pydle',
                'desc': 'Đoán keyword Python 5 chữ cái (kiểu Wordle)',
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
        for key in ['memory_state', 'pydle_state', 'game2048_state', 
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
    elif game == 'pydle':
        game_pydle()
    elif game == '2048py':
        game_2048py()
    elif game == 'minesweeper':
        game_minesweeper_debug()
    elif game == 'bingo':
        game_bingo_solo()
