import streamlit as st
import os
from utils.parser import parse_pdf, parse_docx, extract_structured_data
from utils.ai_service import AIService
from dotenv import load_dotenv

load_dotenv()

# Page Config
st.set_page_config(page_title="AI Resume Builder Pro", page_icon="📝", layout="wide")

# Load CSS
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Application Title
st.markdown("""
<div class="title-container">
    <h1 class="title-text">AI Resume Builder Pro</h1>
    <p style="color: rgba(255,255,255,0.7); font-size: 1.2rem;">Craft ATS-friendly resumes & cover letters with ease.</p>
</div>
""", unsafe_allow_html=True)

# Initialize AI Service
ai_service = AIService()

# Main Sections
tab1, tab2, tab3 = st.tabs(["📄 Build Resume", "📧 Cover Letter", "📁 Portfolio Strategy"])

with tab1:
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("📥 Input Data")
        input_method = st.radio("Choose Input Method", ["Import Existing Resume", "Enter Manually"])
        
        raw_text = ""
        if input_method == "Import Existing Resume":
            uploaded_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])
            if uploaded_file:
                if uploaded_file.name.endswith('.pdf'):
                    raw_text = parse_pdf(uploaded_file.read())
                else:
                    raw_text = parse_docx(uploaded_file.read())
                st.success("File parsed successfully!")
                with st.expander("Show extracted text"):
                    st.text(raw_text)
        else:
            name = st.text_input("👤 Full Name")
            contact_links = st.text_area("🔗 Important Links", placeholder="Phone, Email, LinkedIn, GitHub, etc.")
            skills = st.text_area("🛠️ Skills", placeholder="Python, Java, React, SQL, etc.")
            education = st.text_area("🎓 Education", placeholder="Degree, Institution, Year")
            experience = st.text_area("💼 Experience (Optional)", placeholder="Job Title, Company, Duration, Key Responsibilities")
            projects = st.text_area("🚀 Projects", placeholder="Project Name, Technologies Used, Key Features")
            certifications = st.text_area("📜 Certifications", placeholder="Certificate Name, Issuing Organization")
            
            # Consolidate into structured text for AI
            raw_text = f"""
            NAME: {name}
            CONTACT/LINKS: {contact_links}
            SKILLS: {skills}
            EDUCATION: {education}
            EXPERIENCE: {experience}
            PROJECTS: {projects}
            CERTIFICATIONS: {certifications}
            """

        job_desc = st.text_area("Target Job Description (Optional)", placeholder="Paste the job description to tailor your resume...")

        if st.button("🚀 Generate ATS-Friendly Resume"):
            if not raw_text:
                st.warning("Please provide resume data.")
            else:
                with st.spinner("AI is crafting your resume..."):
                    resume_md = ai_service.generate_resume(raw_text, job_desc)
                    st.session_state['generated_resume'] = resume_md
                    st.success("Resume Generated!")

    with col2:
        if 'generated_resume' in st.session_state:
            st.markdown(f'<div class="paper-preview fade-in">{st.session_state["generated_resume"]}</div>', unsafe_allow_html=True)
        else:
            st.info("Your generated resume will appear here.")

with tab2:
    st.subheader("📧 Cover Letter AI Generator")
    if 'generated_resume' in st.session_state:
        target_job = st.text_area("Target Job Description", value=job_desc if 'job_desc' in locals() else "")
        if st.button("Generate Cover Letter"):
            with st.spinner("Writing your cover letter..."):
                cover_letter = ai_service.generate_cover_letter(st.session_state['generated_resume'], target_job)
                st.session_state['cover_letter'] = cover_letter
                st.markdown(f'<div class="resume-card fade-in">{cover_letter}</div>', unsafe_allow_html=True)
    else:
        st.warning("Please generate a resume first in the 'Build Resume' tab.")

with tab3:
    st.subheader("📁 Portfolio & Projects Strategy")
    if 'generated_resume' in st.session_state:
        st.write("Based on your resume, let's craft a winning portfolio strategy.")
        if st.button("Generate Portfolio Strategy"):
            with st.spinner("Analyzing your profile for projects..."):
                strategy = ai_service.generate_portfolio_strategy(st.session_state['generated_resume'])
                st.session_state['portfolio_strategy'] = strategy
                st.markdown(f'<div class="resume-card fade-in">{strategy}</div>', unsafe_allow_html=True)
    else:
        st.warning("Please generate a resume first in the 'Build Resume' tab.")
    
    st.info("This section helps students highlight their unique strengths through structured project descriptions and strategic portfolio layout.")
