const sun = document.querySelector(".sun")
const moon = document.querySelector(".moon")
const button = document.querySelector("#dark-mode-toggle")
const typeFaceToggle = document.getElementById("typeface-toggle")


button.addEventListener("click", () => {
  sun.classList.toggle("visible")
  moon.classList.toggle("visible")
  document.body.classList.toggle("latex-dark");
  localStorage.darkMode=(localStorage.darkMode=="true")?"false":"true";
})


typeFaceToggle.addEventListener("click", () => {
  document.body.classList.toggle("libertinus")
  typeFaceToggle.title = document.body.classList.contains("libertinus") ? "Libertinus" : "Latin Modern"
  localStorage.typeface = document.body.classList.contains("libertinus") ? "Libertinus" : "Latin Modern";
})


window.onload=function() {
  if(localStorage.darkMode=="true") {
    sun.classList.add("visible")
    moon.classList.remove("visible")
  }
  else {
    moon.classList.add("visible")
    sun.classList.remove("visible")
  }

  if(localStorage.typeface=="Libertinus") {
    document.body.classList.add("libertinus")
  }
  else {
    document.body.classList.remove("libertinus")
  }
  typeFaceToggle.title = localStorage.typeface || "Latin Modern";
};
