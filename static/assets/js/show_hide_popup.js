function showPopUp(popUpElement){
     var opacity = 0;

  // popup.style.display = 'block';

  // Fade in the popup
var fadeIn = setInterval(function() {
    opacity += 0.1;
    popUpElement.style.opacity = opacity;
if (opacity === 0.1){
    popUpElement.classList.add('show')
    popUpElement.style.display = 'block'
}
    if (opacity >= 1) {
      clearInterval(fadeIn);
    }
  }, 20);
}

function hidePopUp(popUpElement){
     var opacity = 1;
  // Fade out the popup
var fadeOut = setInterval(function() {
    opacity -= 0.1;
    popUpElement.style.opacity = opacity;

    if (opacity <= 0) {
      clearInterval(fadeOut);
      popUpElement.classList.remove('show')
    popUpElement.style.display = 'none'
    }
  }, 20);
}
