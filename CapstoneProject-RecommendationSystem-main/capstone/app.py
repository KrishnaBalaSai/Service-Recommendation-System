import streamlit as st
import uuid

from config import *
from models import load_embedder, load_llm
from query.intent import detect_intent, extract_budget
from query.search import search_books, search_services
from rag.llm_synthesizer import generate_answer
from user.activity_tracker import ActivityTracker
from user.profiler import UserProfiler
from query.vector_selector import select_search_vector
from rag.context_builder import build_context
from user.session import SessionProfiler


# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Unified Recommendation Engine",
    layout="wide"
)

st.title("🎓 Unified Recommendation Engine")
st.caption("An intelligent system for book & developer service recommendations")


# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.header("🧭 Session Controls")

    if st.button("🆕 New Chat"):
        st.session_state.messages = []
        st.success("New chat started")

    st.markdown("---")
    st.markdown(
        "<small>Academic prototype for recommendation research.</small>",
        unsafe_allow_html=True
    )


# =========================
# SESSION SETUP
# =========================
if "user_id" not in st.session_state:
    st.session_state.user_id = f"guest_{uuid.uuid4()}"

if "messages" not in st.session_state:
    st.session_state.messages = []


# =========================
# LOAD MODELS
# =========================
embedder = load_embedder()
llm = load_llm(api_key=GEMINI_API_KEY)


# =========================
# HELPERS
# =========================
tracker = ActivityTracker()
profiler = UserProfiler()
session_profiler = SessionProfiler()


# =========================
# CHAT HISTORY
# =========================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# =========================
# USER INPUT
# =========================
query = st.chat_input("Ask about books or developer services...")

if query:

    # show user question clearly
    st.session_state.messages.append({"role": "user", "content": query})

    with st.chat_message("user"):
        st.markdown(query)

    with st.spinner("Thinking like a recommender system…"):

        # 1️⃣ Intent & Budget
        intent = detect_intent(query)
        query_budget = extract_budget(query)

        # 2️⃣ Query Embedding
        query_vector = embedder.encode(
            ["search_query: " + query],
            normalize_embeddings=True
        )[0].tolist()

        # 3️⃣ User Profile
        profiler.create_user_if_not_exists(st.session_state.user_id)
        user_profile = profiler.get_user(st.session_state.user_id)

        # 4️⃣ Session Vector
        session_vector = session_profiler.build_session_vector(
            st.session_state.user_id
        )

        # 5️⃣ Vector Selection
        search_vector, vector_mode = select_search_vector(
            intent=intent,
            query_vector=query_vector,
            user_profile=user_profile,
            session_vector=session_vector
        )

        # =========================
        # SEARCH
        # =========================
        books = services = []

        if intent in ["book", "hybrid"]:
            books = search_books(search_vector, query_budget)

        if intent in ["service", "hybrid"]:
            services = search_services(search_vector, query_budget)

        # =========================
        # DISPLAY RESULTS (COMPACT)
        # =========================
        if books:
            st.subheader("📚 Recommended Books")

            for b in books[:5]:
                st.markdown(
                    f"""
                    <div style="margin-bottom:8px;">
                        <strong>{b['title']}</strong><br>
                        <span style="font-size:13px; color:gray;">
                            Price: ₹{b['price_inr']}
                        </span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        if services:
            st.subheader("🛠️ Developer Services")

            primary = services[0]   # show only best-ranked service

            st.markdown(
                f"""
                <div style="margin-bottom:8px;">
                    <strong>{primary['service_name']}</strong><br>
                    <span style="font-size:13px; color:gray;">
                        Estimated Cost: ₹{primary.get('price_inr', 'Varies')}
                    </span>
                </div>
                """,
                unsafe_allow_html=True
            )


        # =========================
        # RAG + LLM SYNTHESIS
        # =========================
        context, rag_mode = build_context(books, services)

        answer = generate_answer(
            llm=llm,
            query=query,
            context=context,
            rag_mode=rag_mode,
            user_prefs=[],
            vector_mode=vector_mode
        )


    # =========================
    # ASSISTANT RESPONSE
    # =========================
    with st.chat_message("assistant", avatar="🎓"):
        st.markdown("### 🧠 Summary & Suggestions")
        st.markdown(answer)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )

    # =========================
    # FEEDBACK
    # =========================
    st.divider()
    st.caption("Was this recommendation helpful?")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("👍 Yes, this helped"):
            tracker.log_event(
                st.session_state.user_id,
                "summary",
                "response",
                "like"
            )
            st.success("Thanks! I’ll personalize future suggestions better 😊")

    with col2:
        if st.button("👎 Not really"):
            tracker.log_event(
                st.session_state.user_id,
                "summary",
                "response",
                "dislike"
            )
            st.info("Got it. I’ll try a different approach next time.")


# =========================
# FOOTER
# =========================
st.markdown(
    "<small>This system is a research prototype. Recommendations are advisory only.</small>",
    unsafe_allow_html=True
)
