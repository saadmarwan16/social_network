document.addEventListener('DOMContentLoaded', () => {
    const newPassword = document.querySelector('#new-pwd');
    const confirmPassword = document.querySelector('#confirm-pwd');

    document.querySelectorAll('input').forEach(field => {
        field.onkeyup = () => {
            if (newPassword.value.length > 0 && confirmPassword.value.length > 0) {
                if (newPassword.value === confirmPassword.value) {
                    document.querySelector('#pwd-match').classList.replace('pwd-match-times', 'pwd-match-check');
                } else {
                    document.querySelector('#pwd-match').classList.replace('pwd-match-check', 'pwd-match-times');
                }
            }
        }
    })
})