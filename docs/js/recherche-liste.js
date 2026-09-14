const search_selectors = ['.title', '.artist' , '.song-number']

// Simplifie un texte pour la recherche : minuscules, sans accents ni apostrophes
// (« francois » trouve « François », « cest » ou « c’est » trouve « C'est »)
function simplifier(texte) {
	return texte.normalize('NFD')
		.replace(/[\u0300-\u036f]/g, '')   // accents
		.toLowerCase()
		.replace(/['’‘`]/g, '')            // apostrophes droites ou typographiques
		.replace(/œ/g, 'oe')
		.replace(/æ/g, 'ae');
}

function filterSongs() {
    const query_string = simplifier(document.getElementById('search').value.trim());
	// Les éléments sont visibles ssi ils contiennent la chaine de recherche
    window.ITEMS.forEach(list_item => {
		list_item.style.display =
			search_selectors.some(selector => {
				const element = list_item.querySelector(selector);
				return element && simplifier(element.textContent).includes(query_string);
			}) ? "" : "none";  // visible ou unvisible
    });
}

window.onload = function(e) {
	window.ITEMS = document.querySelectorAll('.song-list li');
}
