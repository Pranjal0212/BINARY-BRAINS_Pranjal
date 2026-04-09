from __future__ import annotations

import torch

from model_loader import load_model
from utils import clean_model_output, extract_risk_level, format_final_answer


@torch.inference_mode()
def generate_response(text: str) -> str:
    """
    Required behavior:
    - Prompt: "Clause: <input>\\nExplanation:"
    - model.generate(max_new_tokens=60, do_sample=False, eos_token_id=tokenizer.eos_token_id)
    - Cleaning:
      - Remove everything before "Explanation:"
      - Remove everything after "###" if present
    - Return: "<Risk Level>: <Explanation>" (we return "<Risk> Risk: <Explanation>")
    """
    tokenizer, model = load_model()

    clause = (text or "").strip()
    prompt = f"Clause: {clause}\nExplanation:"

    inputs = tokenizer(prompt, return_tensors="pt")
    inputs = {k: v.to(model.device) for k, v in inputs.items()}

    outputs = model.generate(
        **inputs,
        max_new_tokens=60,
        do_sample=False,
        eos_token_id=tokenizer.eos_token_id,
        pad_token_id=tokenizer.pad_token_id,
    )

    decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)
    cleaned = clean_model_output(decoded)
    risk, explanation = extract_risk_level(cleaned)
    return format_final_answer(risk, explanation)