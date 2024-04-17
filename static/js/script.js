
// Ser till att DOM är laddat innan funktionerna börjar
document.addEventListener("DOMContentLoaded", function () {
    // Detta hämtar elementen från HTML-koden med de angivna klasser och ID. 
    var modal = document.querySelector("#minmodal");
    var modalBtn = document.querySelector("#modalBtn");
    var closeModal = document.querySelector(".close");

    //Här har vi lagt till en event listner, alltså när användaren klickar på angiven knapp så exikveras koden. 
    modalBtn.addEventListener("click", function () {
        modal.style.display = "block";
    });

    //denna funktion är även en lyssnare, och reagerar på när användaren stänger modalen. 
    closeModal.addEventListener("click", function () {
        modal.style.display = "none";
    });

    //även denna funktion är en lyssnare så reagerar på att användarens tänger modalen, men gör så att när användaren klickar utanför så stängs den. 
    window.addEventListener("click", function (event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    });
});

// Denna laddar in HTML elementen från logga in funktionen. 
var modal2 = document.querySelector("#minmodal2");
var modalBtn2 = document.querySelector("#modalBtn2");
var closeModal2 = document.querySelector(".close2");

modalBtn2.addEventListener("click", function () {
    modal2.style.display = "block";
});

closeModal2.addEventListener("click", function () {
    modal2.style.display = "none";
});

window.addEventListener("click", function (event) {
    if (event.target == modal2) {
        modal2.style.display = "none";
    }
});

document.addEventListener("DOMContentLoaded", function () {
    var errorMessage = document.getElementById("errorMessage");
    var loginForm = document.getElementById("loginForm");

    if (errorMessage.innerText === "") {
        errorMessage.style.display = "none";
    } else {
        errorMessage.style.display = "block";
    }
});