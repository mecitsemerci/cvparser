from celery import Celery
from parse_cv import extract_text_from_pdf, parse_linkedin_profile, clean_text
import os

# Initialize Celery
celery_app = Celery("tasks", backend='redis', broker="redis://localhost:6379/0")


@celery_app.task
def process_cv_task(file_path, file_type):
    # Extract text based on the file type
    if file_type == "pdf":
        text = extract_text_from_pdf(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")

    # Clean and parse the extracted text
    cleaned_text = clean_text(text)
    parsed_data = parse_linkedin_profile(cleaned_text)

    # Remove the temp file after processing
    os.remove(file_path)

    return parsed_data
