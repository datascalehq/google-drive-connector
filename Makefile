setup:
	pip3 install -r requirements.txt
	
api_start:
	cd app/ && python3 -m uvicorn main:app --host=0.0.0.0 --port=8080

docker_build:
	docker build -t google_drive_connector .

docker_run:
	docker run -p 8080:8080 google_drive_connector

integration_test:
	cd app && python3 -m pytest tests/integration