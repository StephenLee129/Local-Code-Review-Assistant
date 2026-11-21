from fastapi.testclient import TestClient

from backend.app import main


client = TestClient(main.app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_review_code(monkeypatch):
    def mock_analyze_code(code):
        return {
            "summary": "One issue found.",
            "issues": [
                {
                    "title": "Division by zero",
                    "severity": "high",
                    "description": "The denominator could be zero.",
                    "suggestion": "Check the denominator before dividing.",
                    "line_number": 2
                }
            ]
        }

    monkeypatch.setattr(main, "analyze_code", mock_analyze_code)

    response = client.post(
        "/review",
        json={"code": "def divide(a, b): return a / b"}
    )

    assert response.status_code == 200
    assert response.json()["summary"] == "One issue found."
    assert len(response.json()["issues"]) == 1


def test_review_code_rejects_empty_input():
    response = client.post("/review", json={"code": "   "})

    assert response.status_code == 422


def test_review_code_handles_analysis_error(monkeypatch):
    def mock_analyze_code(code):
        raise main.CodeAnalysisError("Ollama is unavailable.")

    monkeypatch.setattr(main, "analyze_code", mock_analyze_code)

    response = client.post(
        "/review",
        json={"code": "print('hello')"}
    )

    assert response.status_code == 503
    assert response.json()["detail"] == "Ollama is unavailable."