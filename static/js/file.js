// Khi load xong thì lấy dữ liệu
document.onreadystatechange = function () {
    if (document.readyState == "complete") {
        let xhr = new XMLHttpRequest();

        // Khi request xử lý xong chạy function
        xhr.onload = function () {
            let response = JSON.parse(xhr.responseText);
            renderInventory(response["inventory"])
            renderPlaybook(response["playbook"])
            renderRole(response["roles"])

            // High light
            hljs.highlightAll();
        }

        xhr.open('GET', '/fileContent', true);
        xhr.send();
    }
}

function renderInventory(inventory) {
    let mainCard = document.getElementById("inventory").getElementsByClassName("card-body")[0];
    let temp = "";
    for (fileName in inventory) {
        let id = `${fileName.split(".")[0]}-${fileName.split(".")[1]}`
        temp += `<div class="card mb-3">
                    <div class="card-header" id="headingOne">
                        <button class="btn btn-link text-left" type="button" data-toggle="collapse"
                            data-target="#${id}">
                            ${fileName}
                        </button>
                    </div>

                    <div id="${id}" class="collapse">
                        <div class="card-body">
                            <pre><code class="language-ini">${inventory[fileName]}</code></pre>
                        </div>
                    </div>
                </div>`;
    }
    mainCard.innerHTML = temp;
}

function renderPlaybook(playbook) {
    let mainCard = document.getElementById("playbook").getElementsByClassName("card-body")[0];
    let temp = "";
    for (fileName in playbook) {
        let id = `${fileName.split(".")[0]}-${fileName.split(".")[1]}`
        temp += `<div class="card mb-3">
                    <div class="card-header" id="headingOne">
                        <button class="btn btn-link text-left" type="button" data-toggle="collapse"
                            data-target="#${id}">
                            ${fileName}
                        </button>
                    </div>

                    <div id="${id}" class="collapse">
                        <div class="card-body">
                            <pre><code class="language-yaml">${playbook[fileName]}</code></pre>
                        </div>
                    </div>
                </div>`;
    }
    mainCard.innerHTML = temp;
}

function renderRole(role) {
    let mainCard = document.getElementById("role").getElementsByClassName("card-body")[0];
    let roles = "";
    // role name
    for (roleName in role) {
        let folders = "";
        // Folder name
        for (nameFolder in role[roleName]) {
            let files = "";
            for (fileName in role[roleName][nameFolder]) {
                let idFile = `${roleName}-${nameFolder}-${fileName.split(".")[0]}-${fileName.split(".")[1]}`
                files += `<div class="card mb-3">
                    <div class="card-header" id="headingOne">
                        <button class="btn btn-link text-left" type="button" data-toggle="collapse"
                            data-target="#${idFile}">
                            ${fileName}
                        </button>
                    </div>

                    <div id="${idFile}" class="collapse">
                        <div class="card-body">
                            <pre><code class="language-yaml">${role[roleName][nameFolder][fileName]}</code></pre>
                        </div>
                    </div>
                </div>`;
            }
            let idFolder = `${roleName}-${nameFolder}`
            folders += `<div class="card mb-3">
                            <div class="card-header" id="headingOne">
                                <button class="btn btn-link text-left" type="button" data-toggle="collapse"
                                    data-target="#${idFolder}">
                                    ${nameFolder}
                                </button>
                            </div>

                            <div id="${idFolder}" class="collapse">
                                <div class="card-body">
                                    ${files}
                                </div>
                            </div>
                        </div>`;
        }
        idRole = `${roleName}`
        roles += `<div class="card mb-3">
                    <div class="card-header" id="headingOne">
                        <button class="btn btn-link text-left" type="button" data-toggle="collapse"
                            data-target="#${idRole}">
                            ${roleName}
                        </button>
                    </div>

                    <div id="${idRole}" class="collapse">
                        <div class="card-body">
                            ${folders}
                        </div>
                    </div>
                </div>`;
    }
    mainCard.innerHTML = roles;
}