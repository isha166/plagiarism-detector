import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

st.set_page_config(page_title="Plagiarism Detector", layout="wide")

# ---------------- UI ----------------
st.markdown("""
<style>
body { background-color: black; }
.main { background-color: black; color: white; }

h1, h2, h3 { color: #f5f5dc; }

/* Beige 3D boxes */
textarea {
    background-color: #f5f5dc !important;
    color: black !important;
    border-radius: 15px !important;
    box-shadow: 8px 8px 20px rgba(255,255,255,0.1),
                -8px -8px 20px rgba(0,0,0,0.8);
}

/* Cards */
.card {
    background-color: #111;
    padding: 20px;
    border-radius: 20px;
    margin-bottom: 20px;
}

/* Button */
.stButton>button {
    background: linear-gradient(135deg, #d4af37, #f5deb3);
    color: black;
    border-radius: 10px;
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

st.title("Plagiarism Detector")

# ---------------- INPUT ----------------
col1, col2 = st.columns(2)

with col1:
    text1 = st.text_area("📄 Document 1", height=250)

with col2:
    text2 = st.text_area("📄 Document 2", height=250)

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
    w1 = set(clean_words(t1))
    w2 = set(clean_words(t2))
    common = list(w1.intersection(w2))
    return common[:10]

def highlight(t1, t2):
    w1 = set(clean_words(t1))
    w2 = set(clean_words(t2))
    common = w1.intersection(w2)

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

# ---------------- BUTTON ----------------
if st.button("🔍 Analyze"):

    if not text1.strip() or not text2.strip():
        st.warning("Please enter both documents.")
    else:
        sim = similarity(text1, text2)

        # 📊 MAIN SCORE
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("📊 Similarity Score")
        st.write(f"### {sim:.2f}%")
        st.progress(sim/100)
        st.write(verdict(sim))
        st.markdown("</div>", unsafe_allow_html=True)

        # 📈 DOCUMENT STATS
        st.subheader("📈 Document Insights")

        w1, u1, s1, r1 = get_stats(text1)
        w2, u2, s2, r2 = get_stats(text2)

        col3, col4 = st.columns(2)

        with col3:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.write("**Document 1 Stats**")
            st.write(f"Words: {w1}")
            st.write(f"Unique Words: {u1}")
            st.write(f"Avg Sentence Length: {s1:.2f}")
            st.write(f"Vocabulary Richness: {r1:.2f}")
            st.markdown("</div>", unsafe_allow_html=True)

        with col4:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.write("**Document 2 Stats**")
            st.write(f"Words: {w2}")
            st.write(f"Unique Words: {u2}")
            st.write(f"Avg Sentence Length: {s2:.2f}")
            st.write(f"Vocabulary Richness: {r2:.2f}")
            st.markdown("</div>", unsafe_allow_html=True)

        # 🔎 COMMON WORDS
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("🔎 Common Words")
        st.write(common_words(text1, text2))
        st.markdown("</div>", unsafe_allow_html=True)

        # ✨ HIGHLIGHT
        h1, h2 = highlight(text1, text2)

        st.subheader("📌 Highlighted Matches")

        col5, col6 = st.columns(2)

        with col5:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown(h1, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col6:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown(h2, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
