from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from utils.chatbot_utils import build_tfidf_engine, evaluate_questions, get_chatbot_response, load_faq_data


BASE_DIR = Path(__file__).resolve().parent
FAQ_PATH = BASE_DIR / "data" / "faq_mti_unpam.csv"
EVAL_PATH = BASE_DIR / "data" / "evaluation_questions.csv"

st.set_page_config(
    page_title="MTI UNPAM Academic Assistant",
    page_icon="🎓",
    layout="wide",
)

st.markdown(
    """
    <style>
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1180px;
    }
    .app-title {
        font-size: 2rem;
        font-weight: 800;
        margin-bottom: 0.25rem;
    }
    .app-subtitle {
        color: #5f6368;
        font-size: 1rem;
        margin-bottom: 1.25rem;
    }
    .info-card {
        border: 1px solid #e6e8eb;
        border-radius: 16px;
        padding: 1rem 1.1rem;
        background: #ffffff;
        box-shadow: 0 2px 10px rgba(15, 23, 42, 0.04);
    }
    .small-note {
        color: #6b7280;
        font-size: 0.9rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def load_data():
    faq_df = load_faq_data(FAQ_PATH)
    eval_df = pd.read_csv(EVAL_PATH).fillna("") if EVAL_PATH.exists() else pd.DataFrame()
    return faq_df, eval_df


@st.cache_resource
def load_engine(faq_df: pd.DataFrame):
    return build_tfidf_engine(faq_df)


faq_df, eval_df = load_data()
vectorizer, tfidf_matrix = load_engine(faq_df)

with st.sidebar:
    st.title("🎓 MTI Assistant")
    st.caption("Chatbot informasi akademik MTI UNPAM berbasis TF-IDF dan Cosine Similarity.")
    threshold = st.slider("Threshold similarity", 0.05, 0.80, 0.25, 0.05)
    st.divider()
    st.markdown("**Contoh pertanyaan:**")
    st.markdown("- Apa saja mata kuliah semester 1?")
    st.markdown("- Peminatan Data Science belajar apa?")
    st.markdown("- Saya tertarik cyber security, cocok peminatan apa?")
    st.markdown("- Apa perbedaan IoT dan Data Science?")
    st.divider()
    st.caption("Catatan: chatbot ini adalah prototype akademik, bukan kanal resmi PMB.")

st.markdown('<div class="app-title">MTI UNPAM Academic Assistant</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="app-subtitle">Chatbot informasi akademik Program Magister Teknik Informatika berbasis Text Mining.</div>',
    unsafe_allow_html=True,
)

tab_chatbot, tab_dashboard, tab_dataset, tab_about = st.tabs([
    "💬 Chatbot",
    "📊 Dashboard",
    "📚 Dataset FAQ",
    "ℹ️ Tentang Project",
])

with tab_chatbot:
    col_left, col_right = st.columns([1.5, 1])

    with col_left:
        st.subheader("Tanyakan informasi seputar MTI UNPAM")
        user_question = st.text_input(
            "Pertanyaan",
            placeholder="Contoh: Saya tertarik data dan machine learning, cocok ambil peminatan apa?",
        )

        if st.button("Cari Jawaban", type="primary", use_container_width=True):
            result = get_chatbot_response(user_question, faq_df, vectorizer, tfidf_matrix, threshold)
            st.markdown("### Jawaban")
            if result["status"] == "answered":
                st.success(result["answer"])
            elif result["status"] == "fallback":
                st.warning(result["answer"])
            else:
                st.info(result["answer"])

            metric_cols = st.columns(3)
            metric_cols[0].metric("Similarity score", result["similarity_score"])
            metric_cols[1].metric("Kategori", result["category"])
            metric_cols[2].metric("Status", result["status"])

            with st.expander("Lihat pertanyaan FAQ yang paling mirip"):
                st.write(result["matched_question"])

    with col_right:
        st.markdown("### Ringkasan Dataset")
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.metric("Total FAQ", len(faq_df))
        st.metric("Jumlah kategori", faq_df["category"].nunique())
        st.metric("Jumlah peminatan", faq_df.loc[faq_df["peminatan"] != "", "peminatan"].nunique())
        st.markdown('</div>', unsafe_allow_html=True)
        st.caption("Dataset dapat diperluas jika terdapat informasi resmi tambahan dari program studi.")

with tab_dashboard:
    st.subheader("Dashboard Evaluasi dan Distribusi Dataset")

    col1, col2 = st.columns(2)
    category_counts = faq_df["category"].value_counts().reset_index()
    category_counts.columns = ["category", "count"]
    fig_category = px.bar(
        category_counts,
        x="count",
        y="category",
        orientation="h",
        title="Distribusi FAQ berdasarkan kategori",
        labels={"count": "Jumlah FAQ", "category": "Kategori"},
        height=520,
    )
    fig_category.update_layout(template="plotly_white", yaxis={"categoryorder": "total ascending"})
    col1.plotly_chart(fig_category, use_container_width=True)

    semester_df = faq_df.copy()
    semester_df["semester"] = semester_df["semester"].replace("", "Umum")
    semester_counts = semester_df["semester"].value_counts().reset_index()
    semester_counts.columns = ["semester", "count"]
    fig_semester = px.bar(
        semester_counts,
        x="semester",
        y="count",
        title="Distribusi FAQ berdasarkan semester",
        labels={"count": "Jumlah FAQ", "semester": "Semester"},
        height=520,
    )
    fig_semester.update_layout(template="plotly_white")
    col2.plotly_chart(fig_semester, use_container_width=True)

    col3, col4 = st.columns(2)
    peminatan_df = faq_df[faq_df["peminatan"] != ""]
    if not peminatan_df.empty:
        peminatan_counts = peminatan_df["peminatan"].value_counts().reset_index()
        peminatan_counts.columns = ["peminatan", "count"]
        fig_peminatan = px.pie(
            peminatan_counts,
            names="peminatan",
            values="count",
            title="Komposisi FAQ berdasarkan peminatan",
            height=500,
        )
        fig_peminatan.update_layout(template="plotly_white")
        col3.plotly_chart(fig_peminatan, use_container_width=True)

    if not eval_df.empty:
        eval_result = evaluate_questions(eval_df, faq_df, vectorizer, tfidf_matrix, threshold)
        accuracy = eval_result["is_correct"].mean() if len(eval_result) else 0
        col4.metric("Akurasi evaluasi sederhana", f"{accuracy:.2%}")
        fig_eval = px.bar(
            eval_result,
            x="test_question",
            y="similarity_score",
            color="status",
            title="Similarity score pada pertanyaan uji",
            labels={"test_question": "Pertanyaan uji", "similarity_score": "Similarity score"},
            height=500,
        )
        fig_eval.update_layout(template="plotly_white", xaxis_tickangle=-35)
        col4.plotly_chart(fig_eval, use_container_width=True)
        st.dataframe(eval_result, use_container_width=True)

with tab_dataset:
    st.subheader("Dataset FAQ MTI UNPAM")
    st.dataframe(faq_df, use_container_width=True, hide_index=True)
    st.download_button(
        "Download dataset FAQ",
        faq_df.to_csv(index=False).encode("utf-8"),
        file_name="faq_mti_unpam.csv",
        mime="text/csv",
    )

with tab_about:
    st.subheader("Tentang Project")
    st.write(
        "Project ini merupakan prototype chatbot informasi akademik Program Magister Teknik Informatika UNPAM. "
        "Metode yang digunakan adalah text preprocessing sederhana, TF-IDF Vectorizer, dan Cosine Similarity untuk mencocokkan pertanyaan pengguna dengan dataset FAQ."
    )
    st.markdown("""
    **Batasan prototype:**
    - Dataset FAQ masih berbasis informasi awal dan perlu divalidasi kembali jika akan digunakan secara resmi.
    - Chatbot belum menggunakan LLM atau database eksternal.
    - Jawaban bersifat bantuan informasi, bukan pengganti kanal resmi program studi atau PMB.
    """)
