"""Transparent, dictionary-based resume and job-description comparison."""

import re
from pathlib import Path

SKILL_FILE = Path(__file__).with_name("skills.txt")
SKILLS = tuple(
    sorted({line.strip().lower() for line in SKILL_FILE.read_text(encoding="utf-8").splitlines()
    if line.strip()}, key=lambda value: (-len(value), value))
)

# Normalize common variants before matching. Keep this explicit and reviewable.
ALIASES = {
    "js": "javascript",
    "node js": "node.js",
    "postgres": "postgresql",
}


def _normalize(text: str) -> str:
    text = text.lower()
    for alias, canonical in ALIASES.items():
        text = re.sub(r"(?<!\w)" + re.escape(alias) + r"(?!\w)", canonical, text)
    return text


def _contains(text: str, phrase: str) -> bool:
    if phrase == "c":
        return bool(re.search(r"(?<!\w)c(?![\w+#])", text))
    return bool(re.search(r"(?<!\w)" + re.escape(phrase) + r"(?!\w)", text))


def analyze_match(resume: str, job_description: str) -> dict:
    """Return detected skills and a transparent coverage percentage.

    This is a dictionary-based heuristic, not a prediction of hiring outcomes.
    """
    resume_norm = _normalize(resume)
    jd_norm = _normalize(job_description)
    job_skills = [skill for skill in SKILLS if _contains(jd_norm, skill)]
    matched = [skill for skill in job_skills if _contains(resume_norm, skill)]
    missing = [skill for skill in job_skills if skill not in matched]
    score = round(100 * len(matched) / len(job_skills), 1) if job_skills else None
    return {
        "score": score,
        "matched": matched,
        "missing": missing,
        "job_skills": job_skills,
        "coverage": f"{len(matched)} of {len(job_skills)} detected skills",
    }
