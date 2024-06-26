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

  // if(localStorage.typeface=="Libertinus") {
  //   document.body.classList.add("libertinus")
  // }
  // else {
  //   // document.body.classList.remove("libertinus")
  //   // Use libertinus as default
  //   document.body.classList.add("libertinus")
  // }
  typeFaceToggle.title = localStorage.typeface || "Libertinus";
};

let processScroll = () => {
	let docElem = document.documentElement,
		docBody = document.body,
		scrollTop = docElem['scrollTop'] || docBody['scrollTop'],
    	scrollBottom = (docElem['scrollHeight'] || docBody['scrollHeight']) - window.innerHeight,
		scrollPercent = scrollTop / scrollBottom * 100 + '%';

	// console.log(scrollTop + ' / ' + scrollBottom + ' / ' + scrollPercent);

    document.getElementById("progress-bar").style.setProperty("--scrollAmount", scrollPercent);
}

document.addEventListener('scroll', processScroll);

// interactive TOC
// const toc = document.getElementById("table-of-contents");
// // skip first callback when first observing
// let firstCallback = true;
// const observer = new IntersectionObserver(entries => {
//   if (!entries[0].isIntersecting) {
//      if (firstCallback) {
//        firstCallback = false;
//      } else {
//        console.log("Scrolled passed the TOC");

//        side_toc = toc.cloneNode(true)
//        side_toc.id = "side-toc"
//        content = document.getElementById("content")
//        content.appendChild(side_toc)
//      }
//   } else {
//     console.log("TOC in view")
//     side_toc = document.getElementById("side-toc")
//     side_toc.remove()
//   }
// });
// observer.observe(toc);
