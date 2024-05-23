let HamburgerMenu = document.querySelector('.hamburger')
let BackgroundMenu = document.querySelector('.BackgroundMenu')
let ConatinerMenu = document.querySelector('.ConatinerMenu')

HamburgerMenu.addEventListener('click', function () {
    BackgroundMenu.classList.add('view')
    ConatinerMenu.classList.add('view')
})

BackgroundMenu.addEventListener('click', function () {
    BackgroundMenu.classList.remove('view')
    ConatinerMenu.classList.remove('view')
})

function toggleDarkMode(){
    var element = document.body;
    element.classList.toggle("dark-mode");
    if (element.classList.contains("dark-mode")) {
        localStorage.setItem("theme", "dark");
    } else {
        localStorage.setItem("theme", "light");
    }
}

window.onload = function(){
    if (localStorage.getItem("theme") === "dark") {
        document.body.classList.add("dark-mode");
    }
}