import os
import fnmatch
import json
import re
from flask import Flask, render_template, url_for
from flask import request, redirect
from ara.clients.offline import AraOfflineClient
import pandas as pd

client = AraOfflineClient()


app = Flask(__name__, static_url_path='',
            static_folder='static', template_folder='templates')

path_to_savefile = "./static/savefile"
gg = "./static/savefile/log.txt"
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
def upload_inventory():
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
            if re.findall(
                r"^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)(\.(?!$)|$)){4}$",
                    i):
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
    if "UNREACHABLE" in str(
        status["status"]) or status == {
        "ip": [],
            "status": []}:
        flag = False

    # Cho thêm connection_status vào dict
    status.update({"connection status": flag})

    # Nếu file không connect 100% thì xoá
    if not flag:
        os.system("rm " + path_to_savefile + "/" + file.filename)

    return json.dumps(status)


# Chỉ upload file playbook và return về upload status format json
@app.route('/upload_playbook', methods=["POST"])
def upload_playbook():
    # Không cần kiểm tra file có hay không, đã valid ở front end
    file = request.files["file"]
    file.save(os.path.join(app.config["UPLOADS"], file.filename))

    return json.dumps({"upload status": True})


# Chỉ upload file role và return về upload status format json
@app.route('/upload_role', methods=["POST"])
def upload_role():
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
    os.system(
        "export ANSIBLE_CALLBACK_PLUGINS=$(python3 -m ara.setup.callback_plugins)")
    os.system(
        "ansible-playbook -i " + path_to_savefile + "/" + input_inventory + " " +
        path_to_savefile +
        "/" +
        input_playbook +
        " > " +
        gg)

    return json.dumps({"deploy status": True})


# Ansible ara
# Trả về tast result và host result của playbook
@app.route('/history/playbooks/<plb_id>', methods=["GET"])
def playbook(plb_id):
    # Get data from api
    results = client.get("/api/v1/results?playbook=%s" % plb_id)
    tasks = client.get("/api/v1/tasks", playbook=plb_id)
    hosts = client.get("/api/v1/hosts", playbook=plb_id)

    if results["count"] == 0 or tasks["count"] == 0 or hosts["count"] == 0:
        return json.dumps({"count": 0})

    # Convert to dataframe
    tasks = pd.DataFrame(tasks["results"]).set_index("id")
    hosts = pd.DataFrame(hosts["results"]).set_index("id")

    data = {'status': [],
            'host': [],
            'action': [],
            'task': [],
            'duration': [],
            'timestamp': []}

    # For each result information
    for result in results["results"]:
        idTask = result["task"]
        idHost = result["host"]

        data["status"].append(result["status"])
        data["host"].append(hosts.loc[idHost]["name"])
        data["action"].append(tasks.loc[idTask]["action"])
        data["task"].append(tasks.loc[idTask]["name"])
        data["duration"].append(result["duration"])
        data["timestamp"].append(result["ended"])

    # Convert
    taskResult = pd.DataFrame(data, dtype="string")

    # Process hostResult
    hostResult = taskResult.groupby(
        ['host', 'status']).size().reset_index(name='counts')
    hostResult = hostResult.sort_values(by=['host'])
    temp = dict()
    for index, row in hostResult.iterrows():
        if (index == 0) or (index > 0 and nameHost != row['host']):
            nameHost = row['host']
            temp[nameHost] = dict()

        temp[nameHost][row["status"]] = row["counts"]

    # Combination to 1 json
    result = dict()
    result["count"] = taskResult.shape[0]

    result["hostResult"] = temp

    taskResult = json.loads(taskResult.to_json(orient="records"))
    result["taskResult"] = taskResult

    # Convert to json
    return json.dumps(result)


# Lấy thông tin playbook mới nhất
@app.route('/history/lastplaybook', methods=["GET"])
def lastPlaybook():
    if request.method == "GET":
        playbook = client.get("/api/v1/playbooks", limit=1)

        # init
        temp = dict()
        temp["count"] = playbook["count"]

        if playbook["count"] != 0:
            temp["id"] = playbook["results"][0]["id"]
            temp["status"] = playbook["results"][0]["status"]
            temp["ansible_version"] = playbook["results"][0]["ansible_version"]

        return json.dumps(temp)


@app.route('/file', methods=["GET"])
def file():
    return render_template("file.html")

# Trả về File và nội dung


@app.route('/fileContent', methods=["GET"])
def getFilesContent():
    result = dict()

    # Inventory
    result["inventory"] = dict()
    for i in fnmatch.filter(os.listdir(app.config["UPLOADS"]), "*.ini"):
        with open("./static/savefile/%s" % i, "r") as f:
            result["inventory"][i] = f.read()

    # Playbook
    result["playbook"] = dict()
    for i in fnmatch.filter(os.listdir(app.config["UPLOADS"]), "*.yml"):
        with open("./static/savefile/%s" % i, "r") as f:
            result["playbook"][i] = f.read()
    result["roles"] = dict()
    # Tên các role
    for i in os.listdir(app.config["UPLOADS"] + "/roles"):
        result["roles"][i] = dict()
        # Tên các thư mục trong mỗi role
        for j in os.listdir(app.config["UPLOADS"] + "/roles/%s" % i):
            result["roles"][i][j] = dict()
            # Đọc từng file
            for k in os.listdir(
                    app.config["UPLOADS"] + "/roles/%s/%s" %
                    (i, j)):
                with open(app.config["UPLOADS"] + "/roles/%s/%s/%s" % (i, j, k), "r") as f:
                    result["roles"][i][j][k] = f.read()
    return json.dumps(result)
if __name__ == "__main__":
    app.run(debug=True)
