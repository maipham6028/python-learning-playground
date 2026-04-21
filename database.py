"""
Database module - Handles all database operations
Uses SQLite (no external database needed)
"""
import sqlite3
import hashlib
import json
from datetime import datetime
from pathlib import Path

DB_PATH = "python_playground.db"


def init_database():
    """Initialize database with all required tables"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            full_name TEXT,
            avatar TEXT DEFAULT '👤',
            level INTEGER DEFAULT 1,
            total_points INTEGER DEFAULT 0,
            streak_days INTEGER DEFAULT 0,
            last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Progress table - tracks chapter completion
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            chapter_id INTEGER,
            quiz_score INTEGER DEFAULT 0,
            quiz_completed INTEGER DEFAULT 0,
            challenges_completed TEXT DEFAULT '[]',
            completion_percentage INTEGER DEFAULT 0,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            UNIQUE(user_id, chapter_id)
        )
    """)
    
    # Quiz attempts table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quiz_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            chapter_id INTEGER,
            score INTEGER,
            total_questions INTEGER,
            time_taken INTEGER,
            completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    
    # Code submissions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS code_submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            challenge_id TEXT,
            code TEXT,
            passed INTEGER DEFAULT 0,
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    
    # Achievements table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS achievements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            badge_name TEXT,
            badge_icon TEXT,
            unlocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            UNIQUE(user_id, badge_name)
        )
    """)
    
    conn.commit()
    conn.close()


def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()


def register_user(username, email, password, full_name=""):
    """Register a new user"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        password_hash = hash_password(password)
        cursor.execute("""
            INSERT INTO users (username, email, password_hash, full_name)
            VALUES (?, ?, ?, ?)
        """, (username, email, password_hash, full_name or username))
        
        user_id = cursor.lastrowid
        
        # Initialize progress for all 10 chapters
        for chapter_id in range(1, 11):
            cursor.execute("""
                INSERT INTO progress (user_id, chapter_id)
                VALUES (?, ?)
            """, (user_id, chapter_id))
        
        conn.commit()
        return True, "Đăng ký thành công!"
    
    except sqlite3.IntegrityError as e:
        if "username" in str(e):
            return False, "Username đã tồn tại!"
        elif "email" in str(e):
            return False, "Email đã được sử dụng!"
        return False, f"Lỗi: {str(e)}"
    finally:
        conn.close()


def login_user(username, password):
    """Login user and return user info"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    password_hash = hash_password(password)
    
    cursor.execute("""
        SELECT id, username, email, full_name, avatar, level, total_points, streak_days
        FROM users 
        WHERE (username = ? OR email = ?) AND password_hash = ?
    """, (username, username, password_hash))
    
    user = cursor.fetchone()
    
    if user:
        # Update last active
        cursor.execute("""
            UPDATE users SET last_active = CURRENT_TIMESTAMP WHERE id = ?
        """, (user[0],))
        conn.commit()
        
        user_data = {
            'id': user[0],
            'username': user[1],
            'email': user[2],
            'full_name': user[3],
            'avatar': user[4],
            'level': user[5],
            'total_points': user[6],
            'streak_days': user[7]
        }
        conn.close()
        return True, user_data
    
    conn.close()
    return False, "Sai username hoặc password!"


def get_user_progress(user_id):
    """Get user's progress across all chapters"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT chapter_id, quiz_score, quiz_completed, 
               challenges_completed, completion_percentage
        FROM progress 
        WHERE user_id = ?
        ORDER BY chapter_id
    """, (user_id,))
    
    progress = []
    for row in cursor.fetchall():
        progress.append({
            'chapter_id': row[0],
            'quiz_score': row[1],
            'quiz_completed': bool(row[2]),
            'challenges_completed': json.loads(row[3]) if row[3] else [],
            'completion_percentage': row[4]
        })
    
    conn.close()
    return progress


def update_quiz_progress(user_id, chapter_id, score, total_questions, time_taken):
    """Update user's quiz progress"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Record attempt
    cursor.execute("""
        INSERT INTO quiz_attempts (user_id, chapter_id, score, total_questions, time_taken)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, chapter_id, score, total_questions, time_taken))
    
    # Calculate percentage
    percentage = int((score / total_questions) * 100) if total_questions > 0 else 0
    points_earned = score * 10  # 10 points per correct answer
    
    # Update progress (keep highest score)
    cursor.execute("""
        UPDATE progress 
        SET quiz_score = MAX(quiz_score, ?),
            quiz_completed = 1,
            completion_percentage = MAX(completion_percentage, ?),
            last_updated = CURRENT_TIMESTAMP
        WHERE user_id = ? AND chapter_id = ?
    """, (percentage, percentage, user_id, chapter_id))
    
    # Update user total points
    cursor.execute("""
        UPDATE users 
        SET total_points = total_points + ?,
            level = (total_points + ?) / 500 + 1
        WHERE id = ?
    """, (points_earned, points_earned, user_id))
    
    conn.commit()
    conn.close()
    
    return points_earned


def update_code_progress(user_id, challenge_id, chapter_id, code, passed):
    """Update code challenge progress"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Record submission
    cursor.execute("""
        INSERT INTO code_submissions (user_id, challenge_id, code, passed)
        VALUES (?, ?, ?, ?)
    """, (user_id, challenge_id, code, int(passed)))
    
    if passed:
        # Get current challenges completed
        cursor.execute("""
            SELECT challenges_completed FROM progress
            WHERE user_id = ? AND chapter_id = ?
        """, (user_id, chapter_id))
        
        result = cursor.fetchone()
        if result:
            completed = json.loads(result[0]) if result[0] else []
            if challenge_id not in completed:
                completed.append(challenge_id)
                
                # Award points
                points = 20  # 20 points per challenge
                cursor.execute("""
                    UPDATE progress 
                    SET challenges_completed = ?,
                        last_updated = CURRENT_TIMESTAMP
                    WHERE user_id = ? AND chapter_id = ?
                """, (json.dumps(completed), user_id, chapter_id))
                
                cursor.execute("""
                    UPDATE users 
                    SET total_points = total_points + ?
                    WHERE id = ?
                """, (points, user_id))
                
                conn.commit()
                conn.close()
                return True, points
    
    conn.commit()
    conn.close()
    return False, 0


def get_leaderboard(limit=10):
    """Get top users by points"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT username, full_name, avatar, total_points, level, streak_days
        FROM users
        ORDER BY total_points DESC
        LIMIT ?
    """, (limit,))
    
    leaderboard = []
    for i, row in enumerate(cursor.fetchall(), 1):
        leaderboard.append({
            'rank': i,
            'username': row[0],
            'full_name': row[1],
            'avatar': row[2],
            'total_points': row[3],
            'level': row[4],
            'streak_days': row[5]
        })
    
    conn.close()
    return leaderboard


def get_user_achievements(user_id):
    """Get user's achievements"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT badge_name, badge_icon, unlocked_at
        FROM achievements
        WHERE user_id = ?
        ORDER BY unlocked_at DESC
    """, (user_id,))
    
    achievements = []
    for row in cursor.fetchall():
        achievements.append({
            'name': row[0],
            'icon': row[1],
            'unlocked_at': row[2]
        })
    
    conn.close()
    return achievements


def check_and_award_achievements(user_id):
    """Check and award new achievements"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    new_achievements = []
    
    # Get user stats
    cursor.execute("""
        SELECT total_points, streak_days FROM users WHERE id = ?
    """, (user_id,))
    user_stats = cursor.fetchone()
    
    if not user_stats:
        conn.close()
        return []
    
    total_points, streak = user_stats
    
    # Get progress stats
    cursor.execute("""
        SELECT COUNT(*) FROM progress 
        WHERE user_id = ? AND quiz_completed = 1
    """, (user_id,))
    quizzes_completed = cursor.fetchone()[0]
    
    cursor.execute("""
        SELECT challenges_completed FROM progress WHERE user_id = ?
    """, (user_id,))
    total_challenges = 0
    for row in cursor.fetchall():
        if row[0]:
            total_challenges += len(json.loads(row[0]))
    
    # Define achievements
    achievements_to_check = [
        ('First Quiz', '🥇', quizzes_completed >= 1),
        ('Quiz Master', '🏆', quizzes_completed >= 5),
        ('Python Scholar', '🎓', quizzes_completed >= 10),
        ('Code Warrior', '⚔️', total_challenges >= 5),
        ('Code Master', '👑', total_challenges >= 20),
        ('100 Points', '💯', total_points >= 100),
        ('500 Points', '💎', total_points >= 500),
        ('1000 Points', '🌟', total_points >= 1000),
        ('Week Streak', '🔥', streak >= 7),
    ]
    
    for badge_name, badge_icon, condition in achievements_to_check:
        if condition:
            try:
                cursor.execute("""
                    INSERT INTO achievements (user_id, badge_name, badge_icon)
                    VALUES (?, ?, ?)
                """, (user_id, badge_name, badge_icon))
                new_achievements.append({'name': badge_name, 'icon': badge_icon})
            except sqlite3.IntegrityError:
                pass  # Already has this achievement
    
    conn.commit()
    conn.close()
    return new_achievements


def get_user_stats(user_id):
    """Get comprehensive user statistics"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get user info
    cursor.execute("""
        SELECT username, full_name, avatar, level, total_points, streak_days, created_at
        FROM users WHERE id = ?
    """, (user_id,))
    user = cursor.fetchone()
    
    # Count completed quizzes
    cursor.execute("""
        SELECT COUNT(*) FROM progress 
        WHERE user_id = ? AND quiz_completed = 1
    """, (user_id,))
    quizzes_completed = cursor.fetchone()[0]
    
    # Count total challenges
    cursor.execute("""
        SELECT challenges_completed FROM progress WHERE user_id = ?
    """, (user_id,))
    total_challenges = 0
    for row in cursor.fetchall():
        if row[0]:
            total_challenges += len(json.loads(row[0]))
    
    # Average quiz score
    cursor.execute("""
        SELECT AVG(quiz_score) FROM progress 
        WHERE user_id = ? AND quiz_completed = 1
    """, (user_id,))
    avg_score = cursor.fetchone()[0] or 0
    
    conn.close()
    
    return {
        'username': user[0] if user else '',
        'full_name': user[1] if user else '',
        'avatar': user[2] if user else '👤',
        'level': user[3] if user else 1,
        'total_points': user[4] if user else 0,
        'streak_days': user[5] if user else 0,
        'created_at': user[6] if user else '',
        'quizzes_completed': quizzes_completed,
        'challenges_completed': total_challenges,
        'avg_score': round(avg_score, 1)
    }
