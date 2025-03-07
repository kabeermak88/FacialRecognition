document.getElementById('uploadForm').onsubmit = async function (event) {
    event.preventDefault();

    let formData = new FormData();
    formData.append("image1", document.getElementById("image1").files[0]);
    formData.append("image2", document.getElementById("image2").files[0]);

    let response = await fetch("/verify", {
        method: "POST",
        body: formData
    });

    let result = await response.json();
    document.getElementById("result").innerHTML = `<p>${result.message} <br> <b>Confidence:</b> ${result.confidence}%</p>`;
};
