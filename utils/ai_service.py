import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
import streamlit as st

class AIService:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if self.api_key:
            self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=self.api_key)
        else:
            self.llm = None

    def generate_resume(self, raw_data, job_description=None):
        if not self.llm:
            return "Error: AI Model not configured. Please provide an API key."

        prompt_template = """
        You are an expert resume writer and ATS optimizer. 
        Given the following raw resume data:
        {raw_data}

        And the target job description (if provided):
        {job_description}

        Generate a professional, high-fidelity resume in Markdown format. 

        CRITICAL HEADER FORMAT:
        Line 1: # [FULL NAME]
        Line 2: [Professional Headline (e.g., Professional Accountant, Full Stack Developer)]
        Line 3: [Phone] | [Email] | [LinkedIn Link] | [Location]
        
        STRUCTURE & NAMING:
        - Use ## ABOUT ME for the summary.
        - Use ## EDUCATION for studies.
        - Use ## WORK EXPERIENCE for jobs. 
          Inside jobs, use: [Organization Name] | [Localization/Dates] followed by ### [Job Title]
        - Use ## SKILLS for the skills section.
        - Use ## PROJECTS if applicable.
        
        STRICT NEGATIVE CONSTRAINTS:
        - NEVER combine name and headline.
        - NEVER combine headline and contact.
        - ALWAYS follow this exact order: Name, Headline, Contact.
        - Use the XYZ formula for bullet points (Accomplished [X] as measured by [Y], by doing [Z]).
        """
        
        prompt = PromptTemplate(template=prompt_template, input_variables=["raw_data", "job_description"])
        # Use newer LangChain syntax
        chain = prompt | self.llm
        response = chain.invoke({"raw_data": raw_data, "job_description": job_description or "General professional role"})
        return response.content

    def generate_cover_letter(self, resume_data, job_description):
        if not self.llm:
            return "Error: AI Model not configured. Please provide an API key."

        prompt_template = """
        You are an expert career coach. 
        Based on this resume:
        {resume_data}

        And this job description:
        {job_description}

        Write a compelling, professional cover letter that highlights the candidate's fit for the role.
        """
        prompt = PromptTemplate(template=prompt_template, input_variables=["resume_data", "job_description"])
        chain = prompt | self.llm
        response = chain.invoke({"resume_data": resume_data, "job_description": job_description})
        return response.content

    def generate_portfolio_strategy(self, resume_data):
        if not self.llm:
            return "Error: AI Model not configured. Please provide an API key."

        prompt_template = """
        You are a career consultant for software engineers and students. 
        Based on the following resume data:
        {resume_data}

        Suggest a portfolio strategy to showcase their skills effectively. 
        Include:
        1. 2-3 specific project ideas that would fill gaps or highlight strengths.
        2. Tips on how to present these projects on a personal website or GitHub.
        3. A suggested layout for their portfolio.
        """
        prompt = PromptTemplate(template=prompt_template, input_variables=["resume_data"])
        chain = prompt | self.llm
        response = chain.invoke({"resume_data": resume_data})
        return response.content
