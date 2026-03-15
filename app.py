import streamlit as st
import plotly.express as px
import pandas as pd
import PyPDF2
import os


VISIT_FILE = "visits.txt"

if not os.path.exists(VISIT_FILE):
    with open(VISIT_FILE, "w") as f:
        f.write("0")

with open(VISIT_FILE, "r") as f:
    visits = int(f.read())

visits += 1

with open(VISIT_FILE, "w") as f:
    f.write(str(visits))
st.sidebar.markdown("---")
st.sidebar.markdown("### 👥 Total Users")

st.sidebar.success(f"{visits} people used this app")

from streamlit_option_menu import option_menu

st.set_page_config(page_title="PlacementIQ AI", layout="wide")

st.title("🎓 PlacementIQ - AI Career Assistant")

# Sidebar Navigation
with st.sidebar:
    selected = option_menu(
        "Menu",
       ["Dashboard","Skill Analyzer","Career Roadmap","Interview Prep","Resume Analyzer","AI Mentor"],
        icons=["house","bar-chart","map","chat"],
        menu_icon="menu-button",
        default_index=0
    )

# ---------------- DASHBOARD ----------------

if selected == "Dashboard":

    st.header("Welcome to PlacementIQ")

    col1,col2,col3 = st.columns(3)

    col1.metric("Python Skill","7/10")
    col2.metric("DSA Skill","6/10")
    col3.metric("Communication","8/10")

    st.info("Use the sidebar to explore placement preparation tools.")

# ---------------- SKILL ANALYZER ----------------

elif selected == "Skill Analyzer":

    st.header("Skill Analyzer")

    python = st.slider("Python",0,10)
    dsa = st.slider("DSA",0,10)
    sql = st.slider("SQL",0,10)
    communication = st.slider("Communication",0,10)

    skills = {
        "Skill":["Python","DSA","SQL","Communication"],
        "Score":[python,dsa,sql,communication]
    }

    df = pd.DataFrame(skills)

    fig = px.line_polar(df,r="Score",theta="Skill",line_close=True)

    st.plotly_chart(fig)

    score = (python+dsa+sql+communication)/4

    st.subheader("Placement Readiness Score")

    st.progress(score/10)

    st.write("Score:",round(score,2),"/10")

# ---------------- CAREER ROADMAP ----------------

elif selected == "Career Roadmap":

    st.header("Career Roadmap Generator")

    career = st.selectbox(
        "Select Career Goal",
        ["Data Analyst","Software Developer","Data Scientist"]
    )

    if st.button("Generate Roadmap"):

        if career == "Data Analyst":

            st.write("Learn Python, Pandas, SQL")
            st.write("Learn Power BI / Tableau")
            st.write("Work on real datasets")

        elif career == "Software Developer":

            st.write("Practice DSA daily")
            st.write("Learn Web Development")
            st.write("Build projects")

        elif career == "Data Scientist":

            st.write("Learn Machine Learning")
            st.write("Study Statistics")
            st.write("Build ML models")

# ---------------- INTERVIEW PREP ----------------

elif selected == "Interview Prep":

    st.header("Interview Preparation")

    st.subheader("Common HR Questions")

    st.write("Tell me about yourself")
    st.write("Why should we hire you?")
    st.write("What are your strengths and weaknesses?")

    st.subheader("Technical Preparation")

    st.write("Practice DSA problems")
    st.write("Revise core concepts")
    st.write("Prepare projects explanation")
    # ---------------- RESUME ANALYZER ----------------

elif selected == "Resume Analyzer":

    st.header("AI Resume Analyzer")

    uploaded_file = st.file_uploader(
        "Upload your resume (PDF)", type="pdf"
    )

    if uploaded_file is not None:

        pdf_reader = PyPDF2.PdfReader(uploaded_file)

        text = ""

        for page in pdf_reader.pages:
            text += page.extract_text()

        st.success("Resume uploaded successfully")

        if st.button("Analyze Resume"):

            prompt = f"""
            Analyze this resume and give suggestions to improve it
            for placements. Mention missing skills and improvements.

            Resume:
            {text}
            """

            answer = ask_ai(prompt)

            st.subheader("AI Resume Feedback")

            st.write(answer)
import streamlit as st
import requests

st.title("PlacementIQ AI Mentor")

st.subheader("Ask anything about placements, coding interviews, or career guidance")

API_KEY = st.secrets["API_KEY"]


def ask_ai(question):

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
    "model": "meta-llama/llama-3-8b-instruct",
    "messages": [
        {"role": "system", "content": "You are a helpful AI mentor that gives career, coding, and placement preparation advice for students."},
        {"role": "user", "content": question}
    ]
}

    response = requests.post(url, headers=headers, json=data)

    if response.status_code != 200:
        return f"API Error: {response.text}"

    result = response.json()

    if "choices" in result:
        return result["choices"][0]["message"]["content"]
    else:
        return str(result)


question = st.text_input("Ask placement question")

if st.button("Ask AI"):
    if question:
        answer = ask_ai(question)
        st.write(answer)

