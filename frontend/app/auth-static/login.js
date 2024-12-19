document.getElementById('loginButton').addEventListener('click', async () => {
    const loginInput = document.getElementById('login');
    const errorInutLogin = document.getElementById('errorInputLogin');
    const loginLabel = document.getElementById('loginLabel');
    const loginError = document.getElementById('loginError');
    const errorInutPassword = document.getElementById('errorInputPassword');
    const passwordError = document.getElementById('passwordError');
    const passwordLabel = document.getElementById('passwordLabel');
    const passwordInput = document.getElementById('password');

    errorInutLogin.classList.remove('error-input');
    loginLabel.classList.remove('error-label');
    loginError.textContent = '';

    errorInutPassword.classList.remove('error-input');
    passwordLabel.classList.remove('error-label');
    passwordError.textContent = '';


    const login = loginInput.value.toString();
    const password = passwordInput.value.toString();

    var checkErrorFlag = false;

    if(login.length < 5){
        errorInutLogin.classList.add('error-input');
        loginLabel.classList.add('error-label');
        loginError.textContent = 'login to short';
        checkErrorFlag = true;
    }

    if(password.length < 5){
        errorInutPassword.classList.add('error-input');
        passwordLabel.classList.add('error-label');
        passwordError.textContent = 'password to short';
     
        checkErrorFlag = true;
    }

    if(checkErrorFlag){
        return;
    }


    try {
        const response = await fetch('/api/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({username_or_email : login, password  : password})
        });
        const data = await response.json();
        if (!response.ok) {
            // Parse error response
            if (data.detail.type === 'invalid_username_or_email') {
                errorInutLogin.classList.add('error-input');
                loginLabel.classList.add('error-label');
                loginError.textContent = data.detail.message;
            } else if (data.detail.type === 'invalid_password') {
                errorInutPassword.classList.add('error-input');
                passwordLabel.classList.add('error-label');
                passwordError.textContent = data.detail.message;
            } else {
                errorInutLogin.classList.add('error-input');
                loginLabel.classList.add('error-label');
                loginError.textContent = data.detail[0].msg;
                errorInutPassword.classList.add('error-input');
                passwordLabel.classList.add('error-label');
                passwordError.textContent = data.detail[0].msg;

            }
        } else {
            // Success logic here
            localStorage.setItem('access_token', data.access_token);
            localStorage.setItem('refresh_token', data.refresh_token);
            localStorage.setItem('exp', data.exp);
            const currentURL = new URL(window.location.href); 
            currentURL.pathname = '/';
            window.location.href = currentURL;
        }
    } catch (error) {
        alert('An unexpected error occurred.');
    }
});
