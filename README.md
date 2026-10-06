# 🤖 CodeAlpha AI Internship – Task 2: FAQ Chatbot

A simple, fast, and intelligent AI-powered FAQ Chatbot built for **CodeAlpha AI Internship (Task 2)** using Python, Flask, HTML5/CSS3/JavaScript, and Natural Language Processing (NLP) with TF-IDF and Cosine Similarity.

---

## 📌 Project Overview

This chatbot answers frequently asked questions (FAQs) about college timings, courses, admissions, certificates, and internship procedures using text normalization, intent matching, and similarity scoring. It operates entirely offline without needing paid API keys or external cloud dependencies.

---

## ✨ Features

- **Interactive Glassmorphic UI**: Sleek dark slate glassmorphism design with responsive message bubbles.
- **Natural Language Intent Matching**: Uses **TF-IDF (Term Frequency-Inverse Document Frequency)** and **Cosine Similarity** to match non-exact queries.
- **Robust Fallback Engine**: Built-in Jaccard & overlap matching if scikit-learn is not installed.
- **Structured Knowledge Base**: 15+ curated FAQs stored in an easily editable `data/faqs.json` file.
- **Interactive Quick Chips**: One-click sample query buttons for instant testing.
- **Typing & Loading Animation**: Realistic visual feedback for bot responses.
- **Clear Chat Option**: Reset conversation history with a single click.
- **Mobile & Desktop Responsive**: Looks great on screens of any size.

---

## 🛠️ Tech Stack

- **Backend**: Python 3.11+, Flask Web Framework
- **Frontend**: HTML5, Vanilla CSS3 (Glassmorphic dark design), JavaScript (ES6+ Fetch API)
- **NLP Engine**: `scikit-learn` (`TfidfVectorizer`, `cosine_similarity`), custom text normalization

---

## 🧠 NLP & Intent Matching Approach

```
[User Input] 
     │
     ▼
[Text Normalization] ➔ Lowercasing, punctuation stripping, synonym mapping, stop-word removal
     │
     ▼
[TF-IDF Vectorization] ➔ Converts text corpus & user query into TF-IDF n-gram feature vectors
     │
     ▼
[Cosine Similarity] ➔ Computes similarity score between user query & vector space of FAQs
     │
     ▼
[Threshold Decision] 
     ├── Confidence ≥ 0.22 ➔ Return Best Matching Answer + Matched Tag
     └── Confidence < 0.22 ➔ Return Default Fallback Message
```

---

## 📁 Project Structure

```text
CodeAlpha-FAQ-Chatbot/
│
├── app.py              # Flask application & NLP intent matching backend
├── requirements.txt    # Python dependencies
├── README.md           # Documentation
├── .gitignore          # Git exclusion patterns
├── templates/
│   └── index.html      # Glassmorphic chat interface HTML
├── static/
│   ├── style.css       # UI Styling & animations
│   └── script.js       # Client AJAX fetch & DOM manipulation
└── data/
    └── faqs.json       # FAQ Knowledge Base JSON (15+ Q&A pairs)
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher installed on your system.

### Step 1: Clone the Repository
```bash
git clone https://github.com/your-username/CodeAlpha-FAQ-Chatbot.git
cd CodeAlpha-FAQ-Chatbot
```

### Step 2: Create a Virtual Environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 💻 How to Run in VS Code

1. Open the project folder `CodeAlpha-FAQ-Chatbot` in VS Code (`File > Open Folder...`).
2. Open the terminal in VS Code (`Ctrl + ~` or `Terminal > New Terminal`).
3. Ensure your virtual environment is active.
4. Start the Flask server:
   ```bash
   python app.py
   ```
5. Open your web browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```

---

## 🧪 Example Test Questions

Try asking the chatbot using different phrasing:

| Target Topic | Prepared FAQ Question | Example User Queries to Test |
| :--- | :--- | :--- |
| **College Timings** | *What are the college timings?* | "When does college start?", "What are the hours?", "Timing of college?" |
| **Available Courses** | *What courses are available?* | "What can I learn?", "Which classes are offered?", "Course list" |
| **Registration** | *How can I register?* | "How to sign up?", "Where can I apply?", "Registration process" |
| **Internship Benefits**| *What are the internship benefits?*| "What perks do I get?", "Why join this internship?", "Internship advantages" |
| **Certificates** | *What is the certificate process?* | "When will I get my cert?", "Do I get a certificate?", "Certification info" |
| **Unknown Query** | *N/A* | "What is the weather today in Tokyo?" *(Triggers fallback response)* |

---

## 📸 Screenshots

*(Add screenshots of your running chatbot application here before submitting your project)*

- **Chat Interface**: Clear message bubbles with typing indicator.
- **Match Notification**: Shows confidence tag on matched questions.

---

## 🔮 Future Enhancements

- **Voice Input / Speech-to-Text**: Allow users to speak questions using Web Speech API.
- **Multi-language Support**: Translate questions and responses dynamically.
- **Admin Panel**: Web UI to add, edit, or delete FAQ entries without modifying JSON.
- **Analytics Dashboard**: Track frequently asked unmatched questions to expand knowledge base.

---

## 📜 License & Acknowledgements

Created as part of **CodeAlpha AI Internship - Task 2**.  
Designed & Developed with ❤️ for AI learning.
