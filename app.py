
# app.py (Enhanced Streamlit UI)
import streamlit as st
import pandas as pd
import json
from datetime import datetime
from io import StringIO, BytesIO

st.set_page_config(page_title="AI Career Path Recommender", page_icon="🎓", layout="wide")



# --- Simple login page ---

def login_page():
    st.markdown("""
        <style>
        .login-card {
            background: linear-gradient(135deg, #e0e7ff 0%, #f0fdfa 100%);
            border-radius: 18px;
            box-shadow: 0 4px 24px rgba(60,60,120,0.12);
            padding: 2.5rem 2rem 2rem 2rem;
            max-width: 400px;
            margin: 60px auto 0 auto;
        }
        .login-title {
            font-size: 2.2rem;
            font-weight: 700;
            color: #3b3b5c;
            text-align: center;
            margin-bottom: 0.5rem;
        }
        .login-sub {
            font-size: 1.1rem;
            color: #5c5c7a;
            text-align: center;
            margin-bottom: 2rem;
        }
        .login-icon {
            display: flex;
            justify-content: center;
            margin-bottom: 1.2rem;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center;margin-bottom:1.5rem;">
        <img src="https://cdn-icons-png.flaticon.com/512/1055/1055687.png" width="80" alt="Books Icon" style="margin-bottom:0.5rem;"/>
        <h1 style="font-size:2.1rem;font-weight:700;color:#3b3b5c;margin:0;">Career Path Recommender</h1>
        <div style="font-size:1.1rem;color:#5c5c7a;margin-bottom:0.5rem;">AI-powered career guidance for tech enthusiasts</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    st.markdown('<div class="login-icon"><img src="https://cdn-icons-png.flaticon.com/512/3064/3064197.png" width="60" alt="Login Icon" style="border-radius:50%;box-shadow:0 2px 8px #ccc;"/></div>', unsafe_allow_html=True)
    st.markdown('<div class="login-title">Welcome Back!</div>', unsafe_allow_html=True)
    st.markdown('<div class="login-sub">Sign in to unlock your personalized career recommendations.<br>Modern, secure, and AI-powered.</div>', unsafe_allow_html=True)

    with st.form("login_form"):
        username = st.text_input("Username", placeholder="Enter your username", key="login_user")
        password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_pass")
        login_btn = st.form_submit_button("Login", help="Sign in to continue")
    if login_btn:
        # Hardcoded credentials (change as needed)
        if username == "user" and password == "pass":
            st.session_state["logged_in"] = True
            st.success("Login successful! Redirecting...")
            st.rerun()
        else:
            st.error("Invalid username or password.")
            st.markdown('<div style="text-align:center;color:#e53e3e;font-size:1.1rem;">Please try again.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# --- Logout button (visible after login) ---
if "logged_in" in st.session_state and st.session_state["logged_in"]:
    with st.sidebar:
        if st.button("Logout", help="Sign out and return to login page"):
            st.session_state["logged_in"] = False
            st.session_state["skills_input"] = ""
            st.rerun()

if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    login_page()
    st.stop()

# --- Import ML recommender ---
USE_NEW_API = False
try:
    from data.recommender_ml import recommend, generate_deep_advice, load_data as load_data_fn, train_vectorizer
    USE_NEW_API = True
except Exception as e:
    st.error("Could not import recommender functions from data/recommender_ml.py. Check file and function names.")
    raise

# --- Page config + header ---
st.set_page_config(page_title="AI Career Path Recommender", page_icon="🎓", layout="wide")
st.markdown("<style> .big-font { font-size:22px !important; } </style>", unsafe_allow_html=True)

# Header
col1, col2 = st.columns([4,1])
with col1:
    st.markdown("<h1 style='margin:0;'>🎓 AI Career Path Recommender</h1>", unsafe_allow_html=True)
    st.markdown("Enter your skills or interests and get ranked, detailed career roadmaps and suggested starter projects.")
with col2:
    st.image("https://cdn-icons-png.flaticon.com/512/1055/1055687.png", width=80, caption="Tech & Books", output_format="PNG")

st.write("") # spacer

# --- Sidebar controls ---
with st.sidebar:
    st.header("About")
    st.write("This app suggests career paths based on your skills. It uses an ML-based recommender and returns step-by-step roadmaps.")
    st.markdown("---")
    st.header("Quick examples")
    st.write("- `python, sql, machine learning`")
    st.write("- `html, css, javascript, react`")
    st.write("- `aws, docker, kubernetes`")
    st.markdown("---")
    st.header("Options")
    top_k = st.slider("How many careers to show", 1, 8, 3)
    show_scores = st.checkbox("Show match scores", True)
    detail_mode = st.radio("Response style", ["Deep-dive (detailed)", "Short summary"], index=0)
    st.markdown("---")
    st.write("Project by: **You**")
    st.write("[GitHub repo](https://github.com/yourusername/yourrepo)")

# --- Main input area ---
st.markdown("### Tell me your skills / interests")
input_col, examples_col = st.columns([3,1])
with input_col:
    skills_input = st.text_area(
        "Enter skills (comma-separated)",
        value=st.session_state.get("skills_input", ""),
        height=110,
        placeholder="e.g. Python, SQL, Machine Learning"
    )
    st.session_state["skills_input"] = skills_input
    skill_chips = st.text_input("Quick add skills (press Enter after each):", value="") # optional quick field
with examples_col:
    st.markdown("#### Try examples")
    if st.button("Data / ML example"):
        st.session_state["skills_input"] = "Python, SQL, Machine Learning"
        st.rerun()
    if st.button("Web dev example"):
        st.session_state["skills_input"] = "HTML, CSS, JavaScript, React"
        st.rerun()
    if st.button("Cloud example"):
        st.session_state["skills_input"] = "AWS, Docker, Kubernetes"
        st.rerun()

if "skills_input" in st.session_state:
    skills_input = st.session_state["skills_input"]


# -------------------------
# Caching helpers
# -------------------------
@st.cache_data(show_spinner=False)
def load_dataset():
    return load_data_fn()


# -------------------------
# Run recommendation
# -------------------------
run = st.button("🚀 Get Recommendations")
dataset = load_dataset()
if run:
    if not skills_input or not skills_input.strip():
        st.warning("Please enter at least one skill.")
    else:
        with st.spinner("Finding best matches..."):
            try:
                vectorizer, tfidf = train_vectorizer(dataset)
                recs = recommend(skills_input, dataset, vectorizer, tfidf, top_k=top_k)
                results = []
                for r in recs:
                    try:
                        deep_text = generate_deep_advice(skills_input, r)
                    except Exception:
                        deep_text = r.get("description","")
                    results.append({
                        "career": r.get("career"),
                        "description": r.get("description",""),
                        "roadmap": r.get("learning_path",""),
                        "score": r.get("score"),
                        "deep_text": deep_text
                    })
            except Exception as e:
                st.error(f"Error running recommender: {e}")
                raise

        # -------------------------
        # Present results - interactive layout
        # -------------------------
        st.success(f"Top {len(results)} matches found")
        main_col, side_col = st.columns([3,1])

        # LEFT: list of match cards
        with main_col:
            for i, r in enumerate(results, start=1):
                score = r.get("score")
                title = f"{i}. {r['career']}" if r.get("career") else f"{i}. (Unnamed)"
                st.markdown(f"#### {title}")
                if show_scores and score is not None:
                    st.progress(min(max(score, 0)/100.0, 1.0))
                    st.write(f"Match score: **{score:.1f}**")
                # condensed summary or deep-dive
                if detail_mode == "Short summary":
                    st.write(r.get("description") or r.get("deep_text") or "No description available.")
                else:
                    # If generate_deep_advice produced text, show it inside expander
                    content = r.get("deep_text") or (
                        f"**About:** {r.get('description','')}\n\n**Roadmap:** {r.get('roadmap','')}"
                    )
                    with st.expander("Show deep-dive guidance"):
                        st.markdown(content)
                # CTA: Save to personal plan
                if st.button(f"Save '{r['career']}' to plan", key=f"save_{i}"):
                    st.success(f"Saved {r['career']} to your plan (locally).")
                st.markdown("---")

        # RIGHT: details and download
        with side_col:
            st.markdown("### 📥 Export & Extras")
            payload = {"user_input": skills_input, "timestamp": datetime.utcnow().isoformat(), "results": results}
            json_bytes = json.dumps(payload, indent=2).encode("utf-8")
            st.download_button("Download JSON", data=json_bytes, file_name="career_recs.json", mime="application/json")
            # CSV conversion
            df_export = pd.DataFrame(results)
            csv_buf = df_export.to_csv(index=False).encode("utf-8")
            st.download_button("Download CSV", data=csv_buf, file_name="career_recs.csv", mime="text/csv")
            st.markdown("---")
            st.markdown("### ⚡ Quick tips")
            st.write("- Try short tokens like `ml` or `devops` and also longer phrases like `natural language processing`.")
            st.write("- Use the slider to increase top matches. ")

        st.balloons()

