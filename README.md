# TalentMatch

A small Flask application that compares skills mentioned in a job description with skills detected in pasted resume text or a text-based PDF.

## How matching works

The app loads a curated vocabulary from `skills.txt`, detects whole-word skill phrases in the job description, then checks which of those phrases also appear in the resume. The displayed percentage is the share of detected job-description skills also detected in the resume. It is a transparent keyword-coverage heuristic; it does not use TF-IDF, cosine similarity, an LLM, or a trained model, and it should not be used to make hiring decisions.

Common aliases are normalized in `matcher.py`. This is intentionally a small, explainable demo and may miss synonyms, context, negation, or skills absent from the vocabulary.

## Run locally

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000. Use resume text or upload a PDF up to 5 MB. Only PDFs with selectable text are supported; scanned documents need OCR, which is not included.

## Tests

```bash
python -m unittest discover -s tests -v
```

The tests cover alias and whole-word matching, empty input, form validation, and unsupported file types.

## Privacy and limitations

This prototype processes submitted content in the running Flask process and does not intentionally persist it. Do not deploy with real personal data without adding appropriate security, privacy controls, operational protections, and a review of applicable requirements. The built-in development server is not intended for production.
