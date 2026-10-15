import io
import unittest

from app import app


class AppTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_compares_resume_and_job_text(self):
        response = self.client.post("/", data={
            "resume": "Python and JavaScript",
            "jd": "Python and SQL",
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Skill coverage", response.data)
        self.assertIn(b"python", response.data)

    def test_requires_both_text_inputs(self):
        response = self.client.post("/", data={"resume": "Python", "jd": ""})
        self.assertIn(b"Provide both resume content", response.data)

    def test_rejects_non_pdf_upload(self):
        response = self.client.post("/", data={
            "resume_file": (io.BytesIO(b"not a pdf"), "resume.txt"),
            "jd": "Python",
        }, content_type="multipart/form-data")
        self.assertIn(b"Upload a PDF file", response.data)


if __name__ == "__main__":
    unittest.main()
