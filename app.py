# import streamlit as st
# from llm_client import generate_response
# from prompts import resume_prompt


# # Add at the top of app.py
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []

# # When user submits a new query:
# st.session_state.chat_history.append({"role": "user", "content": user_query})
# prompt = resume_prompt(resume_text, user_query)

# # Append last few turns for continuity
# for past in st.session_state.chat_history[-3:]:
#     prompt += f"\n\n{past['role'].capitalize()}: {past['content']}"

# reply = generate_response(prompt)
# st.session_state.chat_history.append({"role": "assistant", "content": reply})


# st.set_page_config(page_title="Resume Chatbot", page_icon="💼", layout="centered")

# st.title("💼 Resume Assistant (Gemini 2.5 / GPT-4.1 Optional)")
# st.write("Ask questions about your resume, rewriting, or interview prep.")

# # Sidebar for model selection
# st.sidebar.header("⚙️ Settings")
# provider_choice = st.sidebar.radio("Choose LLM", ["Gemini 2.5", "GPT-4.1 (optional)"])
# st.sidebar.info("Default: Gemini 2.5 (free-tier)")

# resume_text = st.text_area("📄 Paste your resume (optional):", height=200)
# user_query = st.text_area("💬 Ask your question:", placeholder="e.g., Rewrite my bullets for a Data Scientist role")

# if st.button("Generate Response"):
#     if not user_query.strip():
#         st.warning("Please enter a question.")
#     else:
#         st.spinner("Thinking...")
#         full_prompt = resume_prompt(resume_text, user_query)
#         reply = generate_response(full_prompt)
#         st.success("✅ Response:")
#         st.markdown(reply)






import streamlit as st
import os
from dotenv import load_dotenv
import PyPDF2
from llm_client import generate_response
from prompts import resume_prompt

# --------------------------------------------------------------------
# ✅ Page Configuration
# --------------------------------------------------------------------
st.set_page_config(page_title="Resume Assistant", page_icon="💼", layout="centered")
load_dotenv()

# --------------------------------------------------------------------
# ✅ Sidebar Settings
# --------------------------------------------------------------------
st.sidebar.header("⚙️ Settings")
provider_choice = st.sidebar.radio("Choose LLM", ["Gemini 2.5", "GPT-4.1 (optional)"])
st.sidebar.info("Default: Gemini 2.5 (free-tier)")

# Set environment variable dynamically for llm_client routing
os.environ["LLM_PROVIDER"] = "gpt4" if "GPT" in provider_choice else "gemini"

# --------------------------------------------------------------------
# ✅ Initialize Session State
# --------------------------------------------------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --------------------------------------------------------------------
# ✅ Page Header
# --------------------------------------------------------------------
st.title("💼 Resume Assistant (Gemini 2.5 / GPT-4.1 Optional)")
st.write("Ask questions about your resume, rewriting, optimization, or interview preparation.")

# --------------------------------------------------------------------
# 📎 Resume Input Section (PDF + Text)
# --------------------------------------------------------------------
st.subheader("📄 Provide Your Resume")

resume_text = ""

uploaded_file = st.file_uploader("Upload your resume (PDF optional)", type=["pdf"])
if uploaded_file is not None:
    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        for page in pdf_reader.pages:
            resume_text += page.extract_text() + "\n"
        st.success("✅ Resume text extracted from PDF successfully!")
    except Exception as e:
        st.error(f"❌ Error reading PDF: {e}")

if not resume_text.strip():
    resume_text = st.text_area("Or paste your resume text here:", height=200)

# --------------------------------------------------------------------
# 💬 Chat Section
# --------------------------------------------------------------------
st.subheader("💬 Ask Your Question")
user_query = st.text_area(
    "Ask your resume question or request (e.g., 'Rewrite for Data Scientist role')",
    placeholder="Example: Tailor my resume for a Senior Data Scientist position at Google",
)

# --------------------------------------------------------------------
# 🧠 Conversation & LLM Interaction
# --------------------------------------------------------------------
if st.button("Generate Response"):
    if not user_query.strip():
        st.warning("Please enter a question before submitting.")
    else:
        # Build dynamic prompt with history context
        st.session_state.chat_history.append({"role": "user", "content": user_query})
        base_prompt = resume_prompt(resume_text, user_query)

        # Append last 3 exchanges for continuity
        for past in st.session_state.chat_history[-3:]:
            base_prompt += f"\n\n{past['role'].capitalize()}: {past['content']}"

        with st.spinner("🤔 Thinking..."):
            reply = generate_response(base_prompt)

        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        st.success("✅ Response:")
        st.markdown(reply)

# --------------------------------------------------------------------
# 🕓 Display Conversation History
# --------------------------------------------------------------------
if st.session_state.chat_history:
    st.subheader("📜 Chat History")
    for i, msg in enumerate(st.session_state.chat_history[-6:]):
        role = "🧑‍💻 You" if msg["role"] == "user" else "🤖 ResumeGPT"
        with st.expander(f"{role} says:", expanded=False):
            st.markdown(msg["content"])

# --------------------------------------------------------------------
# 💡 Info Section
# --------------------------------------------------------------------
st.sidebar.markdown("---")
st.sidebar.markdown("**Made with 💙 using Gemini 2.5 and Streamlit**")
st.sidebar.markdown("Tips:")
st.sidebar.markdown("- Upload your PDF or paste your resume")
st.sidebar.markdown("- Ask for rewriting, tailoring, or summaries")
st.sidebar.markdown("- Toggle GPT-4.1 for deeper analysis (optional)")
