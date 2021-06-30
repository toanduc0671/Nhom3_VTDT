// Khi load xong thì lấy dữ liệu cho vào select
document.onreadystatechange = function () {
    if (document.readyState == "complete") {
        let xhr = new XMLHttpRequest();

        // Khi request xử lý xong chạy function
        xhr.onload = function () {
            let response = JSON.parse(xhr.responseText);
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
var eleHostResult = document.getElementById("host-result");
var eleTaskResult = document.getElementById("task-result");

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

	let interval = undefined

    let formData = new FormData(form);

    let xhr = new XMLHttpRequest();

    // Khi request xử lý xong chạy function
    xhr.onload = function () {

        let response = JSON.parse(xhr.responseText);

        console.log(response);

        // Edit button to default
        submit.classList.remove("button--loading");
        submit.removeAttribute("disabled");

		// Dừng lấy process
		clearInterval(interval)
		// Lấy lần cuối - cho chắc
		update_process()
    }

    // Khi state đang bằng 1 (đã được open) thì chạy function này
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 1) {
			// Ngủ 5s rồi mới bắt đầu fetch data -> để cho backend chạy ổn
			setTimeout(() => {
				// Update process every 1,721s
				interval = setInterval(update_process, 1721);
			}, 5000);
        }
    };

    xhr.open('POST', "/deploy", true);
    xhr.send(formData);
}

// Function để lấy result fetch vào front end
function update_process() {
    let xhr = new XMLHttpRequest();
    // Khi request xử lý xong chạy function
    xhr.onload = function () {
        let response = JSON.parse(xhr.responseText);

        // Count = 0 -> ko có playbook nào cả thì exit
        if (response["count"] == 0) {
            return;
        }

        process_result(response["id"])
    }

    xhr.open('GET', "/history/lastplaybook", true);
    xhr.send();
}

function process_result(id) {
    let xhr = new XMLHttpRequest();

    // Khi request xử lý xong chạy function
    xhr.onload = function () {
        let response = JSON.parse(xhr.responseText);
		
		// Count = 0 thì exit
		if (response["count"] == 0){
			return
		}

        let hostResult = response["hostResult"];
        let taskResult = response["taskResult"];

        // Host result
        let tbodyHost = eleHostResult.getElementsByTagName("tbody")[0];
        let result = "";
        Object.keys(hostResult).forEach(function (host, i) {
            temp = "";
            Object.keys(hostResult[host]).forEach(function (status, j) {
                temp += `<span class="tag ${status.toLowerCase()}">${hostResult[host][status] + " " + status.toUpperCase()}</span>`;
            });

            result += `<tr>
                        <td scope="row">${host}</td>
                        <td>${temp}</td>
                    </tr>`;
        });
        tbodyHost.innerHTML = result;
		// Remove hidden
		eleHostResult.removeAttribute("hidden")

        // Task result
        let tbodyTask = eleTaskResult.getElementsByTagName("tbody")[0];
        result = "";
		for (let x of taskResult) {
			let temp = `<span class="tag ${x['status'].toLowerCase()}">${x['status'].toUpperCase()}</span>`;
			result += `<tr>
                        <td scope="row">${temp}</td>
                        <td>${x['host']}</td>
						<td>${x['action']}</td>
						<td>${x['task']}</td>
						<td>${x['duration'].slice(0, -4)}</td>
						<td>${dateFormat(new Date(x['timestamp']), "dd-mm-yyyy HH:MM:ss")}</td>
                    </tr>`;
		  }
		tbodyTask.innerHTML = result
		// Remove hidden
		eleTaskResult.removeAttribute("hidden")
    }

    xhr.open('GET', `/history/playbooks/${id}`, true);
    xhr.send();
}