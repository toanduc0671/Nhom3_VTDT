import os
import fnmatch 
from flask import Flask, render_template
from flask import request, redirect
from flask import jsonify

app=Flask(__name__, static_url_path='', static_folder='static', template_folder='templates')

app.config["UPLOADS"] = "/home/toan/Desktop/Nhom3_VTDT-front-end/static/savefile"

@app.route('/')
def home():
    app.route('/')
    return render_template("home.html")

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        if request.files:
            file = request.files["file"]
            file.save(os.path.join(app.config["UPLOADS"], file.filename))
            path = "/home/toan/Desktop/Nhom3_VTDT-front-end/static/savefile"
            files = fnmatch.filter(os.listdir(path), "*.zip")            
            print("File saved")

            first_string = str(files)
            partitioned_string = first_string.rpartition('\'')
            second_string = partitioned_string[0]
            partitioned2_string = second_string.rpartition('\'')
            print(partitioned2_string[2])

            return redirect(request.url)
        if request.form.get('action') == 'check connection':
            os.system("ansible -i /home/toan/Desktop/Nhom3_VTDT-front-end/static/savefile/inventory.ini -m ping all > /home/toan/Desktop/gg.txt")
            f = open("/home/toan/Desktop/gg.txt", "r")
            gg = f.read()
            return render_template("upload.html", gg=gg)

    return render_template("upload.html")

@app.route("/deploy", methods=["GET", "POST"])
def deploy():
    if request.method == "POST":
        if request.form.get('action') == 'start Deploy':
            check1 = os.path.isfile('/home/toan/Desktop/Nhom3_VTDT-front-end/static/savefile/inventory.ini')
            print(check1)
            if check1==True:
                os.system("ansible-playbook -i /home/toan/Desktop/Nhom3_VTDT-front-end/static/savefile/inventory.ini /home/toan/Desktop/Nhom3_VTDT-front-end/static/savefile/site.yml> /home/toan/Desktop/gg.txt") 

        if request.form.get('action') == 'List playbook':
            path = "/home/toan/Desktop/Nhom3_VTDT-front-end/static/savefile"
            files = fnmatch.filter(os.listdir(path), "*.yml")
            print(files)
            return render_template("deploy.html", files=files)

    return render_template("deploy.html")

if __name__=="__main__":
    app.run(debug=True)
