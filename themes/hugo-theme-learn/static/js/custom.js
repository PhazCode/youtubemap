function changepage() {
elements = document.getElementsByClassName('dropdown');
el = elements[Math.floor(Math.random()*elements.length)];
document.location.href = el.getAttribute('data-nav-id');
}
