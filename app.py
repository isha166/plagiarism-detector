import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Plagiarism Detector", layout="wide")

# ---------------- UI (FONTS + NEUMORPHISM) ----------------
st.markdown("""
<style>

/* Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&family=Playfair+Display:wght@500;600;700&display=swap');

/* Background */
body {
    background-color: #0d0d0d;
}

.main {
    background-color: #0d0d0d;
    color: white;
    font-family: 'Poppins', sans-serif;
}

/* Headings */
h1 {
    font-family: 'Playfair Display', serif;
    font-size: 48px;
    font-weight: 700;
    color: #f5f5dc;
}

h2, h3 {
    font-family: 'Playfair Display', serif;
    color: #f5f5dc;
}

/* Neumorphic Cards */
.neu-card {
    background: #111;
    border-radius: 25px;
    padding: 20px;
    box-shadow: 
        8px 8px 15px #000,
        -8px -8px 15px #1a1a1a;
    margin-bottom: 20px;
}

/* Textarea (Document Input) */
textarea {
    background: #e8e0d4 !important;
    color: black !important;
    border-radius: 20px !important;
    padding: 15px !important;
    box-shadow: 
        inset 6px 6px 10px rgba(0,0,0,0.2),
        inset -6px -6px 10px rgba(255,255,255,0.5);
    border: none !important;
}

/* Button */
.stButton>button {
    background: #111;
    color: #f5f5dc;
    border-radius: 15px;
    padding: 10px 20px;
    font-weight: 500;
    box-shadow: 
        5px 5px 10px #000,
        -5px -5px 10px #1a1a1a;
}

.stButton>button:hover {
    box-shadow: 
        inset 5px 5px 10px #000,
        inset -5px -5px 10px #1a1a1a;
}

/* Highlight */
.highlight {
    background-color: #facc15;
    color: black;
    padding: 2px 6px;
    border-radius: 5px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.markdown("<h1>🖤 Smart Plagiarism Detector</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#d4d4d4;'>Analyze documents with intelligent insights and clean visualization.</p>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------- INPUT SECTION ----------------
col1, col2 = st.columns(2)

with col1:
    st.markdown("<div class='neu-card'>", unsafe_allow_html=True)
    text1 = st.text_area("📄 Document 1", height=250)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='neu-card'>", unsafe_allow_html=True)
    text2 = st.text_area("📄 Document 2", height=250)
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- FUNCTIONS ----------------
def clean_words(text):
    return re.findall(r'\w+', text.lower())

def similarity(doc1, doc2):
    tfidf = TfidfVectorizer()
    vec = tfidf.fit_transform([doc1, doc2])
    return cosine_similarity(vec[0], vec[1])[0][0] * 100

def get_stats(text):
    words = clean_words(text)
    sentences = re.split(r'[.!?]+', text)

    word_count = len(words)
    unique_words = len(set(words))
    avg_sentence = word_count / len(sentences) if len(sentences) > 0 else 0
    richness = unique_words / word_count if word_count > 0 else 0

    return word_count, unique_words, avg_sentence, richness

def common_words(t1, t2):
    return list(set(clean_words(t1)).intersection(set(clean_words(t2))))[:10]

def highlight(t1, t2):
    common = set(clean_words(t1)).intersection(set(clean_words(t2)))

    def mark(text):
        result = []
        for word in text.split():
            clean = re.sub(r'\W+', '', word.lower())
            if clean in common:
                result.append(f"<span class='highlight'>{word}</span>")
            else:
                result.append(word)
        return " ".join(result)

    return mark(t1), mark(t2)

def verdict(score):
    if score < 30:
        return "🟢 Low Plagiarism"
    elif score < 70:
        return "🟡 Moderate Plagiarism"
    else:
        return "🔴 High Plagiarism"

# ---------------- ANALYZE BUTTON ----------------
st.markdown("<br>", unsafe_allow_html=True)

if st.button("🔍 Analyze"):

    if not text1.strip() or not text2.strip():
        st.warning("Please enter both documents.")
    else:
        sim = similarity(text1, text2)

        # ---------------- SCORE ----------------
        st.markdown("<div class='neu-card'>", unsafe_allow_html=True)
        st.subheader("📊 Plagiarism Result")
        st.write(f"### 🔴 Plagiarism Detected: {sim:.2f}%")
        st.progress(sim / 100)
        st.write(verdict(sim))
        st.markdown("</div>", unsafe_allow_html=True)

        # ---------------- STATS ----------------
        st.subheader("📈 Document Insights")

        w1, u1, s1, r1 = get_stats(text1)
        w2, u2, s2, r2 = get_stats(text2)

        col3, col4 = st.columns(2)

        with col3:
            st.markdown("<div class='neu-card'>", unsafe_allow_html=True)
            st.write("**Document 1**")
            st.write(f"Words: {w1}")
            st.write(f"Unique Words: {u1}")
            st.write(f"Avg Sentence Length: {s1:.2f}")
            st.write(f"Vocabulary Richness: {r1:.2f}")
            st.markdown("</div>", unsafe_allow_html=True)

        with col4:
            st.markdown("<div class='neu-card'>", unsafe_allow_html=True)
            st.write("**Document 2**")
            st.write(f"Words: {w2}")
            st.write(f"Unique Words: {u2}")
            st.write(f"Avg Sentence Length: {s2:.2f}")
            st.write(f"Vocabulary Richness: {r2:.2f}")
            st.markdown("</div>", unsafe_allow_html=True)

        # ---------------- COMMON WORDS ----------------
        st.markdown("<div class='neu-card'>", unsafe_allow_html=True)
        st.subheader("🔎 Common Words")
        st.write(common_words(text1, text2))
        st.markdown("</div>", unsafe_allow_html=True)

        # ---------------- HIGHLIGHT ----------------
        h1, h2 = highlight(text1, text2)

        st.subheader("📌 Highlighted Matches")

        col5, col6 = st.columns(2)

        with col5:
            st.markdown("<div class='neu-card'>", unsafe_allow_html=True)
            st.markdown(h1, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col6:
            st.markdown("<div class='neu-card'>", unsafe_allow_html=True)
            st.markdown(h2, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
