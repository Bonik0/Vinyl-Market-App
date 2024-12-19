



function isValidUrl(string) {
    try {
      new URL(string);
      return true;
    } catch (err) {
      return false;
    }
  }



async function CreateVinylRecord() {
    const titleInput = document.getElementById('title');
    const errorInputTitle = document.getElementById('errorInputTitle');
    errorInputTitle.classList.remove('error-input');
    const titleLabel = document.getElementById('titleLabel');
    titleLabel.classList.remove('error-label');
    const TitleError = document.getElementById('TitleError');
    TitleError.textContent = '';

    const title = titleInput.value.toString();

    var checkErrorFlag = false;

    if(title.length < 1){
        errorInputTitle.classList.add('error-input');
        titleLabel.classList.add('error-label');
        TitleError.textContent = 'title to short';
        checkErrorFlag = true;
    }


    const quantityInput = document.getElementById('quantity');
    const errorInputQuantity = document.getElementById('errorInputQuantity');
    errorInputQuantity.classList.remove('error-input');
    const quantityLabel = document.getElementById('quantityLabel');
    quantityLabel.classList.remove('error-label');
    const QuantityError = document.getElementById('QuantityError');
    QuantityError.textContent = '';

    const quantity = parseInt(quantityInput.value.toString());
    

    if(!quantity){
        errorInputQuantity.classList.add('error-input');
        quantityLabel.classList.add('error-label');
        QuantityError.textContent = 'quantity is not number';
        checkErrorFlag = true;
    }


    const releaseDateInput = document.getElementById('releaseDate');
    const errorInputReleaseDate = document.getElementById('errorInputReleaseDate');
    errorInputReleaseDate.classList.remove('error-input');
    const releaseDateLabel = document.getElementById('releaseDateLabel');
    releaseDateLabel.classList.remove('error-label');
    const ReleaseDateError = document.getElementById('ReleaseDateError');
    ReleaseDateError.textContent = '';

    const releaseDate = releaseDateInput.value.toString();

    if(!releaseDate){
        errorInputReleaseDate.classList.add('error-input');
        releaseDateLabel.classList.add('error-label');
        ReleaseDateError.textContent = 'incorrect release date';
        checkErrorFlag = true;
    }


    const UPCInput = document.getElementById('UPC');
    const errorInputUPC = document.getElementById('errorInputUPC');
    errorInputUPC.classList.remove('error-input');
    const UPCLabel = document.getElementById('UPCLabel');
    UPCLabel.classList.remove('error-label');
    const UPCError = document.getElementById('UPCError');
    UPCError.textContent = '';

    const UPC = parseInt(UPCInput.value.toString());    

    if(!UPC){
        errorInputUPC.classList.add('error-input');
        UPCLabel.classList.add('error-label');
        UPCError.textContent = 'UPC is not number';
        checkErrorFlag = true;
    }


    const priceInput = document.getElementById('price');
    const errorInputPrice = document.getElementById('errorInputPrice');
    errorInputPrice.classList.remove('error-input');
    const priceLabel = document.getElementById('priceLabel');
    priceLabel.classList.remove('error-label');
    const PriceError = document.getElementById('PriceError');
    PriceError.textContent = '';

    const price = parseFloat(priceInput.value.toString());

    if(!price){
        errorInputPrice.classList.add('error-input');
        priceLabel.classList.add('error-label');
        PriceError.textContent = 'price is not number';
        checkErrorFlag = true;
    }



    const imageUrlInput = document.getElementById('imageUrl');
    const errorInputImageUrl = document.getElementById('errorInputImageUrl');
    errorInputImageUrl.classList.remove('error-input');
    const imageUrlLabel = document.getElementById('imageUrlLabel');
    imageUrlLabel.classList.remove('error-label');
    const ImageUrlError = document.getElementById('ImageUrlError');
    ImageUrlError.textContent = '';


    const imageUrl = imageUrlInput.value.toString();

    if(!isValidUrl(imageUrl)){
        errorInputImageUrl.classList.add('error-input');
        imageUrlLabel.classList.add('error-label');
        ImageUrlError.textContent = 'is not url';
        checkErrorFlag = true;
    }


    const artistsInput = document.getElementById('artists');

    artists = artistsInput.value.toString();

    if(artists === ''){
        artists = null;
    }

    const genresInput = document.getElementById('genres');

    genres = genresInput.value.toString();

    if(genres === ''){
        genres = null;
    }


    if(checkErrorFlag){
        return;
    }


    try {
        const response = await fetchWithToken('/api/seller/vinyl-records', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                                title : title,
                                quantity : quantity, 
                                release_date : releaseDate, 
                                upc : UPC,
                                price : price,
                                image_url : imageUrl,
                                genres : genres,
                                artists : artists
                        })
        });
        const data = await response.json();
        if (!response.ok) {
            // Parse error response
            if (data.detail.type === 'title_already_exist') {
                errorInputTitle.classList.add('error-input');
                titleLabel.classList.add('error-label');
                TitleError.textContent = data.detail.message;
            } else {
                errorInputTitle.classList.add('error-input');
                titleLabel.classList.add('error-label');
                TitleError.textContent = data.detail[0].msg;

            }
        } else {
            const currentURL = new URL(window.location.href); 
            currentURL.pathname = `/vinyl-record/${data}`;
            window.location.href = currentURL;
        } 
    } catch (error) {
        alert('An unexpected error occurred.');
    }
    


    
};














window.addEventListener('load', function() {

    setTimeout(() => {
        fetchWithToken('/seller/vinyl-records/create-info', {
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
                    createButton.addEventListener('click', CreateVinylRecord);
                }

            }).catch(error => {
                console.error('Error loading page:', error);
            })
    }, 175);
    
});