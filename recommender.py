import pandas as pd

# Load dataset
df = pd.read_csv("career_data.csv")

# Simple recommender function
def recommend_career(skill):
    # Filter rows where "Skills" column contains the user skill
    matches = df[df["skills"].str.contains(skill, case=False, na=False)]
    
    if matches.empty:
        return f"Sorry, no career found for skill: {skill}"
    else:
        careers = matches["career"].unique()
        return f"Based on your skill '{skill}', you can explore: {', '.join(careers)}"

# ---- Test the recommender ----
if __name__ == "__main__":
    user_skill = input("Enter a skill you have: ")
    print(recommend_career(user_skill))