# 🎓 AI Career Path Recommender

A modern, ML-powered web application that recommends personalized career paths based on your skills and interests using semantic similarity and machine learning.

## 🌟 Features

- **Modern Login System** - Secure authentication with an attractive, responsive UI
- **ML-Based Recommendations** - Uses TF-IDF vectorization and cosine similarity for accurate matches
- **Deep-Dive Guidance** - Structured, step-by-step learning roadmaps for each recommended career
- **Responsive Design** - Beautiful Streamlit UI with gradient backgrounds and intuitive controls
- **Multiple Export Formats** - Download recommendations as JSON or CSV
- **Real-Time Processing** - Instant career recommendations based on your input
- **Tech Stack Awareness** - Recommends careers for popular tech stacks (Python, JavaScript, AWS, etc.)

## 🛠️ How It Works

1. **Login** - Authenticate using the login form
2. **Enter Skills** - Type your skills or use the example buttons
3. **Get Recommendations** - Click the "Get Recommendations" button
4. **View Results** - See top matching careers with detailed roadmaps
5. **Export** - Download results as JSON or CSV

### ML Recommender Algorithm

- **Input Processing**: Normalizes and expands skill synonyms
- **Vectorization**: Converts skills and career descriptions to TF-IDF vectors
- **Similarity Scoring**: Uses cosine similarity to rank careers
- **Output Generation**: Produces structured learning paths and project suggestions

## 🎨 UI/UX Highlights

- **Gradient Card Design** - Modern, attractive login page
- **Sidebar Controls** - Easy access to recommendation options
- **Example Buttons** - Quick-start with pre-filled tech stacks
- **Expandable Details** - Deep-dive guidance in interactive expanders
- **Progress Indicators** - Visual match score representations

## 📊 Career Dataset

The `data/careers.csv` includes 47+ career paths with:
- Required skills
- Job description
- Learning roadmap
- Starter projects
- Resume keywords
- Industry domain

## 📦 Dependencies

- **streamlit** - Web framework
- **pandas** - Data processing
- **scikit-learn** - ML algorithms (TF-IDF, cosine similarity)
- **sentence-transformers** - Semantic embeddings (for future enhancements)
- **torch** - Deep learning backend

See `requirements.txt` for full dependency list.

## 📝 License

This project is open source and available under the MIT License.


**GAME is GAME❤️**
