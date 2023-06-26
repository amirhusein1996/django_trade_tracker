const removeImageCheckBox = document.querySelector("form input[type='checkbox']")
const iconTopRight = document.querySelector(".icon-container .top-right i") // display : none;
const iconCenter = document.querySelector(".icon-container .center i") // opacity : 0;
const image = document.querySelector('.image-preview')
const trashIcon = 'fa-solid fa-trash'
const undoIcon = 'fa fa-undo'



///hide
function hide(element){
    var opacity = 1

    var fadeOut = setInterval(function() {
        opacity -= 0.1;
        element.style.opacity = opacity;
    
        if (opacity <= 0) {
          clearInterval(fadeOut);
        }
      }, 20);
}

///show
function show(element){
    var opacity = 0

    var fadeIn = setInterval(function() {
        opacity += 0.1;
        element.style.opacity = opacity;

        if (opacity >= 1) {
          clearInterval(fadeIn);
        }
      }, 20);
}



if (removeImageCheckBox){
    iconTopRight.style.display = 'block'

    iconTopRight.addEventListener('click' , ()=> {
        var isChecked = removeImageCheckBox.checked
            
        if (isChecked){
            iconTopRight.setAttribute('class', trashIcon)
            show(image);
            hide(iconCenter)


            
        }else{
            iconTopRight.setAttribute('class', undoIcon)
            show(iconCenter)
            hide(image)
        }
        removeImageCheckBox.checked = !isChecked
    } )



}




const imageInput = document.querySelector('form input[type="file"]')
const imagePreview = document.querySelector(".image-container img")
console.log(imagePreview);

imageInput.addEventListener('change' , ()=> {
    var imageFile = imageInput.files[0]; 
    var reader = new FileReader();
    reader.addEventListener('load' , () => {
        imagePreview.src = reader.result;
    });
reader.readAsDataURL(imageFile);
});