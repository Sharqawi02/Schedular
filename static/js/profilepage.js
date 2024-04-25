// FOR THE CHANGING OF THE SECTIONS
document.addEventListener("DOMContentLoaded", function() {
    const accountSettings = document.querySelector('.account-settings');
    const passwordSettings = document.querySelector('.password-settings');
    const notificationsSettings = document.querySelector('.notifications-settings');

    accountSettings.addEventListener('click', function() {
        toggleSettings('.account-info');
    });

    passwordSettings.addEventListener('click', function() {
        toggleSettings('.password-info');
    });

    notificationsSettings.addEventListener('click', function() {
        toggleSettings('.notification-info');
    });

    function toggleSettings(activeSetting) {
        const allSettings = document.querySelectorAll('.settings-container > .account-info, .settings-container > .password-info, .settings-container > .notification-info');
        allSettings.forEach(function(setting) {
            if (setting.classList.contains(activeSetting.substring(1))) {
                setting.style.display = 'block';
            } else {
                setting.style.display = 'none';
            }
        });
    }
});