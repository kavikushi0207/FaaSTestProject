import json
import re
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

BASE_DIR = Path(__file__).resolve().parent

with open(BASE_DIR / "skills.json", "r", encoding="utf-8") as file:
    SKILL_KEYWORDS = json.load(file)

with open(BASE_DIR / "skill_aliases.json", "r", encoding="utf-8") as file:
    SKILL_ALIASES = json.load(file)

SKILL_SCORE_WEIGHT = 0.7
TFIDF_SCORE_WEIGHT = 0.3


def contains_skill(text, skill):
    pattern = r"(?<![a-zA-Z0-9+#.])" + re.escape(skill) + r"(?![a-zA-Z0-9+#.])"
    return re.search(pattern, text) is not None


def extract_skills(text):
    text_lower = text.lower()
    found_skills = set()

    for skill in SKILL_KEYWORDS:
        if contains_skill(text_lower, skill):
            found_skills.add(skill)

    for alias, standard_skill in SKILL_ALIASES.items():
        if contains_skill(text_lower, alias):
            found_skills.add(standard_skill)

    return sorted(found_skills)


def format_skill_name(skill):
    special_names = {
        "ci/cd": "CI/CD",
        "nlp": "NLP",
        "aws": "AWS",
        "azure": "Azure",
        "gcp": "GCP",
        "api gateway": "API Gateway",
        "rest api": "REST API",
    }
    return special_names.get(skill, skill.title())


def build_match_summary(matched_skills, missing_skills):
    if matched_skills and missing_skills:
        matched_text = ", ".join(format_skill_name(skill) for skill in matched_skills)
        missing_text = ", ".join(format_skill_name(skill) for skill in missing_skills)
        return f"Candidate matches {matched_text}, but is missing {missing_text}."

    if matched_skills and not missing_skills:
        matched_text = ", ".join(format_skill_name(skill) for skill in matched_skills)
        return f"Candidate matches all detected JD skills: {matched_text}."

    if not matched_skills and missing_skills:
        missing_text = ", ".join(format_skill_name(skill) for skill in missing_skills)
        return f"Candidate is missing the detected JD skills: {missing_text}."

    return "No known technical skills were detected in the job description."


def validate_match_request(req_body):
    if not isinstance(req_body, dict):
        return "Request body must be a JSON object."

    resume_text = req_body.get("resume")
    jd_text = req_body.get("jd")

    if resume_text is None:
        return "Missing required field: resume."

    if jd_text is None:
        return "Missing required field: jd."

    if not isinstance(resume_text, str):
        return "Field 'resume' must be a string."

    if not isinstance(jd_text, str):
        return "Field 'jd' must be a string."

    if not resume_text.strip():
        return "Field 'resume' cannot be empty."

    if not jd_text.strip():
        return "Field 'jd' cannot be empty."

    if len(resume_text.split()) < 5:
        return "Field 'resume' is too short. Please provide at least 5 words."

    if len(jd_text.split()) < 5:
        return "Field 'jd' is too short. Please provide at least 5 words."

    return None


def calculate_match_scores(resume_text, jd_text):
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)

    matched_skills = sorted(set(resume_skills) & set(jd_skills))
    missing_skills = sorted(set(jd_skills) - set(resume_skills))
    summary = build_match_summary(matched_skills, missing_skills)

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([resume_text, jd_text])
    tfidf_score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0] * 100

    if jd_skills:
        skill_score = (len(matched_skills) / len(jd_skills)) * 100
    else:
        skill_score = 0

    match_score = (SKILL_SCORE_WEIGHT * skill_score) + (TFIDF_SCORE_WEIGHT * tfidf_score)

    return {
        "match_score": round(match_score, 2),
        "tfidf_score": round(tfidf_score, 2),
        "skill_score": round(skill_score, 2),
        "summary": summary,
    }
