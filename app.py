import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Plagiarism Detector",
    layout="wide",
)

# ---------------- CUSTOM CSS (Pinterest Style) ----------------
st.markdown("""
<style>
body {
    background-color: #f8fafc;
}

.main {
    background: linear-gradient(135deg, #fdfbfb, #ebedee);
}

h1, h2, h3 {
    color: #1e293b;
}

.card {
    background-color: white;
    padding: 20px;
    border-radius: 18px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.05);
    margin-bottom: 15px;
}

textarea {
    border-radius: 12px !important;
}

.stButton>button {
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    color: white;
    border-radius: 12px;
    padding: 10px 20px;
    border: none;
}

.highlight {
    background-color: #a5f3fc;
    padding: 2px 6px;
    border-radius: 6px;
}

.score {
    font-size: 28px;
    font-weight: bold;
    color: #6366f1;
}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.title("✨Plagiarism Detector")
st.write("Compare two documents and detect similarity in a clean, visual way.")

# ---------------- INPUT SECTION ----------------
col1, col2 = st.columns(2)

with col1:
    text1 = st.text_area("📄 Document 1", height=250)

with col2:
    text2 = st.text_area("📄 Document 2", height=250)

# ---------------- SIMILARITY FUNCTION ----------------
def calculate_similarity(doc1, doc2):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([doc1, doc2])
    similarity = cosine_similarity(vectors[0], vectors[1])
    return similarity[0][0] * 100

# ---------------- HIGHLIGHT FUNCTION ----------------
def highlight(text1, text2):
    words1 = re.findall(r'\w+', text1.lower())
    words2 = re.findall(r'\w+', text2.lower())

    common = set(words1).intersection(set(words2))

    def highlight_text(text):
        words = text.split()
        highlighted = []
        for word in words:
            clean = re.sub(r'\W+', '', word.lower())
            if clean in common:
                highlighted.append(f"<span class='highlight'>{word}</span>")
            else:
                highlighted.append(word)
        return " ".join(highlighted)

    return highlight_text(text1), highlight_text(text2)

# ---------------- BUTTON ----------------
if st.button("🔍 Analyze Similarity"):

    if text1.strip() == "" or text2.strip() == "":
        st.warning("Please enter both documents.")
    else:
        similarity = calculate_similarity(text1, text2)

        # ---------------- SCORE ----------------
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("📊 Similarity Score")
        st.markdown(f"<div class='score'>{similarity:.2f}% Match</div>", unsafe_allow_html=True)
        st.progress(min(similarity / 100, 1.0))
        st.markdown("</div>", unsafe_allow_html=True)

        # ---------------- HIGHLIGHT ----------------
        h1, h2 = highlight(text1, text2)

        st.subheader("📌 Highlighted Comparison")

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
