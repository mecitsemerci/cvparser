# Linkedin CV Parser Example



## Instalations

1. Install the Required Packages:

You need to install the following dependencies:

```bash
pip install -r requirements.txt
```

2.	Set Up Redis and Celery:

 - Redis will act as the message broker for Celery.
 - You can install Redis using your package manager or via Docker:
  
```bash
docker run -d -p 6379:6379 redis
```

3. Loading SpaCy Model

```bash
python -m spacy download en_core_web_sm
```

4. Start Celery Worker

```bash
celery -A celery_worker worker --loglevel=info
```

5. Run FastAPI

```bash
uvicorn app:app --reload
```

Using API the following endpoints are available:

- Upload a CV PDF via the **/upload-cv/** endpoint.
- Check the task status using **/task-status/{task_id}**.

The Celery task processes the uploaded file in the background, allowing you to handle large file uploads and parsing without blocking the API.

This is sample code and **it's not ready for production**. You should use the correct endpoint to upload the file.