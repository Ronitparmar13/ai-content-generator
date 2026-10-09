"""Application configuration for AI Content Generator."""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()
    GROQ_MODEL = os.getenv(
        "GROQ_MODEL",
        "openai/gpt-oss-20b",
    ).strip()

    MAX_OUTPUT_TOKENS = 2500
    MAX_TOPIC_CHARS = 500
    MAX_SOURCE_CHARS = 25000
    MAX_INSTRUCTIONS_CHARS = 2000

    ALLOWED_CONTENT_TYPES = {
        "blog_post",
        "social_caption",
        "summary",
    }

    ALLOWED_TONES = {
        "professional",
        "casual",
        "creative",
        "persuasive",
        "friendly",
        "informative",
    }

    ALLOWED_LENGTHS = {
        "short",
        "medium",
        "long",
    }

    SECRET_KEY = os.getenv(
        "FLASK_SECRET_KEY",
        "local-development-only-change-before-deployment",
    )