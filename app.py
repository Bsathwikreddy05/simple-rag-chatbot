import streamlit as st
from rag_pipeline import ask_rag

# --------------------------------------------------
# 1. PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="HR Policy RAG Assistant",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --------------------------------------------------
# 2. MODERN OBSIDIAN / CYAN STYLING & HIGH-CONTRAST FIXES
# --------------------------------------------------
st.markdown("""
<style>
    /* Dark app canvas */
    .stApp {
        background: radial-gradient(circle at 50% 0%, #0d1527 0%, #080b11 100%);
        color: #ffffff;
    }

    /* Main chat bubble container */
    div[data-testid="stChatMessage"] {
        background: #111827 !important;
        border: 1px solid #1f2937 !important;
        border-radius: 12px !important;
        padding: 18px 22px !important;
        margin-bottom: 14px !important;
    }

    /* Crisp, bright, high-contrast response text */
    div[data-testid="stChatMessage"] p, 
    div[data-testid="stChatMessage"] li, 
    div[data-testid="stChatMessage"] span {
        color: #ffffff !important;
        font-size: 15px !important;
        line-height: 1.65 !important;
        font-weight: 400 !important;
    }

    /* Cyan highlight for bold headings/phrases in answers */
    div[data-testid="stChatMessage"] strong {
        color: #38bdf8 !important;
        font-weight: 600 !important;
    }

    /* Link formatting inside responses */
    div[data-testid="stChatMessage"] a {
        color: #00f2fe !important;
        text-decoration: underline !important;
    }

    /* Fix expander completely: eliminate white glitch on toggle */
    div[data-testid="stExpander"],
    div[data-testid="stExpander"] details,
    div[data-testid="stExpander"] summary {
        background-color: #0b1220 !important;
        border: 1px solid #1f2937 !important;
        border-radius: 8px !important;
        color: #94a3b8 !important;
    }

    div[data-testid="stExpander"] summary:hover {
        color: #38bdf8 !important;
    }

    div[data-testid="stExpander"] div[role="region"],
    div[data-testid="stExpander"] div[data-testid="stVerticalBlock"] {
        background-color: #0b1220 !important;
        color: #cbd5e1 !important;
    }

    div[data-testid="stExpander"] p,
    div[data-testid="stExpander"] li {
        color: #cbd5e1 !important;
        font-size: 14px !important;
    }

    /* Bottom Input Container */
    div[data-testid="stChatInput"] {
        background-color: transparent !important;
    }

    div[data-testid="stChatInput"] > div {
        background-color: #111827 !important;
        border: 1px solid #374151 !important;
        border-radius: 12px !important;
    }

    /* High visibility input typing area & glowing cursor */
    div[data-testid="stChatInput"] textarea {
        color: #ffffff !important;
        font-size: 15px !important;
        background-color: transparent !important;
        caret-color: #00f2fe !important;
    }

    div[data-testid="stChatInput"] textarea::placeholder {
        color: #64748b !important;
    }

    /* Send arrow button styling */
    div[data-testid="stChatInput"] button {
        color: #00f2fe !important;
    }

    /* Example question buttons and sidebar button */
    .stButton button {
        background: #111827 !important;
        color: #38bdf8 !important;
        border: 1px solid #1f2937 !important;
        border-radius: 10px !important;
        font-size: 0.85rem !important;
    }

    .stButton button:hover {
        border-color: #38bdf8 !important;
    }

    /* Simple dark sidebar */
    section[data-testid="stSidebar"] {
        background: #0b1220 !important;
    }

    section[data-testid="stSidebar"] * {
        color: #cbd5e1 !important;
    }

    /* App Header Typography */
    .hero-title {
        font-size: 2.3rem;
        font-weight: 800;
        text-align: center;
        color: #ffffff;
        margin-top: 20px;
    }

    .hero-subtitle {
        font-size: 0.95rem;
        color: #94a3b8;
        text-align: center;
        margin-bottom: 28px;
    }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# 3. HEADER
# --------------------------------------------------
st.markdown('<div class="hero-title">🛡️ HR Policy RAG Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Instant, verified workplace answers from the employee handbook</div>', unsafe_allow_html=True)

# --------------------------------------------------
# 4. CHAT STATE, SOURCES HELPER & SIDEBAR
# --------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []


def show_sources(sources):
    """Show the handbook sections used for an answer in a small dropdown."""
    if sources:
        with st.expander("📚 Sources"):
            for source in sources:
                st.markdown(f"- {source}")


with st.sidebar:
    st.markdown("### HR Policy Assistant")
    st.caption("Handbook version: v2026.1")
    st.caption("Internal HR Knowledge Base")
    if st.button("🗑️ Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --------------------------------------------------
# 5. CHAT HISTORY & EXAMPLE QUESTIONS
# --------------------------------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        show_sources(message.get("sources", []))

EXAMPLE_QUESTIONS = [
    "What is the notice period?",
    "How does PTO carry forward work?",
    "How do I claim OPD expenses?",
]

# Example questions only show on an empty chat
example_area = st.empty()
clicked_question = None

if not st.session_state.messages:
    with example_area.container():
        columns = st.columns(len(EXAMPLE_QUESTIONS))
        for column, question in zip(columns, EXAMPLE_QUESTIONS):
            if column.button(question, use_container_width=True):
                clicked_question = question

# --------------------------------------------------
# 6. USER INPUT & QUERY EXECUTION
# --------------------------------------------------
user_prompt = st.chat_input("Ask about leave rules, insurance, probation, or notice period...") or clicked_question

if user_prompt:
    example_area.empty()

    # Display user query
    with st.chat_message("user"):
        st.markdown(user_prompt)
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    # Generate assistant answer
    with st.chat_message("assistant"):
        with st.spinner("Checking policy records..."):
            try:
                result = ask_rag(user_prompt, chat_history=st.session_state.messages[:-1])

                if isinstance(result, tuple):
                    bot_response, sources = result
                else:
                    bot_response, sources = result, []

                st.markdown(bot_response)
                show_sources(sources)
                st.session_state.messages.append(
                    {"role": "assistant", "content": bot_response, "sources": sources}
                )
            except Exception as e:
                err_msg = f"Error querying policy system: {e}"
                st.error(err_msg)
                st.session_state.messages.append({"role": "assistant", "content": err_msg})