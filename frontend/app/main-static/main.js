

function fetchWithToken(url, options = {}) {

    const token = localStorage.getItem('access_token');

    if (!options.headers) {
        options.headers = {};
    }
    if (token){
        options.headers['Authorization'] = `Bearer ${token}`;
    }
    return fetch(url, options);
};


function AddToBucket(id){
    if (!localStorage.getItem('access_token')){
        const currentUrl = new URL(window.location.href); 
        currentUrl.pathname = '/auth/login';
        window.location.href = currentUrl;
        return;
    }
    fetchWithToken(`/api/me/bucket/create/${id}`, 
        {
            method : 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        }
    ).then(response => {
            const currentUrl = new URL(window.location.href); 
            currentUrl.pathname = '/me/bucket';
            window.location.href = currentUrl;
            return response.json();
        }
    ).then(data => {
            if(data.detail.type === 'can_not_insert'){
                alert(data.detail.message);
            }
    });
    
}


window.addEventListener('load', function() {
    const exp = localStorage.getItem('exp');
    if(!exp){
        return;
    }

    if (exp - 600000 > Date.now()){
        return;
    }
    const refresh_token = localStorage.getItem('refresh_token');

    fetch('/api/auth/update-tokens', 
        {
            method : 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({refresh_token : refresh_token})
        }
    ).then(response => {
            if(!response.ok){
                localStorage.removeItem('refresh_token');
                localStorage.removeItem('exp');
                localStorage.removeItem('access_token');
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        }).then(data => {
            localStorage.setItem('access_token', data.access_token);
            localStorage.setItem('refresh_token', data.refresh_token);
            localStorage.setItem('exp', data.exp);
        });
});



const TextSearchButton = document.getElementById('searchButton');
const AdvancedSearch = document.getElementById('advancedSearchButton');


if(AdvancedSearch  !== null){
    AdvancedSearch.addEventListener('click', function() {
        const currentUrl = new URL(window.location.href);
        currentUrl.search = '';
        currentUrl.pathname = '/advanced-search';
        window.location.href = currentUrl;
        
    });
}
if(TextSearchButton  !== null){
    TextSearchButton.addEventListener('click', function() {
        const input = document.getElementById('searchInput').value.trim();
        if (input) { 
            const url = new URL(window.location.href); 
            url.pathname = '/';
            url.searchParams.set('page', 1);
            url.searchParams.set('text', input); 
            window.location.href = url;
        }
    });
}
