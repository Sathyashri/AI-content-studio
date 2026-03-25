import streamlit as st
from llm_helper import generate_from_llm
from utils.prompt_builder import build_linkedin_prompt, build_youtube_prompt
from models.embeddings import find_similar_posts
from database import create_tables, register_user, login_user, save_content, get_user_content

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI Content Studio", page_icon="🤖", layout="wide", initial_sidebar_state="expanded")

create_tables()

if "user" not in st.session_state:
    st.session_state.user = None

if "page" not in st.session_state:
    st.session_state.page = "main"

# ---------------- GLOBAL CSS (UPDATED THEME ONLY) ----------------
st.markdown("""
<style>

.block-container { padding-top: 0rem !important; }
header[data-testid="stHeader"] { display: none; }

/* 🌿 SAGE GREEN + LILY PINK THEME */
.stApp {
    background: linear-gradient(135deg, #A8D5BA, #CDE7BE, #F8C8DC);
    color: #1e1e1e;
}

section.main > div { max-width: 1100px; margin: auto; }

.card {
    background: rgba(255,255,255,0.6);
    padding: 20px;
    border-radius: 16px;
    backdrop-filter: blur(10px);
    margin-bottom: 15px;
}

.output-card {
    background: #ffffff;
    color: #1e1e1e;
    padding: 20px;
    border-radius: 16px;
    border-left: 6px solid #A8D5BA;
    margin-top: 20px;
}

.stTextInput input, .stTextArea textarea {
    background: white !important;
    color: black !important;
    border-radius: 10px !important;
}

.stButton>button {
    background: linear-gradient(90deg, #A8D5BA, #F8C8DC);
    color: #1e1e1e;
    border-radius: 10px;
    font-weight: bold;
}

.user-box {
    padding:10px;
    border-radius:10px;
    background: linear-gradient(90deg,#A8D5BA,#F8C8DC);
    text-align:center;
    font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

# ---------------- LOGIN UI ----------------
if st.session_state.user is None:

    st.markdown("<h1 style='text-align:center;'>🚀 AI Content Studio</h1>", unsafe_allow_html=True)

    st.markdown('<div class="card" style="max-width:400px;margin:auto;text-align:center;">', unsafe_allow_html=True)

    st.subheader("Welcome")

    choice = st.radio("Choose option", ["Sign In", "Create Account"], horizontal=True)

    if choice == "Sign In":
        st.markdown("### Sign in to continue")

        u = st.text_input("Email / Username")
        p = st.text_input("Password", type="password")

        if st.button("Sign In", use_container_width=True):
            user = login_user(u, p)
            if user:
                st.session_state.user = user
                st.success("Welcome back 🤖")
                st.rerun()
            else:
                st.error("Invalid credentials")

    else:
        st.markdown("### Create your account")

        # ✅ USERNAME CLARITY FIX
        u = st.text_input("Username (this will be your profile name)")
        p = st.text_input("Password", type="password")

        if st.button("Create Account", use_container_width=True):
            if len(u) < 3:
                st.warning("Username too short")
            elif len(p) < 5:
                st.warning("Password too weak")
            else:
                if register_user(u, p):
                    st.session_state.user = login_user(u, p)
                    st.success("Account created 🎉")
                    st.rerun()
                else:
                    st.error("Username exists")

    st.markdown("---")
    st.markdown("### Or continue with")

    col1, col2 = st.columns(2)
    with col1:
        st.button("🔵 Google", use_container_width=True)
    with col2:
        st.button("🟣 Microsoft", use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

    st.stop()

# ---------------- SIDEBAR ----------------
st.sidebar.title("🤖 AI Tools")
st.sidebar.markdown(f"""
<div class="user-box">
👤 {st.session_state.user[1]}
</div>
""", unsafe_allow_html=True)

if st.sidebar.button("👤 Profile"):
    st.session_state.page = "profile"

if st.sidebar.button("Logout"):
    st.session_state.user = None
    st.rerun()

tool = st.sidebar.selectbox("Choose Tool", [
    "LinkedIn Post Generator",
    "Blog Writer",
    "Content Summarizer",
    "YouTube Description",
    "YouTube Titles & Ideas",
    "Instagram Hashtags",
    "Article Rewriter",
    "Book Ideas Generator"
])

# ---------------- PROFILE PAGE (UPDATED) ----------------
if st.session_state.page == "profile":

    st.title("👤 Your Profile")

    username = st.session_state.user[1]

    st.markdown(f"""
<div class="card">
<h3>👤 {username}</h3>
<p>Your personal dashboard</p>
</div>
""", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📜 History", "✏ Edit Profile"])

    # HISTORY INSIDE PROFILE
    with tab1:
        data = get_user_content(st.session_state.user[0])

        if not data:
            st.info("No history yet.")
        else:
            for d in data:
                st.markdown(f"""
<div class="card">
<b>🛠 Tool:</b> {d[0]}<br><br>
<b>📥 Input:</b><br>{d[1]}<br><br>
<b>📤 Output:</b><br>{d[2]}
</div><br>
""", unsafe_allow_html=True)

    # EDIT PROFILE
    with tab2:
        st.subheader("Update Username")

        new_name = st.text_input("New Username")

        if st.button("Update Profile"):
            if len(new_name) < 3:
                st.warning("Username too short")
            else:
                st.session_state.user = (
                    st.session_state.user[0],
                    new_name
                )
                st.success("Profile updated ✅")
                st.rerun()

    if st.button("⬅ Back"):
        st.session_state.page = "main"
        st.rerun()

    st.stop()

# ---------------- MAIN PAGE ----------------
if st.session_state.page == "main":

# ---------------- HEADER ----------------
    st.title("🤖 AI Content Studio")
    st.caption("Generate high-quality AI content instantly")

# ---------------- INPUT ----------------
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)

        topic = ""
        category = ""
        length = ""

        if tool == "LinkedIn Post Generator":
            topic = st.text_input("💡 Topic")
            category = st.selectbox("📂 Category", ["Career Advice", "Job Search", "Artificial Intelligence", "Startup & Entrepreneurship", "Productivity", "Personal Branding", "Motivation & Mindset", "Technology Trends", "Marketing & Sales", "Finance & Investing", "Student Life", "Leadership", "Remote Work", "Freelancing", "Networking"])
            length = st.selectbox("📏 Length", ["Short","Medium","Long"])

        elif tool == "Blog Writer":
            topic = st.text_input("💡 Blog Topic")

        elif tool == "Content Summarizer":
            topic = st.text_area("📄 Paste Content", height=250)

        elif tool == "YouTube Description":
            topic = st.text_input("🎥 Video Topic")

        elif tool == "YouTube Titles & Ideas":
            topic = st.text_input("🎯 Topic")

        elif tool == "Instagram Hashtags":
            topic = st.text_input("📸 Topic")
            length = st.selectbox("🔢 Number of Hashtags", list(range(5, 51)), index=15)

        elif tool == "Article Rewriter":
            topic = st.text_area("✍️ Paste Article", height=250)

        elif tool == "Book Ideas Generator":
            topic = st.text_input("📚 Topic")

        st.markdown('</div>', unsafe_allow_html=True)

# ---------------- GENERATE ----------------
    if st.button("✨ Generate Content"):

        if not topic:
            st.warning("⚠️ Please enter input")
        else:
            with st.spinner("⚡ Generating..."):

                if tool == "LinkedIn Post Generator":
                    examples = find_similar_posts(topic)
                    prompt = build_linkedin_prompt(topic, category, length)

                    if len(examples) >= 2:
                        prompt += f"\n\nExamples:\n{examples[0]}\n\n{examples[1]}"

                elif tool == "Blog Writer":
                    prompt = f"""
                Write a well-structured blog post on the topic below.

                Topic: {topic}

                Requirements:
                - Clear introduction
                - 3–5 sections with headings
                - Simple explanation
                - Engaging tone
                - Proper conclusion

                Output ONLY the blog content.
                """

                elif tool == "Content Summarizer":
                    prompt = f"Summarize:\n{topic}"

                elif tool == "YouTube Description":
                    prompt = f"Write YouTube description for {topic}"

                elif tool == "YouTube Titles & Ideas":
                    prompt = build_youtube_prompt(topic)

                elif tool == "Instagram Hashtags":
                    prompt = f"Generate {length} Instagram hashtags for {topic}"

                elif tool == "Article Rewriter":
                    prompt = f"Rewrite this content:\n{topic}"

                elif tool == "Book Ideas Generator":
                    prompt = f"""
                Generate creative book ideas.

                Topic: {topic}

                Requirements:
                - Generate exactly 3 book titles
                - Each should include:
                    - Short description (2 lines)
                    - 4 chapter ideas

                Keep it clean and readable.

                Output format:

                Book Title:
                Description:
                Chapters:
                """

                output = generate_from_llm(prompt)

                if tool == "LinkedIn Post Generator":
                    if "#" not in output:
                        output += "\n\n#growth #success #career #learning #motivation"

                save_content(st.session_state.user[0], tool, topic, output)

            st.markdown("### ✨ Output")

            st.markdown('<div class="output-card">', unsafe_allow_html=True)
            st.markdown(output)
            st.markdown('</div>', unsafe_allow_html=True)