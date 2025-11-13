
# app.py (Enhanced Streamlit UI)
import streamlit as st
import pandas as pd
import json
from datetime import datetime
from io import StringIO, BytesIO

st.set_page_config(page_title="AI Career Path Recommender", page_icon="🎓", layout="wide")

# No login required - direct access for portfolio demo

# --- Import ML recommender ---
USE_NEW_API = False
try:
    from data.recommender_ml import recommend, generate_deep_advice, load_data as load_data_fn, train_vectorizer
    USE_NEW_API = True
except Exception as e:
    st.error("Could not import recommender functions from data/recommender_ml.py. Check file and function names.")
    raise

# --- Page config + header ---
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

