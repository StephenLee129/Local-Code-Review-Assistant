import ollama

from ollama import ResponseError
from pydantic import ValidationError

from .models import CodeReview
from .prompts import SYSTEM_PROMPT


MODEL_NAME = "qwen2.5-coder:7b"


class CodeAnalysisError(Exception):
    """Raised when code analysis fails."""


def analyze_code(code: str) -> CodeReview:
    """
    Submit source code to the local LLM and return a validated code review.
    """
    try:
        response = ollama.chat(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": f"Review the following source code:\n\n{code}"
                }
            ],
            format=CodeReview.model_json_schema()
        )

        return CodeReview.model_validate_json(response.message.content)

    except (ResponseError, ValidationError) as error:
        raise CodeAnalysisError(
            "Unable to generate a valid code review."
        ) from error

    except Exception as error:
        raise CodeAnalysisError(
            "An unexpected error occurred during code analysis."
        ) from error