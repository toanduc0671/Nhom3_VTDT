import os
from flask import Flask, render_template
from flask import request, redirect

app=Flask(__name__, static_url_path='', static_folder='static', template_folder='templates')

app.config["UPLOADS"] = "/home/toan/Desktop/Nhom3_VTDT-main/static/savefile"

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
            print("File saved")
            return redirect(request.url)
        if request.form.get('action') == 'start Deploy':
            check1 = os.path.isfile('/home/toan/Desktop/Nhom3_VTDT-main/static/savefile/inventory')
            if check1==True:
                os.system("ansible-playbook -i /home/toan/Desktop/Nhom3_VTDT-main/static/savefile/inventory /home/toan/Desktop/Nhom3_VTDT-main/static/savefile/playbook.yaml > /home/toan/Desktop/gg.txt")
                
    return render_template("upload.html")

@app.route("/about")
def about():
    return render_template("about.html")

if __name__=="__main__":
    app.run(debug=True)
