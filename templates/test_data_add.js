document.getElementById("showFormButton").addEventListener("click", function () {
    var form = document.getElementById("dataForm");
    if (form.style.display === "none") {
        form.style.display = "block";
    } else {
        form.style.display = "none";
    }
});