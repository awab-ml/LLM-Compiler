"""Configuration utilities for LLMs."""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv()


def get_llm(model: str = None, temperature: float = 0.0) -> ChatOpenAI:
    """Get a configured LLM instance.
    
    Args:
        model: Model name (defaults to DEFAULT_MODEL from env)
        temperature: Temperature for generation
    
    Returns:
        Configured ChatOpenAI instance
    """
    if model is None:
        model = os.getenv("DEFAULT_MODEL", "gpt-4o")
    
    return ChatOpenAI(
        model=model,
        temperature=temperature,
        api_key=os.getenv("OPENAI_API_KEY")
    )


def get_planner_llm() -> ChatOpenAI:
    """Get LLM configured for planning tasks.
    
    Returns:
        Configured ChatOpenAI instance for planning
    """
    model = os.getenv("PLANNER_MODEL", "gpt-4-turbo-preview")
    return get_llm(model=model, temperature=0.0)


def get_joiner_llm() -> ChatOpenAI:
    """Get LLM configured for joining/synthesizing results.
    
    Returns:
        Configured ChatOpenAI instance for joining
    """
    model = os.getenv("JOINER_MODEL", "gpt-4o")
    return get_llm(model=model, temperature=0.0)
