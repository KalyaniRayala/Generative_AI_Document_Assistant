import streamlit as st

from app.services.retriever_service import RetrieverService
from app.services.llm_service import LLMService

st.set_page_config(
    page_title="GenAI Document Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 GenAI Document Assistant")

retriever = RetrieverService()
llm = LLMService()

question = st.text_input("Ask a question")

if st.button("Ask"):

    if question.strip():

        with st.spinner("Searching..."):

            results = retriever.search(
                question,
                n_results=5
            )

        st.subheader("Retrieved Documents")

        docs = results.get("documents", [[]])[0]

        if len(docs) == 0:

            st.error("No documents retrieved.")

        else:

            for i, doc in enumerate(docs, start=1):

                st.markdown(f"### Chunk {i}")

                st.code(doc)

            context = "\n\n".join(docs)

            answer = llm.generate_answer(
                question,
                context
            )

            st.subheader("Answer")

            st.success(answer)