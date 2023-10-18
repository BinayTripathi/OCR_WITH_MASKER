

import cv2
import numpy as np
import base64
import json




def ResizeWithAspectRatio(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    return cv2.resize(image, dim, interpolation=inter)

def data_uri_to_cv2_img(uri):
    encoded_data = uri.split(',')[0]
    nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img


def masker(base64Image):
    # Read an input image as a gray image
    img = data_uri_to_cv2_img(base64Image)

    # create a mask
    mask = np.full(img.shape[:2],255, dtype="uint8")
    #mask[1000:3000, 200:1900] = 255
    cv2.rectangle(mask, (185,2975), (830, 2876), 0, -1)

    # compute the bitwise AND using the mask
    masked_img = cv2.bitwise_and(img,img,mask = mask)

    # display the mask, and the output image
    '''imS = ResizeWithAspectRatio(img, width=700)
    cv2.imshow("Image", imS)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    mask = ResizeWithAspectRatio(mask, width=700)
    cv2.imshow('Mask',mask)
    cv2.waitKey(0)

    masked_img = ResizeWithAspectRatio(masked_img, width=700)
    cv2.imshow('Masked Image',masked_img)
    cv2.waitKey(0)'''
    cv2.imwrite("masked.jpg", masked_img) 

    #data_encode = np.array(masked_img) 
    #base64Ret = base64.b64encode(data_encode)

    base64Image = ''
    with open("masked.jpg", "rb") as image_file:
        base64Image = base64.b64encode(image_file.read())
    #im_bytes = masked_img.tobytes()
    #im_b64 = base64.b64encode(masked_img).decode()
    return base64Image
    '''f = open("demofile2.txt", "a")
    f.write(im_b64)
    f.close()
    return im_b64'''
    #return base64.b64encode(cv2.imencode('.jpg', masked_img)[1]).decode()
   


def mask_and_return(base64Image):
    '''f = open('data.json')
    data = json.load(f)
    imageData = data["image"]
    data_uri = imageData["content"]'''
    return masker(base64Image)
