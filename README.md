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

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip or conda

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/AI-Career-Path-Recommender.git
cd AI-Career-Path-Recommender
```

2. **Create a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

### Running Locally

```bash
streamlit run app.py
```

Then open your browser to `http://localhost:8501`

## 🔐 Default Credentials

**Username:** `user`  
**Password:** `pass`

> ⚠️ Change these in production!

## 📁 Project Structure

```
AI-Career-Path-Recommender/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── .gitignore                 # Git ignore rules
├── README.md                  # This file
├── career_data.csv            # Career dataset (classic recommender)
├── data/
│   ├── careers.csv            # Extended career dataset (ML recommender)
│   └── recommender_ml.py      # ML-based recommender logic
├── recommender_v3.py          # Classic rule-based recommender
└── results/                   # Output folder for saved recommendations
```

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

## 🔧 Configuration

### Change Login Credentials

Edit `app.py` (lines ~55-60):

```python
if username == "user" and password == "pass":
    # Change "user" and "pass" to your desired credentials
```

### Add More Careers

Edit `data/careers.csv` and add new rows with:
- Career name
- Skills (comma/semicolon-separated)
- Description
- Learning path
- Projects
- Resources
- Resume keywords
- Domain

## 🚢 Deployment

### Deploy on Streamlit Cloud

1. Push your code to GitHub
2. Visit [Streamlit Cloud](https://streamlit.io/cloud)
3. Click "New app" and select your repository
4. Set main file to `app.py`
5. Click "Deploy"

### Deploy on Your Own Server

```bash
# Install Streamlit
pip install streamlit

# Run the app
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

## 📦 Dependencies

- **streamlit** - Web framework
- **pandas** - Data processing
- **scikit-learn** - ML algorithms (TF-IDF, cosine similarity)
- **sentence-transformers** - Semantic embeddings (for future enhancements)
- **torch** - Deep learning backend

See `requirements.txt` for full dependency list.

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'data.recommender_ml'"
- Ensure `data/` folder and `recommender_ml.py` are in the repository root
- Check that your import path matches the file structure

### Login page takes time to redirect
- This is normal on first load; subsequent loads are faster
- Clear browser cache if redirects are stuck

### Images not loading
- Check your internet connection
- External image URLs may be temporarily unavailable
- Use local images as fallback

## 🎯 Future Enhancements

- [ ] User authentication with database (PostgreSQL)
- [ ] Save user preferences and history
- [ ] Advanced filtering by salary, location, and industry
- [ ] Integration with job boards (LinkedIn, Indeed)
- [ ] Skill gap analysis
- [ ] Resume builder
- [ ] Multi-language support

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📧 Contact

For questions or feedback, reach out at: [your-email@example.com]

---

**Made with ❤️ by Your Name**
