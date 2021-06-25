// Add the following code if you want the name of the file appear on select
$(".custom-file-input").on("change", function () {
    var fileName = $(this).val().split("\\").pop();
    $(this).siblings(".custom-file-label").addClass("selected").html(fileName);
});

var form = document.getElementById("uploadform");
var submit = document.getElementById("submitButton");
var successIcon = document.getElementById("successIcon");
var unreachableIcon = document.getElementById("unreachableIcon");
var detailsText = document.getElementById("details");
var modalTitle = document.getElementsByClassName("modal-title")[0];
var notiText = document.getElementById("notiText");

// Huỷ submit thật mà thay bằng gọi thằng khác
form.onsubmit = function () {
    // IMPORTANT
    return false; // To avoid actual submission of the form
}

// Khi click nó sẽ chạy function này (submit vẫn chạy song song nhưng sẽ bị huỷ do thằng ở trên)
submit.onclick = function () {
    // Reset part
    // Reset to disable
    successIcon.setAttribute("hidden", "");
    unreachableIcon.setAttribute("hidden", "");
    detailsText.setAttribute("hidden", "");
    // Hide collapse in modal
    $('#collapseDetails').collapse('hide');

    // Valid does upload file empty or not
    if (form["file"].value.length == 0) {
        // Edit modal
        modalTitle.textContent = "File is empty";
        unreachableIcon.removeAttribute("hidden");
        notiText.innerHTML = "You haven't selected file.";

        // Show modal
        $('#notiModal').modal('show');
        return;
    }

    // Switch case từng select của người dùng
    switch (form["typeFileSelect"].value) {
        case "playbook":
            upload("upload status", "Upload successfully", "Upload file successfully",
                "Upload unsuccessfully", "Upload file unsuccessfully", false, "/upload_playbook");
            break;
        case "role":
            upload("upload status", "Upload successfully", "Upload file successfully",
                "Upload unsuccessfully", "Upload file unsuccessfully", false, "/upload_role");
            break;
        default:
            upload("connection status", "Connection successfully", "Connect to all host successfully",
                "Connection unsuccessfully", "Connect to all host unsuccessfully", true, "/upload_inventory");
    }
}

function upload(responseArg, successTitle, successText, failTitle, failText, isShowDetails, actionLink) {
    let formData = new FormData(form);

    let xhr = new XMLHttpRequest();

    // Khi request xử lý xong chạy function
    xhr.onload = function () {
        let response = JSON.parse(this.responseText);

        // Setup icon and title of modal
        if (response[responseArg]) {
            // Success
            modalTitle.textContent = successTitle;
            successIcon.removeAttribute("hidden");
            notiText.innerHTML = successText;
        } else {
            // Unreachable
            modalTitle.textContent = failTitle;
            unreachableIcon.removeAttribute("hidden");
            notiText.innerHTML = failText;
        }

        // Kiểm tra có cần phải show details không
        if (isShowDetails) {
            // Show details collapse
            detailsText.removeAttribute("hidden");

            // Create details of modal
            let details = "";
            for (let i = 0; i < response.ip.length; i++) {
                let className = "successCode";
                if (response["status"][i] === "UNREACHABLE") {
                    className = "unreachableCode";
                }

                details += `<div class="row justify-content-between">
                            <div class="col-md-auto">
                                <code class="${className}">${response["ip"][i]}</code>
                            </div>
                            <div class="col-md-auto">
                                <code class="${className}">${response["status"][i]}</code>
                            </div>
                        </div>`;
            }
            // Writing details in modal
            document.querySelector("#collapseDetails > div").innerHTML = details;
        }

        // Show modal
        $('#notiModal').modal('show');

        // Edit button to default
        submit.classList.remove("button--loading");
        submit.removeAttribute("disabled");
    }

    // Khi state đang bằng 1 (đã được open) thì chạy function này
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 1) {
            // Edit button to loading status
            submit.classList.add("button--loading");
            submit.setAttribute("disabled", "");
        }
    };

    xhr.open('POST', actionLink, true);
    xhr.send(formData);
}