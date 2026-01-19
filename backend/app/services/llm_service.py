# app/services/llm_service.py
from langchain_openai import ChatOpenAI
from app.config import settings


def get_llm() -> ChatOpenAI:
    """Create and return a configured OpenAI chat model."""

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.2,
        api_key=settings.openai_api_key,
    )

    return llm
