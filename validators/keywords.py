def validate_keywords(text: str, required_keywords: list[str]) -> dict:
    missing = [
        kw for kw in required_keywords
        if kw.lower() not in text.lower()
    ]

    if missing:
        return {
            "passed": False,
            "reason": f"Missing keywords: {', '.join(missing)}"
        }

    return {"passed": True, "reason": "OK"}
