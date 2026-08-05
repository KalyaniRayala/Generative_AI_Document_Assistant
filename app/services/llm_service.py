from groq import Groq
from openai import OpenAI  # used for OpenRouter + DeepSeek (both OpenAI-compatible APIs)
import google.generativeai as genai

from app import config


SYSTEM_PROMPT = """
You are a Retrieval-Augmented Generation (RAG) document assistant.

Answer the user's question using ONLY the retrieved document context
provided with the current question.

Rules:
1. The retrieved document context is the only source of truth.
2. Do not use previous answers or conversation history as factual evidence.
3. If the user selects a specific document, answer only from that document.
4. Never mix information from different documents.
5. If the answer cannot be found in the retrieved context, respond:
   "I couldn't find that information in the selected document."
6. Do not guess or invent information.
7. Give a concise and accurate answer.
"""


class BaseLLMProvider:
    def generate_answer(self, prompt: str, context: str) -> str:
        raise NotImplementedError


class GroqProvider(BaseLLMProvider):
    def __init__(self, model: str = None):
        self.client = Groq(api_key=config.GROQ_API_KEY)
        self.model = model or config.PROVIDER_MODELS["groq"]

    def generate_answer(self, prompt: str, context: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"{context}\n\nQuestion: {prompt}"},
            ],
            temperature=0.3,
        )
        return response.choices[0].message.content


class GeminiProvider(BaseLLMProvider):
    def __init__(self, model: str = None):
        genai.configure(api_key=config.GEMINI_API_KEY)
        self.model_name = model or config.PROVIDER_MODELS["gemini"]
        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            system_instruction=SYSTEM_PROMPT,
        )

    def generate_answer(self, prompt: str, context: str) -> str:
        response = self.model.generate_content(
            f"{context}\n\nQuestion: {prompt}"
        )
        return response.text


class OpenRouterProvider(BaseLLMProvider):
    def __init__(self, model: str = None):
        self.client = OpenAI(
            api_key=config.OPENROUTER_API_KEY,
            base_url="https://openrouter.ai/api/v1",
        )
        self.model = model or config.PROVIDER_MODELS["openrouter"]

    def generate_answer(self, prompt: str, context: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"{context}\n\nQuestion: {prompt}"},
            ],
            temperature=0.3,
        )
        return response.choices[0].message.content


class DeepSeekProvider(BaseLLMProvider):
    def __init__(self, model: str = None):
        self.client = OpenAI(
            api_key=config.DEEPSEEK_API_KEY,
            base_url="https://api.deepseek.com",
        )
        self.model = model or config.PROVIDER_MODELS["deepseek"]

    def generate_answer(self, prompt: str, context: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"{context}\n\nQuestion: {prompt}"},
            ],
            temperature=0.3,
        )
        return response.choices[0].message.content


PROVIDER_REGISTRY = {
    "groq": GroqProvider,
    "gemini": GeminiProvider,
    "openrouter": OpenRouterProvider,
    "deepseek": DeepSeekProvider,
}


class LLMService:
    """
    Router that picks a provider adapter based on `provider` (and optional
    `model` override). Usage stays the same as before:
        llm = LLMService(provider="groq")
        llm.generate_answer(prompt, context)
    """

    def __init__(self, provider: str = None, model: str = None):
        provider = provider or config.DEFAULT_PROVIDER
        if provider not in PROVIDER_REGISTRY:
            raise ValueError(
                f"Unknown provider '{provider}'. "
                f"Choose from: {list(PROVIDER_REGISTRY.keys())}"
            )
        self._impl = PROVIDER_REGISTRY[provider](model=model)
        self.provider = provider
        self.model = model or config.PROVIDER_MODELS[provider]

    def generate_answer(self, prompt: str, context: str) -> str:
        try:
            return self._impl.generate_answer(prompt, context)
        except Exception as e:
            return f"⚠️ Error from {self.provider} ({self.model}): {str(e)}"