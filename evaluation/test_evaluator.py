
import pytest

from evaluation.evaluator import evaluate_findings


EXPECTED_FINDINGS = [
    {"id": "issue_1", "description": "First issue"},
    {"id": "issue_2", "description": "Second issue"},
    {"id": "issue_3", "description": "Third issue"},
]


def test_perfect_evaluation():
    results = evaluate_findings(
        EXPECTED_FINDINGS,
        ["issue_1", "issue_2", "issue_3"],
    )

    assert results["precision"] == 1.0
    assert results["recall"] == 1.0
    assert results["f1_score"] == 1.0


def test_partial_evaluation():
    results = evaluate_findings(
        EXPECTED_FINDINGS,
        ["issue_1", "issue_2"],
    )

    assert results["precision"] == 1.0
    assert results["recall"] == pytest.approx(2 / 3)
    assert results["f1_score"] == pytest.approx(0.8)


def test_false_positive():
    results = evaluate_findings(
        EXPECTED_FINDINGS,
        ["issue_1", "unexpected_issue"],
    )

    assert results["true_positives"] == ["issue_1"]
    assert results["false_positives"] == ["unexpected_issue"]
    assert results["false_negatives"] == ["issue_2", "issue_3"]

    assert results["precision"] == 0.5
    assert results["recall"] == pytest.approx(1 / 3)


def test_no_detected_findings():
    results = evaluate_findings(
        EXPECTED_FINDINGS,
        [],
    )

    assert results["precision"] == 0
    assert results["recall"] == 0
    assert results["f1_score"] == 0


def test_no_expected_findings():
    results = evaluate_findings(
        [],
        ["unexpected_issue"],
    )

    assert results["precision"] == 0
    assert results["recall"] == 0
    assert results["f1_score"] == 0
