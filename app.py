import os
import fnmatch
import time
import json
import re
from flask import Flask, render_template
from flask import request, redirect
from flask import jsonify

app=Flask(__name__, static_url_path='', static_folder='static', template_folder='templates')

path_to_savefile = "./static/savefile"
gg = "gg.txt"
app.config["UPLOADS"] = path_to_savefile


@app.route('/')
def home():
    app.route('/')
    return render_template("home.html")

@app.route("/deploy", methods=["GET", "POST"])
def deploy():
    if request.method == "POST":

        if request.form.get('action') == 'List Inventory and Playbook':
            inven = fnmatch.filter(os.listdir(path_to_savefile), "*.ini") 
            playbook = fnmatch.filter(os.listdir(path_to_savefile), "*.yml")
            return render_template("deploy.html", inven=inven, playbook=playbook)

        if request.form.get('action') == 'Start Deploy':
            inven = fnmatch.filter(os.listdir(path_to_savefile), "*.ini")      #bien nay list cac file .ini
            playbook = fnmatch.filter(os.listdir(path_to_savefile), "*.yml")   #bien nay list cac file .yml
            input_inventory = request.form['input_inventory']
            input_playbook = request.form['input_playbook']
            check1 = os.path.isfile(path_to_savefile + "/" + input_inventory)
            # print(check1)
            if check1==True:
                os.system("ansible-playbook -i " + path_to_savefile + "/" + input_inventory + " " + path_to_savefile + "/" + input_playbook + " > /home/toan/Desktop/gg.txt") 

            if input_playbook in playbook and input_inventory in inven:
                processed_text = "successful deploy "
                return render_template("deploy.html", processed_text=processed_text, inven=inven, playbook=playbook)
            else:
                processed_text = "wrong input"
                return render_template("deploy.html", processed_text=processed_text, inven=inven, playbook=playbook)
 
    return render_template("deploy.html")

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        if request.form.get('action') == 'Upload Playbook':
            return render_template("upload_playbook.html")
        if request.form.get('action') == 'Upload Inventory':
            return render_template("upload_inventory.html")
        if request.form.get('action') == 'Upload Roles':
            return render_template("upload_role.html")
    return render_template("upload.html")

@app.route('/upload_inventory', methods=["GET", "POST"])
def inventory():
    if request.method == "POST":
        if request.files:
            file = request.files["file"]
            file.save(os.path.join(app.config["UPLOADS"], file.filename))
            os.system("ansible -i " + path_to_savefile + "/" + file.filename + " -m ping all > " + gg)
            f = open(gg, "r")
            text = f.read()
            def getStatus(logs):
                lstIp = list()
                for i in list(dict.fromkeys(logs.split())):
                    if re.findall(r"^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)(\.(?!$)|$)){4}$", i):
                        lstIp.append(i)
             
                valueList = re.findall(r"SUCCESS|UNREACHABLE", logs)
                result = dict()
                result['ip'] = lstIp
                result['status'] = valueList
                return result
            a = getStatus(text)
            flag = True
            temp = {"ip": [], "status": []}
            if "UNREACHABLE" in str(a["status"]) or a == temp:
                flag = False
            connection_status = {"connection status": flag}

            json_dumps = json.dumps(connection_status)              #bien nay tra ve {"connection status": true}
            ip_status =  json.dumps(getStatus(text))                #bien nay tra ve {"ip": ["192.168.1.16", "192.168.1.12"], "status": ["SUCCESS", "SUCCESS"]}
            print("File saved")
            if (flag == False):
                os.system("rm " + path_to_savefile + "/" + file.filename)
            return render_template("upload_inventory.html", ip_status=ip_status, json_dumps=json_dumps)
    return render_template("upload_inventory.html")

@app.route('/upload_playbook', methods=["GET", "POST"])
def playbook():
    if request.method == "POST":
        if request.files:
            file = request.files["file"]
            file.save(os.path.join(app.config["UPLOADS"], file.filename))
            print("File saved")
            return redirect(request.url)
    return render_template("upload_playbook.html")

@app.route('/upload_role', methods=["GET", "POST"])
def role():
    if request.method == "POST":
        if request.files:
            file = request.files["file"]
            file.save(os.path.join(app.config["UPLOADS"], file.filename))
            print("File saved")
            os.system("unzip -o " + path_to_savefile + "/" + file.filename + " -d" + path_to_savefile)
            return redirect(request.url)
    return render_template("upload_role.html")


if __name__=="__main__":
    app.run(debug=True)
