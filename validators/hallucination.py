import re
from typing import List

# Patterns that often indicate hallucinated authority or specifics
SUSPICIOUS_PATTERNS = [
    r"\brfc\s?\d+\b",
    r"\biso\/iec\b",
    r"\bnist\b",
    r"\baccording to\b",
    r"\bofficially\b",
    r"\bmandated by\b",
]

def extract_entities(text: str) -> List[str]:
    """
    Extract capitalized words / phrases that look like named entities.
    Simple heuristic, production-friendly.
    """
    return re.findall(r"\b[A-Z][a-zA-Z0-9\-]{2,}\b", text)


def validate_hallucination(
    response_text: str,
    input_text: str,
    allowed_entities: List[str] | None = None
) -> dict:
    """
    Flags hallucinations when the model introduces new entities
    or authoritative claims not present in input.
    """
    if not response_text:
        return {"passed": False, "reason": "Empty response"}

    input_entities = set(extract_entities(input_text))
    response_entities = set(extract_entities(response_text))

    allowed_entities = set(allowed_entities or [])

    new_entities = response_entities - input_entities - allowed_entities

    suspicious_claims = [
        p for p in SUSPICIOUS_PATTERNS
        if re.search(p, response_text.lower())
    ]

    if new_entities:
        return {
            "passed": False,
            "reason": f"New unexplained entities introduced: {list(new_entities)[:5]}"
        }

    if suspicious_claims:
        return {
            "passed": False,
            "reason": f"Suspicious authoritative claims detected: {suspicious_claims}"
        }

    return {"passed": True, "reason": "OK"}
