import streamlit as st
import random

# --- Page Configuration ---
st.set_page_config(
    page_title="Math Quest",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- Custom CSS for Professional Mobile Game Look ---
st.markdown("""
<style>
    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #6ee7b7 0%, #3b82f6 100%);
        font-family: 'Comic Neue', sans-serif;
    }

    /* Main Container */
    .main-container {
        background: white;
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
    }

    /* Title */
    .title {
        font-size: 2.5rem;
        font-weight: 900;
        text-align: center;
        color: #1e40af;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }

    /* Math Problem */
    .math-problem-hero {
        font-size: 4.5rem;
        font-weight: 900;
        text-align: center;
        color: #db2777;
        background: #f0f9ff;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        animation: pulse 2s infinite;
    }

    /* Animation for Math Problem */
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }

    /* Control Buttons */
    .control-buttons .stButton button {
        background: #f59e0b;
        color: white;
        font-weight: 600;
        font-size: 1rem;
        border-radius: 12px;
        padding: 0.7rem;
        transition: all 0.3s ease;
        width: 100%;
        margin-bottom: 0.5rem;
    }
    .control-buttons .stButton button:hover {
        background: #d97706;
        transform: translateY(-2px);
    }

    /* Answer Input */
    .stNumberInput input {
        font-size: 2.5rem;
        text-align: center;
        font-weight: 700;
        color: #1e40af;
        background: #f8fafc;
        border: 2px solid #3b82f6;
        border-radius: 12px;
        padding: 1rem !important;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }

    /* Submit Button */
    .stButton[aria-label*="Check Answer"] button, .stButton[aria-label*="Next Question"] button {
        background: #10b981;
        color: white;
        font-size: 1.2rem;
        font-weight: 600;
        border-radius: 12px;
        padding: 0.8rem;
        width: 100%;
        transition: all 0.3s ease;
    }
    .stButton[aria-label*="Next Question"] button {
        background: #8b5cf6;
    }
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }

    /* Feedback Boxes */
    .story-box, .joke-box {
        padding: 1rem;
        border-radius: 12px;
        margin: 1rem 0;
        font-size: 1.1rem;
        line-height: 1.5;
        border-left: 6px solid;
        animation: fadeIn 0.5s ease-in;
    }
    .story-box {
        background: #fef3c7;
        border-color: #facc15;
        color: #78350f;
    }
    .joke-box {
        background: #e0f2fe;
        border-color: #38bdf8;
        color: #1e3a8a;
        text-align: center;
    }

    /* Animation for Feedback */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Stats Section */
    .stats-container {
        display: flex;
        gap: 1rem;
        justify-content: space-between;
    }
    .stat-card {
        background: #f1f5f9;
        padding: 1rem;
        border-radius: 12px;
        text-align: center;
        flex: 1;
        border: 1px solid #e2e8f0;
    }
    .stat-card h3 {
        font-size: 0.8rem;
        color: #64748b;
        text-transform: uppercase;
        margin: 0 0 0.5rem 0;
    }
    .stat-card p {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1e40af;
        margin: 0;
    }

    /* Mobile Responsiveness */
    @media (max-width: 600px) {
        .title { font-size: 2rem; }
        .math-problem-hero { font-size: 3rem; padding: 1rem; }
        .stNumberInput input { font-size: 2rem; padding: 0.8rem !important; }
        .stats-container { flex-direction: column; }
        .control-buttons { grid-template-columns: 1fr; }
    }
</style>
""", unsafe_allow_html=True)

# --- Game State and Data ---
if 'score' not in st.session_state:
    st.session_state.score = 0
    st.session_state.problems_solved = 0
    st.session_state.streak = 0
    st.session_state.game_mode = 'story'
    st.session_state.operation_mode = 'addition'
    st.session_state.current_problem = ""
    st.session_state.correct_answer = 0
    st.session_state.feedback_text = ""
    st.session_state.feedback_type = None
    st.session_state.current_joke = ""
jokes = [
    "🐄 What do you call a sleeping bull? A bulldozer! 😴",
    "🍌 Why don't bananas ever feel lonely? Because they hang out in bunches!",
    "🐧 What do you call a penguin in the desert? Lost! 🏜️"
]
story_chapters = [
    "🏰 Princess Luna needs your help! Solve problems to collect crystal fragments!",
    "✨ Wonderful! You found a fragment in the Enchanted Forest!",
    "🌳 Amazing! The magical unicorn guides you toward the Crystal Lake.",
    "🦄 Fantastic! A friendly dragon tells you the final pieces are in the Cloud Castle!",
    "☁️ Incredible! You're so close to saving Princess Luna's kingdom!",
    "👑 AMAZING! You've collected all the fragments! The kingdom is saved!"
]

# --- Game Functions ---
def generate_problem():
    """Generates a new math problem."""
    op = st.session_state.operation_mode
    if op == 'mixed': op = random.choice(['addition', 'subtraction'])

    if op == 'addition':
        num1, num2 = random.randint(1, 10), random.randint(1, 10)
        st.session_state.correct_answer = num1 + num2
        st.session_state.current_problem = f"{num1} + {num2} = ?"
    else:  # Subtraction
        num1 = random.randint(5, 15)
        num2 = random.randint(1, num1)
        st.session_state.correct_answer = num1 - num2
        st.session_state.current_problem = f"{num1} − {num2} = ?"
    
    st.session_state.feedback_text = ""
    st.session_state.feedback_type = None
    st.session_state.current_joke = ""

def check_answer(user_answer):
    """Checks the answer and updates all game state features."""
    if user_answer is None:
        st.session_state.feedback_text = "Please enter an answer first!"
        st.session_state.feedback_type = "error"
        return

    st.session_state.problems_solved += 1
    if user_answer == st.session_state.correct_answer:
        st.session_state.score += 1
        st.session_state.streak += 1
        st.session_state.feedback_text = random.choice(["🎉 Excellent!", "⭐ Amazing!", "🎊 Fantastic!", "🏆 You got it!"])
        st.session_state.feedback_type = "success"
        if st.session_state.game_mode == 'joke' and st.session_state.streak > 0 and st.session_state.streak % 3 == 0:
            st.session_state.current_joke = random.choice(jokes)
    else:
        st.session_state.streak = 0
        st.session_state.feedback_text = f"Oops! The answer was {st.session_state.correct_answer}."
        st.session_state.feedback_type = "error"

# Initialize game on first run
if not st.session_state.current_problem:
    generate_problem()

# --- App Layout ---
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Title
st.markdown('<p class="title">🌟 Math Quest! 🌟</p>', unsafe_allow_html=True)

# Control Buttons
with st.container():
    st.markdown('<div class="control-buttons">', unsafe_allow_html=True)
    cols = st.columns(3)
    if cols[0].button("📖 Story", use_container_width=True): st.session_state.game_mode = 'story'
    if cols[1].button("😂 Jokes", use_container_width=True): st.session_state.game_mode = 'joke'
    if cols[2].button("⚡ Practice", use_container_width=True): st.session_state.game_mode = 'practice'
    cols = st.columns(3)
    if cols[0].button("➕ Add", use_container_width=True): 
        st.session_state.operation_mode = 'addition'; generate_problem(); st.rerun()
    if cols[1].button("➖ Subtract", use_container_width=True): 
        st.session_state.operation_mode = 'subtraction'; generate_problem(); st.rerun()
    if cols[2].button("🎲 Mixed", use_container_width=True): 
        st.session_state.operation_mode = 'mixed'; generate_problem(); st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# Math Problem and Answer Input
st.markdown(f'<p class="math-problem-hero">{st.session_state.current_problem}</p>', unsafe_allow_html=True)

with st.form(key="answer_form", clear_on_submit=True):
    user_answer = st.number_input(
        "Enter your answer",
        value=None,
        placeholder="",
        min_value=-100,
        max_value=200,
        step=1,
        label_visibility="collapsed"
    )
    submitted = st.form_submit_button("Check Answer! ✓", use_container_width=True)
    if submitted:
        check_answer(user_answer)
        st.rerun()

# Feedback
if st.session_state.feedback_text:
    if st.session_state.feedback_type == "success":
        st.success(st.session_state.feedback_text, icon="✅")
        if st.session_state.current_joke:
            st.markdown(f'<div class="joke-box"><b>Joke Unlocked!</b><br>{st.session_state.current_joke}</div>', unsafe_allow_html=True)
        st.balloons()
    else:
        st.error(st.session_state.feedback_text, icon="❌")

    if st.button("Next Question 🎲", use_container_width=True):
        generate_problem()
        st.rerun()

st.markdown("---")

# Story and Stats
if st.session_state.game_mode == 'story':
    chapter_index = min(st.session_state.score // 4, len(story_chapters) - 1)
    st.markdown(f'<div class="story-box"><b>Story:</b> {story_chapters[chapter_index]}</div>', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="stats-container">', unsafe_allow_html=True)
    cols = st.columns(2)
    with cols[0]:
        score_display = f"💎 {st.session_state.score}" if st.session_state.game_mode == 'story' else f"{st.session_state.score}/{st.session_state.problems_solved}"
        st.markdown(f'<div class="stat-card"><h3>🏆 Score</h3><p>{score_display}</p></div>', unsafe_allow_html=True)
    with cols[1]:
        streak_display = f"{st.session_state.streak} / 3" if st.session_state.game_mode == 'joke' and st.session_state.streak < 3 else str(st.session_state.streak)
        st.markdown(f'<div class="stat-card"><h3>🔥 Streak</h3><p>{streak_display}</p></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
