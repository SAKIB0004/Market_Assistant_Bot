import re

ACTIONABLE_PATTERNS = [
    r"\byou should (buy|sell|hold)\b",
    r"\bi recommend\b",
    r"\bmy recommendation\b",
    r"\benter at\b",
    r"\bexit at\b",
    r"\btarget (price)?\b",
    r"\bstop[- ]loss\b",
    r"\bbuy now\b",
    r"\bsell now\b",
    r"\bstrong (buy|sell)\b",
    r"\btop pick\b",
    r"\bbest stock\b",
]

REFUSAL = (
    "I can’t help with buy/sell recommendations, stock tips, or personalized investing advice.\n\n"
    "If you want, I *can* teach a simple evaluation framework (business, valuation, risk, diversification) "
    "or explain concepts like ETFs, SIPs, and risk management.\n\n"
    "Educational purposes only — not investment advice."
)

def enforce_output_safety(text: str) -> str:
    lower = text.lower()
    if any(re.search(p, lower) for p in ACTIONABLE_PATTERNS):
        return REFUSAL
    return text
