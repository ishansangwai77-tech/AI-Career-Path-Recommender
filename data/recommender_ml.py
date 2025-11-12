# recommender_ml.py

import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import html
import textwrap
# Sentence Embeddings
from sentence_transformers import SentenceTransformer
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')  # Change to your downloaded model name if different

DATA_PATH = "data/careers.csv"

# --- Helpers: normalization and synonyms ---
SYNONYMS = {
    "ml": "machine learning",
    "ai": "artificial intelligence",
    "nlp": "natural language processing",
    "cv": "computer vision",
    "db": "database",
    "js": "javascript",
    "ds": "data science",
    "etl": "extract transform load",
    "ci/cd": "continuous integration continuous delivery",
    "devops": "devops"
}

def normalize_text(s: str) -> str:
    if not isinstance(s, str):
        return ""
    s = s.lower()
    s = re.sub(r"[\(\)\[\]\-\/]", " ", s) # remove punctuation chars that split tokens
    s = re.sub(r"[,;]+", ",", s) # unify separators
    s = re.sub(r"\s+", " ", s).strip()
    # expand synonyms tokens in-line: replace tokens with full forms
    tokens = []
    for token in re.split(r"[,\s]+", s):
        tok = token.strip()
        if tok in SYNONYMS:
            tokens.append(SYNONYMS[tok])
        tokens.append(tok)
    return " ".join(dict.fromkeys(tokens)) # dedupe keeping order

# --- Load dataset ---
def load_data(path=DATA_PATH):
    import os
    print("Loading from:", os.path.abspath(path))
    df = pd.read_csv(path)
    # ensure all needed fields exist
    for c in ["career","skills","description","learning_path","projects","resources","resume_keywords","domain"]:
        if c not in df.columns:
            df[c] = ""
    # create a combined text field for vectorization
    df["skills_norm"] = df["skills"].fillna("").apply(normalize_text)
    df["text_blob"] = (df["career"].fillna("") + " " + df["skills_norm"] + " " + df["description"].fillna("")).str.strip()
    return df

# --- Train vectorizer ---
def train_vectorizer(df):
    vectorizer = TfidfVectorizer(ngram_range=(1,2), max_features=6000)
    tfidf = vectorizer.fit_transform(df["text_blob"].fillna(""))
    return vectorizer, tfidf

# --- Recommend function ---
def recommend(user_input: str, df, vectorizer, tfidf_matrix, top_k=5):
    u = normalize_text(user_input)
    u_vec = vectorizer.transform([u])
    sims = cosine_similarity(u_vec, tfidf_matrix).flatten()
    idxs = sims.argsort()[-top_k:][::-1]
    results = []
    for idx in idxs:
        score = float(sims[idx]) * 100.0
        row = df.iloc[idx].to_dict()
        # compute matched tokens (simple method)
        matched = []
        for token in set(re.split(r"[,\s]+", u)):
            token = token.strip()
            if token and token in row["skills_norm"]:
                matched.append(token)
        results.append({
            "career": row.get("career",""),
            "domain": row.get("domain",""),
            "score": round(score,1),
            "matched_skills": matched,
            "description": row.get("description",""),
            "learning_path": row.get("learning_path",""),
            "projects": row.get("projects",""),
            "resources": row.get("resources",""),
            "resume_keywords": row.get("resume_keywords","")
        })
    return results

# --- Generate deep-dive paragraph advice ---
def generate_deep_advice(user_input: str, rec):
    """
    Rec is a dict returned by recommend(...). Build a multi-part paragraph:
    - short verdict
    - why it fits
    - detailed step-by-step plan (split learning_path into bullets)
    - suggested projects (from dataset or generic)
    - resume bullets & next roles
    - confidence note
    """
    career = rec["career"]
    score = rec["score"]
    matched = rec["matched_skills"]
    desc = rec["description"]
    lp = rec["learning_path"]
    projects = rec["projects"]
    resources = rec["resources"]
    resume_kw = rec["resume_keywords"]

    # Build text
    # Structured, readable output
    output = f"""
## Recommendation for {career}

**Summary:** Based on your input (*{user_input}*), the role **{career}** is a strong match ({score}% similarity).

**About the role:** {desc if desc else 'No description available.'}

**Why this fits you:** {'You already have keywords matching this career: ' + ', '.join(matched) + '. These skills are directly used in day-to-day work for this role.' if matched else 'While no exact keywords matched, the profile aligns semantically with this career according to skill and description similarity.'}

**Step-by-step learning path:**
{chr(10).join(['- ' + s.strip() for s in re.split(r';', lp) if s.strip()]) if lp and str(lp).strip() else '- Start with fundamentals in programming and domain topics, then build small projects and iterate.'}

**Recommended starter projects:**
{chr(10).join(['- ' + p.strip() for p in re.split(r';', str(projects)) if p.strip()][:3]) if projects and str(projects).strip() else '- Build 2-3 small projects that highlight core skills and deployment.'}

**Resources to learn from:** {', '.join([r.strip() for r in re.split(r';', str(resources)) if r.strip()][:3]) if resources and str(resources).strip() else 'Online courses and documentation for core libraries and tools.'}

**Resume keywords & entry titles:** {resume_kw if resume_kw and str(resume_kw).strip() else 'N/A'}
**Next roles you can aim for:** Junior {career}, Internship, Associate {career}
**Confidence:** This recommendation scores {score}% by content similarity. Combine with practical projects to improve chances.
"""
    return output

# --- CLI quick-run ---
def cli():
    print("Loading dataset and vectorizer (may take a few seconds)...")
    df = load_data()
    vectorizer, tfidf = train_vectorizer(df)
    while True:
        user = input("\nEnter skills/interests (or 'quit'): ").strip()
        if not user or user.lower() in ("q","quit","exit"):
            break
        recs = recommend(user, df, vectorizer, tfidf, top_k=5)
        print("\nTop 5 detailed recommendations:\n")
        for r in recs:
            text = generate_deep_advice(user, r)
            print("="*80)
            print(textwrap.fill(text, 100))
            print("\n")

if __name__ == "__main__":
    cli()

