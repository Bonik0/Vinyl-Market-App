


function DeleteFromBucket(id){
    if (!localStorage.getItem('access_token')){
        const currentUrl = new URL(window.location.href); 
        currentUrl.pathname = '/auth/login';
        window.location.href = currentUrl;
        return;
    }
    fetchWithToken(`/api/me/bucket/delete/${id}`, 
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
            if(!response.ok){
                throw new Error(`HTTP error! status: ${response.status}`);
            }
        });
    
}

function OrderFromBucket(id){
    if (!localStorage.getItem('access_token')){
        const currentUrl = new URL(window.location.href); 
        currentUrl.pathname = '/auth/login';
        window.location.href = currentUrl;
        return;
    }
    fetchWithToken(`/api/me/orders/create/${id}`, 
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
            if(data.detail.type === 'zero_quantity'){
                alert(data.detail.message);
            }
    });
    
}


window.addEventListener('load', function() {

    setTimeout(() => {
        fetchWithToken('/me/bucket-info', {
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
            }).catch(error => {
                console.error('Error loading page:', error);
            })
    }, 175);
    
});