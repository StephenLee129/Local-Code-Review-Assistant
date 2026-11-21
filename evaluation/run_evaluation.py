from evaluation.evaluator import evaluate_findings
from evaluation.payment_processing import EXPECTED_FINDINGS


# Findings identified in our latest Qwen review.
detected_ids = [
    "hardcoded_api_key",
    "negative_payment",
    "missing_none_handling",
    "unused_import",
]


results = evaluate_findings(
    expected_findings=EXPECTED_FINDINGS,
    detected_ids=detected_ids,
)

print("Evaluation Results:")
print(results)