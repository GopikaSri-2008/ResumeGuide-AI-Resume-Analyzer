# ResumeGuide – AI Resume Analyzer

ResumeGuide is a web-based AI Resume Analyzer built using Python and Flask. It analyzes a candidate's resume and compares it with a given job description to identify matching skills, missing skills, and relevant keywords.

## Features

- Upload resume in PDF or DOCX format
- Enter a job description
- Extract resume text automatically
- Identify skills from the resume
- Compare resume skills with job requirements
- Calculate a resume matching score
- Display matching skills
- Display missing skills
- Identify important job keywords
- Provide improvement recommendations
- Simple and responsive web interface

## Technologies Used

- Python
- Flask
- PyPDF2
- python-docx
- Werkzeug
- HTML5
- CSS3
- Jinja2

## Project Structure

ResumeGuide/
├── app.py
├── requirements.txt
├── templates/
│   ├── index.html
│   └── result.html
├── static/
│   └── style.css
└── uploads/

## Installation

1. Clone the repository.

2. Install the required packages:

```bash
pip install -r requirements.txt