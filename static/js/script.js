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