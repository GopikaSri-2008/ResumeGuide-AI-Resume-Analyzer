from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader
from docx import Document
import os
import re

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf", "docx"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Common technical skills
SKILLS = [
    "python", "java", "c", "c++", "html", "css", "javascript",
    "flask", "django", "sql", "mysql", "sqlite", "mongodb",
    "git", "github", "rest api", "api", "machine learning",
    "data science", "pandas", "numpy", "scikit-learn",
    "react", "node.js", "php", "excel", "powerpoint",
    "communication", "teamwork", "problem solving",
    "data structures", "oops", "object oriented programming"
]


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


def extract_pdf_text(filepath):
    text = ""

    reader = PdfReader(filepath)

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + " "

    return text


def extract_docx_text(filepath):
    document = Document(filepath)

    text = []

    for paragraph in document.paragraphs:
        text.append(paragraph.text)

    return " ".join(text)


def extract_text(filepath, extension):
    if extension == "pdf":
        return extract_pdf_text(filepath)

    if extension == "docx":
        return extract_docx_text(filepath)

    return ""


def find_skills(text):
    text = text.lower()
    found = []

    for skill in SKILLS:
        pattern = r"\b" + re.escape(skill) + r"\b"

        if re.search(pattern, text):
            found.append(skill.title())

    return sorted(set(found))


def calculate_score(resume_skills, job_skills):
    if not job_skills:
        return 0

    matched = set(resume_skills).intersection(set(job_skills))

    score = int((len(matched) / len(set(job_skills))) * 100)

    return min(score, 100)


def get_recommendations(resume_skills, missing_skills, resume_text):
    recommendations = []

    if missing_skills:
        recommendations.append(
            "Consider adding relevant missing skills if you genuinely have experience with them."
        )

    if len(resume_skills) < 5:
        recommendations.append(
            "Add more relevant technical or professional skills to your resume."
        )

    if "summary" not in resume_text.lower() and "objective" not in resume_text.lower():
        recommendations.append(
            "Consider adding a clear professional summary or career objective."
        )

    if "project" not in resume_text.lower():
        recommendations.append(
            "Include relevant academic or personal projects with clear descriptions."
        )

    if "education" not in resume_text.lower():
        recommendations.append(
            "Make sure your education details are clearly mentioned."
        )

    if not recommendations:
        recommendations.append(
            "Your resume contains several relevant sections. Continue tailoring it to each job description."
        )

    return recommendations


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    if "resume" not in request.files:
        return "No resume file selected."

    file = request.files["resume"]

    if file.filename == "":
        return "Please select a resume."

    if not allowed_file(file.filename):
        return "Only PDF and DOCX files are supported."

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    file.save(filepath)

    extension = filename.rsplit(".", 1)[1].lower()

    try:
        resume_text = extract_text(filepath, extension)
    except Exception:
        return "Unable to read the uploaded resume."

    if not resume_text.strip():
        return "No readable text found in the resume."

    job_description = request.form.get("job_description", "").strip()

    resume_skills = find_skills(resume_text)
    job_skills = find_skills(job_description)

    matching_skills = sorted(
        set(resume_skills).intersection(set(job_skills))
    )

    missing_skills = sorted(
        set(job_skills) - set(resume_skills)
    )

    if job_description:
        score = calculate_score(resume_skills, job_skills)
    else:
        # Basic resume score when no job description is given
        score = min(len(resume_skills) * 10, 100)

    recommendations = get_recommendations(
        resume_skills,
        missing_skills,
        resume_text
    )

    return render_template(
        "dashboard.html",
        score=score,
        resume_skills=resume_skills,
        job_skills=job_skills,
        matching_skills=matching_skills,
        missing_skills=missing_skills,
        recommendations=recommendations
    )


if __name__ == "__main__":
    app.run(debug=True)