const sun = document.querySelector('.sun')
const moon = document.querySelector('.moon')
const button = document.querySelector('#dark-mode-toggle')

button.addEventListener('click', () => {
  sun.classList.toggle('visible')
  moon.classList.toggle('visible')
  document.body.classList.toggle("latex-dark");
})
