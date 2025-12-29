# LLM Eval Guard

LLM Eval Guard is a lightweight evaluation framework that detects
quality regressions in LLM outputs when prompts or models change.

It is designed to catch silent failures such as:
- Loss of critical information
- Over-simplified or incomplete responses
- Hallucinated technical details
- Unsafe or ungrounded claims

This mirrors real-world AI reliability and QA problems faced by teams
deploying LLM-powered features.

---

## Why This Exists

Prompt changes are frequent in production systems.
Small edits intended to “simplify” or “shorten” prompts often
silently degrade output quality.

This project answers one question:

**Did this change make the AI worse?**

---

## What It Does

- Runs the same dataset against multiple prompt versions
- Evaluates outputs using deterministic validators
- Scores responses and detects regressions
- Produces a structured report for debugging and review
- Supports both cloud and local LLMs (via Ollama)

---

## Evaluation Signals

The framework checks for:
- Minimum response completeness
- Required domain keywords
- Refusal or non-answer patterns
- Hallucinated or ungrounded technical entities
- Regression between prompt versions

---

## Example Output

```json
{
  "id": 2,
  "regression": true,
  "v1_score": { "score": 3, "max_score": 4 },
  "v2_score": { "score": 2, "max_score": 4 }
}
