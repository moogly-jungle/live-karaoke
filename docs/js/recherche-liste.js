const items = document.querySelectorAll('.song-list li');
const search_selectors = ['.title', '.artist' , '.song-number']

function filterSongs() {
    const query_string = document.getElementById('search').value.trim().toLowerCase();
	// Les éléments sont visibles ssi ils contiennent la chaine de recherche
    window.ITEMS.forEach(list_item => {
		list_item.style.display = 
			search_selectors.some(selector => {
				const element = list_item.querySelector(selector);
				return element &&  element.textContent.toLowerCase().includes(query_string);
			}) ? "" : "none";  // visible ou unvisible
    });
}

window.onload = function(e) {
	window.ITEMS = document.querySelectorAll('.song-list li');
}

