import streamlit as st
import anthropic
import time

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Medical Chatbot",
    page_icon="🏥",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #e8f5e9 0%, #e3f2fd 100%);
    }

    /* Chat message bubbles */
    .user-bubble {
        background: #1976D2;
        color: white;
        padding: 12px 18px;
        border-radius: 20px 20px 4px 20px;
        margin: 8px 0;
        max-width: 80%;
        margin-left: auto;
        font-size: 15px;
    }
    .bot-bubble {
        background: white;
        color: #1a1a1a;
        padding: 12px 18px;
        border-radius: 20px 20px 20px 4px;
        margin: 8px 0;
        max-width: 85%;
        border-left: 4px solid #43A047;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        font-size: 15px;
    }
    .disclaimer-box {
        background: #fff3e0;
        border-left: 4px solid #FF9800;
        padding: 10px 14px;
        border-radius: 6px;
        font-size: 13px;
        color: #555;
        margin-bottom: 10px;
    }
    .title-area {
        text-align: center;
        padding: 10px 0 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# ─── Title ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class='title-area'>
    <h1>🏥 AI Medical Chatbot</h1>
    <p style='color:#555; font-size:16px;'>Your intelligent medical assistant — ask about symptoms, conditions, medications & more</p>
</div>
""", unsafe_allow_html=True)

# ─── Disclaimer ──────────────────────────────────────────────────────────────
st.markdown("""
<div class='disclaimer-box'>
⚠️ <b>Medical Disclaimer:</b> This chatbot provides general medical information only.
It is <b>not a substitute</b> for professional medical advice, diagnosis, or treatment.
Always consult a qualified healthcare provider for medical concerns.
</div>
""", unsafe_allow_html=True)

# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/caduceus.png", width=80)
    st.markdown("## ⚙️ Settings")

    api_key = st.text_input(
        "🔑 Anthropic API Key",
        type="password",
        placeholder="sk-ant-...",
        help="Get your free key at console.anthropic.com"
    )

    st.markdown("---")
    st.markdown("### 🩺 Chatbot Mode")
    mode = st.selectbox(
        "Specialization",
        [
            "General Medicine",
            "Pediatrics",
            "Cardiology",
            "Dermatology",
            "Mental Health",
            "Nutrition & Diet",
            "Emergency First Aid",
        ]
    )

    st.markdown("---")
    st.markdown("### 💬 Quick Questions")
    quick_questions = [
        "What are symptoms of diabetes?",
        "How to treat a fever at home?",
        "What causes high blood pressure?",
        "Signs of a heart attack?",
        "How to manage anxiety?",
    ]
    for q in quick_questions:
        if st.button(q, use_container_width=True):
            st.session_state.quick_input = q

    st.markdown("---")
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.markdown("""
    <small style='color:#888;'>
    Built with ❤️ using<br>
    Python · Streamlit · Claude AI
    </small>
    """, unsafe_allow_html=True)

# ─── System Prompt ────────────────────────────────────────────────────────────
SYSTEM_PROMPTS = {
    "General Medicine": """You are Dr. MedBot, an expert AI medical assistant with knowledge 
    equivalent to a board-certified general physician. Your role:
    - Answer medical questions clearly and compassionately
    - Explain symptoms, conditions, treatments, and medications in simple language
    - Always mention when emergency care (911/ER) is needed
    - Always end with: recommend consulting a real doctor for diagnosis
    - Use structured answers with bullet points when listing symptoms or steps
    - Never make a definitive diagnosis""",

    "Pediatrics": """You are Dr. PediBot, a pediatric AI assistant specializing in child health 
    (newborns to 18 years). Focus on child-specific symptoms, development milestones, 
    vaccinations, and pediatric dosing. Always remind parents to consult a pediatrician.""",

    "Cardiology": """You are Dr. CardioBot, a cardiology-focused AI assistant. Help users 
    understand heart conditions, ECG basics, blood pressure, cholesterol, and cardiac symptoms. 
    Immediately flag potential emergency cardiac symptoms. Always recommend cardiologist consultation.""",

    "Dermatology": """You are Dr. DermBot, a dermatology AI assistant. Help describe skin 
    conditions, rashes, lesions, and treatments. Recommend when to see a dermatologist.
    Note that visual diagnosis requires in-person examination.""",

    "Mental Health": """You are Dr. MindBot, a mental health AI assistant trained in psychology 
    and psychiatry. Discuss anxiety, depression, stress management, and mental wellness compassionately.
    Always provide crisis resources (988 Suicide & Crisis Lifeline) when needed.
    Never replace a licensed therapist.""",

    "Nutrition & Diet": """You are NutriBot, an AI nutritionist and dietitian assistant.
    Help with dietary plans, nutrient information, healthy eating, and managing conditions 
    through diet (diabetes, hypertension, etc.). Always suggest consulting a registered dietitian.""",

    "Emergency First Aid": """You are FirstAidBot, an emergency first aid AI assistant.
    Provide clear, step-by-step first aid instructions for injuries and emergencies.
    Always start with: CALL 911 for life-threatening emergencies.
    Cover CPR basics, wound care, burns, fractures, allergic reactions, etc.""",
}

# ─── Session State ────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "quick_input" not in st.session_state:
    st.session_state.quick_input = None

# ─── Display Chat History ─────────────────────────────────────────────────────
chat_container = st.container()
with chat_container:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"<div class='user-bubble'>👤 {msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='bot-bubble'>🤖 {msg['content']}</div>", unsafe_allow_html=True)

# ─── Input Area ───────────────────────────────────────────────────────────────
st.markdown("---")

# Handle quick question injection
default_val = ""
if st.session_state.quick_input:
    default_val = st.session_state.quick_input
    st.session_state.quick_input = None

col1, col2 = st.columns([5, 1])
with col1:
    user_input = st.text_input(
        "Ask your medical question...",
        value=default_val,
        placeholder="e.g. What are the symptoms of pneumonia?",
        label_visibility="collapsed",
        key="chat_input"
    )
with col2:
    send_btn = st.button("Send 📨", use_container_width=True, type="primary")

# ─── Process & Respond ────────────────────────────────────────────────────────
def get_ai_response(messages, system_prompt, api_key):
    """Stream response from Claude API."""
    client = anthropic.Anthropic(api_key=api_key)
    
    # Build message history for API
    api_messages = [
        {"role": m["role"], "content": m["content"]}
        for m in messages
    ]
    
    with client.messages.stream(
        model="claude-haiku-4-5-20251001",   # Fast + affordable model
        max_tokens=1024,
        system=system_prompt,
        messages=api_messages,
    ) as stream:
        for text in stream.text_stream:
            yield text


if (send_btn or user_input) and user_input.strip():

    # Validate API key
    resolved_key = api_key or st.secrets.get("ANTHROPIC_API_KEY", "")
    if not resolved_key:
        st.error("❌ Please enter your Anthropic API key in the sidebar.")
        st.stop()

    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input.strip()})

    # Display user bubble immediately
    st.markdown(f"<div class='user-bubble'>👤 {user_input.strip()}</div>", unsafe_allow_html=True)

    # Stream AI response
    system_prompt = SYSTEM_PROMPTS.get(mode, SYSTEM_PROMPTS["General Medicine"])
    
    with st.spinner("🩺 Analyzing your question..."):
        response_placeholder = st.empty()
        full_response = ""

        try:
            for chunk in get_ai_response(
                st.session_state.messages,
                system_prompt,
                resolved_key
            ):
                full_response += chunk
                response_placeholder.markdown(
                    f"<div class='bot-bubble'>🤖 {full_response}▌</div>",
                    unsafe_allow_html=True
                )
            
            # Final display (remove cursor)
            response_placeholder.markdown(
                f"<div class='bot-bubble'>🤖 {full_response}</div>",
                unsafe_allow_html=True
            )

            # Save to history
            st.session_state.messages.append({
                "role": "assistant",
                "content": full_response
            })

        except anthropic.AuthenticationError:
            st.error("❌ Invalid API key. Please check your key in the sidebar.")
        except anthropic.RateLimitError:
            st.error("⏳ Rate limit reached. Please wait a moment and try again.")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style='text-align:center; color:#999; font-size:12px;'>
🏥 AI Medical Chatbot · For informational purposes only · Not a substitute for professional medical advice<br>
Emergency? Call <b>911</b> · Mental Health Crisis? Call <b>988</b>
</div>
""", unsafe_allow_html=True)
