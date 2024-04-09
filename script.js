document.addEventListener("DOMContentLoaded", function () {
    var modal = document.querySelector("#minmodal");
    var modalBtn = document.querySelector("#modalBtn");
    var closeModal = document.querySelector(".close");

    modalBtn.addEventListener("click", function () {
        modal.style.display = "block";
    });

    closeModal.addEventListener("click", function () {
        modal.style.display = "none";
    });

    window.addEventListener("click", function (event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    });
});
