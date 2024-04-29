// Wait for the DOM to be loaded before executing the JavaScript code
document.addEventListener("DOMContentLoaded", function () {
    // Get modal elements
    var modal = document.querySelector("#minmodal");
    var modalBtn = document.querySelector("#modalBtn");
    var closeModal = document.querySelector(".close");

    // Event listener for showing the modal
    modalBtn.addEventListener("click", function (event) {
        event.preventDefault(); // Prevent default behavior of the anchor tag
        modal.style.display = "block";
    });

    // Event listener for closing the modal
    closeModal.addEventListener("click", function () {
        modal.style.display = "none";
    });

    // Event listener to close the modal when clicking outside of it
    window.addEventListener("click", function (event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    });

    // Get login modal elements
    var modal2 = document.querySelector("#minmodal2");
    var modalBtn2 = document.querySelector("#modalBtn2");
    var closeModal2 = document.querySelector(".close2");

    // Event listener for showing the login modal
    modalBtn2.addEventListener("click", function (event) {
        event.preventDefault(); // Prevent default behavior of the anchor tag
        modal2.style.display = "block";
    });

    // Event listener for closing the login modal
    closeModal2.addEventListener("click", function () {
        modal2.style.display = "none";
    });

    // Event listener to close the login modal when clicking outside of it
    window.addEventListener("click", function (event) {
        if (event.target == modal2) {
            modal2.style.display = "none";
        }
    });

    // Check if there is an error message and display it
    var errorMessage = document.querySelector(".error");
    if (errorMessage && errorMessage.innerText !== "") {
        // If there is an error message, display the modal
        modal.style.display = "block";
    }
});
