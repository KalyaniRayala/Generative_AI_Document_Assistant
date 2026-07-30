from app.services.retriever_service import RetrieverService
from app.services.llm_service import LLMService


def main():

    retriever = RetrieverService()
    llm = LLMService()

    print("=" * 60)
    print("🤖 AI Document Assistant")
    print("Type 'exit' to quit.")
    print("=" * 60)

    while True:

        question = input("\n👤 You: ").strip()

        if question.lower() in ["exit", "quit"]:
            print("\n👋 Goodbye!")
            break

        if question == "":
            print("Please enter a question.")
            continue

        print("\n🔍 Searching documents...")

        results = retriever.search(
            query=question,
            n_results=3
        )

        documents = results["documents"][0]

        context = "\n\n".join(documents)

        print("🤖 Generating answer...\n")

        answer = llm.generate_answer(
            question=question,
            context=context
        )

        print("=" * 60)
        print("🤖 AI:")
        print(answer)
        print("=" * 60)


if __name__ == "__main__":
    main()