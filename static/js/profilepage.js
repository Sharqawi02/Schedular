// FOR THE CHANGING OF THE SECTIONS
function showAccountInfo() {
    document.querySelector('.account-info').style.display = 'block';
    document.querySelector('.password-info').style.display = 'none';
    document.querySelector('.notification-info').style.display = 'none';
}

function showPasswordInfo() {
    document.querySelector('.account-info').style.display = 'none';
    document.querySelector('.password-info').style.display = 'block';
    document.querySelector('.notification-info').style.display = 'none';
}

function showNotificationInfo() {
    document.querySelector('.account-info').style.display = 'none';
    document.querySelector('.password-info').style.display = 'none';
    document.querySelector('.notification-info').style.display = 'block';
}
