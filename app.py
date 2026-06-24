from pathlib import Path
import streamlit as st

# =========================================================
# Import chatbot engine
# =========================================================
try:
    from utils.chatbot_utils import chatbot_response as chatbot_engine
except ImportError:
    try:
        from utils.chatbot_utils import get_chatbot_response as chatbot_engine
    except ImportError:
        chatbot_engine = None


# =========================================================
# Konfigurasi path
# =========================================================
PROJECT_ROOT = Path(__file__).resolve().parent
ASSETS_DIR = PROJECT_ROOT / "assets"

LOGO_PATH = ASSETS_DIR / "logo-unpam.png"
ANIME_PATH = ASSETS_DIR / "anime-unpam.png"

FIXED_THRESHOLD = 0.31


# =========================================================
# Konfigurasi halaman
# =========================================================
st.set_page_config(
    page_title="MTI Assistant UNPAM",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# Custom CSS ringan
# =========================================================
st.markdown(
    """
    <style>
        #MainMenu {
            visibility: hidden;
        }

        footer {
            visibility: hidden;
        }

        header {
            visibility: hidden;
        }

        [data-testid="collapsedControl"] {
            display: none;
        }

        section[data-testid="stSidebar"] {
            display: none;
        }

        .block-container {
            max-width: 1180px;
            padding-top: 1.5rem;
            padding-bottom: 1.5rem;
        }

        h1, h2, h3 {
            color: #0f172a;
        }

        .app-subtitle {
            color: #475569;
            font-size: 0.98rem;
            line-height: 1.65;
            margin-top: -0.4rem;
        }

        .small-note {
            color: #64748b;
            font-size: 0.86rem;
            line-height: 1.5;
        }

        .assistant-box {
            background-color: #f8fafc;
            border-left: 5px solid #1d4ed8;
            padding: 0.85rem 1rem;
            border-radius: 0.8rem;
            font-size: 0.94rem;
            line-height: 1.65;
            color: #334155;
        }

        .example-box {
            background-color: #fff7ed;
            border-left: 5px solid #f59e0b;
            padding: 0.85rem 1rem;
            border-radius: 0.8rem;
            font-size: 0.92rem;
            line-height: 1.65;
            color: #334155;
        }

        div[data-testid="stChatMessage"] {
            border-radius: 0.9rem;
            padding: 0.25rem 0.35rem;
        }

        .stButton > button {
            border-radius: 0.75rem;
            height: 2.7rem;
            font-weight: 600;
        }

        div[data-testid="stTextInput"] input {
            border-radius: 0.75rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# Helper function
# =========================================================
def reset_chat():
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Halo, selamat datang di **MTI Assistant UNPAM** 👋\n\n"
                "Silakan ajukan pertanyaan seputar Program Magister Teknik Informatika, "
                "mata kuliah, peminatan, tesis, Data Mining, Data Science, dan informasi akademik "
                "yang tersedia pada dataset chatbot."
            ),
        }
    ]


def get_bot_answer(user_question: str) -> str:
    """
    Mengambil jawaban dari chatbot engine.
    Threshold dibuat tetap agar tidak muncul pada UI.
    """

    if chatbot_engine is None:
        return (
            "Maaf, engine chatbot belum berhasil dimuat. "
            "Pastikan file `utils/chatbot_utils.py` tersedia dan fungsi chatbot sudah benar."
        )

    try:
        result = chatbot_engine(user_question, threshold=FIXED_THRESHOLD)
    except TypeError:
        try:
            result = chatbot_engine(user_question)
        except Exception as exc:
            return f"Maaf, terjadi kendala saat memproses pertanyaan: `{exc}`"
    except Exception as exc:
        return f"Maaf, terjadi kendala saat memproses pertanyaan: `{exc}`"

    if isinstance(result, dict):
        return str(
            result.get("answer")
            or result.get("response")
            or result.get("bot_response")
            or result.get("message")
            or "Maaf, saya belum dapat memberikan jawaban yang sesuai."
        )

    if isinstance(result, (tuple, list)) and len(result) > 0:
        return str(result[0])

    return str(result)


# =========================================================
# Session state
# =========================================================
if "messages" not in st.session_state:
    reset_chat()


# =========================================================
# Header aplikasi
# =========================================================
header_col1, header_col2 = st.columns([1, 8])

with header_col1:
    if LOGO_PATH.exists():
        st.image(str(LOGO_PATH), width=92)
    else:
        st.markdown("## 🎓")

with header_col2:
    st.markdown("# MTI Assistant UNPAM")
    st.markdown(
        """
        <div class="app-subtitle">
            Chatbot informasi akademik Program Magister Teknik Informatika Universitas Pamulang
            berbasis <b>FAQ</b>, <b>TF-IDF</b>, dan <b>Cosine Similarity</b>.
            Aplikasi ini dirancang sebagai project final Data Mining untuk membantu pengguna
            memperoleh informasi akademik secara cepat, sederhana, dan mudah dipahami.
        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()


# =========================================================
# Layout utama
# =========================================================
left_col, right_col = st.columns([1.05, 2.35], gap="large")


# =========================================================
# Panel kiri: Anime assistant
# =========================================================
with left_col:
    with st.container(border=True):
        st.subheader("Asisten Virtual Akademik")

        if ANIME_PATH.exists():
            st.image(str(ANIME_PATH), use_container_width=True)
        else:
            st.warning("File `assets/anime-unpam.png` belum ditemukan.")

        st.markdown(
            """
            <div class="assistant-box">
                Halo 👋<br><br>
                Saya siap membantu menjawab pertanyaan akademik seputar
                <b>MTI UNPAM</b>, mata kuliah, peminatan, tesis,
                Data Mining, Data Science, dan topik pembelajaran terkait.
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.write("")

        st.markdown(
            """
            <div class="example-box">
                <b>Contoh pertanyaan:</b><br>
                • Apa itu Data Mining?<br>
                • Apa saja mata kuliah semester 1?<br>
                • Apa peminatan di MTI UNPAM?<br>
                • Apa yang dibahas pada tesis?
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.write("")

        if st.button("Reset Percakapan", use_container_width=True):
            reset_chat()
            st.rerun()

        st.markdown(
            '<div class="small-note">Gunakan tombol reset untuk memulai percakapan baru.</div>',
            unsafe_allow_html=True,
        )


# =========================================================
# Panel kanan: Area chat
# =========================================================
with right_col:
    with st.container(border=True):
        st.subheader("Area Chat")

        chat_area = st.container(height=520, border=True)

        with chat_area:
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

        st.write("")

        with st.form("chat_form", clear_on_submit=True):
            user_prompt = st.text_input(
                label="Pertanyaan",
                placeholder="Tulis pertanyaan Anda di sini...",
                label_visibility="collapsed",
            )

            submit_col1, submit_col2 = st.columns([1, 4])

            with submit_col1:
                submitted = st.form_submit_button("Kirim", use_container_width=True)

            with submit_col2:
                st.markdown(
                    '<div class="small-note">Contoh: Apa yang dibahas pada tesis?</div>',
                    unsafe_allow_html=True,
                )

        if submitted and user_prompt.strip():
            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": user_prompt.strip(),
                }
            )

            bot_answer = get_bot_answer(user_prompt.strip())

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": bot_answer,
                }
            )

            st.rerun()


# =========================================================
# Footer
# =========================================================
st.divider()
st.markdown(
    """
    <div class="small-note" style="text-align:center;">
        MTI Assistant UNPAM • Project Final Data Mining • FAQ-based Chatbot with TF-IDF and Cosine Similarity
    </div>
    """,
    unsafe_allow_html=True,
)