"""
Python Learning Playground - Main Application
Features: Login, Quiz, Code Grader, Progress Tracking, Leaderboard
"""
import streamlit as st
import time
from datetime import datetime
import pandas as pd

# Import our modules
from database import (
    init_database, register_user, login_user, get_user_progress,
    update_quiz_progress, update_code_progress, get_leaderboard,
    get_user_achievements, check_and_award_achievements, get_user_stats
)
from quiz_data import get_quiz, get_all_chapters, QUIZ_QUESTIONS
from code_challenges import get_challenges, run_code_tests, CODE_CHALLENGES

# Initialize database
init_database()

# Page config
st.set_page_config(
    page_title="Python Learning Playground",
    page_icon="🐍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 1rem;
    }
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white !important;
        text-align: center;
    }
    .stat-card h1, .stat-card h2, .stat-card h3, .stat-card p {
        color: white !important;
    }
    .quiz-question {
        background: transparent;
        border: 2px solid #667eea;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    .quiz-question h4 {
        color: inherit !important;
        font-size: 1.2rem;
        font-weight: 600;
        margin: 0;
    }
    .achievement-badge {
        display: inline-block;
        background: #f0c040;
        color: #333 !important;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        margin: 0.25rem;
    }
    div[data-testid="stRadio"] label {
        font-size: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'user' not in st.session_state:
    st.session_state.user = None
if 'page' not in st.session_state:
    st.session_state.page = 'login'
if 'quiz_state' not in st.session_state:
    st.session_state.quiz_state = {}


# =============================================================================
# AUTHENTICATION PAGES
# =============================================================================

def show_login_page():
    """Display login/register page"""
    st.markdown('<h1 class="main-header">🐍 Python Learning Playground</h1>', 
                unsafe_allow_html=True)    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        tab1, tab2 = st.tabs(["🔐 Đăng nhập", "📝 Đăng ký"])
        
        with tab1:
            st.markdown("#### Đăng nhập vào tài khoản")
            
            with st.form("login_form"):
                username = st.text_input("Username hoặc Email")
                password = st.text_input("Password", type="password")
                submit = st.form_submit_button("🚀 Đăng nhập", use_container_width=True)
                
                if submit:
                    if username and password:
                        success, result = login_user(username, password)
                        if success:
                            st.session_state.user = result
                            st.session_state.page = 'dashboard'
                            st.success(f"✅ Chào mừng {result['full_name']}!")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error(f"❌ {result}")
                    else:
                        st.warning("⚠️ Vui lòng nhập đầy đủ thông tin")
        
        with tab2:
            st.markdown("#### Tạo tài khoản mới")
            
            with st.form("register_form"):
                new_username = st.text_input("Username", 
                                            help="Chỉ chữ cái, số, không dấu")
                new_email = st.text_input("Email")
                new_full_name = st.text_input("Họ và tên (optional)")
                new_password = st.text_input("Password", type="password",
                                            help="Tối thiểu 6 ký tự")
                confirm_password = st.text_input("Xác nhận password", type="password")
                
                submit_reg = st.form_submit_button("📝 Đăng ký", use_container_width=True)
                
                if submit_reg:
                    if not all([new_username, new_email, new_password]):
                        st.warning("⚠️ Vui lòng điền đầy đủ thông tin")
                    elif len(new_password) < 6:
                        st.warning("⚠️ Password phải có ít nhất 6 ký tự")
                    elif new_password != confirm_password:
                        st.error("❌ Password không khớp")
                    elif "@" not in new_email:
                        st.error("❌ Email không hợp lệ")
                    else:
                        success, msg = register_user(new_username, new_email, 
                                                   new_password, new_full_name)
                        if success:
                            st.success(f"✅ {msg} Hãy đăng nhập!")
                        else:
                            st.error(f"❌ {msg}")


# =============================================================================
# DASHBOARD
# =============================================================================

def show_dashboard():
    """Main dashboard showing user stats and progress"""
    user = st.session_state.user
    stats = get_user_stats(user['id'])
    
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    
    with col1:
        st.markdown(f"## Xin chào, **{stats['full_name']}**")
        st.caption(f"@{stats['username']} · Level {stats['level']}")
    with col2:
        st.metric("Điểm tích lũy", stats['total_points'])
    with col3:
        st.metric("Quiz hoàn thành", f"{stats['quizzes_completed']}/10")
    with col4:
        st.metric("Bài code", stats['challenges_completed'])
    
    st.markdown("---")
    st.markdown("### Tiến độ học tập")
    
    progress = get_user_progress(user['id'])
    
    total_completion = sum(p['completion_percentage'] for p in progress) / 10
    st.progress(total_completion / 100)
    st.caption(f"Tổng tiến độ: **{total_completion:.1f}%**")
    
    chapters = get_all_chapters()
    cols = st.columns(2)
    
    for idx, (chapter_id, chapter_title) in enumerate(chapters):
        chapter_progress = next((p for p in progress if p['chapter_id'] == chapter_id), 
                               {'completion_percentage': 0, 'quiz_score': 0, 
                                'challenges_completed': []})
        
        with cols[idx % 2]:
            with st.container():
                st.markdown(f" {chapter_title}"),
                completion = chapter_progress['completion_percentage']
                st.progress(completion / 100)
                
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    st.caption(f"Quiz: {chapter_progress['quiz_score']}%")
                with col_b:
                    total_challenges = len(CODE_CHALLENGES.get(chapter_id, []))
                    completed = len(chapter_progress['challenges_completed'])
                    st.caption(f"Code: {completed}/{total_challenges}")
                with col_c:
                    if completion == 100:
                        st.caption("Hoàn thành")
                    elif completion > 0:
                        st.caption(f"{completion}%")
                    else:
                        st.caption("Chưa bắt đầu")
                
                st.markdown("")


# =============================================================================
# QUIZ MODULE
# =============================================================================

def show_quiz_page():
    """Quiz interface with timer and scoring"""
    st.markdown("## Quiz - Kiểm tra kiến thức")
    
    if 'active_quiz' not in st.session_state.quiz_state:
        st.markdown("### Chọn chương để làm quiz:")
        
        chapters = get_all_chapters()
        cols = st.columns(2)
        
        for idx, (chapter_id, chapter_title) in enumerate(chapters):
            with cols[idx % 2]:
                quiz = get_quiz(chapter_id)
                num_questions = len(quiz['questions'])
                
                if st.button(
                    chapter_title ,
                    key=f"start_quiz_{chapter_id}",
                    use_container_width=True
                ):
                    st.session_state.quiz_state = {
                        'active_quiz': chapter_id,
                        'current_question': 0,
                        'answers': [],
                        'score': 0,
                        'start_time': time.time(),
                    }
                    st.rerun()
        
        return
    
    # Active quiz
    chapter_id = st.session_state.quiz_state['active_quiz']
    quiz = get_quiz(chapter_id)
    questions = quiz['questions']
    current_idx = st.session_state.quiz_state['current_question']
    
    # Quiz completed
    if current_idx >= len(questions):
        show_quiz_results(chapter_id, quiz)
        return
    
    # Display current question
    question = questions[current_idx]
    
    # Header
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.markdown(f"### {quiz['title']}")
        st.caption(f"Câu {current_idx + 1}/{len(questions)}")
    with col2:
        st.metric("Điểm", f"{st.session_state.quiz_state['score']}/{current_idx}")
    with col3:
        elapsed = int(time.time() - st.session_state.quiz_state['start_time'])
        st.metric("Thời gian", f"{elapsed}s")
    
    # Progress bar
    progress = (current_idx) / len(questions)
    st.progress(progress)
    
    # Question
    st.markdown(f"""
    <div class="quiz-question">
        <h4>❓ {question['question']}</h4>
    </div>
    """, unsafe_allow_html=True)
    
    # Options
    answer = st.radio(
        "Chọn đáp án:",
        question['options'],
        key=f"q_{current_idx}",
        index=None
    )
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        if st.button("Xác nhận", use_container_width=True, type="primary"):
            if answer is not None:
                selected_idx = question['options'].index(answer)
                is_correct = selected_idx == question['correct']
                
                st.session_state.quiz_state['answers'].append({
                    'question': question['question'],
                    'selected': answer,
                    'correct': question['options'][question['correct']],
                    'is_correct': is_correct,
                    'explanation': question['explanation']
                })
                
                if is_correct:
                    st.session_state.quiz_state['score'] += 1
                    st.success(f"Chính xác! {question['explanation']}")
                else:
                    st.error(f"Sai rồi. Đáp án đúng: **{question['options'][question['correct']]}**")
                    st.info(f"Giải thích: {question['explanation']}")
                
                time.sleep(2)
                
                st.session_state.quiz_state['current_question'] += 1
                st.rerun()
            else:
                st.warning("Vui lòng chọn đáp án!")
    
    with col1:
        if st.button("Thoát quiz", use_container_width=True):
            st.session_state.quiz_state = {}
            st.rerun()


def show_quiz_results(chapter_id, quiz):
    """Show quiz results and update progress"""
    score = st.session_state.quiz_state['score']
    total = len(quiz['questions'])
    percentage = (score / total) * 100
    time_taken = int(time.time() - st.session_state.quiz_state['start_time'])
    
    # Update database
    user_id = st.session_state.user['id']
    points_earned = update_quiz_progress(user_id, chapter_id, score, total, time_taken)
    
    # Check achievements
    new_achievements = check_and_award_achievements(user_id)
    
    st.markdown(f"## Kết quả: {quiz['title']}")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Điểm", f"{score}/{total}")
    with col2:
        st.metric("Tỉ lệ đúng", f"{percentage:.1f}%")
    with col3:
        st.metric("Thời gian", f"{time_taken}s")
    with col4:
        st.metric("Points nhận được", f"+{points_earned}")
    
    if percentage >= 90:
        st.balloons()
        st.success("Xuất sắc! Bạn đã nắm vững kiến thức chương này.")
    elif percentage >= 70:
        st.success("Tốt lắm! Tiếp tục phát huy.")
    elif percentage >= 50:
        st.warning("Khá ổn, nhưng cần ôn thêm một chút.")
    else:
        st.error("Hãy xem lại tài liệu và thử lại nhé.")
    
    if new_achievements:
        st.markdown("### Thành tích mới mở khóa!")
        for ach in new_achievements:
            st.markdown(f"**{ach['icon']} {ach['name']}**")
    
    st.markdown("---")
    st.markdown("### Xem lại câu trả lời")
    
    for i, ans in enumerate(st.session_state.quiz_state['answers'], 1):
        icon = 'Đúng' if ans['is_correct'] else 'Sai'
        with st.expander(f"Câu {i} [{icon}]: {ans['question'][:60]}..."):
            st.markdown(f"**Câu hỏi:** {ans['question']}")
            st.markdown(f"**Bạn chọn:** {ans['selected']}")
            st.markdown(f"**Đáp án đúng:** {ans['correct']}")
            st.info(f"Giải thích: {ans['explanation']}")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Làm lại", use_container_width=True):
            st.session_state.quiz_state = {}
            st.rerun()
    with col2:
        if st.button("Về Dashboard", use_container_width=True, type="primary"):
            st.session_state.quiz_state = {}
            st.session_state.page = 'dashboard'
            st.rerun()


# =============================================================================
# CODE CHALLENGES MODULE
# =============================================================================

def show_code_challenges():
    """Code challenges interface with auto-grading"""
    st.markdown("## Code Challenges")
    st.caption("Luyện tập viết code với hệ thống chấm điểm tự động.")
    
    chapters = get_all_chapters()
    chapter_options = {title: cid for cid, title in chapters}
    
    selected = st.selectbox("Chọn chương:", list(chapter_options.keys()))
    chapter_id = chapter_options[selected]
    
    challenges = get_challenges(chapter_id)
    
    if not challenges:
        st.info("Chưa có bài tập cho chương này.")
        return
    
    user_id = st.session_state.user['id']
    progress = get_user_progress(user_id)
    chapter_progress = next((p for p in progress if p['chapter_id'] == chapter_id), None)
    completed_challenges = chapter_progress['challenges_completed'] if chapter_progress else []
    
    st.markdown(f"**{len(completed_challenges)}/{len(challenges)} bài đã hoàn thành**")
    
    for challenge in challenges:
        is_completed = challenge['id'] in completed_challenges
        status = "Hoàn thành" if is_completed else challenge['difficulty']
        
        # Track failed attempts per challenge
        attempts_key = f"attempts_{challenge['id']}"
        if attempts_key not in st.session_state:
            st.session_state[attempts_key] = 0
        
        failed_attempts = st.session_state[attempts_key]
        MAX_ATTEMPTS = 3
        
        with st.expander(
            f"[{status}] {challenge['title']}",
            expanded=not is_completed
        ):
            st.markdown(f"**Yêu cầu:** {challenge['description']}")
            
            # Show attempts counter if failing
            if failed_attempts > 0 and not is_completed:
                remaining = MAX_ATTEMPTS - failed_attempts
                if remaining > 0:
                    st.warning(f"Số lần thử sai: {failed_attempts}/{MAX_ATTEMPTS} - Còn {remaining} lần trước khi hiện đáp án.")
                else:
                    st.error(f"Đã thử sai {MAX_ATTEMPTS} lần. Đáp án được hiện bên dưới.")
            
            code_key = f"code_{challenge['id']}"
            if code_key not in st.session_state:
                st.session_state[code_key] = challenge['starter_code']
            
            user_code = st.text_area(
                "Code:",
                value=st.session_state[code_key],
                height=200,
                key=f"editor_{challenge['id']}"
            )
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("Chạy & Kiểm tra", key=f"run_{challenge['id']}", 
                            use_container_width=True, type="primary"):
                    with st.spinner("Đang chạy tests..."):
                        all_passed, results, error = run_code_tests(user_code, challenge)
                        
                        if error:
                            st.error(f"Lỗi: {error}")
                            st.session_state[attempts_key] += 1
                        else:
                            passed_count = sum(1 for r in results if r['passed'])
                            total_tests = len(results)
                            
                            if all_passed:
                                # Reset attempts on success
                                st.session_state[attempts_key] = 0
                                st.success(f"Tất cả {total_tests} tests đã pass!")
                                
                                is_new, points = update_code_progress(
                                    user_id, challenge['id'], chapter_id, 
                                    user_code, True
                                )
                                
                                if is_new:
                                    st.balloons()
                                    st.success(f"+{points} điểm!")
                                    check_and_award_achievements(user_id)
                                    time.sleep(2)
                                    st.rerun()
                            else:
                                # Count failed attempt
                                st.session_state[attempts_key] += 1
                                st.warning(f"Passed {passed_count}/{total_tests} tests")
                            
                            st.markdown("**Chi tiết:**")
                            for r in results:
                                if r['passed']:
                                    st.success(f"Test {r['test_num']}: Pass")
                                else:
                                    if 'error' in r:
                                        st.error(f"Test {r['test_num']}: Lỗi - {r['error']}")
                                    else:
                                        st.error(
                                            f"Test {r['test_num']}: Fail\n"
                                            f"- Input: `{r['input']}`\n"
                                            f"- Expected: `{r['expected']}`\n"
                                            f"- Got: `{r['actual']}`"
                                        )
            
            with col2:
                if st.button("Gợi ý", key=f"hint_{challenge['id']}", 
                            use_container_width=True):
                    hints = challenge.get('hints', [])
                    if hints:
                        st.info("\n".join(f"- {h}" for h in hints))
            
            with col3:
                if st.button("Reset", key=f"reset_{challenge['id']}", 
                            use_container_width=True):
                    st.session_state[code_key] = challenge['starter_code']
                    st.session_state[attempts_key] = 0
                    st.rerun()
            
            # Show solution after MAX_ATTEMPTS failed tries
            if st.session_state[attempts_key] >= MAX_ATTEMPTS and not is_completed:
                st.markdown("---")
                st.markdown("#### Gợi ý đáp án")
                solution = challenge.get('solution', None)
                if solution:
                    st.code(solution, language="python")
                else:
                    # Auto-generate solution hint from hints list
                    st.info("Xem lại phần gợi ý bên trên và thử kết hợp chúng lại.")
                    hints = challenge.get('hints', [])
                    if hints:
                        st.code(
                            f"# Hướng dẫn từng bước:\n" +
                            "\n".join(f"# {h}" for h in hints),
                            language="python"
                        )
                
                if st.button("Thử lại từ đầu", key=f"retry_{challenge['id']}", 
                            use_container_width=True):
                    st.session_state[attempts_key] = 0
                    st.session_state[code_key] = challenge['starter_code']
                    st.rerun()


# =============================================================================
# LEADERBOARD
# =============================================================================

def show_leaderboard():
    """Show global leaderboard"""
    st.markdown("## Bảng xếp hạng")
    st.caption("Top học viên xuất sắc nhất.")
    
    leaderboard = get_leaderboard(limit=20)
    
    if not leaderboard:
        st.info("Chưa có dữ liệu. Hãy là người đầu tiên!")
        return
    
    # Top 3 podium
    if len(leaderboard) >= 3:
        st.markdown("### Top 3")
        col1, col2, col3 = st.columns(3)
        
        medals = ['2nd', '1st', '3rd']
        positions = [1, 0, 2]
        
        for col, pos in zip([col1, col2, col3], positions):
            if pos < len(leaderboard):
                user = leaderboard[pos]
                with col:
                    st.markdown(f"""
                    <div class="stat-card">
                        <h3>{medals[pos]}</h3>
                        <h2>{user['full_name']}</h2>
                        <p>@{user['username']}</p>
                        <h3>{user['total_points']} pts</h3>
                        <p>Level {user['level']} · {user['streak_days']} day streak</p>
                    </div>
                    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### Toàn bộ bảng xếp hạng")
    
    leaderboard_data = []
    for user in leaderboard:
        is_current = (user['username'] == st.session_state.user['username'])
        name = f"{user['full_name']} (bạn)" if is_current else user['full_name']
        
        leaderboard_data.append({
            'Hạng': user['rank'],
            'Tên': name,
            'Username': user['username'],
            'Điểm': user['total_points'],
            'Level': user['level'],
            'Streak': f"{user['streak_days']} ngày"
        })
    
    df = pd.DataFrame(leaderboard_data)
    st.dataframe(df, use_container_width=True, hide_index=True)


# =============================================================================
# PROFILE PAGE
# =============================================================================

def show_profile():
    """Show user profile with achievements"""
    user = st.session_state.user
    stats = get_user_stats(user['id'])
    achievements = get_user_achievements(user['id'])
    
    st.markdown("## Hồ sơ cá nhân")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div style="font-size: 4rem;">{stats['avatar']}</div>
            <h2 style="margin-top: 0.5rem;">{stats['full_name']}</h2>
            <p>@{stats['username']}</p>
            <p>Level {stats['level']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### Thống kê")
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Tổng điểm", stats['total_points'])
            st.metric("Quiz hoàn thành", stats['quizzes_completed'])
        with col_b:
            st.metric("Bài code", stats['challenges_completed'])
            st.metric("Điểm TB Quiz", f"{stats['avg_score']}%")
        
        st.markdown(f"Streak hiện tại: **{stats['streak_days']} ngày**")
        st.markdown(f"Ngày tham gia: **{stats['created_at'][:10] if stats['created_at'] else 'N/A'}**")
    
    st.markdown("---")
    
    st.markdown("### Thành tích đã đạt")
    
    if achievements:
        cols = st.columns(4)
        for idx, ach in enumerate(achievements):
            with cols[idx % 4]:
                st.markdown(f"""
                <div class="achievement-badge" style="text-align: center; width: 100%;">
                    <div style="font-size: 2rem;">{ach['icon']}</div>
                    <div><b>{ach['name']}</b></div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("Chưa có thành tích nào. Hãy làm quiz để mở khóa!")
    
    st.markdown("---")
    st.markdown("### Tất cả thành tích")
    
    all_achievements = [
        ('🥇', 'First Quiz', 'Hoàn thành quiz đầu tiên'),
        ('🏆', 'Quiz Master', 'Hoàn thành 5 quiz'),
        ('🎓', 'Python Scholar', 'Hoàn thành 10 quiz'),
        ('⚔️', 'Code Warrior', 'Giải 5 code challenges'),
        ('👑', 'Code Master', 'Giải 20 code challenges'),
        ('💯', '100 Points', 'Đạt 100 điểm'),
        ('💎', '500 Points', 'Đạt 500 điểm'),
        ('🌟', '1000 Points', 'Đạt 1000 điểm'),
        ('🔥', 'Week Streak', 'Học 7 ngày liên tiếp'),
    ]
    
    earned_names = {a['name'] for a in achievements}
    
    cols = st.columns(3)
    for idx, (icon, name, desc) in enumerate(all_achievements):
        with cols[idx % 3]:
            is_earned = name in earned_names
            opacity = "1.0" if is_earned else "0.3"
            status = "Đã đạt" if is_earned else "Chưa đạt"
            
            st.markdown(f"""
            <div style="opacity: {opacity}; padding: 0.75rem; 
                        background: #f0f2f6; border-radius: 10px; 
                        text-align: center; margin: 0.5rem 0;">
                <div style="font-size: 2rem;">{icon}</div>
                <p style="font-weight: 600; margin: 0.25rem 0;">{name}</p>
                <p style="font-size: 0.8rem; opacity: 0.7;">{desc}</p>
                <p style="font-size: 0.75rem;">{status}</p>
            </div>
            """, unsafe_allow_html=True)


# =============================================================================
# MAIN APP
# =============================================================================

def main():
    # If not logged in, show login page
    if st.session_state.user is None:
        show_login_page()
        return
    
    # Logged in - show sidebar and main content
    with st.sidebar:
        user = st.session_state.user
        stats = get_user_stats(user['id'])
        
        st.markdown(f"""
        <div style="text-align: center; padding: 1rem 0;">
            <div style="font-size: 3rem;">{stats['avatar']}</div>
            <div style="font-weight: 600; font-size: 1.1rem; margin-top: 0.5rem;">
                {stats['full_name']}
            </div>
            <div style="opacity: 0.6; font-size: 0.85rem;">
                @{stats['username']}
            </div>
            <div style="margin-top: 0.5rem; font-size: 0.9rem;">
                Level {stats['level']} &nbsp;|&nbsp; {stats['total_points']} pts
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Navigation - clean, no excessive icons
        page = st.radio(
            "Menu",
            ["Dashboard", "Quiz", "Code Challenges", "Leaderboard", "Profile"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        if st.button("Đăng xuất", use_container_width=True):
            st.session_state.user = None
            st.session_state.page = 'login'
            st.session_state.quiz_state = {}
            st.rerun()
        
        st.markdown("---")
        st.caption("Python Learning Playground v2.0")
    
    # Route to correct page
    if page == "Dashboard":
        show_dashboard()
    elif page == "Quiz":
        show_quiz_page()
    elif page == "Code Challenges":
        show_code_challenges()
    elif page == "Leaderboard":
        show_leaderboard()
    elif page == "Profile":
        show_profile()


if __name__ == "__main__":
    main()
