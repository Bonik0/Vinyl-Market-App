const selectQuantity = document.getElementById('items-per-page');

function changePage(pageNumber) {
    const url = new URL(window.location);
    url.searchParams.set('page', pageNumber);
    window.location.href = url;

    document.querySelectorAll('.pagination button').forEach(btn => {
        btn.classList.remove('active');
    });
    document.getElementById(`page-${pageNumber}`).classList.add('active');
};


window.addEventListener('load', function() {
    const urlParams = new URLSearchParams(window.location.search);
    const currentPage = urlParams.get('page') || 1;

    const activeButton = document.getElementById(`page-${currentPage}`);
    if (activeButton) activeButton.classList.add('active');
});


if (selectQuantity !== null){
    selectQuantity.addEventListener('change', function() {
        const selectedValue = parseInt(selectQuantity.value);
        const currentUrl = new URL(window.location.href);
        const nowPerpage = parseInt(currentUrl.searchParams.get('perpage')) || 25;
        if(nowPerpage < selectedValue){
            currentUrl.searchParams.set('page', 1);
        };
        currentUrl.searchParams.set('perpage', selectedValue);

        window.location.href = currentUrl;
    });
}