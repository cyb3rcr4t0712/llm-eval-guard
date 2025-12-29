from typing import List, Dict

def score_validations(results: List[Dict]) -> Dict:
    score = 0
    max_score = len(results)

    reasons = []

    for r in results:
        if r["passed"]:
            score += 1
        else:
            reasons.append(r["reason"])

    return {
        "score": score,
        "max_score": max_score,
        "passed": score == max_score,
        "failures": reasons,
    }
