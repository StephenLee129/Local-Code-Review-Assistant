from fastapi import FastAPI, HTTPException

from .analyzer import CodeAnalysisError, analyze_code
from .models import CodeReview, CodeReviewRequest


app = FastAPI(
    title="Local Code Review Assistant",
    description="AI-powered code reviews using a locally hosted LLM.",
    version="1.0.0"
)


@app.get("/health")
def health_check():
    """Check whether the API is running."""
    return {"status": "ok"}


@app.post("/review", response_model=CodeReview)
def review_code(request: CodeReviewRequest) -> CodeReview:
    """Analyze submitted source code and return a structured review."""
    try:
        return analyze_code(request.code)

    except CodeAnalysisError as error:
        raise HTTPException(
            status_code=503,
            detail=str(error)
        ) from error