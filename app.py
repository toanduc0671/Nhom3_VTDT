import os
from flask import Flask, render_template
from flask import request, redirect

app=Flask(__name__)

app.config["UPLOADS"] = "D:/basicweb/static/savefile"

@app.route('/')
def home():
    app.route('/')
    return render_template("home.html")

@app.route('/about/')
def about():
    return render_template("about.html")


@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        if request.files:
            file = request.files["file"]
            file.save(os.path.join(app.config["UPLOADS"], file.filename))
            print("File saved")
            return redirect(request.url)
    return render_template("upload.html")


if __name__=="__main__":
    app.run(debug=True)