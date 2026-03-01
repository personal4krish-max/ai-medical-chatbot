import streamlit as st
from groq import Groq
import time
import datetime

# ── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MediAI Pro — AI Medical Assistant",
    page_icon="⚕️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Premium CSS Design ─────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Global Reset ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, .stApp {
    background: #060d1a !important;
    font-family: 'DM Sans', sans-serif;
    color: #e8edf5;
}

/* ── Hide Streamlit Junk ── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

/* ── Animated Background Grid ── */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
        linear-gradient(rgba(0, 212, 170, 0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0, 212, 170, 0.03) 1px, transparent 1px);
    background-size: 60px 60px;
    pointer-events: none;
    z-index: 0;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #08111f !important;
    border-right: 1px solid rgba(0, 212, 170, 0.12) !important;
    width: 300px !important;
}
section[data-testid="stSidebar"] > div {
    padding: 0 !important;
}

/* ── Sidebar Logo Area ── */
.sidebar-logo {
    padding: 28px 24px 20px;
    border-bottom: 1px solid rgba(0,212,170,0.1);
    margin-bottom: 8px;
}
.sidebar-logo .logo-icon {
    font-size: 36px;
    display: block;
    margin-bottom: 8px;
}
.sidebar-logo h2 {
    font-family: 'Syne', sans-serif;
    font-size: 22px;
    font-weight: 800;
    background: linear-gradient(135deg, #00d4aa, #4facfe);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.2;
}
.sidebar-logo p {
    color: #4a6080;
    font-size: 12px;
    margin-top: 4px;
    font-weight: 400;
}

/* ── Sidebar Section Headers ── */
.sidebar-section {
    padding: 16px 24px 8px;
    font-family: 'Syne', sans-serif;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #2a4060;
}

/* ── API Key Input ── */
.stTextInput input {
    background: #0d1e35 !important;
    border: 1px solid rgba(0,212,170,0.2) !important;
    border-radius: 10px !important;
    color: #e8edf5 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
    padding: 10px 14px !important;
    transition: all 0.2s ease !important;
}
.stTextInput input:focus {
    border-color: rgba(0,212,170,0.6) !important;
    box-shadow: 0 0 0 3px rgba(0,212,170,0.08) !important;
}
.stTextInput label {
    color: #4a6080 !important;
    font-size: 12px !important;
    font-weight: 500 !important;
}

/* ── Selectbox ── */
.stSelectbox > div > div {
    background: #0d1e35 !important;
    border: 1px solid rgba(0,212,170,0.2) !important;
    border-radius: 10px !important;
    color: #e8edf5 !important;
}
.stSelectbox label {
    color: #4a6080 !important;
    font-size: 12px !important;
    font-weight: 500 !important;
}

/* ── Quick Buttons ── */
.stButton > button {
    background: rgba(0,212,170,0.06) !important;
    border: 1px solid rgba(0,212,170,0.15) !important;
    border-radius: 10px !important;
    color: #7ab8cc !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 12px !important;
    font-weight: 400 !important;
    padding: 8px 12px !important;
    text-align: left !important;
    transition: all 0.2s ease !important;
    width: 100% !important;
}
.stButton > button:hover {
    background: rgba(0,212,170,0.12) !important;
    border-color: rgba(0,212,170,0.35) !important;
    color: #00d4aa !important;
    transform: translateX(3px) !important;
}

/* ── Primary Send Button ── */
.send-btn > button {
    background: linear-gradient(135deg, #00d4aa, #4facfe) !important;
    border: none !important;
    border-radius: 12px !important;
    color: #060d1a !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 13px !important;
    font-weight: 700 !important;
    padding: 12px !important;
    height: 48px !important;
    letter-spacing: 0.5px !important;
    transition: all 0.2s ease !important;
}
.send-btn > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 24px rgba(0,212,170,0.35) !important;
}

/* ── Clear Button ── */
.clear-btn > button {
    background: rgba(255,75,75,0.07) !important;
    border: 1px solid rgba(255,75,75,0.2) !important;
    color: #ff6b6b !important;
    font-size: 12px !important;
}
.clear-btn > button:hover {
    background: rgba(255,75,75,0.14) !important;
    border-color: rgba(255,75,75,0.4) !important;
    transform: none !important;
}

/* ── Main Content Area ── */
.main-wrapper {
    display: flex;
    flex-direction: column;
    height: 100vh;
    padding: 0;
}

/* ── Top Header Bar ── */
.top-bar {
    background: rgba(8, 17, 31, 0.95);
    backdrop-filter: blur(20px);
    border-bottom: 1px solid rgba(0,212,170,0.1);
    padding: 16px 40px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: sticky;
    top: 0;
    z-index: 100;
}
.top-bar-title {
    font-family: 'Syne', sans-serif;
    font-size: 18px;
    font-weight: 700;
    color: #e8edf5;
}
.top-bar-title span {
    background: linear-gradient(135deg, #00d4aa, #4facfe);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.status-pill {
    background: rgba(0,212,170,0.1);
    border: 1px solid rgba(0,212,170,0.25);
    border-radius: 20px;
    padding: 5px 14px;
    font-size: 12px;
    color: #00d4aa;
    font-weight: 500;
    display: flex;
    align-items: center;
    gap: 6px;
}
.status-dot {
    width: 7px;
    height: 7px;
    background: #00d4aa;
    border-radius: 50%;
    animation: pulse-dot 2s infinite;
}
@keyframes pulse-dot {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.5; transform: scale(0.8); }
}

/* ── Disclaimer Banner ── */
.disclaimer-bar {
    background: rgba(255, 167, 38, 0.06);
    border-bottom: 1px solid rgba(255,167,38,0.12);
    padding: 10px 40px;
    font-size: 12px;
    color: #7a6a40;
    text-align: center;
    font-weight: 400;
}
.disclaimer-bar b { color: #ffa726; }

/* ── Chat Area ── */
.chat-area {
    flex: 1;
    overflow-y: auto;
    padding: 32px 40px;
    display: flex;
    flex-direction: column;
    gap: 20px;
}

/* ── Welcome Card ── */
.welcome-card {
    background: linear-gradient(135deg, rgba(0,212,170,0.06), rgba(79,172,254,0.04));
    border: 1px solid rgba(0,212,170,0.12);
    border-radius: 20px;
    padding: 40px;
    text-align: center;
    margin: 20px auto;
    max-width: 600px;
}
.welcome-card .pulse-icon {
    font-size: 56px;
    margin-bottom: 16px;
    display: block;
    animation: float 3s ease-in-out infinite;
}
@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-8px); }
}
.welcome-card h2 {
    font-family: 'Syne', sans-serif;
    font-size: 26px;
    font-weight: 800;
    color: #e8edf5;
    margin-bottom: 12px;
}
.welcome-card p {
    color: #4a6080;
    font-size: 14px;
    line-height: 1.7;
    max-width: 420px;
    margin: 0 auto 24px;
}
.capability-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    margin-top: 20px;
    text-align: left;
}
.capability-item {
    background: rgba(0,212,170,0.05);
    border: 1px solid rgba(0,212,170,0.1);
    border-radius: 12px;
    padding: 12px 14px;
    font-size: 12px;
    color: #7ab8cc;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* ── Message Bubbles ── */
.msg-row {
    display: flex;
    gap: 12px;
    animation: msg-in 0.3s ease-out;
}
@keyframes msg-in {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}
.msg-row.user { flex-direction: row-reverse; }

.avatar {
    width: 36px;
    height: 36px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    flex-shrink: 0;
    margin-top: 2px;
}
.avatar.bot { background: linear-gradient(135deg, #00d4aa22, #4facfe22); border: 1px solid rgba(0,212,170,0.25); }
.avatar.user-av { background: linear-gradient(135deg, #4facfe22, #a855f722); border: 1px solid rgba(79,172,254,0.25); }

.bubble {
    max-width: 70%;
    padding: 14px 18px;
    border-radius: 16px;
    font-size: 14px;
    line-height: 1.7;
    position: relative;
}
.bubble.bot {
    background: #0d1e35;
    border: 1px solid rgba(0,212,170,0.12);
    color: #c8d8e8;
    border-top-left-radius: 4px;
}
.bubble.user {
    background: linear-gradient(135deg, rgba(79,172,254,0.15), rgba(0,212,170,0.1));
    border: 1px solid rgba(79,172,254,0.2);
    color: #e8edf5;
    border-top-right-radius: 4px;
}
.bubble .msg-meta {
    font-size: 10px;
    color: #2a4060;
    margin-top: 8px;
    font-weight: 500;
}

/* ── Typing Indicator ── */
.typing-indicator {
    display: flex;
    gap: 4px;
    align-items: center;
    padding: 16px 18px;
    background: #0d1e35;
    border: 1px solid rgba(0,212,170,0.12);
    border-radius: 16px;
    border-top-left-radius: 4px;
    width: fit-content;
}
.typing-dot {
    width: 8px;
    height: 8px;
    background: #00d4aa;
    border-radius: 50%;
    animation: typing 1.4s infinite;
}
.typing-dot:nth-child(2) { animation-delay: 0.2s; }
.typing-dot:nth-child(3) { animation-delay: 0.4s; }
@keyframes typing {
    0%, 100% { transform: translateY(0); opacity: 0.4; }
    50% { transform: translateY(-6px); opacity: 1; }
}

/* ── Input Area ── */
.input-area {
    background: rgba(8, 17, 31, 0.98);
    border-top: 1px solid rgba(0,212,170,0.1);
    padding: 20px 40px;
    backdrop-filter: blur(20px);
}
.input-bar {
    background: #0d1e35;
    border: 1px solid rgba(0,212,170,0.2);
    border-radius: 16px;
    padding: 4px 4px 4px 16px;
    display: flex;
    align-items: center;
    gap: 10px;
    transition: border-color 0.2s ease;
}
.input-bar:focus-within {
    border-color: rgba(0,212,170,0.5);
    box-shadow: 0 0 0 3px rgba(0,212,170,0.06);
}

/* ── Text Input Override ── */
.stTextInput {
    flex: 1 !important;
}
.input-box input {
    background: transparent !important;
    border: none !important;
    border-radius: 0 !important;
    color: #e8edf5 !important;
    font-size: 14px !important;
    padding: 8px 4px !important;
    box-shadow: none !important;
}
.input-box input::placeholder { color: #2a4060 !important; }
.input-box input:focus { box-shadow: none !important; border: none !important; }
.input-box label { display: none !important; }

/* ── Specialty Cards ── */
.spec-badge {
    background: rgba(0,212,170,0.08);
    border: 1px solid rgba(0,212,170,0.18);
    border-radius: 8px;
    padding: 4px 10px;
    font-size: 11px;
    color: #00d4aa;
    font-weight: 600;
    display: inline-flex;
    align-items: center;
    gap: 4px;
}

/* ── Stats Strip ── */
.stats-strip {
    display: flex;
    gap: 24px;
    padding: 12px 24px;
    border-top: 1px solid rgba(0,212,170,0.06);
    margin-top: 4px;
}
.stat-item { text-align: center; }
.stat-value {
    font-family: 'Syne', sans-serif;
    font-size: 16px;
    font-weight: 700;
    color: #00d4aa;
}
.stat-label {
    font-size: 10px;
    color: #2a4060;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(0,212,170,0.2); border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: rgba(0,212,170,0.4); }

/* ── Specialty Dropdown colors ── */
.stSelectbox svg { color: #00d4aa !important; }
[data-baseweb="select"] {
    background: #0d1e35 !important;
}

/* ── Divider ── */
hr { border-color: rgba(0,212,170,0.08) !important; }

/* ── Spinner Override ── */
.stSpinner > div {
    border-top-color: #00d4aa !important;
}
</style>
""", unsafe_allow_html=True)

# ── Specialty Definitions ──────────────────────────────────────────────────────
SPECIALTIES = {
    "⚕️ General Medicine": {
        "icon": "⚕️",
        "color": "#00d4aa",
        "prompt": """You are MediAI Pro — an elite AI medical assistant with comprehensive knowledge equivalent to a board-certified general physician with 20 years of experience.

Your role:
- Provide accurate, evidence-based medical information in clear, empathetic language
- Explain symptoms, conditions, diagnoses, treatments, medications, and preventive care
- Use structured formatting: bold key terms, bullet points for lists, numbered steps for procedures
- Always flag RED FLAG symptoms that require immediate emergency care (call 911/ER)
- End every response with a brief reminder to consult a licensed healthcare provider

NEVER: provide definitive diagnoses, replace professional medical care, or downplay serious symptoms.
ALWAYS: Be compassionate, thorough, and clear.""",
    },
    "👶 Pediatrics": {
        "icon": "👶",
        "color": "#4facfe",
        "prompt": """You are MediAI Pro — a pediatric specialist AI assistant with deep expertise in child and adolescent health from newborns to 18 years.

Cover: developmental milestones, childhood illnesses, vaccinations, pediatric nutrition, growth concerns, and child behavioral health. Always tailor advice to the child's age group. Remind parents to consult their pediatrician or call emergency services for serious concerns.""",
    },
    "❤️ Cardiology": {
        "icon": "❤️",
        "color": "#ff6b6b",
        "prompt": """You are MediAI Pro — a cardiology AI specialist with expertise in heart and vascular health.

Cover: heart conditions, symptoms (chest pain, palpitations, shortness of breath), blood pressure management, cholesterol, ECG basics, medications (beta-blockers, statins, etc.), cardiac procedures, and lifestyle modifications.

CRITICAL: Immediately and prominently flag any symptoms that could indicate a heart attack or stroke and instruct the user to call 911. Always recommend cardiologist consultation.""",
    },
    "🧠 Neurology": {
        "icon": "🧠",
        "color": "#a855f7",
        "prompt": """You are MediAI Pro — a neurology AI specialist with expertise in brain and nervous system health.

Cover: headaches, migraines, seizures, stroke symptoms (FAST), Parkinson's, multiple sclerosis, neuropathy, memory disorders, sleep disorders, and neurological medications. Flag any signs of stroke or severe neurological emergency immediately and instruct calling 911.""",
    },
    "🌿 Mental Health": {
        "icon": "🌿",
        "color": "#34d399",
        "prompt": """You are MediAI Pro — a compassionate mental health AI assistant with expertise in psychology and psychiatry.

Cover: anxiety, depression, PTSD, bipolar disorder, OCD, stress management, sleep hygiene, mindfulness techniques, and psychiatric medications. Use empathetic, non-judgmental language.

CRITICAL SAFETY: If there is ANY mention of suicidal ideation, self-harm, or crisis — immediately provide the 988 Suicide & Crisis Lifeline and encourage calling 911 if in immediate danger. Never replace a licensed therapist or psychiatrist.""",
    },
    "🦷 Dental Health": {
        "icon": "🦷",
        "color": "#fbbf24",
        "prompt": """You are MediAI Pro — a dental health AI specialist with comprehensive knowledge of oral health.

Cover: toothache, gum disease, cavities, oral infections, dental procedures (root canal, extractions, implants), orthodontics, oral hygiene practices, and medications used in dentistry. Flag severe dental infections or abscesses as requiring urgent dental care.""",
    },
    "🥗 Nutrition & Diet": {
        "icon": "🥗",
        "color": "#10b981",
        "prompt": """You are MediAI Pro — an AI nutritionist and dietitian with clinical expertise in therapeutic nutrition.

Cover: balanced diets, macronutrients, micronutrients, dietary management of conditions (diabetes, hypertension, high cholesterol, obesity), food allergies, supplements, weight management, and eating disorders. Always recommend consultation with a Registered Dietitian for personalized meal plans.""",
    },
    "🚨 Emergency First Aid": {
        "icon": "🚨",
        "color": "#ef4444",
        "prompt": """You are MediAI Pro — an emergency first aid AI assistant trained in advanced life support protocols.

CRITICAL RULE: Always begin with "📞 CALL 911 IMMEDIATELY for life-threatening emergencies."

Provide clear, numbered, step-by-step first aid instructions for: CPR, choking (Heimlich maneuver), severe bleeding, burns, fractures, anaphylaxis (epinephrine auto-injector use), poisoning, drowning, and other emergencies. Keep instructions simple and actionable. Time is critical — be concise and clear.""",
    },
}

QUICK_PROMPTS = {
    "⚕️ General Medicine": [
        "Symptoms of diabetes?",
        "How to treat a fever?",
        "What causes fatigue?",
        "Signs of vitamin deficiency?",
        "When to see a doctor?",
    ],
    "👶 Pediatrics": [
        "Baby fever — when is it serious?",
        "Vaccine schedule for infants?",
        "Toddler not talking at 2?",
        "Child won't eat — is it normal?",
        "Signs of ear infection in kids?",
    ],
    "❤️ Cardiology": [
        "Signs of a heart attack?",
        "What is a normal heart rate?",
        "High blood pressure symptoms?",
        "Difference: angina vs heart attack?",
        "How to lower cholesterol naturally?",
    ],
    "🧠 Neurology": [
        "Migraine vs tension headache?",
        "FAST signs of a stroke?",
        "What causes brain fog?",
        "Epilepsy first aid steps?",
        "Signs of early Parkinson's?",
    ],
    "🌿 Mental Health": [
        "Anxiety vs panic attack?",
        "Natural ways to manage depression?",
        "Signs of PTSD?",
        "How to improve sleep hygiene?",
        "What is CBT therapy?",
    ],
    "🦷 Dental Health": [
        "Home remedies for toothache?",
        "Signs of gum disease?",
        "Wisdom tooth pain relief?",
        "What is a root canal?",
        "How often to floss?",
    ],
    "🥗 Nutrition & Diet": [
        "Best foods for diabetics?",
        "Foods to lower blood pressure?",
        "How much protein daily?",
        "Signs of iron deficiency?",
        "Anti-inflammatory foods?",
    ],
    "🚨 Emergency First Aid": [
        "Steps for CPR?",
        "How to do Heimlich maneuver?",
        "Severe burn first aid?",
        "Signs of anaphylaxis?",
        "How to stop severe bleeding?",
    ],
}

# ── Session State ──────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "quick_input" not in st.session_state:
    st.session_state.quick_input = None
if "msg_count" not in st.session_state:
    st.session_state.msg_count = 0
if "selected_specialty" not in st.session_state:
    st.session_state.selected_specialty = "⚕️ General Medicine"

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    # Logo
    st.markdown("""
    <div class='sidebar-logo'>
        <span class='logo-icon'>⚕️</span>
        <h2>MediAI Pro</h2>
        <p>Intelligent Medical Assistant · v2.0</p>
    </div>
    """, unsafe_allow_html=True)

    # API Key
    st.markdown("<div class='sidebar-section'>🔑 API Configuration</div>", unsafe_allow_html=True)
    api_key = st.text_input(
        "Groq API Key",
        type="password",
        placeholder="gsk_...",
        help="Free at console.groq.com — No credit card needed!"
    )
    st.markdown("""
    <div style='padding:0 0 8px 0;'>
        <a href='https://console.groq.com' target='_blank'
           style='color:#00d4aa; font-size:11px; text-decoration:none; font-weight:500;'>
            🔗 Get free API key at console.groq.com →
        </a>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Specialty
    st.markdown("<div class='sidebar-section'>🩺 Medical Specialty</div>", unsafe_allow_html=True)
    specialty = st.selectbox(
        "Choose specialty",
        list(SPECIALTIES.keys()),
        label_visibility="collapsed"
    )
    st.session_state.selected_specialty = specialty

    st.markdown("---")

    # Quick Prompts
    st.markdown("<div class='sidebar-section'>⚡ Quick Questions</div>", unsafe_allow_html=True)
    for q in QUICK_PROMPTS.get(specialty, []):
        if st.button(q, key=f"qp_{q}", use_container_width=True):
            st.session_state.quick_input = q

    st.markdown("---")

    # Stats
    st.markdown(f"""
    <div class='stats-strip'>
        <div class='stat-item'>
            <div class='stat-value'>{st.session_state.msg_count}</div>
            <div class='stat-label'>Messages</div>
        </div>
        <div class='stat-item'>
            <div class='stat-value'>{len(SPECIALTIES)}</div>
            <div class='stat-label'>Specialties</div>
        </div>
        <div class='stat-item'>
            <div class='stat-value'>Free</div>
            <div class='stat-label'>API Cost</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Clear button
    col_clr = st.container()
    with col_clr:
        st.markdown('<div class="clear-btn">', unsafe_allow_html=True)
        if st.button("🗑️ Clear Conversation", use_container_width=True):
            st.session_state.messages = []
            st.session_state.msg_count = 0
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style='padding:16px 24px; color:#1a3050; font-size:11px; line-height:1.6;'>
        Powered by <b style='color:#00d4aa;'>Groq</b> · LLaMA 3.3 70B<br>
        Ultra-fast inference · 100% Free<br><br>
        ⚕️ MediAI Pro © 2025
    </div>
    """, unsafe_allow_html=True)

# ── Main Content ───────────────────────────────────────────────────────────────
spec_info = SPECIALTIES[specialty]

# Top Bar
st.markdown(f"""
<div class='top-bar'>
    <div style='display:flex; align-items:center; gap:14px;'>
        <div style='font-size:26px;'>{spec_info['icon']}</div>
        <div>
            <div class='top-bar-title'>Medi<span>AI Pro</span></div>
            <div style='font-size:11px; color:#2a4060; margin-top:1px;'>{specialty.split(' ',1)[1] if ' ' in specialty else specialty} Specialist</div>
        </div>
    </div>
    <div class='status-pill'>
        <div class='status-dot'></div>
        AI Online · Groq LLaMA 3.3
    </div>
</div>
""", unsafe_allow_html=True)

# Disclaimer
st.markdown("""
<div class='disclaimer-bar'>
    ⚠️ <b>Medical Disclaimer:</b> MediAI Pro provides general health information only — not a substitute for professional medical advice, diagnosis, or treatment. &nbsp;|&nbsp; Emergency? Call <b>911</b> &nbsp;|&nbsp; Mental Health Crisis? Call <b>988</b>
</div>
""", unsafe_allow_html=True)

# ── Chat Display ───────────────────────────────────────────────────────────────
chat_box = st.container()
with chat_box:

    # Welcome screen
    if not st.session_state.messages:
        st.markdown(f"""
        <div class='welcome-card'>
            <span class='pulse-icon'>{spec_info['icon']}</span>
            <h2>How can I help you today?</h2>
            <p>I'm your AI {specialty.split(' ',1)[1] if ' ' in specialty else specialty} specialist.
            Ask me anything about symptoms, conditions, medications, or general health guidance.</p>
            <div class='capability-grid'>
                <div class='capability-item'>🔬 Symptom Analysis</div>
                <div class='capability-item'>💊 Medication Info</div>
                <div class='capability-item'>📋 Condition Guides</div>
                <div class='capability-item'>🛡️ Preventive Care</div>
                <div class='capability-item'>📊 Lab Results Help</div>
                <div class='capability-item'>🏃 Lifestyle Advice</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Render messages
    now = datetime.datetime.now().strftime("%I:%M %p")
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"""
            <div class='msg-row user'>
                <div class='avatar user-av'>👤</div>
                <div class='bubble user'>
                    {msg['content']}
                    <div class='msg-meta'>{now}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class='msg-row'>
                <div class='avatar bot'>⚕️</div>
                <div class='bubble bot'>
                    {msg['content'].replace(chr(10), '<br>')}
                    <div class='msg-meta'>MediAI Pro · {specialty.split(' ',1)[1] if ' ' in specialty else specialty}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ── Input Area ─────────────────────────────────────────────────────────────────
st.markdown("---")

# Handle quick input
default_val = ""
if st.session_state.quick_input:
    default_val = st.session_state.quick_input
    st.session_state.quick_input = None

col_inp, col_btn = st.columns([6, 1])
with col_inp:
    st.markdown('<div class="input-box">', unsafe_allow_html=True)
    user_input = st.text_input(
        "Message",
        value=default_val,
        placeholder=f"Ask your {specialty.split(' ',1)[1] if ' ' in specialty else specialty} question here...",
        label_visibility="collapsed",
        key="chat_input"
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col_btn:
    st.markdown('<div class="send-btn">', unsafe_allow_html=True)
    send = st.button("Send ➤", use_container_width=True, type="primary")
    st.markdown('</div>', unsafe_allow_html=True)

# ── AI Response ────────────────────────────────────────────────────────────────
def stream_groq(messages, system_prompt, api_key):
    client = Groq(api_key=api_key)
    api_msgs = [{"role": m["role"], "content": m["content"]} for m in messages]

    stream = client.chat.completions.create(
        model="llama-3.3-70b-versatile",   # Best free model on Groq
        messages=[{"role": "system", "content": system_prompt}] + api_msgs,
        max_tokens=1024,
        temperature=0.4,
        stream=True,
    )
    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            yield delta


if (send or user_input) and user_input.strip():

    # Resolve API key
    resolved_key = api_key or st.secrets.get("GROQ_API_KEY", "")
    if not resolved_key:
        st.error("❌ Please enter your Groq API key in the sidebar. Get one free at console.groq.com")
        st.stop()

    user_msg = user_input.strip()
    st.session_state.messages.append({"role": "user", "content": user_msg})
    st.session_state.msg_count += 1

    # Show user bubble
    st.markdown(f"""
    <div class='msg-row user'>
        <div class='avatar user-av'>👤</div>
        <div class='bubble user'>{user_msg}<div class='msg-meta'>Just now</div></div>
    </div>
    """, unsafe_allow_html=True)

    # Typing indicator + stream
    typing_slot = st.empty()
    typing_slot.markdown("""
    <div class='msg-row'>
        <div class='avatar bot'>⚕️</div>
        <div class='typing-indicator'>
            <div class='typing-dot'></div>
            <div class='typing-dot'></div>
            <div class='typing-dot'></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    system_prompt = SPECIALTIES[specialty]["prompt"]
    full_response = ""
    response_slot = st.empty()

    try:
        for chunk in stream_groq(st.session_state.messages, system_prompt, resolved_key):
            full_response += chunk
            typing_slot.empty()
            response_slot.markdown(f"""
            <div class='msg-row'>
                <div class='avatar bot'>⚕️</div>
                <div class='bubble bot'>{full_response.replace(chr(10), '<br>')}▌<div class='msg-meta'>MediAI Pro · {specialty.split(' ',1)[1] if ' ' in specialty else specialty}</div></div>
            </div>
            """, unsafe_allow_html=True)

        # Final without cursor
        typing_slot.empty()
        response_slot.markdown(f"""
        <div class='msg-row'>
            <div class='avatar bot'>⚕️</div>
            <div class='bubble bot'>{full_response.replace(chr(10), '<br>')}
                <div class='msg-meta'>MediAI Pro · {specialty.split(' ',1)[1] if ' ' in specialty else specialty}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.session_state.messages.append({"role": "assistant", "content": full_response})
        st.session_state.msg_count += 1

    except Exception as e:
        typing_slot.empty()
        err = str(e)
        if "authentication" in err.lower() or "api_key" in err.lower() or "401" in err:
            st.error("❌ Invalid API key. Please check your Groq key at console.groq.com")
        elif "rate" in err.lower():
            st.error("⏳ Rate limit reached. Wait a moment and try again (free tier limit).")
        else:
            st.error(f"❌ Error: {err}")
