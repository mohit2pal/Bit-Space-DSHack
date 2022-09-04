import os

from google.cloud import vision
from google.cloud import storage
from google.cloud.vision_v1 import types
from google.cloud.vision_v1 import AnnotateImageResponse
# from google.cloud.vision_v1 import ImageAnnotatorClient

import json

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'vision-api-361120-4edd20376cf6.json'
client = vision.ImageAnnotatorClient()


def gcs_upload(current_user, prep_no):
    # Setting credentials using the downloaded JSON file
    client = storage.Client.from_service_account_json(json_credentials_path='vision-api-361120-4edd20376cf6.json')

    # Creating bucket object
    bucket = client.get_bucket('sto_dat')

    prep_name = current_user + "-" + prep_no + ".jpg"

    # Name of the object to be stored in the bucket
    object_name_in_gcs_bucket = bucket.blob(prep_name)

    # Name of the object in local file system
    object_name_in_gcs_bucket.upload_from_filename('IMAGE.jpg')
    



def ocr_function(current_user, prep_no):
    prep_name = current_user + "-" + prep_no + ".jpg"
    prep_uri = "gs://sto_dat/" + prep_name

    image = vision.Image()
    image.source.image_uri = prep_uri

    response_label = client.text_detection(image=image)

    response_json = AnnotateImageResponse.to_json(response_label)
    response = json.loads(response_json)
    

    return response['fullTextAnnotation']['text']