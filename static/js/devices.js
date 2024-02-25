document.addEventListener('DOMContentLoaded', function () {
    setInterval(checkLidStatus, 5000);
    var open_btn = document.getElementById("open-btn");
    open_btn.addEventListener("click", function (event) {
        open_btn.disabled = true;
        fetch('/open/')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to open lid');
                }
                return response.text();
            })
            .then(data => {
                console.log(data);
            })
            .catch(error => {
                console.error('Error:', error);
            });
    });

    var close_btn = document.getElementById("close-btn");
    close_btn.addEventListener("click", function (event) {
        close_btn.disabled = true;
        fetch('/close/')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to close lid');
                }
                return response.text();
            })
            .then(data => {
                console.log(data);
            })
            .catch(error => {
                console.error('Error:', error);
            });
    });

    var buttons = document.querySelectorAll(".rm-acc-btn");

    buttons.forEach(function (button) {
        button.addEventListener("click", function () {
            var route = '/access/' + this.value + '/remove/';
            fetch(route)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to remove access');
                }
                return response.text();
            })
            .then(data => {
                console.log(data);
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    });

    var add_acc_buttons = document.querySelectorAll(".add-acc-btn");

    add_acc_buttons.forEach(function (button) {
        button.addEventListener("click", function () {
            var device_id = this.value;
            var route = '/pet_names/' + device_id + '/';
            fetch(route)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to remove access');
                }
                return response.text();
            })
            .then(data => {
                var pets = JSON.parse(data);

                var picker_id = "acc_pet_picker_" + device_id;
                var picker = document.getElementById(picker_id);

                picker.innerHTML = '';

                pets.forEach(function(item) {
                    console.log(item[0]);
                    var option = document.createElement("option");
                    option.value = item[0];
                    option.text = item[1];

                    picker.appendChild(option);
                });

                var acc_form_id = "dev_acc_form_" + device_id;
                var acc_form = document.getElementById(acc_form_id);

                acc_form.style.display = "block";

                acc_form.addEventListener("submit", function (event) {
                    event.preventDefault();

                    var pet = picker.options[picker.selectedIndex].value;

                    addAccess(device_id, pet);
                });
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    });
});

function addAccess(device_id, pet_id) {
    var route = "/access/" + pet_id + "/" + device_id + "/";

    fetch(route)
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to add access');
            }
            return response.text();
        })
        .then(data => {
            console.log(data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
}


function checkLidStatus() {
    fetch('/lid_status/')
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to access lid status');
            }
            return response.text();
        })
        .then(data => {
            var open_btn = document.getElementById("open-btn");
            var close_btn = document.getElementById("close-btn");

            document.querySelectorAll(".device-status").forEach(function (status) {
                if (data === 'OPENED') {
                    status.innerText = 'OTWARTY';
                    open_btn.style.display = 'none';
                    close_btn.disabled = false;
                    close_btn.style.display = 'block';
                }
                else {
                    status.innerText = 'ZAMKNIĘTY';
                    close_btn.style.display = 'none';
                    open_btn.disabled = false;
                    open_btn.style.display = 'block';
                }
            });
        })
        .catch(error => {
            console.error('Error:', error);
        });
}