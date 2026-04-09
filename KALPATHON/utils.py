import re
from typing import Literal, Tuple

RiskLevel = Literal["Low", "Medium", "High"]


def _normalize_whitespace(s: str) -> str:
    s = s.replace("\r\n", "\n").replace("\r", "\n")
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


def clean_model_output(decoded: str) -> str:
    """
    Cleaning rules (as required):
    - Remove everything before "Explanation:"
    - Remove everything after "###" if present
    - Return the remaining text (trimmed)
    """
    text = decoded
    if "Explanation:" in text:
        text = text.split("Explanation:", 1)[1]
    if "###" in text:
        text = text.split("###", 1)[0]
    return _normalize_whitespace(text)


def extract_risk_level(text: str) -> Tuple[RiskLevel, str]:
    """
    Tries to extract risk level from model output text and returns:
    (risk_level, explanation_without_risk_prefix_if_present)
    """
    t = _normalize_whitespace(text)

    # Common patterns from fine-tuned outputs.
    patterns = [
        r"^\s*(Low|Medium|High)\s*Risk\s*[:\-]\s*(.*)$",
        r"^\s*(Low|Medium|High)\s*[:\-]\s*(.*)$",
        r"^\s*Risk\s*Level\s*[:\-]\s*(Low|Medium|High)\s*[,\-:]*\s*(.*)$",
        r"^\s*Risk\s*[:\-]\s*(Low|Medium|High)\s*[,\-:]*\s*(.*)$",
    ]
    for pat in patterns:
        m = re.match(pat, t, flags=re.IGNORECASE | re.DOTALL)
        if m:
            if len(m.groups()) == 2:
                g1, g2 = m.group(1), m.group(2)
                level = g1.capitalize()
                expl = g2.strip() if g2 else ""
            else:
                continue
            if level in ("Low", "Medium", "High"):
                return level, expl or t

    # Fallback: keyword search anywhere.
    if re.search(r"\bHigh\s*Risk\b", t, flags=re.IGNORECASE):
        return "High", t
    if re.search(r"\bMedium\s*Risk\b", t, flags=re.IGNORECASE):
        return "Medium", t
    if re.search(r"\bLow\s*Risk\b", t, flags=re.IGNORECASE):
        return "Low", t

    # If the model omitted risk, default to Medium for safety in demo.
    return "Medium", t


def format_final_answer(risk: RiskLevel, explanation: str) -> str:
    explanation = _normalize_whitespace(explanation)
    return f"{risk} Risk: {explanation}"

