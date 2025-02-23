Image Processing

Reduce image size by 50% (tested on image of 20kb which reduced to 7kb)

tech stack : fast API, sqlalchemy, pillow

setup ->
	* python -m venv env
	* source env/bin/activate
	* pip install -r requirements.txt
	* pip install sqlalchemy mysqlclient fastapi
	* sudo mysql -u root -p
		- database should have a user : "user", with password : "pass"
		- create a data base named "image_processing"

execution -> 
	* uvicorn app:app --reload
	* go to page "http://127.0.0.1:8000/"

flow -> 
	* uploaded csv gets saved in local folder. (data/in_csv_files) 
	* csv goes thorugh a check for few conditions, all failed conditions are shown to user. if not failed then flow continues.
	* a new reference number is generated base on total no of entries till now and timestamp. 
	* this reference number is sent to the user and a new async job is created with this referene id 
	* database also gets logged with this new reference number
	* job 
		- all images get downloaded to local folder (data/raw_images)
		- to be unique image name is coded with reference number + s.no. + product name + image sequence no
		- all images are reduced one by one using pillow (50% in height and width)
		- new csv is created with this data 
	* at every step of the job the database gets updated. (status field)
	* when user comes back for new images. the same reference number is used.
	* if job status is done successfully then he can download the new updated csv. if there is any error, it is displayed while check for job status
	* job status can be fetched any time, as it is updated after every step.

dir-tree ->
	├── app.py
	├── data
	│             ├── in_csv_files
	│             │             ├── 202502230413203.csv
	│             ├── out_cvs_files
	│             │             ├── 202502230413203.csv
	│             ├── processed_images
	│             │             ├── 202502230417272>1.>SKU1>0.jpg
	│             │             ├── 202502230417272>1.>SKU1>1.jpg
	│             └── raw_images
	│                 ├── 202502230417272>1.>SKU1>0.jpg
	│                 ├── 202502230417272>1.>SKU1>1.jpg
	│                 
	├── dummy_input_file.csv
	├── html_templates
	│             ├── check_status.html
	│             ├── csv_error.html
	│             ├── requirements.txt
	│             ├── upload_form.html
	│             └── upload_success.html
	├── readme.md
	├── requirements.txt
	└── scripts
	    ├── csv_sanitary_check.py
	    ├── db_connector.py
	    ├── db_create_tables.py
	    ├── db_models.py
	    ├── db_operations.py
	    ├── download_images.py
	    ├── generate_out_csv.py
	    ├── process_images.py

screen-shots ->
![Screenshot](screenshot/1.jpg)
upload page 

![Screenshot](screenshot/2.jpg)
successfully uploaded and job started in async

![Screenshot](screenshot/3.jpg)
if there is any error in csv, or job steps then issue is displayed

![Screenshot](screenshot/4.jpg)
database (mysql)

	



