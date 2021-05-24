
console.log("asdfasdf")
function myFunction(e) {
    btn = e.target
    par = btn.parentElement

    var dots = par.getElementsByClassName("c_dots")[0];
    var moreText = par.getElementsByClassName("c_more")[0];
  
    if (dots.style.display === "none") {
      dots.style.display = "inline";
      btn.innerHTML = "Read more"; 
      moreText.style.display = "none";
    } else {
      dots.style.display = "none";
      btn.innerHTML = "Read less"; 
      moreText.style.display = "inline";
    }

  }