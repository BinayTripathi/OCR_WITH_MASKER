import boto3
import base64
import json

def base64ToByte(base64Image):
    base64_bytes = base64Image.encode('ascii')
    return base64.b64decode(base64_bytes)

def compare_faces(sourceFile, targetFile):

    session = boto3.Session()
    client = session.client('rekognition')

    try: 
        imageSource = base64ToByte(sourceFile)
    except Exception as e: 
        print('Error in source image: %s', e)

    try: 
        imageTarget = base64ToByte(targetFile)
    except Exception as e: 
        print('Error in target image: %s', e)

    

    response = client.compare_faces(SimilarityThreshold=80,
                                    SourceImage={'Bytes': imageSource},
                                    TargetImage={'Bytes': imageTarget})

    faceMatchRes = {}
    for faceMatch in response['FaceMatches']:
        position = faceMatch['Face']['BoundingBox']
        similarity = str(faceMatch['Similarity'])
        msg = 'The face at ' +  str(position['Left']) + ' ' + str(position['Top']) + ' matches with ' + similarity + '% confidence'
        print(msg)
        faceMatchRes = {
            "faceLeftCoordinate" : position['Left'],
            "faceTopCcordinate" : position['Top'],
            "confidence" : similarity
            }
       
        

    #imageSource.close()
    #imageTarget.close()
    #return len(response['FaceMatches'])
    return faceMatchRes

def main():

    f = open('src\\facematchData.json')
    data = json.load(f)
    #source_file = "D:\\ScannedDocuments\\Binay_Photo.jpg"
    source_file = data['source']
    target_file =  data['dest']

   
    face_matches = compare_faces(source_file, target_file)
    print("Face matches: " + str(face_matches))

if __name__ == "__main__":
    main()