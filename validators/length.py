def validate_length(text: str, min_length: int) -> dict:
    if not text:
        return {"passed": False, "reason": "Empty response"}

    if len(text) < min_length:
        return {
            "passed": False,
            "reason": f"Response too short ({len(text)} < {min_length})"
        }

    return {"passed": True, "reason": "OK"}
