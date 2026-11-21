from pydantic import BaseModel, Field
from typing import Literal
from pydantic import BaseModel, Field, field_validator


class CodeReviewRequest(BaseModel):
    """Request containing source code to review."""

    code: str = Field(
        min_length=1,
        description="Source code to analyze"
    )

    @field_validator("code")
    @classmethod
    def validate_code(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Code cannot be empty or whitespace.")

        return value


class CodeIssue(BaseModel):
    """Represents an individual issue found during code review."""

    title: str = Field(description="Short title describing the issue")
    severity: Literal["critical", "high", "medium", "low"] = Field(
        description="Severity level of the issue"
    )
    description: str = Field(
        description="Explanation of the issue and why it matters"
    )
    suggestion: str = Field(
        description="Recommended way to fix or improve the code"
    )
    line_number: int | None = Field(
        default=None,
        description="Approximate line number where the issue occurs, if known"
    )


class CodeReview(BaseModel):
    """Represents the complete result of a code review."""

    summary: str = Field(
        description="Brief overview of the code review"
    )
    issues: list[CodeIssue] = Field(
        default_factory=list,
        description="Issues identified during the review"
    )
