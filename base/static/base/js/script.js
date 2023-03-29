const sun = document.querySelector('.sun')
const moon = document.querySelector('.moon')
const button = document.querySelector('#dark-mode-toggle')

window.onload=function() {
  if(localStorage.darkMode=="true") {
    sun.classList.add('visible')
    moon.classList.remove('visible')
  }
  else {
    moon.classList.add('visible')
    sun.classList.remove('visible')
  }
};

button.addEventListener('click', () => {
  sun.classList.toggle('visible')
  moon.classList.toggle('visible')
  document.body.classList.toggle("latex-dark");
  localStorage.darkMode=(localStorage.darkMode=="true")?"false":"true";
})

