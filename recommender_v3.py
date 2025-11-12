# recommender_v3.py
"""
Robust skill-based career recommender.
Requires 'career_data.csv' in project root with columns starting 'skill' and 'career'.
"""

import pandas as pd
import re
from typing import List, Dict

def find_col(df: pd.DataFrame, key: str) -> str:
	for c in df.columns:
		if c.strip().lower().startswith(key.lower()):
			return c
	raise KeyError(f"No column starting with '{key}' found. Columns: {df.columns.tolist()}")

def normalize_skill_text(text: str) -> List[str]:
	parts = re.split(r'[;,/|]+', str(text))
	return [p.strip().lower() for p in parts if p.strip()]

# Load dataset
df = pd.read_csv("career_data.csv")
skills_col = find_col(df, "skill")
career_col = find_col(df, "career")

# Precompute normalized skill sets
df["_skill_set"] = df[skills_col].fillna("").apply(lambda s: set(normalize_skill_text(s)))

def recommend_careers(user_skills_text: str, top_k: int = 5) -> List[Dict]:
	user_skills = set(normalize_skill_text(user_skills_text))
	if not user_skills:
		return []

	results = []
	for _, row in df.iterrows():
		career = row[career_col]
		career_skills = row["_skill_set"]
		match = user_skills.intersection(career_skills)
		match_count = len(match)
		if match_count == 0:
			continue

		career_req_count = max(len(career_skills), 1)
		user_skill_count = max(len(user_skills), 1)

		ratio_req = match_count / career_req_count
		ratio_user = match_count / user_skill_count

		combined = 0.6 * ratio_req + 0.4 * ratio_user
		score_pct = round(combined * 100, 1)

		results.append({
			"career": career,
			"score_pct": score_pct,
			"match_count": match_count,
			"matched_skills": sorted(match),
			"career_skill_count": career_req_count
		})

	results = sorted(results, key=lambda r: (r["score_pct"], r["match_count"]), reverse=True)
	return results[:top_k]

if __name__ == "__main__":
	s = input("Enter your skills (comma or semicolon separated): ").strip()
	recs = recommend_careers(s, top_k=10)
	if not recs:
		print("No matching careers found. Try different keywords (e.g., 'python', 'sql', 'ml').")
	else:
		print("\nTop recommendations:")
		for r in recs:
			print(f"- {r['career']}  ({r['score_pct']}%)  matched: {r['matched_skills']}")
