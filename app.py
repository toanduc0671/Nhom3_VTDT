import os
import fnmatch
import json
import re
from flask import Flask, render_template, url_for
from flask import request, redirect
from ara.clients.offline import AraOfflineClient

client = AraOfflineClient()


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
    os.system('export ANSIBLE_CALLBACK_PLUGINS="$(python3 -m ara.setup.callback_plugins)"')
    os.system("ansible-playbook -i " + path_to_savefile + "/" + input_inventory +
              " " + path_to_savefile + "/" + input_playbook + " > gg.txt")

    return json.dumps({"deploy status": True})


# Ansible ara
@app.route('/playbook/<plb_id>', methods = ["GET","POST"])
def results(plb_id):
    # playbooks = client.get("/api/v1/playbooks")
    data_list = []
    # Get detail a bout task in playbook

    results = client.get("/api/v1/results?playbook=%s" % plb_id)
    hosts = client.get("/api/v1/hosts?playbook=%s" % plb_id)
    files = client.get("/api/v1/files?playbook=%s" % plb_id)

    host_list = []
    for host in hosts["results"]:
        host_list.append(host["name"])

    file_list = []
    for file in files["results"]:
        file_list.append(file["path"])

    # For each result, print the task and host information
    for result in results["results"]:
        task = client.get("/api/v1/tasks/%s" % result["task"])
        host = client.get("/api/v1/hosts/%s" % result["host"])
        
        data = {
            "id": task["id"],
            "timestamp": result["ended"],
            "host": host["name"],
            "action": task["action"],
            "task": task["name"],
            "status": task["status"],
            "duration": task["duration"],
            "task_file": task["path"],
        }
        data_list.append(data)
    data_list.append(host_list)
    data_list.append(file_list)
    return json.dumps(data_list)


@app.route('/playbooks', methods = ["GET","POST"])
def playbooks():
    if request.method == "GET":
        playbooks = client.get("/api/v1/playbooks")
        data_list = []
        return render_template("detail.html", playbooks = json.dumps(playbooks["results"][0]))
    elif request.method == "POST":
        # if request.form.get("action") == "check_detail" :
        playbooks = client.get("/api/v1/playbooks")
        get_Playbooks = playbooks["results"]
        # get playbook index from form submit to get playbook id to view detail  
        playbook_id = str(get_Playbooks[0]["id"])
        return redirect(url_for('results', plb_id = playbook_id))


if __name__ == "__main__":
    app.run(debug=True)
