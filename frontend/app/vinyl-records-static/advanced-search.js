const AdvancedSearchButton = document.getElementById('StartAdvancedSearch');



AdvancedSearchButton.addEventListener('click', function() {
    const currentUrl = new URL(window.location.href); 
    const title = document.getElementById('title').value.trim();
    const artists = document.getElementById('artists').value.trim();
    const genres = document.getElementById('genres').value.trim();
    currentUrl.pathname = '/';

    if (title) { 
        currentUrl.searchParams.set('text', title); 
    }
    if (artists){
        currentUrl.searchParams.set('artist', artists); 
    }
    if (genres){
        currentUrl.searchParams.set('genre', genres); 
    }

    window.location.href = currentUrl;
});