import os

from dotenv import load_dotenv
from groq import Groq


class LLMService:

    def __init__(self):

        load_dotenv()

        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError("GROQ_API_KEY not found in .env file.")

        self.client = Groq(
            api_key=api_key
        )

    def generate_answer(self, question: str, context: str):

        prompt = f"""
You are an expert AI assistant.

Answer ONLY using the provided context.

If the answer cannot be found in the context, reply exactly:

"I couldn't find the answer in the provided documents."

==========================
Context
==========================

{context}

==========================
Question
==========================

{question}

==========================
Answer
==========================
"""

        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You answer questions only from the supplied context."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0,
            max_tokens=512,
        )

        return response.choices[0].message.content