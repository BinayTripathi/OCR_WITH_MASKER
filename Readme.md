docker build -f ./Dockerfile -t icheckify/ocr_masker:v2 .
docker container run -d -p 80:80  icheckify/ocr_masker:v2