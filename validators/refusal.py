REFUSAL_PATTERNS = [
    "i can't help",
    "i cannot help",
    "as an ai language model",
    "i’m not able to",
]

def validate_refusal(text: str) -> dict:
    lowered = text.lower()

    for pattern in REFUSAL_PATTERNS:
        if pattern in lowered:
            return {
                "passed": False,
                "reason": f"Refusal detected: '{pattern}'"
            }

    return {"passed": True, "reason": "OK"}
