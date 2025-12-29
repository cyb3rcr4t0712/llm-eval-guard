import json
import yaml
import logging
from pathlib import Path

from validators.length import validate_length
from validators.keywords import validate_keywords
from validators.refusal import validate_refusal
from validators.hallucination import validate_hallucination
from validators.scoring import score_validations
from runner.utils import load_dataset


# ---------- Load Config ----------
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

# ---------- Logging ----------
Path("logs").mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    filename="logs/failures.log",
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# ---------- LLM Client Selection ----------
if config["llm"]["provider"] == "ollama":
    from llm.ollama_client import OllamaClient
    client = OllamaClient(model=config["llm"]["model"])

elif config["llm"]["provider"] == "gemini":
    from llm.gemini_client import GeminiClient
    client = GeminiClient(
        model=config["llm"]["model"],
        temperature=config["llm"]["temperature"],
    )

else:
    raise ValueError("Unsupported LLM provider")


# ---------- Load Data ----------
dataset = load_dataset("datasets/eval_dataset.json")

with open("prompts/v1.txt", "r", encoding="utf-8") as f:
    prompt_v1 = f.read().strip()

with open("prompts/v2.txt", "r", encoding="utf-8") as f:
    prompt_v2 = f.read().strip()

if not prompt_v1 or not prompt_v2:
    raise ValueError("Prompt files v1.txt or v2.txt are empty")

# ---------- Report ----------
report = {
    "summary": {
        "total_cases": len(dataset),
        "v1_failures": 0,
        "v2_failures": 0,
    },
    "details": []
}

# ---------- Evaluation Loop ----------
for item in dataset:
    outputs = {}

    for version, prompt in [("v1", prompt_v1), ("v2", prompt_v2)]:
        output = client.generate(prompt, item["input"])

        validations = [
            validate_length(output, config["evaluation"]["min_length"]),
            validate_keywords(output, config["evaluation"]["required_keywords"]),
            validate_refusal(output),
            validate_hallucination(
                response_text=output,
                input_text=item["input"],
                allowed_entities=config["evaluation"].get("allowed_entities", []),
            ),
        ]

        score = score_validations(validations)

        outputs[version] = {
            "text": output,
            "score": score,
        }

    if outputs["v2"]["score"]["score"] < outputs["v1"]["score"]["score"]:
        report["summary"]["v2_failures"] += 1

        regression = {
            "id": item["id"],
            "input": item["input"],
            "v1_score": outputs["v1"]["score"],
            "v2_score": outputs["v2"]["score"],
            "regression": True,
        }

        report["details"].append(regression)
        logging.error(f"REGRESSION: {regression}")

# ---------- Save Report ----------
Path("reports").mkdir(exist_ok=True)

with open("reports/latest_report.json", "w", encoding="utf-8") as f:
    json.dump(report, f, indent=2)

print("Evaluation complete. Report saved to reports/latest_report.json")
