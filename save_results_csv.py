# save_results_csv.py
import os
import pandas as pd
from datetime import datetime
from recommender_v3 import recommend_careers

def save_recs_to_csv(user_skills_text, recs, out_dir="results", prefix="recs"):
    os.makedirs(out_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{prefix}_{timestamp}.csv"
    path = os.path.join(out_dir, filename)

    # Convert list of dicts to DataFrame
    df = pd.DataFrame(recs)
    # Add user input + timestamp columns to each row for traceability
    df["user_input"] = user_skills_text
    df["saved_at"] = timestamp

    df.to_csv(path, index=False)
    return path

if __name__ == "__main__":
    user = "python, sql, ml"
    recs = recommend_careers(user, top_k=10)
    saved = save_recs_to_csv(user, recs)
    print(f"Saved CSV to: {saved}")