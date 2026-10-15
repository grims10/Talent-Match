from io import BytesIO
from pathlib import Path

from flask import Flask, render_template, request
from pypdf import PdfReader

from matcher import analyze_match

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024


@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    error = None
    resume_text = ""
    jd_text = ""

    if request.method == "POST":
        resume_text = request.form.get("resume", "").strip()
        jd_text = request.form.get("jd", "").strip()
        uploaded = request.files.get("resume_file")

        if uploaded and uploaded.filename:
            if Path(uploaded.filename).suffix.lower() != ".pdf":
                error = "Upload a PDF file, or paste resume text below."
            else:
                try:
                    reader = PdfReader(BytesIO(uploaded.read()))
                    resume_text = "\n".join(page.extract_text() or "" for page in reader.pages).strip()
                    if not resume_text:
                        error = "No selectable text was found in that PDF. Paste the resume text instead."
                except Exception:
                    error = "Could not read that PDF. Try another PDF or paste the resume text."

        if not error and (not resume_text or not jd_text):
            error = "Provide both resume content and a job description."
        elif not error:
            result = analyze_match(resume_text, jd_text)
            if not result["job_skills"]:
                error = "No skills from the project's skill list were detected in the job description."
                result = None

    return render_template("index.html", result=result, error=error,
                           resume=resume_text, jd=jd_text)


@app.errorhandler(413)
def file_too_large(_error):
    return render_template("index.html", result=None,
                           error="The upload is too large. PDFs must be 5 MB or smaller.",
                           resume="", jd=""), 413


if __name__ == "__main__":
    app.run(debug=False)
