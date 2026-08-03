import time
import streamlit as st

from app.services.retriever_service import RetrieverService
from app.services.llm_service import LLMService
from app.services.indexing_service import IndexingService
from app.export_chat import export_chat


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Generative AI Document Assistant",
    page_icon="🤖",
    layout="wide"
)


# ==================================================
# INITIALIZE SERVICES
# ==================================================

@st.cache_resource
def get_retriever():
    return RetrieverService()


@st.cache_resource
def get_llm():
    return LLMService()


@st.cache_resource
def get_indexer():
    return IndexingService()


retriever = get_retriever()
llm = get_llm()
indexer = get_indexer()


# ==================================================
# SETTINGS
# ==================================================

MAX_HISTORY = 6

# ChromaDB retrieval distance threshold.
# Smaller distance = closer semantic match.
# This is a starting value and can be tuned later.
MAX_DISTANCE = 1.2


# ==================================================
# SESSION STATE
# ==================================================

if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = {
        "Chat 1": []
    }

if "current_chat" not in st.session_state:
    st.session_state.current_chat = "Chat 1"

if "chat_counter" not in st.session_state:
    st.session_state.chat_counter = 1


# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    st.title("🤖 AI Assistant")

    st.markdown("---")


    # ==================================================
    # SEARCH SETTINGS
    # ==================================================

    st.subheader("⚙ Search Settings")

    top_k = st.slider(
        "Top K Results",
        min_value=1,
        max_value=10,
        value=3
    )


    # ==================================================
# DOCUMENT SELECTION + DELETE
# ==================================================

st.markdown("---")
st.subheader("📄 Document")

try:
    indexed_files = retriever.get_indexed_files()
except Exception as e:
    indexed_files = []
    st.warning(f"Unable to load documents: {e}")


# --------------------------------------------------
# SEARCH DOCUMENT SELECTION
# --------------------------------------------------

document_options = ["All Documents"] + indexed_files

selected_document = st.selectbox(
    "Search in",
    document_options,
    key="document_search_select"
)

selected_file = (
    None
    if selected_document == "All Documents"
    else selected_document
)


# --------------------------------------------------
# DELETE DOCUMENT
# --------------------------------------------------

if indexed_files:

    st.markdown("##### 🗑 Manage Documents")

    document_to_delete = st.selectbox(
        "Document to delete",
        indexed_files,
        key="document_delete_select"
    )

    if st.button(
        "🗑 Delete Document",
        use_container_width=True,
        type="secondary"
    ):

        try:

            deleted_count = indexer.delete_document(
                document_to_delete
            )

            if deleted_count > 0:

                st.success(
                    f"✅ Deleted '{document_to_delete}' "
                    f"({deleted_count} chunks)."
                )

                # Clear Streamlit cached services
                st.cache_resource.clear()

                st.rerun()

            else:

                st.warning(
                    f"No indexed chunks were found for "
                    f"'{document_to_delete}'."
                )

        except Exception as e:

            st.error(
                f"Failed to delete document: {str(e)}"
            )

else:

    st.caption(
        "No indexed documents available to delete."
    )


    # ==================================================
    # DELETE SELECTED DOCUMENT
    # ==================================================

    if selected_file:

        if st.button(
            "🗑 Delete Selected Document",
            use_container_width=True
        ):

            try:

                deleted_count = (
                    indexer.delete_document(
                        selected_file
                    )
                )

                if deleted_count > 0:

                    st.success(
                        f"✅ Deleted "
                        f"{selected_file} "
                        f"({deleted_count} chunks)"
                    )

                    # Refresh cached services
                    st.cache_resource.clear()

                    st.rerun()

                else:

                    st.warning(
                        "Document was not found."
                    )

            except Exception as e:

                st.error(
                    f"Failed to delete document: "
                    f"{str(e)}"
                )


    # ==================================================
    # CHAT SESSIONS
    # ==================================================

    st.markdown("---")

    st.subheader("💬 Chats")


    # ------------------------------
    # NEW CHAT
    # ------------------------------

    if st.button(
        "➕ New Chat",
        use_container_width=True
    ):

        st.session_state.chat_counter += 1

        new_name = (
            f"Chat {st.session_state.chat_counter}"
        )

        st.session_state.chat_sessions[
            new_name
        ] = []

        st.session_state.current_chat = (
            new_name
        )

        st.rerun()


    # ------------------------------
    # CHAT HISTORY
    # ------------------------------

    chat_names = list(
        st.session_state.chat_sessions.keys()
    )


    if (
        st.session_state.current_chat
        not in chat_names
    ):
        st.session_state.current_chat = (
            chat_names[0]
        )


    selected_chat = st.radio(
        "History",
        chat_names,
        index=chat_names.index(
            st.session_state.current_chat
        ),
        label_visibility="collapsed"
    )


    if (
        selected_chat
        != st.session_state.current_chat
    ):

        st.session_state.current_chat = (
            selected_chat
        )

        st.rerun()


    # ------------------------------
    # CLEAR CURRENT CHAT
    # ------------------------------

    st.markdown("---")

    if st.button(
        "🗑 Clear Current Chat",
        use_container_width=True
    ):

        st.session_state.chat_sessions[
            st.session_state.current_chat
        ] = []

        st.rerun()


    # ------------------------------
    # DELETE CURRENT CHAT
    # ------------------------------

    if len(
        st.session_state.chat_sessions
    ) > 1:

        if st.button(
            "❌ Delete Current Chat",
            use_container_width=True
        ):

            del st.session_state.chat_sessions[
                st.session_state.current_chat
            ]

            st.session_state.current_chat = (
                list(
                    st.session_state.chat_sessions.keys()
                )[0]
            )

            st.rerun()


    # ==================================================
    # DATABASE
    # ==================================================

    st.markdown("---")

    st.subheader("📊 Database")

    try:

        indexed_chunks = (
            retriever.collection.count()
        )

        st.metric(
            label="Indexed Chunks",
            value=indexed_chunks
        )

    except Exception:

        st.warning(
            "Unable to read ChromaDB collection."
        )


    # ==================================================
    # PDF UPLOAD
    # ==================================================

    st.markdown("---")

    st.subheader("📂 Upload PDF")

    uploaded_file = st.file_uploader(
        "Add a document to the knowledge base",
        type=["pdf"],
        accept_multiple_files=False
    )


    if uploaded_file is not None:

        st.caption(
            f"Selected: {uploaded_file.name}"
        )


        if st.button(
            "📥 Index this PDF",
            use_container_width=True
        ):

            with st.spinner(
                f"Indexing {uploaded_file.name}..."
            ):

                try:

                    # Get PDF bytes
                    file_bytes = (
                        uploaded_file.getvalue()
                    )

                    # Index PDF
                    n_chunks = (
                        indexer.index_pdf_bytes(
                            file_bytes,
                            uploaded_file.name
                        )
                    )


                    # ----------------------------------
                    # DUPLICATE DOCUMENT
                    # ----------------------------------

                    if n_chunks == -1:

                        st.warning(
                            f"⚠️ {uploaded_file.name} "
                            "is already indexed."
                        )


                    # ----------------------------------
                    # SUCCESS
                    # ----------------------------------

                    elif n_chunks > 0:

                        st.success(
                            f"✅ Indexed {n_chunks} "
                            f"chunks from "
                            f"{uploaded_file.name}"
                        )

                        # Refresh cached services
                        st.cache_resource.clear()

                        st.rerun()


                    # ----------------------------------
                    # NO TEXT
                    # ----------------------------------

                    else:

                        st.warning(
                            "No text could be "
                            "extracted from this PDF."
                        )


                except Exception as e:

                    st.error(
                        f"Failed to index PDF: "
                        f"{str(e)}"
                    )


    # ==================================================
    # ABOUT
    # ==================================================

    st.markdown("---")

    st.info(
        """
### About

**Generative AI Document Assistant**

✅ PDF Upload  
✅ Duplicate Prevention  
✅ Document Management  
✅ Semantic Search  
✅ Document Selection  
✅ Metadata Filtering  
✅ Similarity Filtering  
✅ ChromaDB  
✅ Sentence Transformers  
✅ Groq LLM  
✅ Conversation Memory  
✅ Multi-Chat Sessions  
✅ Chat Export  
✅ Source Documents
"""
    )


# ==================================================
# MAIN PAGE
# ==================================================

st.title(
    "🤖 Generative AI Document Assistant"
)


# ==================================================
# SELECTED DOCUMENT INFORMATION
# ==================================================

if selected_file:

    st.caption(
        f"Session: **{st.session_state.current_chat}** "
        f"— Searching in: **{selected_file}**"
    )

else:

    st.caption(
        f"Session: **{st.session_state.current_chat}** "
        "— Searching in all indexed documents."
    )


# ==================================================
# CURRENT CHAT
# ==================================================

messages = (
    st.session_state.chat_sessions[
        st.session_state.current_chat
    ]
)


# ==================================================
# EXPORT CHAT
# ==================================================

if messages:

    try:

        filename, content = (
            export_chat(
                messages
            )
        )

        st.download_button(
            label="⬇ Export Chat",
            data=content,
            file_name=filename,
            mime="text/plain"
        )

    except Exception as e:

        st.warning(
            f"Unable to export chat: "
            f"{str(e)}"
        )


# ==================================================
# DISPLAY CHAT HISTORY
# ==================================================

for message in messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# ==================================================
# CHAT INPUT
# ==================================================

prompt = st.chat_input(
    "Ask a question about your documents..."
)


# ==================================================
# PROCESS USER QUESTION
# ==================================================

if prompt:

    # --------------------------------------------------
    # SAVE USER MESSAGE
    # --------------------------------------------------

    messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )


    # --------------------------------------------------
    # DISPLAY USER MESSAGE
    # --------------------------------------------------

    with st.chat_message("user"):

        st.markdown(prompt)


    # --------------------------------------------------
    # DEFAULT VALUES
    # --------------------------------------------------

    docs = []

    metadatas = []

    distances = []

    answer = ""


    # ==================================================
    # RAG PIPELINE
    # ==================================================

    with st.spinner(
        "Searching documents..."
    ):

        try:

            # ==========================================
            # 1. RETRIEVE TOP-K CHUNKS
            # ==========================================

            results = retriever.search(
                prompt,
                n_results=top_k,
                file_name=selected_file
            )


            # ==========================================
            # 2. GET RAW DOCUMENTS
            # ==========================================

            raw_docs = (
                results.get(
                    "documents",
                    [[]]
                )[0]
                or []
            )


            # ==========================================
            # 3. GET RAW METADATA
            # ==========================================

            raw_metadatas = (
                results.get(
                    "metadatas",
                    [[]]
                )[0]
                or []
            )


            # ==========================================
            # 4. GET RETRIEVAL DISTANCES
            # ==========================================

            raw_distances = (
                results.get(
                    "distances",
                    [[]]
                )[0]
                or []
            )


            # ==========================================
            # 5. FILTER WEAK RESULTS
            # ==========================================

            docs = []

            metadatas = []

            distances = []


            for i, doc in enumerate(
                raw_docs
            ):

                # ------------------------------
                # Distance
                # ------------------------------

                if i < len(
                    raw_distances
                ):

                    distance = (
                        raw_distances[i]
                    )

                else:

                    distance = None


                # ------------------------------
                # Metadata
                # ------------------------------

                if i < len(
                    raw_metadatas
                ):

                    metadata = (
                        raw_metadatas[i]
                        or {}
                    )

                else:

                    metadata = {}


                # ------------------------------
                # Similarity filtering
                # ------------------------------

                if (
                    distance is not None
                    and distance <= MAX_DISTANCE
                ):

                    docs.append(
                        doc
                    )

                    metadatas.append(
                        metadata
                    )

                    distances.append(
                        distance
                    )


            # ==========================================
            # 6. BUILD DOCUMENT CONTEXT
            # ==========================================

            context = "\n\n".join(
                docs
            )


            # ==========================================
            # 7. CONVERSATION MEMORY
            # ==========================================

            history = ""

            # Current user question is already
            # passed separately to the LLM.
            previous_messages = (
                messages[:-1]
            )


            for message in (
                previous_messages[
                    -MAX_HISTORY:
                ]
            ):

                history += (
                    f"{message['role']}: "
                    f"{message['content']}\n"
                )


            # ==========================================
            # 8. COMBINE HISTORY + DOCUMENT CONTEXT
            # ==========================================

            full_context = f"""
Conversation History
====================

{history}


Retrieved Document Context
==========================

{context}
"""


            # ==========================================
            # 9. GENERATE ANSWER
            # ==========================================

            if docs:

                answer = (
                    llm.generate_answer(
                        prompt,
                        full_context
                    )
                )

            else:

                if selected_file:

                    answer = (
                        "I couldn't find relevant "
                        "information in the selected "
                        "document."
                    )

                else:

                    answer = (
                        "I couldn't find relevant "
                        "information in the indexed "
                        "documents."
                    )


        # ==================================================
        # ERROR HANDLING
        # ==================================================

        except Exception as e:

            answer = (
                f"Error while generating answer: "
                f"{str(e)}"
            )

            docs = []

            metadatas = []

            distances = []


    # ==================================================
    # ASSISTANT RESPONSE
    # ==================================================

    with st.chat_message(
        "assistant"
    ):

        placeholder = st.empty()

        display_text = ""


        # ==================================================
        # TYPING EFFECT
        # ==================================================

        for word in answer.split():

            display_text += (
                word + " "
            )

            placeholder.markdown(
                display_text
            )

            time.sleep(
                0.03
            )


        # ==================================================
        # SOURCE DOCUMENTS
        # ==================================================

        if docs:

            with st.expander(
                "📚 Source Documents"
            ):

                for i, doc in enumerate(
                    docs,
                    start=1
                ):

                    # ----------------------------------
                    # METADATA
                    # ----------------------------------

                    if (
                        i - 1
                        < len(metadatas)
                    ):

                        meta = (
                            metadatas[
                                i - 1
                            ]
                            or {}
                        )

                    else:

                        meta = {}


                    # ----------------------------------
                    # FILE NAME
                    # ----------------------------------

                    file_name = (
                        meta.get(
                            "file_name",
                            f"Chunk {i}"
                        )
                    )

                    st.markdown(
                        f"### 📄 {file_name}"
                    )


                    # ----------------------------------
                    # SOURCE
                    # ----------------------------------

                    source = (
                        meta.get(
                            "source"
                        )
                    )

                    if source:

                        st.caption(
                            f"Source: {source}"
                        )


                    # ----------------------------------
                    # FILE PATH
                    # ----------------------------------

                    file_path = (
                        meta.get(
                            "file_path"
                        )
                    )

                    if file_path:

                        st.caption(
                            f"Path: {file_path}"
                        )


                    # ----------------------------------
                    # RETRIEVAL DISTANCE
                    # ----------------------------------

                    if (
                        i - 1
                        < len(distances)
                    ):

                        distance = (
                            distances[
                                i - 1
                            ]
                        )

                        st.caption(
                            f"Retrieval distance: "
                            f"{distance:.4f}"
                        )


                    # ----------------------------------
                    # RETRIEVED CHUNK
                    # ----------------------------------

                    st.write(
                        doc
                    )

                    st.divider()


    # ==================================================
    # SAVE ASSISTANT RESPONSE
    # ==================================================

    messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )