let pageUrl = new URL(document.location.href);
let searchText = document.getElementById("search-text");

function HandleSearchText() {
    pageUrl.searchParams.set('search-text', searchText.value);
    document.location.href = pageUrl.href;
}