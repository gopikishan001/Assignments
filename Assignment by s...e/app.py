from fastapi import FastAPI, UploadFile, File, HTTPException, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse
from fastapi import Depends
import uuid
import os
import csv
from datetime import datetime
from scripts.csv_sanitary_check import csv_sanitary_check
from scripts.download_images import download_images
from scripts.process_images import process_images
from scripts.generate_out_csv import generate_out_csv
import asyncio
from scripts.db_connector import SessionLocal, Base, engine
from scripts.db_operations import *


# Initialize FastAPI app
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="html_templates")

@app.get("/", response_class=HTMLResponse)
async def get_upload_form(request: Request):
    return templates.TemplateResponse("upload_form.html", {"request": request})

@app.post("/upload_csv/")
async def upload_csv(request: Request, file: UploadFile = File(...), db: Session = Depends(get_db)):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    file_counter = int(get_total_rows(db))
    unique_filename = f"{timestamp}{file_counter}.csv"
    
    file_path = os.path.join('data/in_csv_files/', unique_filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    with open(file_path, "r") as f:
        csv_contents = f.read()

    errors, image_count = csv_sanitary_check(csv_contents)

    if errors:
        os.remove(file_path)
        return templates.TemplateResponse("csv_error.html", {"request": request, "errors": errors})

    asyncio.create_task(run_async_job(file_path, unique_filename, image_count, db))
    return templates.TemplateResponse("upload_success.html", {"request": request, "file_name": unique_filename.replace('.csv', ""), "image_count" : image_count})

@app.get("/check_status", response_class=HTMLResponse)
async def reference_check_form(request: Request):
    return templates.TemplateResponse("check_status.html", {"request": request})

# Route to handle form submission
@app.post("/submit_reference")
async def submit_reference(reference_number: str = Form(...), db: Session = Depends(get_db)):

    valid_req = is_reference_present(db, reference_number)

    if valid_req:
        status = get_status_by_reference(db, reference_number)
        if status == "completed" :
            file_path = f"data/out_cvs_files/{reference_number}.csv"
            if os.path.exists(file_path):
                return FileResponse(file_path, filename=f"{reference_number}.csv", media_type="text/csv")
            else : 
                response = "some thing went wrong, <br>with reference number : {}<br><br>please create a new job".format(reference_number)
        elif "ERROR" in status:
            response = "some thing went wrong, <br>with reference number : {}<br>{}<br><br>please create a new job".format(reference_number, status)
        else :
            response = "File is yet to be processed<br>currently : {}<br>Reference number : {}".format(status, reference_number)        
    else:
        response = "No such job present with<br>Reference number : {}<br><br>check reference number".format(reference_number)
        
    return HTMLResponse(content=response)


async def run_async_job(in_csv_file_path, unique_file_name, image_count, db: Session):
    
    reference_number = int(unique_file_name.replace('.csv', ""))
    images = {}
    status = True
    db_job_log = create_job_log(db, reference_number, [], image_count, "downloading_images")
    all_product_names = []

    try :
        with open(in_csv_file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                sno = row['S. No.']
                product_name = row['Product Name']
                input_images = row['Input Image Urls'].split(',')
                all_product_names.append(product_name)
                
                counter = 0
                for link in input_images : 
                    id = f"{str(reference_number)}>{sno}>{product_name}>{counter}"
                    images[id] = link
                    counter += 1

    except Exception as e:
        status = False

    db_job_log = update_product_names_by_reference(db, reference_number, all_product_names)
       
    if status : status = await download_images(images, 'data/raw_images/')
    if status : db_job_logc = update_status_by_reference(db, reference_number, "reducing size")
    
    if status : status = await process_images(images, 'data/raw_images/', 'data/processed_images/')
    if status : db_job_logc = update_status_by_reference(db, reference_number, "generating new csv")
    
    if status : status = await generate_out_csv(images, unique_file_name, 'data/out_cvs_files/')
    if status : db_job_logc = update_status_by_reference(db, reference_number, "completed" )

    if not status :
        operation = get_status_by_reference(db, reference_number)
        db_job_logc = update_status_by_reference(db, reference_number, "ERROR : " + operation)
 