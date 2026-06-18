from flask import Flask, render_template, request
import re

app = Flask(__name__)

with open("skills.txt", encoding="utf-8") as f:
    SKILLS = [s.strip().lower() for s in f if s.strip()]

SKILLS = [skill for skill in SKILLS if len(skill) > 2]


@app.route("/", methods=["GET", "POST"])
def home():

    score = None
    matched = []
    missing = []
    recommendation = ""
    level = ""

    if request.method == "POST":

        resume = request.form["resume"].lower()
        jd = request.form["jd"].lower()

        jd_skills = []

        for skill in SKILLS:

            if " " in skill:
                if skill in jd:
                    jd_skills.append(skill)

            else:
                pattern = r"\b" + re.escape(skill) + r"\b"

                if re.search(pattern, jd):
                    jd_skills.append(skill)


        jd_skills = list(set(jd_skills))


        for skill in jd_skills:

            if " " in skill:
                # Multi-word skills
                if skill in resume:
                    matched.append(skill)
                else:
                    missing.append(skill)

            else:
                # Exact word match for single-word skills
                pattern = r"\b" + re.escape(skill) + r"\b"

                if re.search(pattern, resume):
                    matched.append(skill)
                else:
                    missing.append(skill)


        if len(jd_skills) > 0:
            score = round((len(matched) / len(jd_skills)) * 100, 2)
        else:
            score = 0


        if score >= 80:
            level = "Excellent Match"

        elif score >= 60:
            level = "Good Match"

        elif score >= 40:
            level = "Average Match"

        else:
            level = "Weak Match"


        if missing:

            top_missing = missing[:10]

            recommendation = (
                "Consider adding projects, certifications, or experience involving: "
                + ", ".join(top_missing)
            )

        else:

            recommendation = (
                "Great fit! Your resume covers all major skills from the job description."
            )

    return render_template(
        "index.html",
        score=score,
        matched=sorted(matched),
        missing=sorted(missing),
        recommendation=recommendation,
        level=level
    )


if __name__ == "__main__":
    app.run(debug=True)