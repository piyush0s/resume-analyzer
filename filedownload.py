import pandas as pd
import random

roles = [
    "Data Scientist", "Software Engineer", "Machine Learning Engineer", "Web Developer",
    "AI Researcher", "DevOps Engineer", "Mobile App Developer", "Product Manager",
    "Business Analyst", "UI/UX Designer", "Cybersecurity Analyst", "Cloud Engineer",
    "Doctor", "Nurse", "Lawyer", "Police Officer", "Army Personnel", "Teacher",
    "Professor", "Civil Engineer", "Mechanical Engineer", "Electrician", "Plumber",
    "Architect", "Accountant", "Sales Executive", "HR Manager", "Journalist"
]

skills_pool = {
    "Data Scientist": ["Python", "Pandas", "NumPy", "Matplotlib", "Scikit-learn", "SQL", "Jupyter"],
    "Software Engineer": ["Java", "Python", "C++", "Git", "Linux", "Agile", "OOP"],
    "Machine Learning Engineer": ["Python", "Scikit-learn", "TensorFlow", "Keras", "ML algorithms", "NLP", "PyTorch"],
    "Web Developer": ["HTML", "CSS", "JavaScript", "React", "Node.js", "Express", "MongoDB"],
    "AI Researcher": ["Deep Learning", "Python", "TensorFlow", "Mathematics", "NLP", "Research"],
    "DevOps Engineer": ["CI/CD", "Docker", "Kubernetes", "AWS", "Linux", "Terraform", "Monitoring"],
    "Mobile App Developer": ["Flutter", "Kotlin", "Java", "React Native", "Android Studio", "Swift"],
    "Product Manager": ["Agile", "Scrum", "Wireframing", "Roadmaps", "Customer Research", "Analytics"],
    "Business Analyst": ["Excel", "SQL", "Power BI", "Requirement Gathering", "UML", "Data Modeling"],
    "UI/UX Designer": ["Figma", "Adobe XD", "Wireframing", "Prototyping", "User Research", "Design Systems"],
    "Cybersecurity Analyst": ["Networking", "Python", "Firewalls", "IDS/IPS", "Vulnerability Assessment", "Ethical Hacking"],
    "Cloud Engineer": ["AWS", "Azure", "GCP", "Terraform", "Linux", "Cloud Architecture", "Networking"],
    "Doctor": ["Anatomy", "Physiology", "Diagnosis", "Surgery", "Prescribing", "Patient Care"],
    "Nurse": ["Patient Monitoring", "First Aid", "IV Insertion", "Medical Records", "Emergency Response"],
    "Lawyer": ["Legal Research", "Court Procedures", "Advocacy", "Drafting", "Criminal Law", "Civil Law"],
    "Police Officer": ["Law Enforcement", "Investigation", "Physical Fitness", "Firearms Training", "Traffic Control"],
    "Army Personnel": ["Discipline", "Combat Training", "Strategy", "Survival Skills", "First Aid"],
    "Teacher": ["Lesson Planning", "Subject Knowledge", "Classroom Management", "Student Assessment", "Communication"],
    "Professor": ["Research", "Teaching", "Seminars", "Academic Writing", "Grading"],
    "Civil Engineer": ["AutoCAD", "Structural Design", "Concrete Technology", "Site Supervision", "Project Management"],
    "Mechanical Engineer": ["Thermodynamics", "CAD", "SolidWorks", "Material Science", "Maintenance"],
    "Electrician": ["Wiring", "Circuit Design", "Troubleshooting", "Installation", "Safety Compliance"],
    "Plumber": ["Pipe Fitting", "Water Systems", "Repair", "Blueprint Reading", "Sanitation"],
    "Architect": ["AutoCAD", "Design", "Blueprints", "Building Codes", "3D Modeling"],
    "Accountant": ["Tally", "Excel", "Taxation", "Bookkeeping", "Financial Analysis"],
    "Sales Executive": ["Negotiation", "Lead Generation", "CRM", "Product Knowledge", "Target Achievement"],
    "HR Manager": ["Recruitment", "Payroll", "Employee Relations", "Compliance", "Training"],
    "Journalist": ["Reporting", "Writing", "Editing", "Interviewing", "Research"]
}

def generate_row():
    role = random.choice(roles)
    features = skills_pool[role]
    chosen = random.sample(features, min(len(features), random.randint(3, 6)))
    return {"role": role, "features": ", ".join(chosen)}

data = [generate_row() for _ in range(16000)]
df = pd.DataFrame(data)
df.to_csv("expanded_job_recommendation_dataset.csv", index=False)
