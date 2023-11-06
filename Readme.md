docker build -f ./Dockerfile -t icheckyfy/ocr_masker:v1 .
docker container run -d -p 80:80  icheckify/ocr_masker:v1