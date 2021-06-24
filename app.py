import os
import fnmatch
import json
import re
from flask import Flask, render_template
from flask import request, redirect

app = Flask(__name__, static_url_path='',
            static_folder='static', template_folder='templates')

path_to_savefile = "./static/savefile"
gg = "gg.txt"
app.config["UPLOADS"] = path_to_savefile


@app.route('/')
def home():
    return render_template("home.html")


# Chỉ return về trang upload
@app.route("/upload", methods=["GET"])
def upload():
    return render_template("upload.html")


# Chỉ upload file inventory và return về connection status format json
@app.route('/upload_inventory', methods=["POST"])
def inventory():
    # Không cần kiểm tra file có hay không, đã valid ở front end
    file = request.files["file"]
    file.save(os.path.join(app.config["UPLOADS"], file.filename))
    os.system("ansible -i " + path_to_savefile + "/" +
              file.filename + " -m ping all > " + gg)
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

    # đổi tên biến
    status = getStatus(text)

    flag = True

    # So sánh trực tiếp
    if "UNREACHABLE" in str(status["status"]) or status == {"ip": [], "status": []}:
        flag = False

    # Cho thêm connection_status vào dict
    status.update({"connection status": flag})

    # Nếu file không connect 100% thì xoá
    if not flag:
        os.system("rm " + path_to_savefile + "/" + file.filename)

    return json.dumps(status)


# Chỉ upload file playbook và return về upload status format json
@app.route('/upload_playbook', methods=["POST"])
def playbook():
    # Không cần kiểm tra file có hay không, đã valid ở front end
    file = request.files["file"]
    file.save(os.path.join(app.config["UPLOADS"], file.filename))

    return json.dumps({"upload status": True})


# Chỉ upload file role và return về upload status format json
@app.route('/upload_role', methods=["POST"])
def role():
    # Không cần kiểm tra file có hay không, đã valid ở front end
    file = request.files["file"]
    file.save(os.path.join(app.config["UPLOADS"], file.filename))

    os.system("unzip -o " + path_to_savefile + "/" +
              file.filename + " -d" + path_to_savefile)

    return json.dumps({"upload status": True})


# Return về list inventory và playbook
@app.route("/list", methods=["GET"])
def listInventory():
    inven = fnmatch.filter(os.listdir(path_to_savefile), "*.ini")
    playbook = fnmatch.filter(os.listdir(path_to_savefile), "*.yml")
    result = {"inventory": inven, "playbook": playbook}
    return json.dumps(result)


@app.route("/deploy", methods=["GET", "POST"])
def deploy():
    # Get return luôn
    if request.method == "GET":
        return render_template("deploy.html")

    # Không cần kiểm tra file tồn tại vì file đã select từ list route ở trên
    input_inventory = request.form['inventorySelect']
    input_playbook = request.form['playbookSelect']

    os.system("ansible-playbook -i " + path_to_savefile + "/" + input_inventory +
              " " + path_to_savefile + "/" + input_playbook + " > gg.txt")

    return json.dumps({"deploy status": True})


if __name__ == "__main__":
    app.run(debug=True)
