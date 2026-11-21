import json
from types import SimpleNamespace

import pytest

from backend.app import analyzer
from backend.app.models import CodeReview
from backend.app.prompts import SYSTEM_PROMPT


def test_analyze_code_returns_validated_review(monkeypatch):
    expected_review = {
        "summary": "No significant issues found.",
        "issues": []
    }

    def mock_chat(**kwargs):
        return SimpleNamespace(
            message=SimpleNamespace(
                content=json.dumps(expected_review)
            )
        )

    monkeypatch.setattr(analyzer.ollama, "chat", mock_chat)

    review = analyzer.analyze_code("print('hello')")

    assert isinstance(review, CodeReview)
    assert review.summary == expected_review["summary"]
    assert review.issues == []


def test_analyze_code_uses_expected_model_and_prompt(monkeypatch):
    captured_arguments = {}

    def mock_chat(**kwargs):
        captured_arguments.update(kwargs)

        return SimpleNamespace(
            message=SimpleNamespace(
                content='{"summary": "Looks good.", "issues": []}'
            )
        )

    monkeypatch.setattr(analyzer.ollama, "chat", mock_chat)

    analyzer.analyze_code("print('hello')")

    assert captured_arguments["model"] == analyzer.MODEL_NAME
    assert captured_arguments["messages"][0]["content"] == SYSTEM_PROMPT
    assert captured_arguments["format"] == CodeReview.model_json_schema()


def test_analyze_code_handles_invalid_model_response(monkeypatch):
    def mock_chat(**kwargs):
        return SimpleNamespace(
            message=SimpleNamespace(content="This is not valid JSON.")
        )

    monkeypatch.setattr(analyzer.ollama, "chat", mock_chat)

    with pytest.raises(analyzer.CodeAnalysisError):
        analyzer.analyze_code("print('hello')")