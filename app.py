import streamlit as st
import hashlib
import re
import numpy as np
import matplotlib.pyplot as plt

# ---------------- STYLE ----------------
st.markdown("""
    <style>
    .main {
        background-color: #0f172a;
        color: white;
    }
    .stTextArea textarea {
        border-radius: 10px;
        border: 1px solid #334155;
    }
    .card {
        padding: 15px;
        border-radius: 12px;
        background-color: #1e293b;
    }
    mark {
        background-color: #38bdf8;
        color: black;
        padding: 2px 4px;
        border-radius: 4px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📄 Visual Plagiarism Detector")
st.caption("Compare documents using fingerprinting + heatmap")

# ---------------- LOGIC ----------------
def preprocess(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return text.split()

def hash_k_gram(k_gram):
    return int(hashlib.md5(" ".join(k_gram).encode()).hexdigest(), 16)

def get_k_grams(words, k):
    if len(words) < k:
        k = max(1, len(words))
    return [(words[i:i+k], i) for i in range(len(words) - k + 1)]

def winnowing(words, k=5, window_size=4):
    if len(words) < k:
        k = max(1, len(words))

    k_grams = get_k_grams(words, k)
    hashes = [(hash_k_gram(kg), pos) for kg, pos in k_grams]

    fingerprints = []
    for i in range(len(hashes) - window_size + 1):
        window = hashes[i:i+window_size]
        fingerprints.append(min(window, key=lambda x: x[0]))

    return fingerprints

def detect_matches(doc1, doc2):
    words1 = preprocess(doc1)
    words2 = preprocess(doc2)

    fp1 = winnowing(words1)
    fp2 = winnowing(words2)

    map1 = {h: pos for h, pos in fp1}
    map2 = {h: pos for h, pos in fp2}

    matches = []
    for h in map1:
        if h in map2:
            matches.append((map1[h], map2[h]))

    similarity = len(matches) / max(len(fp1), 1)

    return similarity, matches, words1, words2

def highlight(words, positions, k=5):
    result = words.copy()
    for pos in positions:
        for i in range(pos, pos+k):
            if i < len(result):
                result[i] = f"<mark>{result[i]}</mark>"
    return " ".join(result)

def heatmap(matches, len1, len2):
    matrix = np.zeros((len1, len2))
    for i, j in matches:
        matrix[i][j] = 1

    fig, ax = plt.subplots()
    ax.imshow(matrix)
    ax.set_title("Similarity Heatmap")
    return fig

# ---------------- UI LAYOUT ----------------
col1, col2 = st.columns(2)

with col1:
    doc1 = st.text_area("📄 Document 1", height=250)

with col2:
    doc2 = st.text_area("📄 Document 2", height=250)

if st.button("🔍 Analyze Similarity"):

    similarity, matches, words1, words2 = detect_matches(doc1, doc2)

    # Progress bar
    st.subheader("Similarity Score")
    st.progress(similarity)

    st.write(f"**{similarity*100:.2f}% match**")

    pos1 = [m[0] for m in matches]
    pos2 = [m[1] for m in matches]

    highlighted1 = highlight(words1, pos1)
    highlighted2 = highlight(words2, pos2)

    st.subheader("📌 Highlighted Comparison")

    col3, col4 = st.columns(2)

    with col3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("**Document 1**", unsafe_allow_html=True)
        st.markdown(highlighted1, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col4:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("**Document 2**", unsafe_allow_html=True)
        st.markdown(highlighted2, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Evidence panel
    st.subheader("📍 Evidence Matches")
    for i, (a, b) in enumerate(matches[:10]):
        st.write(f"Match {i+1}: Doc1 word {a} ↔ Doc2 word {b}")

    # Heatmap
    st.subheader("🔥 Similarity Heatmap")
    fig = heatmap(matches, len(words1), len(words2))
    st.pyplot(fig)