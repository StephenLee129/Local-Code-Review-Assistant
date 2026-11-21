def evaluate_findings(expected_findings: list[dict], detected_ids: list[str]) -> dict:
    """
    Compare manually identified model findings against expected findings.
    """

    expected_ids = {
        finding["id"] for finding in expected_findings
    }

    detected_ids = set(detected_ids)

    true_positives = expected_ids & detected_ids
    false_positives = detected_ids - expected_ids
    false_negatives = expected_ids - detected_ids

    precision_denominator = len(true_positives) + len(false_positives)
    recall_denominator = len(true_positives) + len(false_negatives)

    precision = (
        len(true_positives) / precision_denominator
        if precision_denominator
        else 0
    )

    recall = (
        len(true_positives) / recall_denominator
        if recall_denominator
        else 0
    )

    f1_score = (
        2 * precision * recall / (precision + recall)
        if precision + recall
        else 0
    )

    return {
        "true_positives": sorted(true_positives),
        "false_positives": sorted(false_positives),
        "false_negatives": sorted(false_negatives),
        "precision": precision,
        "recall": recall,
        "f1_score": f1_score,
    }