document.addEventListener('DOMContentLoaded', function () {
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
            var pet_id = this.value;
            var route = '/device_names/' + pet_id + '/';
            fetch(route)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to remove access');
                }
                return response.text();
            })
            .then(data => {
                var devices = JSON.parse(data);

                var picker_id = "acc_dev_picker_" + pet_id;
                var picker = document.getElementById(picker_id);

                picker.innerHTML = '';

                devices.forEach(function(item) {
                    console.log(item[0]);
                    var option = document.createElement("option");
                    option.value = item[0];
                    option.text = item[1];

                    picker.appendChild(option);
                });

                var acc_form_id = "pet_acc_form_" + pet_id;
                var acc_form = document.getElementById(acc_form_id);

                acc_form.style.display = "block";

                acc_form.addEventListener("submit", function (event) {
                    event.preventDefault();

                    var device_id = picker.options[picker.selectedIndex].value;

                    addAccess(device_id, pet_id);
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