"""
Database module - Uses Supabase (PostgreSQL) instead of SQLite
Data persists permanently, not reset when Streamlit restarts
"""
import hashlib
import json
import streamlit as st
from supabase import create_client, Client


# =============================================================================
# SUPABASE CLIENT
# =============================================================================

@st.cache_resource
def get_supabase() -> Client:
    """Get Supabase client (cached)"""
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)


def init_database():
    """No-op for Supabase - tables already created via SQL Editor"""
    pass


# =============================================================================
# AUTH
# =============================================================================

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()


def register_user(username, email, password, full_name=""):
    """Register a new user"""
    supabase = get_supabase()
    
    try:
        # Check username exists
        existing = supabase.table("users").select("id").eq("username", username).execute()
        if existing.data:
            return False, "Username đã tồn tại!"
        
        # Check email exists
        existing_email = supabase.table("users").select("id").eq("email", email).execute()
        if existing_email.data:
            return False, "Email đã được sử dụng!"
        
        # Insert new user
        result = supabase.table("users").insert({
            "username": username,
            "email": email,
            "password_hash": hash_password(password),
            "full_name": full_name or username,
        }).execute()
        
        user_id = result.data[0]['id']
        
        # Initialize progress for all 10 chapters
        progress_rows = [{"user_id": user_id, "chapter_id": i} for i in range(1, 11)]
        supabase.table("progress").insert(progress_rows).execute()
        
        return True, "Đăng ký thành công!"
    
    except Exception as e:
        return False, f"Lỗi: {str(e)}"


def login_user(username, password):
    """Login user"""
    supabase = get_supabase()
    
    try:
        result = supabase.table("users").select(
            "id, username, email, full_name, avatar, level, total_points, streak_days"
        ).or_(f"username.eq.{username},email.eq.{username}").eq(
            "password_hash", hash_password(password)
        ).execute()
        
        if result.data:
            user = result.data[0]
            # Update last_active
            supabase.table("users").update(
                {"last_active": "now()"}
            ).eq("id", user['id']).execute()
            
            return True, user
        
        return False, "Sai username hoặc password!"
    
    except Exception as e:
        return False, f"Lỗi: {str(e)}"


# =============================================================================
# PROGRESS
# =============================================================================

def get_user_progress(user_id):
    """Get user's progress across all chapters"""
    supabase = get_supabase()
    
    try:
        result = supabase.table("progress").select(
            "chapter_id, quiz_score, quiz_completed, challenges_completed, completion_percentage"
        ).eq("user_id", user_id).order("chapter_id").execute()
        
        progress = []
        for row in result.data:
            progress.append({
                'chapter_id': row['chapter_id'],
                'quiz_score': row['quiz_score'] or 0,
                'quiz_completed': bool(row['quiz_completed']),
                'challenges_completed': json.loads(row['challenges_completed']) if row['challenges_completed'] else [],
                'completion_percentage': row['completion_percentage'] or 0
            })
        
        return progress
    
    except Exception as e:
        return []


def update_quiz_progress(user_id, chapter_id, score, total_questions, time_taken):
    """Update quiz progress"""
    supabase = get_supabase()
    
    try:
        percentage = int((score / total_questions) * 100) if total_questions > 0 else 0
        points_earned = score * 10
        
        # Record attempt
        supabase.table("quiz_attempts").insert({
            "user_id": user_id,
            "chapter_id": chapter_id,
            "score": score,
            "total_questions": total_questions,
            "time_taken": time_taken,
        }).execute()
        
        # Get current progress to compare
        current = supabase.table("progress").select(
            "quiz_score, completion_percentage"
        ).eq("user_id", user_id).eq("chapter_id", chapter_id).execute()
        
        if current.data:
            old_score = current.data[0]['quiz_score'] or 0
            old_pct = current.data[0]['completion_percentage'] or 0
            
            supabase.table("progress").update({
                "quiz_score": max(old_score, percentage),
                "quiz_completed": 1,
                "completion_percentage": max(old_pct, percentage),
                "last_updated": "now()",
            }).eq("user_id", user_id).eq("chapter_id", chapter_id).execute()
        
        # Update total points
        user = supabase.table("users").select("total_points").eq("id", user_id).execute()
        if user.data:
            new_points = (user.data[0]['total_points'] or 0) + points_earned
            supabase.table("users").update({
                "total_points": new_points,
                "level": new_points // 500 + 1,
            }).eq("id", user_id).execute()
        
        return points_earned
    
    except Exception as e:
        return 0


def update_code_progress(user_id, challenge_id, chapter_id, code, passed):
    """Update code challenge progress"""
    supabase = get_supabase()
    
    try:
        # Record submission
        supabase.table("code_submissions").insert({
            "user_id": user_id,
            "challenge_id": challenge_id,
            "code": code,
            "passed": int(passed),
        }).execute()
        
        if passed:
            # Get current challenges
            current = supabase.table("progress").select(
                "challenges_completed"
            ).eq("user_id", user_id).eq("chapter_id", chapter_id).execute()
            
            if current.data:
                completed = json.loads(current.data[0]['challenges_completed'] or '[]')
                
                if challenge_id not in completed:
                    completed.append(challenge_id)
                    points = 20
                    
                    supabase.table("progress").update({
                        "challenges_completed": json.dumps(completed),
                        "last_updated": "now()",
                    }).eq("user_id", user_id).eq("chapter_id", chapter_id).execute()
                    
                    # Update points
                    user = supabase.table("users").select("total_points").eq("id", user_id).execute()
                    if user.data:
                        new_points = (user.data[0]['total_points'] or 0) + points
                        supabase.table("users").update({
                            "total_points": new_points,
                            "level": new_points // 500 + 1,
                        }).eq("id", user_id).execute()
                    
                    return True, points
        
        return False, 0
    
    except Exception as e:
        return False, 0


# =============================================================================
# LEADERBOARD
# =============================================================================

def get_leaderboard(limit=10):
    """Get top users by points"""
    supabase = get_supabase()
    
    try:
        result = supabase.table("users").select(
            "username, full_name, avatar, total_points, level, streak_days"
        ).order("total_points", desc=True).limit(limit).execute()
        
        leaderboard = []
        for i, row in enumerate(result.data, 1):
            leaderboard.append({
                'rank': i,
                'username': row['username'],
                'full_name': row['full_name'],
                'avatar': row['avatar'],
                'total_points': row['total_points'] or 0,
                'level': row['level'] or 1,
                'streak_days': row['streak_days'] or 0,
            })
        
        return leaderboard
    
    except Exception as e:
        return []


# =============================================================================
# ACHIEVEMENTS
# =============================================================================

def get_user_achievements(user_id):
    """Get user's achievements"""
    supabase = get_supabase()
    
    try:
        result = supabase.table("achievements").select(
            "badge_name, badge_icon, unlocked_at"
        ).eq("user_id", user_id).order("unlocked_at", desc=True).execute()
        
        return [{'name': r['badge_name'], 'icon': r['badge_icon'], 
                 'unlocked_at': r['unlocked_at']} for r in result.data]
    
    except Exception as e:
        return []


def check_and_award_achievements(user_id):
    """Check and award new achievements"""
    supabase = get_supabase()
    new_achievements = []
    
    try:
        # Get user stats
        user = supabase.table("users").select(
            "total_points, streak_days"
        ).eq("id", user_id).execute()
        
        if not user.data:
            return []
        
        total_points = user.data[0]['total_points'] or 0
        streak = user.data[0]['streak_days'] or 0
        
        # Count quizzes completed
        quizzes = supabase.table("progress").select(
            "quiz_completed"
        ).eq("user_id", user_id).eq("quiz_completed", 1).execute()
        quizzes_completed = len(quizzes.data)
        
        # Count challenges
        progress = supabase.table("progress").select(
            "challenges_completed"
        ).eq("user_id", user_id).execute()
        
        total_challenges = 0
        for row in progress.data:
            if row['challenges_completed']:
                total_challenges += len(json.loads(row['challenges_completed']))
        
        # Get existing achievements
        existing = supabase.table("achievements").select(
            "badge_name"
        ).eq("user_id", user_id).execute()
        existing_names = {r['badge_name'] for r in existing.data}
        
        # Check conditions
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
            if condition and badge_name not in existing_names:
                try:
                    supabase.table("achievements").insert({
                        "user_id": user_id,
                        "badge_name": badge_name,
                        "badge_icon": badge_icon,
                    }).execute()
                    new_achievements.append({'name': badge_name, 'icon': badge_icon})
                except:
                    pass
        
        return new_achievements
    
    except Exception as e:
        return []


# =============================================================================
# USER STATS
# =============================================================================

def get_user_stats(user_id):
    """Get comprehensive user statistics"""
    supabase = get_supabase()
    
    try:
        # User info
        user = supabase.table("users").select(
            "username, full_name, avatar, level, total_points, streak_days, created_at"
        ).eq("id", user_id).execute()
        
        if not user.data:
            return {}
        
        u = user.data[0]
        
        # Quizzes completed
        quizzes = supabase.table("progress").select(
            "quiz_completed"
        ).eq("user_id", user_id).eq("quiz_completed", 1).execute()
        quizzes_completed = len(quizzes.data)
        
        # Challenges completed
        progress = supabase.table("progress").select(
            "challenges_completed"
        ).eq("user_id", user_id).execute()
        
        total_challenges = 0
        for row in progress.data:
            if row['challenges_completed']:
                total_challenges += len(json.loads(row['challenges_completed']))
        
        # Average quiz score
        scores = supabase.table("progress").select(
            "quiz_score"
        ).eq("user_id", user_id).eq("quiz_completed", 1).execute()
        
        avg_score = 0
        if scores.data:
            avg_score = sum(r['quiz_score'] or 0 for r in scores.data) / len(scores.data)
        
        return {
            'username': u['username'],
            'full_name': u['full_name'],
            'avatar': u['avatar'] or '👤',
            'level': u['level'] or 1,
            'total_points': u['total_points'] or 0,
            'streak_days': u['streak_days'] or 0,
            'created_at': u['created_at'] or '',
            'quizzes_completed': quizzes_completed,
            'challenges_completed': total_challenges,
            'avg_score': round(avg_score, 1),
        }
    
    except Exception as e:
        return {
            'username': '', 'full_name': '', 'avatar': '👤',
            'level': 1, 'total_points': 0, 'streak_days': 0,
            'created_at': '', 'quizzes_completed': 0,
            'challenges_completed': 0, 'avg_score': 0
        }
