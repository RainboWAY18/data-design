import firebase_admin
from firebase_admin import credentials
import google
from firebase_admin import firestore
from google.cloud import exceptions
import os
import json
from time import sleep, time
#from date_time_def import get_x_date_in_mill





project_id = os.environ.get('project_id',None)
private_key_id = os.environ.get('private_key_id',None)
private_key = os.environ.get('private_key',None).replace('\\n', '\n')
client_email = os.environ.get('client_email',None)
client_id = os.environ.get('client_id',None)
auth_uri = os.environ.get('auth_uri',None)
token_uri = os.environ.get('token_uri',None)
auth_provider_x509_cert_url = os.environ.get('auth_provider_x509_cert_url',None)
client_x509_cert_url = os.environ.get('client_x509_cert_url',None)
databaseURL = os.environ.get('databaseURL',None)
storageBucket = os.environ.get('storageBucket',None)

cer = {
    "type": "service_account",
    "project_id": project_id,
    "private_key_id": private_key_id,
    "private_key": private_key,
    "client_email": client_email,
    "client_id": client_id,
    "auth_uri": auth_uri,
    "token_uri": token_uri,
    "auth_provider_x509_cert_url":auth_provider_x509_cert_url,
    "client_x509_cert_url": client_x509_cert_url
    }

db = None
cred = credentials.Certificate(cer)
try:
    if firebase_admin._apps.get('[DEFAULT]') == None:
        app = firebase_admin.initialize_app(cred, {
            'databaseURL' : databaseURL,
            'storageBucket': storageBucket
            })
        db = firestore.client()    
           
except Exception as e:
    print(str(e))

def write_newuser(line_user_id, display_name, profile_image_url):
   
    
    try:
        user_ref = db.collection('users')
        doc = user_ref.where('line_user_id', '==', line_user_id).get()
        
        is_user_exsits = False
        for item in doc:
            print('user exsits!')
            print(item.to_dict())
            print(item.id)
            is_user_exsits = True
            break

        current_milli_time = int(time()*1000)
        if is_user_exsits == False:       
            user_ref.add({
            'display_name': display_name,
            'line_user_id': line_user_id,
            'profile_image_url': profile_image_url,
            'createAt': current_milli_time
            })
        else:
            return    
    except google.cloud.exceptions.NotFound as e:
        print('error' + str(e))
