






window.addEventListener('load', function() {

    setTimeout(() => {
        fetchWithToken('/me/account-info', {
            method: 'GET'
        }).then(response => {
                if (!response.ok) {
                    const currentUrl = new URL(window.location.href); 
                    currentUrl.pathname = '/auth/login';
                    window.location.href = currentUrl;
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
            })
    }, 175);
    
});




document.getElementById('registrateButton').addEventListener('click', async () => {
    const phoneNumberInput = document.getElementById('phoneNumber');
    const cityInput = document.getElementById('city');
    const countryInput = document.getElementById('country');


    const errorInputPhoneNumber = document.getElementById('errorInputPhoneNumber');
    const errorInputCity = document.getElementById('errorInputCity');
    const errorInputCountry = document.getElementById('errorInputCountry');


    errorInputPhoneNumber.classList.remove('error-input');
    errorInputCity.classList.remove('error-input');
    errorInputCountry.classList.remove('error-input');


    const phoneNumberLabel = document.getElementById('phoneNumberLabel');
    const cityLabel = document.getElementById('cityLabel');
    const countryLabel = document.getElementById('countryLabel');


    phoneNumberLabel.classList.remove('error-label');
    cityLabel.classList.remove('error-label');
    countryLabel.classList.remove('error-label');


    const PhoneNumberError = document.getElementById('PhoneNumberError');
    const CityError = document.getElementById('CityError');
    const CountryError = document.getElementById('CountryError');


    PhoneNumberError.textContent = '';
    CityError.textContent = '';
    CountryError.textContent = '';


    const phoneNumber = phoneNumberInput.value.toString();
    const city = cityInput.value.toString();
    const country = countryInput.value.toString();

    var checkErrorFlag = false;


    if(phoneNumber.length < 5){
        errorInputPhoneNumber.classList.add('error-input');
        phoneNumberLabel.classList.add('error-label');
        PhoneNumberError.textContent = 'phone number to short';
        checkErrorFlag = true;
    }

    if(phoneNumber.length > 15){
        errorInputPhoneNumber.classList.add('error-input');
        phoneNumberLabel.classList.add('error-label');
        PhoneNumberError.textContent = 'phone number to long';
        checkErrorFlag = true;
    }

    if(city.length < 1){
        errorInputCity.classList.add('error-input');
        cityLabel.classList.add('error-label');
        CityError.textContent = 'city name to short';
        checkErrorFlag = true;
    }
    

    if(country.length < 1){
        errorInputCountry.classList.add('error-input');
        countryLabel.classList.add('error-label');
        CountryError.textContent = 'country name to short';
        checkErrorFlag = true;
    }


    if (checkErrorFlag){
        return;
    }

    try {
        const response = await fetchWithToken('/api/auth/seller-registration', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({city : city, phone_number : phoneNumber, country : country})
        });
        const data = await response.json();
        if (!response.ok) {
            // Parse error response
            if (data.detail.type === 'you_are_seller') {
                errorInputPhoneNumber.classList.add('error-input');
                phoneNumberLabel.classList.add('error-label');
                PhoneNumberError.textContent = data.detail.message;
            } else {
                errorInputPhoneNumber.classList.add('error-input');
                phoneNumberLabel.classList.add('error-label');
                PhoneNumberError.textContent = data.detail[0].msg;

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
