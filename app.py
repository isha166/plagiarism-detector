import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Plagiarism Detector", layout="wide")

# ---------------- DARK + BEIGE 3D UI ----------------
st.markdown("""
<style>
body {
    background-color: #000000;
}

.main {
    background-color: #000000;
    color: white;
}

/* Titles */
h1, h2, h3 {
    color: #f5f5dc;
}

/* 3D Document Boxes */
textarea {
    background-color: #f5f5dc !important;
    color: black !important;
    border-radius: 15px !important;
    box-shadow: 8px 8px 20px rgba(255,255,255,0.1),
                -8px -8px 20px rgba(0,0,0,0.8);
    padding: 10px;
}

/* Cards */
.card {
    background-color: #111;
    padding: 20px;
    border-radius: 20px;
    box-shadow: 0px 10px 30px rgba(255,255,255,0.1);
    margin-bottom: 20px;
}

/* Button */
.stButton>button {
    background: linear-gradient(135deg, #d4af37, #f5deb3);
    color: black;
    border-radius: 12px;
    padding: 10px 20px;
    font-weight: bold;
}

/* Highlight */
.highlight {
    background-color: #facc15;
    color: black;
    padding: 2px 6px;
    border-radius: 5px;
}

/* Score text */
.score {
    font-size: 32px;
    font-weight: bold;
    color: #facc15;
}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.title("🖤 Advanced Plagiarism Detector")
st.write("Deep analysis of document similarity with multiple metrics.")

# ---------------- INPUT ----------------
col1, col2 = st.columns(2)

with col1:
    text1 = st.text_area("📄 Document 1", height=250)

with col2:
    text2 = st.text_area("📄 Document 2", height=250)

# ---------------- FUNCTIONS ----------------

# TF-IDF similarity
def tfidf_similarity(doc1, doc2):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([doc1, doc2])
    return cosine_similarity(vectors[0], vectors[1])[0][0] * 100

# Jaccard similarity
def jaccard_similarity(doc1, doc2):
    words1 = set(re.findall(r'\w+', doc1.lower()))
    words2 = set(re.findall(r'\w+', doc2.lower()))
    intersection = len(words1 & words2)
    union = len(words1 | words2)
    return (intersection / union) * 100 if union != 0 else 0

# Cosine similarity (word count)
def simple_cosine(doc1, doc2):
    words1 = doc1.split()
    words2 = doc2.split()
    all_words = list(set(words1 + words2))

    vec1 = [words1.count(w) for w in all_words]
    vec2 = [words2.count(w) for w in all_words]

    dot = sum(a*b for a,b in zip(vec1, vec2))
    mag1 = sum(a*a for a in vec1) ** 0.5
    mag2 = sum(b*b for b in vec2) ** 0.5

    return (dot/(mag1*mag2))*100 if mag1 and mag2 else 0

# Highlight
def highlight(text1, text2):
    words1 = re.findall(r'\w+', text1.lower())
    words2 = re.findall(r'\w+', text2.lower())
    common = set(words1).intersection(set(words2))

    def mark(text):
        result = []
        for word in text.split():
            clean = re.sub(r'\W+', '', word.lower())
            if clean in common:
                result.append(f"<span class='highlight'>{word}</span>")
            else:
                result.append(word)
        return " ".join(result)

    return mark(text1), mark(text2)

# ---------------- ANALYZE ----------------
if st.button("🔍 Analyze Similarity"):

    if not text1.strip() or not text2.strip():
        st.warning("Please enter both documents.")
    else:
        tfidf = tfidf_similarity(text1, text2)
        jaccard = jaccard_similarity(text1, text2)
        cosine = simple_cosine(text1, text2)

        # ---------------- SCORES ----------------
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("📊 Multi-Metric Analysis")

        st.markdown(f"<div class='score'>TF-IDF Similarity: {tfidf:.2f}%</div>", unsafe_allow_html=True)
        st.progress(tfidf/100)

        st.write(f"🔹 Jaccard Similarity: {jaccard:.2f}%")
        st.write(f"🔹 Cosine Similarity (Word Count): {cosine:.2f}%")

        st.markdown("</div>", unsafe_allow_html=True)

        # ---------------- HIGHLIGHT ----------------
        h1, h2 = highlight(text1, text2)

        st.subheader("📌 Highlighted Matches")

        col3, col4 = st.columns(2)

        with col3:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("**Document 1**")
            st.markdown(h1, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col4:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("**Document 2**")
            st.markdown(h2, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
