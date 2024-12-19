document.getElementById('registrateButton').addEventListener('click', async () => {
    const usernameInput = document.getElementById('username');
    const emailInput = document.getElementById('email');
    const firstnameInput = document.getElementById('firstname');
    const lastnameInput = document.getElementById('lastname');
    const passwordImput = document.getElementById('password');
    const reapeatPasswordImput = document.getElementById('reapeatPassword');


    const errorInputUsername = document.getElementById('errorInputUsername');
    const errorInputEmail = document.getElementById('errorInputEmail');
    const errorInputFirstname = document.getElementById('errorInputFirstname');
    const errorInputLastname = document.getElementById('errorInputLastname');
    const errorInputPassword = document.getElementById('errorInputPassword');
    const repeatErrorInputPassword = document.getElementById('repeatErrorInputPassword');


    errorInputUsername.classList.remove('error-input');
    errorInputEmail.classList.remove('error-input');
    errorInputFirstname.classList.remove('error-input');
    errorInputLastname.classList.remove('error-input');
    errorInputPassword.classList.remove('error-input');
    repeatErrorInputPassword.classList.remove('error-input');


    const usernameLabel = document.getElementById('usernameLabel');
    const emailLabel = document.getElementById('emailLabel');
    const firstnameLabel = document.getElementById('firstnameLabel');
    const lastnameLabel = document.getElementById('lastnameLabel');
    const passwordLabel = document.getElementById('passwordLabel');
    const repeatPasswordLabel = document.getElementById('repeatPasswordLabel');


    usernameLabel.classList.remove('error-label');
    emailLabel.classList.remove('error-label');
    firstnameLabel.classList.remove('error-label');
    lastnameLabel.classList.remove('error-label');
    passwordLabel.classList.remove('error-label');
    repeatPasswordLabel.classList.remove('error-label');

    const UsernameError = document.getElementById('UsernameError');
    const EmailError = document.getElementById('EmailError');
    const FirstnameError = document.getElementById('FirstnameError');
    const LastnameError = document.getElementById('LastnameError');
    const passwordError = document.getElementById('passwordError');
    const repeatPasswordError = document.getElementById('repeatPasswordError');


    UsernameError.textContent = '';
    EmailError.textContent = '';
    FirstnameError.textContent = '';
    LastnameError.textContent = '';
    passwordError.textContent = '';
    repeatPasswordError.textContent = '';


    const username = usernameInput.value.toString();
    const email = emailInput.value.toString();
    const firstname = firstnameInput.value.toString();
    const lastname = lastnameInput.value.toString();
    const password = passwordImput.value.toString();
    const reapeatPassword = reapeatPasswordImput.value.toString();

    var checkErrorFlag = false;

    if(username.length < 5){
        errorInputUsername.classList.add('error-input');
        usernameLabel.classList.add('error-label');
        UsernameError.textContent = 'username to short';
        checkErrorFlag = true;
    }

    if(email.length < 1){
        errorInputEmail.classList.add('error-input');
        emailLabel.classList.add('error-label');
        EmailError.textContent = 'email to short';
        checkErrorFlag = true;
    }

    if(firstname.length < 1){
        errorInputFirstname.classList.add('error-input');
        firstnameLabel.classList.add('error-label');
        FirstnameError.textContent = 'firstname to short';
        checkErrorFlag = true;
    }

    if(lastname.length < 1){
        errorInputLastname.classList.add('error-input');
        lastnameLabel.classList.add('error-label');
        LastnameError.textContent = 'lastname to short';
        checkErrorFlag = true;
    }

    if(password.length < 5){
        errorInputPassword.classList.add('error-input');
        passwordLabel.classList.add('error-label');
        passwordError.textContent = 'password to short';
        checkErrorFlag = true;
    }

    if(password !== reapeatPassword){
        repeatErrorInputPassword.classList.add('error-input');
        repeatPasswordLabel.classList.add('error-label');
        repeatPasswordError.textContent = 'passwords do not match';
        checkErrorFlag = true;
    }

    if (checkErrorFlag){
        return;
    }

    try {
        const response = await fetch('/api/auth/registration', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                                username : username,
                                password : password, 
                                last_name : lastname, 
                                first_name : firstname,
                                email : email
                        })
        });
        const data = await response.json();
        if (!response.ok) {
            // Parse error response
            if (data.detail.type === 'email_occupied') {
                errorInputEmail.classList.add('error-input');
                emailLabel.classList.add('error-label');
                EmailError.textContent = data.detail.message;
            } else if (data.detail.type === 'username_occupied') {
                errorInputUsername.classList.add('error-input');
                usernameLabel.classList.add('error-label');
                UsernameError.textContent = data.detail.message;
            } else {
                errorInputEmail.classList.add('error-input');
                emailLabel.classList.add('error-label');
                EmailError.textContent = data.detail[0].msg;
                errorInputUsername.classList.add('error-input');
                usernameLabel.classList.add('error-label');
                UsernameError.textContent = data.detail[0].msg;

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
