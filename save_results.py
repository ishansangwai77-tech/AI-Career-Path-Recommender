# save_results.py
import json
import os
from datetime import datetime
from recommender_v3 import recommend_careers

def save_recs_to_json(user_skills_text, recs, out_dir="results", prefix="recs"):
    """
    Saves recs (list of dicts) to a timestamped JSON file under out_dir.
    Returns the path to the saved file.
    """
    os.makedirs(out_dir, exist_ok=True) # create folder if missing
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S") # e.g. 20250925_143501
    filename = f"{prefix}_{timestamp}.json"
    path = os.path.join(out_dir, filename)

    data = {
        "timestamp": timestamp,
        "user_input": user_skills_text,
        "recommendations": recs
    }

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return path

if __name__ == "__main__":
    user = "python, sql, ml" # replace or prompt input() here
    recs = recommend_careers(user, top_k=10)
    saved_path = save_recs_to_json(user, recs)
    print(f"Saved recommendations to: {saved_path}")