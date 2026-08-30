
import streamlit as st
import os

from document_loader import load_pdf
from text_splitter import split_text
from vector_store import add_documents
from rag_pipeline import ask_rag


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Simple RAG Chatbot",
    page_icon="🤖",
    layout="wide"
)


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

/* ---------- Main App ---------- */

.stApp {
    background-color: #0F172A;
    color: #FFFFFF;
}


/* ---------- Main Container ---------- */

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1200px;
}


/* ---------- Main Title ---------- */

.main-title {
    text-align: center;
    font-size: 44px;
    font-weight: 800;
    color: #FFFFFF;
    margin-bottom: 8px;
}


/* ---------- Subtitle ---------- */

.subtitle {
    text-align: center;
    color: #E2E8F0;
    font-size: 17px;
    margin-bottom: 35px;
}


/* ---------- Sidebar ---------- */

section[data-testid="stSidebar"] {
    background-color: #1E293B;
    border-right: 1px solid #334155;
}

section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #FFFFFF;
}


/* ---------- Sidebar Text ---------- */

section[data-testid="stSidebar"] label {
    color: #E2E8F0 !important;
}


/* ---------- File Uploader ---------- */

[data-testid="stFileUploader"] {
    background-color: #0F172A;
    border: 1px solid #475569;
    border-radius: 12px;
    padding: 10px;
}


/* ---------- Buttons ---------- */

.stButton > button {
    background-color: #8B5CF6;
    color: #FFFFFF;
    border: none;
    border-radius: 10px;
    font-weight: 600;
    padding: 10px 18px;
    transition: 0.2s ease;
}

.stButton > button:hover {
    background-color: #7C3AED;
    color: #FFFFFF;
    border: none;
}


/* ---------- Chat Input ---------- */

[data-testid="stChatInput"] {
    background-color: #1E293B;
    border: 1px solid #475569;
    border-radius: 12px;
}

[data-testid="stChatInput"] textarea {
    color: #FFFFFF !important;
}


/* ---------- Chat Messages ---------- */

[data-testid="stChatMessage"] {
    background-color: #1E293B;
    border: 1px solid #334155;
    border-radius: 14px;
    padding: 12px;
    margin-bottom: 12px;
}


/* ---------- General Text ---------- */

.stMarkdown {
    color: #FFFFFF;
}


/* ---------- AI Response ---------- */

[data-testid="stChatMessage"]:has(
    [data-testid="chatAvatarIcon-assistant"]
) {
    border-left: 4px solid #38BDF8;
}


/* ---------- Success Message ---------- */

div[data-testid="stAlert"] {
    border-radius: 10px;
}


/* ---------- Document Status ---------- */

.document-status {
    background-color: #1E293B;
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 15px 20px;
    margin: 20px 0;
    color: #E2E8F0;
}


/* ---------- Section Divider ---------- */

hr {
    border-color: #334155;
}


/* ---------- Spinner ---------- */

.stSpinner > div {
    border-top-color: #38BDF8 !important;
}


/* ---------- Links ---------- */

a {
    color: #38BDF8 !important;
}


/* ---------- Warning / Info ---------- */

[data-testid="stAlert"] p {
    color: #E2E8F0;
}


/* ---------- Mobile ---------- */

@media (max-width: 768px) {

    .main-title {
        font-size: 32px;
    }

    .subtitle {
        font-size: 15px;
    }

}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "document_loaded" not in st.session_state:
    st.session_state.document_loaded = False


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    '<div class="main-title">🤖 Simple RAG Chatbot</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Upload a PDF and ask intelligent questions about it'
    '</div>',
    unsafe_allow_html=True
)


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.header("📄 Document")

    st.caption("Upload a PDF to build your knowledge base.")

    uploaded_file = st.file_uploader(
        "Upload PDF",
        type=["pdf"]
    )

    if uploaded_file:

        if st.button(
            "📚 Process Document",
            use_container_width=True
        ):

            with st.spinner("Processing document..."):

                try:

                    # Create data folder
                    os.makedirs("data", exist_ok=True)

                    # Save uploaded PDF
                    file_path = os.path.join(
                        "data",
                        uploaded_file.name
                    )

                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())


                    # -----------------------------
                    # Load PDF
                    # -----------------------------

                    text = load_pdf(file_path)

                    if not text.strip():

                        st.error(
                            "Could not extract text from this PDF."
                        )

                        st.stop()


                    # -----------------------------
                    # Split Text
                    # -----------------------------

                    chunks = split_text(text)

                    if not chunks:

                        st.error(
                            "No text chunks were created."
                        )

                        st.stop()


                    # -----------------------------
                    # Create Vector Store
                    # -----------------------------

                    add_documents(chunks)


                    # Document ready
                    st.session_state.document_loaded = True

                    st.success(
                        f"✅ Document processed successfully!\n\n"
                        f"📚 {len(chunks)} chunks created."
                    )


                except Exception as e:

                    st.error(
                        f"Document processing failed:\n{e}"
                    )


    st.markdown("---")


    # Clear Chat
    if st.button(
        "🗑️ Clear Chat",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.rerun()


# --------------------------------------------------
# DOCUMENT STATUS
# --------------------------------------------------

if st.session_state.document_loaded:

    st.markdown(
        """
        <div class="document-status">
        ✅ <b>Document is ready!</b><br>
        You can now ask questions about your uploaded PDF.
        </div>
        """,
        unsafe_allow_html=True
    )

else:

    st.info(
        "📄 Upload a PDF from the sidebar and process it first."
    )


# --------------------------------------------------
# CHAT HISTORY
# --------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# --------------------------------------------------
# CHAT INPUT
# --------------------------------------------------

question = st.chat_input(
    "💬 Ask something about your document..."
)


# --------------------------------------------------
# PROCESS QUESTION
# --------------------------------------------------

if question:

    if not st.session_state.document_loaded:

        st.warning(
            "Please upload and process a PDF before asking questions."
        )

    else:

        # -----------------------------
        # User Message
        # -----------------------------

        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.chat_message("user"):

            st.markdown(question)


        # -----------------------------
        # AI Response
        # -----------------------------

        with st.chat_message("assistant"):

            with st.spinner("🔎 Searching your document..."):

                try:

                    answer = ask_rag(question)

                    st.markdown(answer)

                except Exception as e:

                    answer = f"Error: {e}"

                    st.error(answer)


        # Save AI response
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )