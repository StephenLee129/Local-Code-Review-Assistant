import pytest
from pydantic import ValidationError

from backend.app.models import CodeIssue, CodeReview


def test_valid_code_review():
    review = CodeReview(
        summary="One issue found.",
        issues=[
            CodeIssue(
                title="Division by zero",
                severity="high",
                description="The denominator could be zero.",
                suggestion="Check the denominator before dividing.",
                line_number=2
            )
        ]
    )

    assert review.summary == "One issue found."
    assert len(review.issues) == 1
    assert review.issues[0].severity == "high"


def test_invalid_severity():
    with pytest.raises(ValidationError):
        CodeIssue(
            title="Test issue",
            severity="urgent",
            description="Test description",
            suggestion="Test suggestion"
        )


def test_empty_review():
    review = CodeReview(summary="No issues found.")

    assert review.issues == []
