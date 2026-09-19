from PyPDF2 import PdfReader
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():

    # Get the uploaded file
    resume = request.files["resume"]

    # Check if a file was uploaded
    if not resume or resume.filename == "":
        return "Please upload a PDF resume."

    # Read the PDF directly without saving it
    reader = PdfReader(resume.stream)

    # Store all the text here
    text = ""

    # Read every page of the PDF
    for page in reader.pages:
        text += page.extract_text() or ""

    # List of skills
    skills = [
        "Python",
        "Java",
        "C",
        "SQL",
        "HTML",
        "CSS",
        "JavaScript",
        "Git",
        "GitHub",
        "Flask",
        "Machine Learning",
        "React",
        "Pandas",
        "NumPy",
        "Docker",
        "REST API",
        "VS Code"
    ]

    # Find skills present in the resume
    found_skills = []

    for skill in skills:
        if skill.lower() in text.lower():
            found_skills.append(skill)

    # Calculate ATS score
    total_skills = len(skills)
    found = len(found_skills)

    ats_score = (found / total_skills) * 100

    # Find missing skills
    missing_skills = []

    for skill in skills:
        if skill not in found_skills:
            missing_skills.append(skill)

    # Find suitable job roles
    job_roles = []

    if "Python" in found_skills:
        job_roles.append("Python Developer")

    if "HTML" in found_skills:
        job_roles.append("Frontend Developer")

    if "Machine Learning" in found_skills:
        job_roles.append("Machine Learning Engineer")

    if "SQL" in found_skills:
        job_roles.append("Data Analyst")

    if "Java" in found_skills:
        job_roles.append("Software Developer")

    if "JavaScript" in found_skills:
        job_roles.append("Web Developer")

    # Recommend courses for missing skills
    courses = []

    if "Flask" in missing_skills:
        courses.append("Learn Flask")

    if "React" in missing_skills:
        courses.append("Learn React")

    if "Docker" in missing_skills:
        courses.append("Learn Docker")

    if "Pandas" in missing_skills:
        courses.append("Learn Pandas")

    if "NumPy" in missing_skills:
        courses.append("Learn NumPy")

    # Display results
    return render_template(
        "result.html",
        ats_score=round(ats_score),
        found_skills=found_skills,
        missing_skills=missing_skills,
        job_roles=job_roles,
        courses=courses
    )


if __name__ == "__main__":
    app.run(debug=True)