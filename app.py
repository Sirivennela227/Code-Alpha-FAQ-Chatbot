import os
import json
import math
import string
from collections import Counter
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# ── Load FAQ Knowledge Base ──────────────────────────────────────────────────
DATA_FILE = os.path.join(os.path.dirname(__file__), 'data', 'faqs.json')

def load_faqs():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

FAQS = load_faqs()

# ── Stop Words ───────────────────────────────────────────────────────────────
STOP_WORDS = {
    "a","an","the","is","are","was","were","be","been","being",
    "have","has","had","do","does","did","to","at","by","for",
    "with","about","against","between","into","through","during",
    "before","after","above","below","from","up","down","in","out",
    "on","off","over","under","again","then","once","here","there",
    "when","where","why","how","all","any","both","each","few",
    "more","most","other","some","such","no","nor","not","only",
    "same","so","than","too","very","can","will","just","should",
    "now","i","me","my","we","our","you","your","tell","please",
    "want","know","what","get","give","let","make","need","see",
    "find","use","go","look","take"
}

# ── Synonym Map ───────────────────────────────────────────────────────────────
SYNONYMS = {
    # timings
    "timing":"timings","time":"timings","hours":"timings",
    "schedule":"timings","open":"timings","start":"timings",
    "begin":"timings","ends":"timings","end":"timings",
    # courses
    "course":"courses","class":"courses","classes":"courses",
    "program":"courses","programs":"courses","subject":"courses",
    "subjects":"courses","learning":"courses","study":"courses",
    # support / contact
    "contact":"support","reach":"support","helpline":"support",
    "call":"support","email":"support","message":"support",
    "help":"support","assist":"support","assistance":"support",
    # registration
    "register":"register","registration":"register",
    "signup":"register","sign":"register","apply":"register",
    "join":"register","enroll":"register","enrollment":"register",
    "admission":"register",
    # certificate
    "cert":"certificate","certification":"certificate",
    "degree":"certificate","certified":"certificate",
    # duration
    "duration":"duration","length":"duration","period":"duration",
    "long":"duration","weeks":"duration","months":"duration",
    # online
    "remote":"online","virtual":"online","offline":"online",
    # benefits
    "perks":"benefits","perk":"benefits","benefit":"benefits",
    "advantage":"benefits","advantages":"benefits","gain":"benefits",
    # skills
    "skill":"skills","requirement":"skills","prerequisite":"skills",
    "prerequisites":"skills","qualification":"skills",
    # submit / project
    "submit":"submit","submission":"submit","upload":"submit",
    "send":"submit","submitting":"submit",
    "project":"project","projects":"project","task":"project",
    "assignment":"project","assignments":"project",
    # documents
    "document":"documents","proof":"documents","papers":"documents",
    "id":"documents","identity":"documents",
    # internship
    "intern":"internship","internships":"internship",
    "training":"internship","programme":"internship",
    # ignore-noise words
    "weather":"__IGNORE__","today":"__IGNORE__",
    "tomorrow":"__IGNORE__","yesterday":"__IGNORE__",
    "news":"__IGNORE__","random":"__IGNORE__",
}

# ── Text Normalisation ────────────────────────────────────────────────────────
def clean(text: str) -> list[str]:
    """Lowercase → strip punctuation → synonym map → remove stop words."""
    text = text.lower().strip().translate(str.maketrans("", "", string.punctuation))
    tokens = []
    for tok in text.split():
        mapped = SYNONYMS.get(tok, tok)
        if mapped == "__IGNORE__":
            continue
        if mapped not in STOP_WORDS:
            tokens.append(mapped)
    # if everything was filtered, fall back to raw non-stop tokens
    if not tokens:
        tokens = [t for t in text.split() if t not in STOP_WORDS] or text.split()
    return tokens

# ── Pure-Python TF-IDF + Cosine Similarity ───────────────────────────────────
def _tf(tokens: list[str]) -> dict[str, float]:
    c = Counter(tokens)
    total = len(tokens) or 1
    return {w: cnt / total for w, cnt in c.items()}

def _build_idf(corpus: list[list[str]]) -> dict[str, float]:
    N = len(corpus)
    df: dict[str, int] = {}
    for doc in corpus:
        for w in set(doc):
            df[w] = df.get(w, 0) + 1
    return {w: math.log((N + 1) / (freq + 1)) + 1 for w, freq in df.items()}

def _tfidf_vec(tokens: list[str], idf: dict[str, float]) -> dict[str, float]:
    tf = _tf(tokens)
    return {w: tf[w] * idf.get(w, 1.0) for w in tf}

def _cosine(a: dict[str, float], b: dict[str, float]) -> float:
    common = set(a) & set(b)
    if not common:
        return 0.0
    dot = sum(a[w] * b[w] for w in common)
    mag_a = math.sqrt(sum(v * v for v in a.values()))
    mag_b = math.sqrt(sum(v * v for v in b.values()))
    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / (mag_a * mag_b)

# Pre-build corpus at startup
_corpus_tokens  = [clean(faq["question"]) for faq in FAQS]
_idf            = _build_idf(_corpus_tokens)
_corpus_vecs    = [_tfidf_vec(toks, _idf) for toks in _corpus_tokens]

def find_best_match(user_query: str):
    q_tokens = clean(user_query)
    q_vec    = _tfidf_vec(q_tokens, _idf)

    best_idx, best_score = 0, 0.0
    for idx, faq_vec in enumerate(_corpus_vecs):
        score = _cosine(q_vec, faq_vec)
        if score > best_score:
            best_score, best_idx = score, idx
    return best_idx, round(best_score, 3)

THRESHOLD = 0.25   # minimum cosine similarity to count as a match

# ── API Routes ────────────────────────────────────────────────────────────────
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/faqs', methods=['GET'])
def get_faqs():
    return jsonify(FAQS)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({"error": "Invalid payload. 'message' field is required."}), 400

    user_msg = data['message'].strip()
    if not user_msg:
        return jsonify({
            "answer": "Please type a valid question so I can assist you!",
            "matched_question": None,
            "confidence": 0.0
        })

    if not FAQS:
        return jsonify({
            "answer": "FAQ database is currently empty. Please check back later.",
            "matched_question": None,
            "confidence": 0.0
        })

    best_idx, confidence = find_best_match(user_msg)

    if confidence >= THRESHOLD:
        matched = FAQS[best_idx]
        return jsonify({
            "answer":           matched["answer"],
            "matched_question": matched["question"],
            "confidence":       confidence
        })
    else:
        return jsonify({
            "answer": "Sorry, I couldn't find an answer to that question. "
                      "Please try asking in a different way.",
            "matched_question": None,
            "confidence":       confidence
        })

# ── Entry Point ───────────────────────────────────────────────────────────────
if __name__ == '__main__':
    print(f"\n{'='*55}")
    print("  CodeAlpha FAQ Chatbot — Task 2")
    print(f"  Loaded {len(FAQS)} FAQs  |  NLP: Pure-Python TF-IDF")
    print(f"  URL: http://127.0.0.1:5000/")
    print(f"{'='*55}\n")
    app.run(host='127.0.0.1', port=5000, debug=True)
