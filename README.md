# 🚦 LLM Eval Guard

![Python](https://img.shields.io/badge/python-3.11-blue)
![License](https://img.shields.io/badge/license-MIT-green)

**Prevent silent AI failures before they hit production**

LLM Eval Guard is a lightweight, production-minded evaluation framework that detects quality regressions in LLM outputs when prompts, datasets, or models change. 

---

## 🔥 Why This Exists

In real products, prompts evolve, models update, and teams "optimize" responses — but most teams don't test LLM outputs like code.  Failures slip into production silently. 

**This project answers one question:  Did this change make the AI worse?**

| Failure Type | Description |
|--------------|-------------|
| 🔻 Information Loss | Critical details missing from responses |
| 📉 Over-simplification | Incomplete or shallow answers |
| 🎭 Hallucinations | Fabricated technical details |
| 🔄 Behavioral Drift | Inconsistent behavior after updates |

---

## 🧭 How It Works

```
┌─────────────┐
│   Dataset   │
└──────┬──────┘
       │
       ▼
┌──────────────────────────────────────────┐
│                                          │
│  ┌─────────┐           ┌─────────┐       │
│  │Prompt v1│           │Prompt v2│       │
│  └────┬────┘           └────┬────┘       │
│       ▼                     ▼            │
│  ┌─────────┐           ┌─────────┐       │
│  │   LLM   │           │   LLM   │       │
│  └────┬────┘           └────┬────┘       │
│       ▼                     ▼            │
│  ┌──────────┐         ┌──────────┐       │
│  │Validators│         │Validators│       │
│  └────┬─────┘         └────┬─────┘       │
│       ▼                    ▼             │
│  ┌─────────┐           ┌─────────┐       │
│  │ Score: 3│           │ Score: 2│       │
│  └─────────┘           └─────────┘       │
│                                          │
└──────────────────┬───────────────────────┘
                   ▼
          ┌────────────────┐
          │   Regression   │
          │    Detected!   │
          └────────────────┘
```

---

## ✅ What The Framework Does

- ✔️ Runs the same dataset across multiple prompt versions
- ✔️ Evaluates outputs using deterministic validators
- ✔️ Scores responses objectively
- ✔️ Flags regressions with structured JSON reports
- ✔️ Works with cloud + local models (Ollama supported)

---

## 🧠 Evaluation Signals

The framework validates responses for: 

- **Minimum completeness** — Is the response substantive?
- **Required domain keywords** — Does it cover expected concepts?
- **Refusal / non-answer patterns** — Did the model decline to answer?
- **Hallucinated entities** — Are there ungrounded claims? 
- **Regression score** — Is v2 measurably worse than v1? 

### Example Validator

Validators are simple and hackable:

```python
# validators/keywords.py
REQUIRED = ["authentication", "authorization", "token"]

def validate(response_text):
    text = response_text.lower()
    matches = sum(1 for keyword in REQUIRED if keyword in text)
    return {
        "passed": matches == len(REQUIRED),
        "score": matches,
        "max_score": len(REQUIRED),
        "missing": [k for k in REQUIRED if k not in text]
    }
```

---

## 📊 Example Regression Result

```json
{
  "id": 2,
  "regression":  true,
  "v1_score": { "score": 3, "max_score": 4 },
  "v2_score": { "score": 2, "max_score": 4 }
}
```

**Interpretation:** Prompt v2 produced a weaker answer than v1 → regression detected. 

---

## 🛠️ Tech Stack

- **Python**
- **Deterministic custom validators**
- **Supported LLM Providers:**
  - OpenAI
  - Google Gemini
  - Ollama (local LLMs)
- **CI-driven evaluation workflow**

---

## ▶️ Getting Started

### Installation

```bash
pip install -r requirements.txt
```

### Run Evaluation

```bash
python -m runner.run_eval
```

### Output

Reports are saved to: 
```
/reports/latest_report.json
```

---

## 📁 Project Structure

```
├── datasets/
│   └── eval_dataset.json     # Test cases
├── prompts/
│   ├── v1.txt                # Baseline prompt
│   └── v2.txt                # Updated prompt
├── validators/
│   ├── length.py             # Length / completeness checks
│   ├── keywords.py           # Domain keyword coverage
│   ├── refusal.py            # Non-answer detection
│   └── hallucination.py      # Ungrounded claim detection
├── runner/
│   └── run_eval.py           # Evaluation runner
└── reports/
    └── latest_report.json    # Generated reports
```

---

## 🔄 CI Integration

This repo includes GitHub Actions CI that automatically runs evaluation when:

- Prompts change
- Datasets change
- Validators change

**This prevents unnoticed regressions from entering `main`.**

CI enforces evaluation discipline without relying on manual review.

---

## 🎯 Real-World Use Cases

- **AI Feature QA** — Validate outputs before releases
- **Prompt Engineering Quality Gates** — Ensure prompt changes don't degrade quality
- **Model Upgrade Regression Checks** — Test new model versions safely
- **Enterprise Reliability Workflows** — Build trust in AI systems

---

## 🚀 Roadmap

- [ ] **Fail CI if regression score drops below threshold** ← Quality gates
- [ ] Human review mode for flagged edge cases
- [ ] Baseline locking for enterprise audit trails
- [ ] Richer validators (JSON/schema validation)
- [ ] Scoring dashboards with historical trends
- [ ] Multi-model comparison reports

---

## 📄 License

Apache License 2.0

---

## 🤝 Contributing

Contributions welcome! Please open an issue or PR. 