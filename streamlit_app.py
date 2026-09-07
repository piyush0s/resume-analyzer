from io import BytesIO

import streamlit as st


st.set_page_config(
    page_title="Resume Analyzer",
    page_icon="📄",
    layout="wide",
)


@st.cache_resource
def load_analyzer():
    from app import (
        extract_contact,
        extract_education,
        extract_name,
        extract_skills,
        predicted_category,
        recommended_job,
        skills_list,
    )

    return {
        "extract_contact": extract_contact,
        "extract_education": extract_education,
        "extract_name": extract_name,
        "extract_skills": extract_skills,
        "predicted_category": predicted_category,
        "recommended_job": recommended_job,
        "skills_list": skills_list,
    }


def extract_uploaded_text(uploaded_file):
    file_bytes = uploaded_file.getvalue()
    file_name = uploaded_file.name.lower()

    if file_name.endswith(".pdf"):
        from PyPDF2 import PdfReader

        reader = PdfReader(BytesIO(file_bytes))
        return "\n".join(page.extract_text() or "" for page in reader.pages)

    if file_name.endswith(".txt"):
        return file_bytes.decode("utf-8", errors="replace")

    raise ValueError("Unsupported file format. Please upload a PDF or TXT file.")


def show_values(title, values):
    if values:
        st.markdown(f"**{title}**")
        st.write(", ".join(values))


st.markdown(
    """
    <style>
    .main { background: #f7f8f6; }
    .block-container { max-width: 1050px; padding-top: 3rem; }
    .hero {
        background: linear-gradient(135deg, #173f3a, #28745d);
        color: white;
        padding: 2.5rem 3rem;
        border-radius: 18px;
        margin-bottom: 2rem;
    }
    .hero h1 { margin: 0; font-size: 2.7rem; }
    .hero p { margin: .75rem 0 0; color: #d9eee5; font-size: 1.05rem; }
    </style>
    <div class="hero">
        <h1>Resume Analyzer</h1>
        <p>Upload a resume to extract key details, predict its category, and get a job recommendation.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

analyzer = load_analyzer()

uploaded_file = st.file_uploader(
    "Upload your resume",
    type=["pdf", "txt"],
    help="Supported formats: PDF and plain text.",
)

if uploaded_file is not None:
    if st.button("Analyze resume", type="primary", use_container_width=True):
        try:
            with st.spinner("Analyzing your resume..."):
                resume_text = extract_uploaded_text(uploaded_file)
                if not resume_text.strip():
                    raise ValueError("The uploaded file does not contain readable text.")

                name = analyzer["extract_name"](resume_text)
                contact = analyzer["extract_contact"](resume_text)
                education = analyzer["extract_education"](resume_text)
                skills = analyzer["extract_skills"](
                    resume_text, analyzer["skills_list"]
                )
                category = analyzer["predicted_category"](resume_text)
                job = analyzer["recommended_job"](resume_text)

            st.success("Resume analyzed successfully.")
            st.subheader("Analysis results")

            result_columns = st.columns(2)
            with result_columns[0]:
                st.metric("Predicted category", category)
            with result_columns[1]:
                st.metric("Recommended job", job)

            st.divider()
            details_columns = st.columns(2)
            with details_columns[0]:
                if name:
                    st.markdown(f"**Name**\n\n{name}")
                if contact["emails"]:
                    st.markdown(f"**Email**\n\n{contact['emails'][0]}")
                if contact["phone_numbers"]:
                    st.markdown(f"**Phone**\n\n{contact['phone_numbers'][0]}")
            with details_columns[1]:
                show_values("Education", education)
                show_values("Skills", skills)

        except ValueError as error:
            st.error(str(error))
        except Exception:
            st.error("The resume could not be analyzed. Please check the file and try again.")
else:
    st.info("Choose a PDF or TXT resume above to begin.")
