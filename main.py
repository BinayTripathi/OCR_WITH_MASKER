from flask import Flask, request, jsonify
import requests
from masker import mask_and_return

# Init app
app = Flask(__name__)

# Create a Product
@app.route('/', methods=['POST'])
def get_image():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        resp = get_ocr_data(json["image"])
        return resp
    else:
        return 'Content-Type not supported!'
    


def get_ocr_data(base64Image):

    data = '''{	"requests": [{"image": {"content": "%s" },"features": [{"type": "TEXT_DETECTION","maxResults": 1}]}]}''' % (base64Image)
    #response = requests.post(url="https://vision.googleapis.com/v1/images:annotate?key=AIzaSyDXQq3xhrRFxFATfPD4NcWlHLE8NPkzH2s",data=data)
    masked_image =  mask_and_return(base64Image)
    #(masked_image)
    return masked_image


if __name__ == '__main__':
    app.run(debug=True)


