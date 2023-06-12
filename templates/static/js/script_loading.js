var loading = document.getElementById('loading');
        
function carregamento() {
    loading.classList.remove('disabled');
}

document.addEventListener('htmx:beforeRequest', function(event) {
    loading.classList.remove('disabled');
});
 
document.addEventListener('htmx:afterSwap', function() {
    loading.classList.add('disabled');
});
 