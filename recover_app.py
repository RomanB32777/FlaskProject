from flask import Flask, render_template, flash, url_for, redirect, request, session
from operator import setitem
import cameralist_forms
import json
import os


# from googleapiclient.http import MediaIoBaseDownload,MediaFileUpload
from googleapiclient.discovery import build
import pprint
import io

import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient import errors


import google.oauth2.credentials
import googleapiclient.discovery


import paho.mqtt.client as mqtt


# App config
app = Flask(__name__)


# Session config

SECRET_KEY = os.urandom(16)
app.config['SECRET_KEY'] = SECRET_KEY

app.config['SESSION_COOKIE_NAME'] = 'google-login-session'
# app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)


# oAuth Setup



pp = pprint.PrettyPrinter(indent=4)
SCOPES = ['https://www.googleapis.com/auth/drive']



# mosquitto 

# ----------------------- paho.mqtt --------------------------- 


app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_REFRESH_TIME'] = 1.0  # refresh time in seconds

topic_token = 'accounts/gdrive/token'

client = mqtt.Client()
client.connect('localhost')

# ----------------------- end paho.mqtt --------------------------- 


# @mqtt.on_connect()
# def handle_connect(client, userdata, flags, rc):
#     mqtt.subscribe('hello/world')


@app.context_processor
def lib_versions():
    return dict(
        user = dict(session).get('user', None),
        user_drive = dict(session).get('user_drive', None)
    )

def auth_drive():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
            pp.pprint(creds)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            #flow.redirect_uri()
            creds = flow.run_local_server(host='localhost', port=5010, authorization_prompt_message='Please visit this URL to authorize this application: {url}', success_message='The authentication flow has completed. You may close this window.', open_browser=True)
           
        with open('token.pickle', 'wb') as token:
                pp.pprint(creds.token)
                client.publish('accounts/gdrive/token', creds.token, qos = 0, retain = True )
                pickle.dump(creds, token)
    return build('drive', 'v3', credentials=creds)
     

def user_drive():
    service = auth_drive()
    try:
        about = service.about().get(fields='user').execute()
    except errors.HttpError:
        pp.pprint('error')
    return about['user']

@app.route('/login_drive')
def login_drive():
    service = auth_drive()
    user_info = user_drive()
    session['user_drive'] = user_info
    client.publish('accounts/gdrive/email', user_info['emailAddress'], qos = 0, retain = True )
    return redirect('/drive')

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/create')
def create_drive():
    # folder_id = '0B8uE0i3GtAuBdFoyMzhMTWZkZGc'
    name = 'Scripts222'
    # file_path = 'bright-torus-290521-4d28909f99f7.json'
    file_metadata = {
     'name': name,
     'mimeType': 'application/vnd.google-apps.folder',
    #'parents': [folder_id]
     }
     #media = MediaFileUpload(file_path, resumable=True)
     #r = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    r = auth_drive().files().create(body=file_metadata, fields='id').execute()
    pp.pprint(r)
    return str(r)

@app.route('/login')
def login_page():
    if 'user' in session:
        user = session['user']
        return 'Hello, you are logge in as {user}!'
   
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    #cur_user = current_user()
 
    #session.permanent = True  # make the session permanant so it keeps existing after broweser gets closed
    return redirect('/')


@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    #oauth.singOut()
    if os.path.exists('token.pickle'):
        os.remove('token.pickle')
    return redirect('/drive')

@app.route('/drive')
def drive_page():
    # pp.pprint(dict(session).get('user_drive', None))
    return render_template('drive.html')


@app.route('/recorder', methods=['GET', 'POST'])
def recorder():
    addForm = cameralist_forms.AddCameraForm()
    deleteAllForm = cameralist_forms.DeleteAllForm()
    deleteCameraForm = cameralist_forms.DeleteCameraForm()
    
    # adding new camera to json
    if addForm.addSubmit.data and addForm.validate():
        # writing data to file
        with open('cams.json', 'r+') as json_file:
            data = json.load(json_file)
            temp = data['cams']
            new_cam = {
                        "name": addForm.cameraName.data,
                        "address": addForm.rtspName.data
                    }
            temp.append(new_cam)
            json_file.seek(0)
            json.dump(data, json_file, indent=4)
            json_file.close()

        # web-page success message
        flash('Camera {addForm.cameraName.data} has been added successfuly!', 'success')
        return redirect(url_for('recorder'))
    

    # # delete all cameras
    if deleteAllForm.deleteAllSubmit.data and deleteAllForm.validate():
        # reading data from file
        with open('cams.json', 'r') as json_file:
            data = json.load(json_file)
            json_file.close()
        
        # writing empty data to json
        with open('cams.json', 'w') as json_file:
            temp = data['cams']
            temp.clear()
            data['cams'] = temp
            json.dump(data, json_file, indent=4)
            json_file.close()

        # web-page success message
        flash('All cameras have been removed successfuly', 'success')
        return redirect(url_for('recorder'))
    

    # delete specified camera
    if deleteCameraForm.deleteCameraSubmit.data and deleteCameraForm.validate():
        # reading data from file
        with open('cams.json', 'r') as json_file:
            data = json.load(json_file)
            json_file.close()
        
        # writing data to json
        with open('cams.json', 'w') as json_file:
            temp = data['cams']
            formValues = request.values.to_dict()
            cameraID = formValues['cameraID']
            temp.pop(int(cameraID))
            data['cams'] = temp
            json.dump(data, json_file, indent=4)
            json_file.close()

        # web-page success message
        flash('Camera with ID={cameraID} has been removed successfuly', 'success')
        return redirect(url_for('recorder'))


    # reading cameras from json
    with open('cams.json') as json_file:
        data = json.load(json_file)
        # cams = {}
        # for i in range(len(data['cams'])):
        #     cams.update({data['cams'][i]['name']: data['cams'][i]['address']})
        
        cams = []
        id = 0
        for item in data['cams']:
            cams.append([id, item['name'], item['address']])
            id += 1

    return render_template('recorder.html', cams=cams, addForm=addForm, 
                            deleteAllForm=deleteAllForm, deleteCameraForm=deleteCameraForm)


@app.route('/recorder/edit/<cameraID>', methods=['GET', 'POST'])
def recorder_edit(cameraID):
    editForm = cameralist_forms.EditCameraForm()

    # searching camera info by id in json
    with open('cams.json', 'r') as json_file:
        data = json.load(json_file)
        cameraInfo = data['cams'][int(cameraID)]
        json_file.close()
    
    # if delete button was pressed
    if editForm.deleteSubmit.data and editForm.validate():
        with open('cams.json', 'r') as json_file:
            data = json.load(json_file)
            json_file.close()
        
        with open('cams.json', 'w') as json_file:
            temp = data['cams']
            temp.pop(int(cameraID))
            data['cams'] = temp
            json.dump(data, json_file, indent=4)
            json_file.close()
        
        # web-page success message
        flash('Camera "{editForm.cameraName.data}" has been removed successfuly', 'success')
        return redirect(url_for('recorder'))
    
    # if edit button was pressed
    if editForm.editSubmit.data and editForm.validate():
        with open('cams.json', 'r') as json_file:
            data = json.load(json_file)
            json_file.close()
        
        with open('cams.json', 'w') as json_file:
            temp = data['cams']
            temp[int(cameraID)] = {
                        "name": editForm.cameraName.data,
                        "address": editForm.rtspName.data
                    }
            json_file.seek(0)
            json.dump(data, json_file, indent=4)
            json_file.close()
        
        # web-page success message
        flash('Camera "{editForm.cameraName.data}" has been edited successfuly', 'success')
        return redirect(url_for('recorder'))
    
    return render_template('recorder_edit.html', camera=cameraInfo, editForm=editForm)

# @login.user_loader
# def load_user(user_id):
#     return user_id
    #User.objects(pk=user_id).first()




if __name__ == "__main__":
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"

    app.run(debug=True)
