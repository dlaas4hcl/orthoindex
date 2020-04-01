import sys
import json
import requests
import cv2
import numpy as np


def get_prediction(server_host='127.0.0.1', server_port=8500, model_name='ccd'):
    
    img_name = '14.jpg'
    img = cv2.imread(img_name)
    resized_image = cv2.resize(img, (224, 224)) 
    resized_image=resized_image/255
    resized_image = np.expand_dims(resized_image,axis=0)

    data = json.dumps({"signature_name": "serving_default", "instances": resized_image.tolist()})
    headers = {"content-type": "application/json"}
    json_response = requests.post('http://' + server_host + ':' + str(server_port) + '/v1/models/' + str(model_name) + ':predict',
                                  data=data, headers=headers)
    print(json_response)
    print(json.loads(json_response.text).predictions)
    


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: client server_host server_port model_name")
        sys.exit(-1)
    server_host = sys.argv[1]
    server_port = int(sys.argv[2])
    model_name = sys.argv[3]
    get_prediction(server_host=server_host, server_port=server_port,model_name=model_name)

