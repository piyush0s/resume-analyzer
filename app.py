from flask import Flask, render_template, request
import pickle
from PyPDF2 import PdfReader
import re

app = Flask(__name__)

# Load pre-trained models
rf_classifier = pickle.load(open('rf_classifier.pkl', 'rb'))
tfidf_vectorizer = pickle.load(open('tfidf_vectorizer.pkl', 'rb'))
rf_classifier1 = pickle.load(open('rf_classifier1.pkl', 'rb'))
tfidf_vectorizer1 = pickle.load(open('tfidf_vectorizer1.pkl', 'rb'))

# Helper: Extract text from PDF
def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ''
    for page in reader.pages:
        text += page.extract_text()
    return text

# Helper: Extract Name
def extract_name(resume_text):
    name_match = re.search(r"(?:Name|Full Name)\s*[:\-]?\s*([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)", resume_text)
    if name_match:
        return name_match.group(1)
    lines = resume_text.strip().split('\n')
    for line in lines[:10]:
        if re.match(r"^[A-Z][a-z]+(?:\s[A-Z][a-z]+)+$", line.strip()):
            return line.strip()
    return None

# Helper: Extract Contact Info
def extract_contact(resume_text):
    phone_pattern = r'\b\d{10}\b'
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    phone_numbers = re.findall(phone_pattern, resume_text)
    emails = re.findall(email_pattern, resume_text)
    return {
        'phone_numbers': phone_numbers,
        'emails': emails
    }

# Helper: Clean Text
def cleanResume(text):
    text = re.sub(r'\W+', ' ', text)
    return text.lower().strip()

# Helper: Extract Skills
def extract_skills(resume_text, skills_list):
    skills = []
    for skill in skills_list:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, resume_text, re.IGNORECASE):
            skills.append(skill)
    return skills

# Helper: Extract Education
def extract_education(resume_text):
    education_keywords = [
        "computer science", "mechanical engineering", "civil engineering", "pharmacy", "artificial intelligence",
        "law", "finance", "mathematics", "english literature", "psychology", "education", "graphic design",
        "data science", "information technology", "electrical engineering", "biotechnology", "economics", "physics",
        "chemistry", "biology", "architecture", "marketing", "business administration", "statistics", "environmental science", "history", "sociology", "nursing", "journalism", "public relations",
        "international relations", "agriculture", "hospitality management", "sports science", "philosophy", "anthropology", "performing arts", "visual arts", "media studies", "communication studies", "linguistics", "theology", "library science", "information systems", "supply chain management"
    ]
    education = []
    for keyword in education_keywords:
        pattern = r'\b' + re.escape(keyword) + r'\b'
        if re.search(pattern, resume_text, re.IGNORECASE):
            education.append(keyword)
    return education

# Predefined skills list (shortened for demo)
skills_list = [
    # --- Programming Languages & Frameworks ---
    "python", "java", "javascript", "c++", "c#", "ruby", "go", "rust", "kotlin", "swift",
    "typescript", "php", "r", "perl", "sql", "bash", "shell scripting", "matlab", "scala", "haskell",
    "html", "css", "react.js", "vue.js", "angular", "node.js", "express.js", "next.js", "tailwind css", "bootstrap",
    "sass", "jquery", "flask", "django", "rest api", "graphql", "websockets", "ajax", "webpack", "vite",

    # --- Data Science & Machine Learning ---
    "pandas", "numpy", "matplotlib", "seaborn", "scipy", "scikit-learn", "tensorflow", "keras", "pytorch", "jupyter notebooks",
    "data wrangling", "data cleaning", "data visualization", "eda", "feature engineering", "model evaluation", "classification", "regression", "clustering", "time series analysis",
    "nlp", "computer vision", "supervised learning", "unsupervised learning", "deep learning", "reinforcement learning", "mlops", "automl", "cross-validation", "model deployment",

    # --- DevOps & Cloud ---
    "aws", "azure", "gcp", "docker", "kubernetes", "terraform", "jenkins", "github actions", "ci/cd", "linux administration",
    "ansible", "cloudformation", "monitoring", "prometheus", "grafana", "nginx", "apache", "load balancing", "ssl", "firewall configuration",

    # --- Cybersecurity ---
    "network security", "ethical hacking", "penetration testing", "owasp", "burp suite", "kali linux", "encryption", "vpn", "siem", "incident response",
    "vulnerability assessment", "threat modeling", "malware analysis", "digital forensics", "security compliance", "risk assessment", "identity management", "intrusion detection", "zero trust security", "firewall rules",

    # --- Database & Big Data ---
    "mysql", "postgresql", "mongodb", "firebase", "sqlite", "oracle", "cassandra", "redis", "hive", "snowflake",
    "data warehousing", "etl", "bigquery", "apache spark", "hadoop", "kafka", "airflow", "elasticsearch", "indexing", "database normalization",

    # --- UI/UX & Design ---
    "figma", "sketch", "adobe xd", "photoshop", "illustrator", "canva", "lightroom", "procreate", "wireframing", "prototyping",
    "usability testing", "user research", "design thinking", "interaction design", "color theory", "typography", "layout design", "responsive design", "accessibility", "motion design",

    # --- Game & AR/VR Development ---
    "unity", "unreal engine", "c# scripting", "blueprints", "game physics", "2d animation", "3d modeling", "character rigging", "game ui design", "multiplayer networking",
    "vr development", "ar development", "oculus sdk", "shader programming", "unity physics", "sprite animation", "level design", "game sound design", "collision detection", "game optimization",

    # --- Digital Marketing & SEO ---
    "seo", "sem", "google ads", "facebook ads", "linkedin marketing", "instagram marketing", "email marketing", "affiliate marketing", "influencer marketing", "content marketing",
    "google analytics", "ahrefs", "semrush", "hootsuite", "mailchimp", "copywriting", "conversion optimization", "crm", "brand strategy", "a/b testing",

    # --- Business & Finance ---
    "financial modeling", "budgeting", "forecasting", "investment analysis", "accounting", "bookkeeping", "tax planning", "auditing", "quickbooks", "ms excel",
    "balance sheet analysis", "cash flow management", "valuation", "risk management", "erp systems", "sap", "business analysis", "strategic planning", "kpi tracking", "market research",

    # --- Education & Training ---
    "curriculum design", "instructional design", "lesson planning", "e-learning", "classroom management", "academic writing", "assessment design", "educational technology", "student engagement", "learning management systems",

    # --- Engineering & Robotics ---
    "cad", "solidworks", "autocad", "revit", "circuit design", "embedded systems", "arduino", "raspberry pi", "mechatronics", "matlab simulation",
    "finite element analysis", "thermodynamics", "mechanical design", "electrical wiring", "microcontroller programming", "pcb design", "3d printing", "robot kinematics", "sensor integration", "robot operating system",

    # --- Writing & Communication ---
    "technical writing", "content writing", "academic writing", "creative writing", "blogging", "proofreading", "editing", "copyediting", "storytelling", "presentation skills",

    # --- Soft Skills ---
    "communication", "leadership", "critical thinking", "problem solving", "creativity", "emotional intelligence", "time management", "adaptability", "teamwork", "negotiation",
    "conflict resolution", "public speaking", "strategic thinking", "self-motivation", "collaboration", "work ethic", "resilience", "decision making", "attention to detail", "growth mindset",

    # --- Tools & Platforms ---
    "microsoft excel", "word", "powerpoint", "google docs", "google sheets", "slack", "notion", "trello", "jira", "asana",
    "zoom", "microsoft teams", "obs studio", "vs code", "postman", "git", "github", "bitbucket", "intellij", "android studio",

    # --- Language Skills ---
    "english", "french", "spanish", "german", "mandarin", "hindi", "arabic", "japanese", "portuguese", "russian",

    # --- Personal Development & Productivity ---
    "speed reading", "note taking", "mind mapping", "goal setting", "journaling", "meditation", "stress management", "time blocking", "habit tracking", "self discipline",

    # --- Multimedia & Editing ---
    "video editing", "audio editing", "color grading", "motion graphics", "sound design", "vfx", "voiceover", "animation", "screen recording", "youtube optimization",

    # --- Miscellaneous Practical Skills ---
    "first aid", "cooking", "baking", "photography", "gardening", "car maintenance", "basic electronics", "fitness training", "yoga", "diet planning"
]

# Predict category
def predicted_category(resume_text):
    cleaned_text = cleanResume(resume_text)
    vectorized_text = tfidf_vectorizer.transform([cleaned_text])
    return rf_classifier.predict(vectorized_text)[0]

# Recommend job
def recommended_job(resume_text):
    cleaned_text = cleanResume(resume_text)
    vectorized_text = tfidf_vectorizer1.transform([cleaned_text])
    return rf_classifier1.predict(vectorized_text)[0]

# Home route
@app.route('/')
def resume():
    return render_template('resume.html')

# Prediction route
@app.route('/pred', methods=['POST'])
def pred():
    if 'resume' in request.files:
        file = request.files['resume']
        filename = file.filename

        if filename.endswith('.pdf'):
            text = extract_text_from_pdf(file)
        elif filename.endswith('.txt'):
            text = file.read().decode('utf-8')
        else:
            return render_template('resume.html', error='Unsupported file format. Please upload a PDF or TXT file.')

        name = extract_name(text)
        contact_info = extract_contact(text)
        education = extract_education(text)
        skills = extract_skills(text, skills_list)

        predicted_category_result = predicted_category(text)
        recommended_job_result = recommended_job(text)

        return render_template(
            'resume.html',
            name=name,
            phone_numbers=contact_info.get('phone_numbers'),
            emails=contact_info.get('emails'),
            education=education,
            skills=skills,
            predicted_category=predicted_category_result,
            recommended_job=recommended_job_result
        )
    else:
        return render_template('resume.html', error='No file uploaded. Please upload a resume file.')

# Main
if __name__ == '__main__':
    app.run(debug=True)
