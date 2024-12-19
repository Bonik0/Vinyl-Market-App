



function CancelOrder(id){
    if (!localStorage.getItem('access_token')){
        const currentUrl = new URL(window.location.href); 
        currentUrl.pathname = '/auth/login';
        window.location.href = currentUrl;
        return;
    }
    fetchWithToken(`/api/me/orders/cancel/${id}`, 
        {
            method : 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        }
    ).then(response => {
            const currentUrl = new URL(window.location.href); 
            currentUrl.pathname = '/me/orders';
            window.location.href = currentUrl;
            return response.json();
        }
    ).then(data => {
            if(data.detail.type === 'cant_cancel'){
                alert(data.detail.message);
            }
    });
}



window.addEventListener('load', function() {

    setTimeout(() => {
        fetchWithToken('/me/orders-info', {
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