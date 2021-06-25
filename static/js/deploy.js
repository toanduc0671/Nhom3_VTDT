// Khi load xong thì lấy dữ liệu cho vào select
document.onreadystatechange = function () {
    if (document.readyState == "complete") {
        let xhr = new XMLHttpRequest();

        // Khi request xử lý xong chạy function
        xhr.onload = function () {
            let response = JSON.parse(this.responseText);
            // Inventory
            let options = "";
            for (let x of response["inventory"]) {
                options += `<option value="${x}">${x.split(".")[0].toLowerCase().replace(/\w/, firstLetter => firstLetter.toUpperCase())}</option>`;
            }
            document.getElementById("inventorySelect").innerHTML = options;

            // Playbook
            options = "";
            for (let x of response["playbook"]) {
                options += `<option value="${x}">${x.split(".")[0].toLowerCase().replace(/\w/, firstLetter => firstLetter.toUpperCase())}</option>`;
            }
            document.getElementById("playbookSelect").innerHTML = options;
        }

        xhr.open('GET', '/list', true);
        xhr.send();
    }
}

var form = document.getElementById("deployform");
var submit = document.getElementById("submitButton");

// Huỷ submit thật mà thay bằng gọi thằng khác
form.onsubmit = function () {
    // IMPORTANT
    return false; // To avoid actual submission of the form
}

// Khi click nó sẽ chạy function này (submit vẫn chạy song song nhưng sẽ bị huỷ do thằng ở trên)
submit.onclick = function () {
    // Edit button to loading status
    submit.classList.add("button--loading");
    submit.setAttribute("disabled", "");

    let formData = new FormData(form);

    let xhr = new XMLHttpRequest();

    // Khi request xử lý xong chạy function
    xhr.onload = function () {
        let response = JSON.parse(this.responseText);

        console.log(response);

        // Edit button to default
        submit.classList.remove("button--loading");
        submit.removeAttribute("disabled");
    }

    xhr.open('POST', "/deploy", true);
    xhr.send(formData);
}