




function DeleteVinylRecord(id){
    if (!localStorage.getItem('access_token')){
        const currentUrl = new URL(window.location.href); 
        currentUrl.pathname = '/auth/login';
        window.location.href = currentUrl;
        return;
    }
    fetchWithToken(`/api/seller/vinyl-records/${id}`, 
        {
            method : 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        }
    ).then(response => {
            const currentUrl = new URL(window.location.href); 
            currentUrl.pathname = '/seller/vinyl-records';
            window.location.href = currentUrl;
            return response.json();
        }
    ).then(data => {
            if(data.detail.type === 'not_close_orders'){
                alert(data.detail.message);
            }
    });
}


function CreateVinyl(){
    const currentUrl = new URL(window.location.href);
    currentUrl.pathname = '/seller/vinyl-records/create';
    window.location.href = currentUrl;
}


function UpdateFunc(id){
    const currentUrl = new URL(window.location.href);
    currentUrl.pathname = `/seller/vinyl-records/${id}/update`;
    window.location.href = currentUrl;
}








window.addEventListener('load', function() {

    setTimeout(() => {
        fetchWithToken('/seller/vinyl-records-info', {
            method: 'GET'
        }).then(response => {
                if (!response.ok) {
                    const currentUrl = new URL(window.location.href); 
                    currentUrl.pathname = '/auth/seller-registrate';
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


                const createButton = document.getElementById('CreateButton');

                if(createButton){
                    createButton.addEventListener('click', CreateVinyl);
                }

            }).catch(error => {
                console.error('Error loading page:', error);
            })
    }, 175);
    
});