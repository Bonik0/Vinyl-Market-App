

function FetchFunc(logoutUrl){
    fetchWithToken(logoutUrl, {
        method: 'GET'
    }).then(response => {
            if (!response.ok) {
                const currentUrl = new URL(window.location.href); 
                currentUrl.pathname = '/auth/login';
                window.location.href = currentUrl;
                throw new Error(`HTTP error! status: ${response.status}`);
            }
    });
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('exp');
    const currentURL = new URL(window.location.href); 
    currentURL.pathname = '/';
    window.location.href = currentURL;
}




function logoutFunc(){
    FetchFunc('/api/me/logout');
}


function fullLogoutFunc(){
    FetchFunc('/api/me/full-logout');
}


function becomeSellerFunc(){
    const currentUrl = new URL(window.location.href);
    currentUrl.search = '';
    currentUrl.pathname = '/auth/seller-registrate';
    window.location.href = currentUrl;
};


function sellerRecordsFunc(){
    const currentUrl = new URL(window.location.href);
    currentUrl.search = '';
    currentUrl.pathname = '/seller/vinyl-records';
    window.location.href = currentUrl;
}


function sellerOrdersFunc(){
    const currentUrl = new URL(window.location.href);
    currentUrl.search = '';
    currentUrl.pathname = '/seller/orders';
    window.location.href = currentUrl;
}





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
                return response.text();
            }).then(html => {
                const container = document.getElementById('container');

                if (!container) {
                    return;
                }
                container.innerHTML = html;
                const logout = document.getElementById('logout');
                const fullLogout = document.getElementById('full-logout');
                const becomeSeller = document.getElementById('userRegistrationAsSeller');
                const sellerRecords = document.getElementById('SellerRecords');
                const sellerOrders = document.getElementById('SellerOrders');

                logout.addEventListener('click', logoutFunc);
                fullLogout.addEventListener('click', fullLogoutFunc);

                if(sellerRecords){
                    sellerRecords.addEventListener('click', sellerRecordsFunc);
                }
                if(sellerOrders){
                    sellerOrders.addEventListener('click', sellerOrdersFunc);
                }

                if (becomeSeller){
                    becomeSeller.addEventListener('click', becomeSellerFunc);
                }
            }).catch(error => {
                console.error('Error loading page:', error);
            })
    }, 175);
    
});