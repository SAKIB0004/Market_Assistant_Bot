import re

ADVICE_PATTERNS = [
    r"\bwhich stock\b",
    r"\bwhat stock\b",
    r"\bbest stock\b",
    r"\bpick\b",
    r"\brecommend\b",
    r"\bintraday\b",
    r"\btoday buy\b",
    r"\bshould i buy\b",
    r"\bshould i sell\b",
    r"\btarget price\b",
    r"\bentry\b|\bexit\b",
]

COMMENTARY_PATTERNS = [
    r"\bwhy (is|are) the market\b",
    r"\bmarket (down|up)\b",
    r"\btoday's news\b|\bsummarize (today|todays)\b",
    r"\bwhat happened today\b",
]

def detect_mode(user_text: str) -> str:
    t = user_text.lower().strip()

    if any(re.search(p, t) for p in ADVICE_PATTERNS):
        return "GUARDRAIL"
    if any(re.search(p, t) for p in COMMENTARY_PATTERNS):
        return "COMMENTARY"
    return "COACH"
