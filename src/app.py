from flask import Flask, request, jsonify, make_response
import requests
from masker import maskImage
from faceMatcher import compare_faces
import json
import re

# Init app
app = Flask(__name__)

@app.route('/faceMatch', methods=['POST'])
def face_match():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        resp = compare_faces(json["source"], json["dest"])
        return  jsonify(resp), 200
    else:
        return 'Content-Type not supported!'

# Create a Product
@app.route('/', methods=['POST'])
def get_image():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        resp = get_ocr_data(json["image"])
        return  jsonify(resp), 200
    else:
        return 'Content-Type not supported!'
    
@app.route('/')
def hello_geek():
    return '<h1>Hello from Flask & Docker</h2>'
    


def get_ocr_data(base64Image):

    data = '''{	"requests": [{"image": {"content": "%s" },"features": [{"type": "TEXT_DETECTION","maxResults": 1}]}]}''' % (base64Image)
    response = requests.post(url="https://vision.googleapis.com/v1/images:annotate?key=AIzaSyDXQq3xhrRFxFATfPD4NcWlHLE8NPkzH2s",data=data)
    imageOCRDetails = getDocTypeAndMaskingCoordinates(response.json())
    print(imageOCRDetails)
    masked_image =  maskImage(base64Image, imageOCRDetails[2])
    #(masked_image)
    return {
        "maskedImage" : masked_image.decode("utf-8"),
        "docType" : imageOCRDetails[0],
        "documentId" : imageOCRDetails[1]
    }


def getDocTypeAndMaskingCoordinates(responseData):
    #f = open('sampleResponse.json')
    #data = json.load(f)
    allAnnnotation = responseData['responses'][0]
    textAnnotations = allAnnnotation['textAnnotations']
    description = textAnnotations[0]["description"]
    documentType, documentId = checkPAN(description)
    
    boundingBox = ''
    for eachWord in textAnnotations:
        if eachWord["description"] == documentId:
            boundingBox = eachWord["boundingPoly"]["vertices"]    #Handle cases where doc id is printed multiple times
            break

    return documentType, documentId, boundingBox
    
#Handle the case where its not a PAN    
def checkPAN(description):
    panLabel = re.search("Permanent Account Number\\n", description)
    panNumber = description[panLabel.regs[0][1] : panLabel.regs[0][1]+10]
    return 'PAN', panNumber
    


if __name__ == '__main__':
    app.run(debug=True, port=8080)


