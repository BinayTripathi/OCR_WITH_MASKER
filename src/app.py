from flask import Flask, request, jsonify, make_response
import requests
from masker import maskImage
from faceMatcher import compare_faces
from panVerify import verify
import json
import re
import logging

logging.basicConfig(level=logging.DEBUG)

# Init app
app = Flask(__name__)

class APIError(Exception):   
    code = 403
    description = "Authentication Error"

@app.errorhandler(APIError)
def handle_exception(err):
    """Return custom JSON when APIError or its children are raised"""
    response = {"error": err.description, "message": ""}
    if len(err.args) > 0:
        response["message"] = err.args[0]
    # Add some logging so that we can monitor different types of errors 
    print(f"{err.description}: {response['message']}")
    return jsonify(response), err.code

@app.route('/faceMatch', methods=['POST'])
def face_match():
    json = request.json
    resp = compare_faces(json["source"], json["dest"])
    return  jsonify(resp), 200


# Create a Product
@app.route('/ocr', methods=['POST'])
def get_image():
    try:
        json = request.json
        resp = get_ocr_data(json["image"])
        return  jsonify(resp), 200
    except Exception as e: 
        logging.error(e)
        return  jsonify({"Error" : "Error in masking"}), 500

    
@app.route('/')
def hello_geek():
    return '<h1>Hello from Flask & Docker</h2>'
    
@app.route('/verifyPan', methods=['POST'])
def verifyPan():
    json = request.json
    resp = verify(json["pan"])
    return  jsonify(resp), 200
   

def get_ocr_data(base64Image):

    try:
        data = '''{	"requests": [{"image": {"content": "%s" },"features": [{"type": "TEXT_DETECTION","maxResults": 1}]}]}''' % (base64Image)
        response = requests.post(url="https://vision.googleapis.com/v1/images:annotate?key=AIzaSyDXQq3xhrRFxFATfPD4NcWlHLE8NPkzH2s",data=data)
        response.encoding = "utf-8"
        imageOCRDetails = getDocTypeAndMaskingCoordinates(response.json())
        masked_image =  maskImage(base64Image, imageOCRDetails[2])
        #(masked_image)
        return {
            "maskedImage" : masked_image.decode("utf-8"),
            "docType" : imageOCRDetails[0],
            "documentId" : imageOCRDetails[1],
            "ocrData":  imageOCRDetails[3]
        }
    except Exception as e:
        logging.error(e)
        logging.error("Base64 Image : " + base64Image)
        raise Exception(e)

def getDocTypeAndMaskingCoordinates(responseData):
    try :
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

        return documentType, documentId, boundingBox, description
    except Exception as e:
        logging.error(responseData)
        raise Exception(e)

    
#Handle the case where its not a PAN    
def checkPAN(description):
    panLabel = re.search("Permanent Account Number\\n", description)
    panNumber = description[panLabel.regs[0][1] : panLabel.regs[0][1]+10]
    return 'PAN', panNumber
    


if __name__ == '__main__':
    app.run(debug=True, port=8080)


