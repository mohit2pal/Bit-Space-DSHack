from flask import Flask, render_template, session, abort, redirect, request
from flask_cors import CORS, cross_origin
from form import *
from goog_functions import ocr_function , gcs_upload

import os
import pathlib
import json
import base64

import requests
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests

app = Flask(__name__)
app.secret_key = "Bits-Space"
CORS(app)

current_user = "not_defined"
name2=""
age2=""
gender2=""
blood_group2=""
height2=""
weight2=""
contact2=""
bmi2=""
email=""

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

GOOGLE_CLIENT_ID = "842363639124-useb2nft637f7petod0fqk68e101tbm2.apps.googleusercontent.com"
client_secrets_file = os.path.join(
    pathlib.Path(__file__).parent, "client_secret.json")


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('login.html')


@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        img_base64 = request.get_json()
        
        decode = open('IMAGE.jpg', 'wb')
        decode.write(base64.b64decode(img_base64['pdf']))
        
    

    return render_template('account.html',current_user_id=current_user)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    
    global name2 
    global age2 
    global gender2 
    global blood_group2 
    global height2 
    global weight2 
    global contact2 
    global bmi2
    
    with open("./static/json/user_heal_data.json", "r") as k:
        user_data = json.load(k)
        
    if current_user in user_data:
        print("Going to profile details")
        return redirect("/profile_details")
    
    else:
        form = SignUpForm()
        if form.is_submitted():
         result= request.form
         name2 =request.form['name']
         age2 =request.form['age']
         gender2 =request.form['gender']
         blood_group2 =request.form['blood_group']
         height2 =request.form['height']
         weight2 =request.form['weight']
         contact2 =request.form['contact']
         print(name2,age2,gender2,blood_group2,height2,weight2,contact2)
         
         h2 = float(float(height2) * float(height2))
         bmir = float(float(weight2)/float(h2))
         
         bmi2 = round(bmir,2)
         
         
         with open("./static/json/user_heal_data.json", "r") as o:
             user_data = json.load(o)
     
         user_data[current_user] = { "Name" : name2 , "Email":email,"Age" : age2,"Gender":gender2,"Height":height2,"Weight":weight2,"BMI":bmi2,"Blood group":blood_group2,"Contact info":contact2}
       
         with open("./static/json/user_heal_data.json", "w") as p:
             json.dump(user_data , p)
         return redirect("/profile_details")
        return render_template('profile.html',current_user_id=current_user,form=form)
        
        


@app.route('/profile_details', methods=['GET', 'POST'])
def profile_detail():
       with open("./static/json/user_heal_data.json", "r") as l:
             user_data = json.load(l)
       
       nameh = user_data[current_user]['Name']
       emailh = user_data[current_user]['Email']
       ageh = user_data[current_user]['Age']
       genderh = user_data[current_user]['Gender']
       heighth = user_data[current_user]['Height']
       weighth = user_data[current_user]['Weight']
       bmih = user_data[current_user]['BMI']
       bloodgrouph = user_data[current_user]['Blood group']
       contacth = user_data[current_user]['Contact info']
       return render_template('profile_details.html',current_user_id=current_user,namet=nameh,emailt=emailh,aget=ageh,gendert=genderh,blood_groupt=bloodgrouph,heightt=heighth,weightt=weighth,bmit=bmih,contactt=contacth)



@app.route('/Edit_details', methods=['GET', 'POST'])
def edit():
    with open("./static/json/user_heal_data.json", "r") as m:
        user_data = json.load(m)
        
    if current_user in user_data:
        print("Going to profile")
        del user_data[current_user]
        with open("./static/json/user_heal_data.json", "w") as x:
             json.dump(user_data , x)
        print(user_data)
        return redirect("/profile")

        
    
        
    
    
# @app.route('/profilename', methods=['GET', 'POST'])
# def profilename():
#     if request.method == "POST":
#         name = request.form.get("fname")
    
#     return "Your name is"+ name




flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile",
            "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1:5000/callback"
)


def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)  # Authorization required
        else:
            return function()

    return wrapper


@app.route("/login")
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


@app.route("/callback")
def callback():
    
    global current_user
    global email
    
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(
        session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )
    
    email = id_info.get("email")
    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    session["email"] = id_info.get("email")
    
    
    current_user = id_info.get("sub")
      
    with open('./static/json/user_id.json', 'r') as u:
        user_id_json_data = json.load(u)
        
    user_id_json_data[id_info.get("sub")] = { "user_name" : id_info.get("name") , "user_email" : id_info.get("email"), "user_dp": id_info.get("picture")}
    
    with open('./static/json/user_id.json', 'w') as y:
        json.dump(user_id_json_data, y)
        
    return redirect("/home")


@app.route("/logout")
def logout():
    global current_user
    session.clear()
    current_user = "not_defined"
    return redirect("/")



if __name__ == '__main__':
    app.run()
