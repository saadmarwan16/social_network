document.addEventListener('DOMContentLoaded', () => {
    const password = document.querySelector('.password');
    const confirm = document.querySelector('.confirm');

    document.querySelectorAll('.pwd').forEach(field => {
        field.onkeyup = () => {
            if (password.value.length > 0 || confirm.value.length > 0) {
                document.querySelector('.password-validation').style.display = 'block';
                let containsUpper = false;
                let containsLower = false;
                let containsDigit = false;

                // Check if password is at least 8 characters long
                if (password.value.length >= 8) {
                    document.querySelector('#pwd-8-char').style.color = 'rgb(10, 95, 10)';
                    document.querySelector('#pwd-8-char').style.backgroundColor = 'rgba(16, 207, 16, 0.5)';
                } else {
                    document.querySelector('#pwd-8-char').style.color = 'rgb(95, 10, 10)';
                    document.querySelector('#pwd-8-char').style.backgroundColor = 'rgba(255, 16, 16, 0.5)';
                }

                // Check if password contains at least one uppercase character
                for (let i = 0; i < password.value.length; i++) {
                    if (password.value[i] >= 'A' && password.value[i] <= 'Z') {
                        if (password.value[i] === password.value[i].toUpperCase() && isNaN(password.value[i])) {
                            containsUpper = true;
                            break;
                        }
                    }
                }

                // Give a red or gren color based on whether password contains at least one lowercase character
                if (containsUpper) {
                    document.querySelector('#pwd-uppercase').style.color = 'rgb(10, 95, 10)';
                    document.querySelector('#pwd-uppercase').style.backgroundColor = 'rgba(16, 207, 16, 0.5)';
                } else {
                    document.querySelector('#pwd-uppercase').style.color = 'rgb(95, 10, 10)';
                    document.querySelector('#pwd-uppercase').style.backgroundColor = 'rgba(255, 16, 16, 0.5)';
                }

                // Check if password contains at least one lowercase character
                for (let i = 0; i < password.value.length; i++) {
                    if (password.value[i] >= 'a' && password.value[i] <= 'z') {
                        if (password.value[i] === password.value[i].toLowerCase() && isNaN(password.value[i])) {
                            containsLower = true;
                            break;
                        }
                    }
                }

                // Give a red or gren color based on whether password contains at least one lower character
                if (containsLower) {
                    document.querySelector('#pwd-lowercase').style.color = 'rgb(10, 95, 10)';
                    document.querySelector('#pwd-lowercase').style.backgroundColor = 'rgba(16, 207, 16, 0.5)';
                } else {
                    document.querySelector('#pwd-lowercase').style.color = 'rgb(95, 10, 10)';
                    document.querySelector('#pwd-lowercase').style.backgroundColor = 'rgba(255, 16, 16, 0.5)';
                }

                // Check if password contains at least one digit
                for (let i = 0; i < password.value.length; i++) {
                    if (!isNaN(password.value[i])) {
                        containsDigit = true;
                        break;
                    }
                }

                // Give a red or gren color based on whether password contains at least one digit
                if (containsDigit) {
                    document.querySelector('#pwd-digit').style.color = 'rgb(10, 95, 10)';
                    document.querySelector('#pwd-digit').style.backgroundColor = 'rgba(16, 207, 16, 0.5)';
                } else {
                    document.querySelector('#pwd-digit').style.color = 'rgb(95, 10, 10)';
                    document.querySelector('#pwd-digit').style.backgroundColor = 'rgba(255, 16, 16, 0.5)';
                }

                // Check if passwords match
                if (password.value === confirm.value) {
                    document.querySelector('#pwd-match').style.color = 'rgb(10, 95, 10)';
                    document.querySelector('#pwd-match').style.backgroundColor = 'rgba(16, 207, 16, 0.5)';
                } else {
                    document.querySelector('#pwd-match').style.color = 'rgb(95, 10, 10)';
                    document.querySelector('#pwd-match').style.backgroundColor = 'rgba(255, 16, 16, 0.5)';
                }
            } else {
                document.querySelector('.password-validation').style.display = 'none';
            }
        }
    })
})