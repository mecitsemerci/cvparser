import spacy
import pdfplumber
import re

# Load SpaCy model
nlp = spacy.load("en_core_web_sm")


# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text


# Clean the extracted text
def clean_text(text):
    return re.sub(r"\s+", " ", text).strip()


# Function to extract information using regex and NLP
def parse_linkedin_profile(text):
    parsed_data = {
        "name": "",
        "contact": {"phone": "", "email": "", "linkedin": ""},
        "top_skills": [],
        "languages": [],
        "certifications": [],
        "experience": [],
        "education": [],
    }

    # Extract contact details using regex
    email_regex = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
    phone_regex = r"\+?\d[\d -]{8,}\d"
    linkedin_regex = r"(https:\/\/[a-z]{2,3}\.linkedin\.com\/in\/[a-zA-Z0-9-]+)"

    parsed_data["contact"]["email"] = (
        re.search(email_regex, text).group(0) if re.search(email_regex, text) else ""
    )
    parsed_data["contact"]["phone"] = (
        re.search(phone_regex, text).group(0) if re.search(phone_regex, text) else ""
    )
    parsed_data["contact"]["linkedin"] = (
        re.search(linkedin_regex, text).group(0)
        if re.search(linkedin_regex, text)
        else ""
    )

    # Use SpaCy NLP to detect entities like names and companies
    doc = nlp(text)

    # Extracting name (PERSON entity)
    for ent in doc.ents:
        if ent.label_ == "PERSON" and not parsed_data["name"]:
            parsed_data["name"] = ent.text
            break

    # Extract top skills
    skills_match = re.search(r"Top Skills(.+?)Languages", text, re.DOTALL)
    if skills_match:
        parsed_data["top_skills"] = [
            skill.strip()
            for skill in skills_match.group(1).split("\n")
            if skill.strip()
        ]

    # Extract languages
    languages_match = re.search(r"Languages(.+?)Certifications", text, re.DOTALL)
    if languages_match:
        parsed_data["languages"] = [
            lang.strip()
            for lang in languages_match.group(1).split("\n")
            if lang.strip()
        ]

    # Extract certifications
    certifications_match = re.search(r"Certifications(.+?)Experience", text, re.DOTALL)
    if certifications_match:
        parsed_data["certifications"] = [
            cert.strip()
            for cert in certifications_match.group(1).split("\n")
            if cert.strip()
        ]

    # Extract experience section
    experience_match = re.search(r"Experience(.+?)Education", text, re.DOTALL)
    if experience_match:
        experience_text = experience_match.group(1).strip()
        parsed_data["experience"] = extract_experience(experience_text)

    # Extract education section
    education_match = re.search(r"Education(.+?)$", text, re.DOTALL)
    if education_match:
        education_text = education_match.group(1).strip()
        parsed_data["education"] = extract_education(education_text)

    return parsed_data


# Function to extract experience
def extract_experience(experience_text):
    experiences = re.split(
        r"([A-Za-z]+\s\d{4}\s-\s[A-Za-z]+\s\d{4}|Present)", experience_text
    )
    experience_list = []
    for i in range(0, len(experiences), 2):
        if i + 1 < len(experiences):
            position = experiences[i].strip()
            duration = experiences[i + 1].strip()
            experience_list.append({"position": position, "duration": duration})
    return experience_list


# Function to extract education
def extract_education(education_text):
    education_list = re.split(
        r"([A-Za-z]+\s\d{4}\s-\s[A-Za-z]+\s\d{4}|Present)", education_text
    )
    education = []
    for i in range(0, len(education_list), 2):
        if i + 1 < len(education_list):
            degree = education_list[i].strip()
            duration = education_list[i + 1].strip()
            education.append({"degree": degree, "duration": duration})
    return education
