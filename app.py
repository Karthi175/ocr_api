from flask import Flask,request,jsonify,make_response
import requests
import pytesseract
from pytesseract import Output
import cv2
import json
from pdf2image import convert_from_path
from flask_cors import CORS, cross_origin


app = Flask(__name__)
CORS(app)


@app.route("/ocr",methods=['POST'])
@cross_origin()
def extraction():
    try:
        file = request.files['file']
        print(file.filename)
        file.save("./test.pdf")
        dict1 = {}
        file = "./test.pdf"
        images = convert_from_path(file)
        for page,image in enumerate(images):
            image.save('outfile.png', 'PNG')
            img1 = cv2.imread('outfile.png')
            d = pytesseract.image_to_data(img1, output_type=Output.DICT)
            n_boxes = len(d['level'])
            temp_list=[]
            for i in range(n_boxes):
                if int(float(d['conf'][i])) >= 0 and d['text'][i] != '':
                    temp_list.append(d['text'][i])
            temp_str=' '.join(temp_list)
            dict1['page_{}'.format(page + 1)] = temp_str
        print(dict1)  
   

        return {'ocr_op':dict1}
    except Exception as e:
        print('in exception',e)
        raise Exception(e,"caught on exception")

if __name__ == "__main__":
    app.run()

def _build_cors_preflight_response():    
    response = make_response()
    print('cors resp')
    response.headers.add("Access-Control-Allow-Origin", "http://localhost:4500/ocr")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    response.headers.add('CORS_ALLOWED_ORIGINS ', "http://localhost:4500/ocr")
    response.headers.add('CORS_ORIGIN_ALLOW_ALL', "True")

    return response

def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

# #AFTER REQUEST
@app.after_request
def afterRequest(response):
    if (request.method == 'OPTIONS'):
        return _build_cors_preflight_response()
    elif (request.method == 'POST'):
        return _corsify_actual_response(response)