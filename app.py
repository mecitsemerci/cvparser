from fastapi import FastAPI, UploadFile, File
from tasks import process_cv_task
from celery.result import AsyncResult
from fastapi.responses import JSONResponse

app = FastAPI()


# Endpoint for uploading a CV file
@app.post("/upload-cv/")
async def upload_cv(file: UploadFile = File(...)):
    # Save the uploaded file temporarily
    file_location = f"temp/{file.filename}"
    with open(file_location, "wb") as f:
        f.write(await file.read())

    # Queue the task for processing the CV
    task = process_cv_task.delay(file_location, file.content_type.split("/")[-1])

    # Return task ID to the client
    return {"task_id": task.id, "status": "Processing started"}


# Endpoint to check the status of the background task
@app.get("/task-status/{task_id}")
async def get_task_status(task_id: str):
    task_result = AsyncResult(task_id)
    print(task_result)
    if task_result.state == "PENDING":
        return {"status": "Pending..."}
    elif task_result.state == "SUCCESS":
        return JSONResponse(
            content={"status": "Completed", "result": task_result.result}
        )
    else:
        return {"status": "In Progress"}
