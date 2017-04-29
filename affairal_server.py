from flask import Flask,url_for,render_template,request,jsonify,send_from_directory
import requests
import json
import pprint
from flask.ext.pymongo import PyMongo
from werkzeug import secure_filename
from bson import ObjectId
import os

app = Flask(__name__)
##MONGODB CONFIG
mongousername='champrakri'
mongopassword='databasepassword'

## NOT HANDLING CONNECTION & SERVER DOWN EXCEPTIONS
#app.config['MONGO_URI']='mongodb://localhost:27017/affairal_hiring'
app.config['MONGO_URI']='mongodb://champrakri:databasepassword@ds123351.mlab.com:23351/affairal_hiring'
mongo = PyMongo(app)

#FILE UPLOADS
app.config['UPLOAD_FOLDER'] = 'uploads/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set([ 'png', 'jpg', 'jpeg'])

# For a given file, return whether it's an allowed type or not







def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
##------------------------------- Validate User Credentials -----------------------------

def valid_user_creds(user):
    #sample code for now , NOT VALIDATING EXPLICITLY!
    if(('fullname' in user) and ('mobilenumber' in user) and ('email' in user) and ('notickets' in user) and ('regtype' in user) and ('idfile' in user) ):
        if((user['fullname']!='') and (user['mobilenumber']!='') and (user['email']!='') and (user['notickets']!='') and (user['regtype']!='') and (user['idfile']!='')):
            return True
        else:
            return False
    else:
        return False

def register_the_user(user):
    #NOT HANDLING DATA BASE DOWN ERRORS, JUST INSERTING FOR NOW

    result=mongo.db.users.insert(user)


    #result=mongo.db.users.insert(user)

    print 'user_reg_done'
    return jsonify({'done':'user_reg_done','regid':str(result)})





@app.route('/')
def home_page():
    #result=mongo.db.users.insert([{'name':'RadhaKrishna','age':'18'},{'name':'RadhaKrishna1','age':'18'},{'name':'RadhaKrishna2','age':'18'}])
    #print result
    return render_template('index.html')

@app.route('/event')
def render_event():
    return render_template('event.html')
@app.route('/admin')
def render_admin():
    return render_template('admin.html')


@app.route('/regstats')
def render_regstats():
    x=[]
    x.append(mongo.db.users.count(({'regtype':'self'})))
    x.append(mongo.db.users.count(({'regtype':'group'})))
    x.append(mongo.db.users.count(({'regtype':'corporate'})))
    x.append(mongo.db.users.count(({'regtype':'others'})))
    return render_template('regstats.html',data=x)


@app.route('/register',methods=['POST'])
def register_user():
    user= request.get_json()['user']
    from datetime import datetime
    user['time']=str(datetime.now())

    if request.method=='POST':
        if(valid_user_creds(user)):
            return register_the_user(user)
        else:
            error='invalid_creds'
    else:
        error='invalid_req'
    return jsonify({'error':error})

@app.route('/regdata',methods=['GET'])
def get_reg_data():
    users=mongo.db.users.find(({}),({"idfile":0}))
    #print list(users)
    return render_template('registrations.html',usersdata=users)

@app.route('/proofid/<ids>',methods=['GET'])
def get_profid_data(ids):
    prid=mongo.db.users.find(({'_id':ObjectId(ids)}),({"idfile":1}))
    x= list(prid)
    #print x
    return render_template('proofid.html',datas=x)




    #return json.dumps(pincode_req.json())



@app.route('/shutdown', methods=['GET','POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'
if __name__ == '__main__':
     app.debug = True
     port = int(os.environ.get("PORT", 33507))
     app.run(host='0.0.0.0', port=port)
