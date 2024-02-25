document.addEventListener("DOMContentLoaded", function() {
    setScanEvent();

    // wyświetlanie obrazka podczas dodawania
    document.getElementById("pet-picture").addEventListener("change", function(event) {
    var file = event.target.files[0];
    var img = document.getElementById("pet-img");

    // Check if a file is selected
    if (file) {
        // Check if the file is an image
        if (file.type.match('image.*')) {
            var reader = new FileReader();
            reader.onload = function(e) {
                // Update the image src attribute with the data URL
                img.src = e.target.result;
                img.style.display = 'block'; // Show the image
            };
            // Read the file as a data URL
            reader.readAsDataURL(file);
        } else {
            alert("Please select a valid image file.");
        }
    }
    });

    document.getElementById("pet-btn").addEventListener("click", function (event){
        updateTagInfo("Przyłóż zawieszkę do czytnika");

        var tag;

        scanRFID(function(data) {
            try {
                tag = data;
                document.getElementById("pet-rfid").value = tag;
                updateTagInfo("Zeskanowano");
            } catch (error) {
                console.error('Error:', error);
            }
        });
    });

});

window.addEventListener('beforeunload', function(event) {
    // Cancel the event to prevent the browser from closing immediately
    event.preventDefault();
    clearScanEvent();
    event.returnValue = null;
});

function setScanEvent() {
    fetch('/set_event/scan/')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to set event');
                }
                return response.text();
            })
            .then(data => {
                console.log(data); // Log the response from the server
            })
            .catch(error => {
                console.error('Error:', error);
            });
}


function clearScanEvent() {
    fetch('/clear_event/scan/')
        .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to clear event');
                }
                return response.text();
            })
            .then(data => {
                console.log(data); // Log the response from the server
            })
            .catch(error => {
                console.error('Error:', error);
            });
}


function scanRFID(callback) {
    fetch('/scan_rfid/')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to scan RFID tag');
                }
                return response.text();
            })
            .then(data => {
                callback(data);
            })
            .catch(error => {
                console.error('Error:', error);
            });
}


function updateTagInfo(msg){
    document.getElementById("pet-tag-info").textContent = msg;
}