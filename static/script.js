document.addEventListener("DOMContentLoaded", function () {
    console.log("✅ JavaScript Loaded!");

    document.getElementById("uploadForm").addEventListener("submit", function (event) {
        event.preventDefault(); // Prevent page reload

        let formData = new FormData(this);

        // Log file names before sending
        for (let pair of formData.entries()) {
            console.log("Uploading:", pair[0], pair[1]);
        }

        fetch("/compare", {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            console.log("📢 Server Response:", data);
            let resultDiv = document.getElementById("result");

            if (data.error) {
                resultDiv.innerHTML = `<span class="error">${data.error}</span>`;
            } else {
                resultDiv.innerHTML = `<span class="success">${data.result}</span>`;
            }
        })
        .catch(error => console.error("❌ Error:", error));
    });
});
