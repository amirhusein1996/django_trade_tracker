const imageInput = document.querySelector('.image-input-container .image-input');
const imageInputLabel = document.querySelector('.image-input-container .image-input-label');
const labelIcon = document.querySelector('.image-input-container .image-input-label i');
const labelInnerSpan = document.querySelector('.image-input-container .image-input-label span')
const allowedFileExtensions = /(\.jpg|\.jpeg|\.jfif|\.jpe|\.png|\.bmp|\.dib|\.tif|\.tiff|\.gif\.xbm|\.ico|\.svg|\.webp|\.svgz|\.pjp|\.avif|\.pjpeg|\.apng)$/i
const checkedIcon = 'fa fa-check';
const attachedIcon = 'fa fa-paperclip'
const alertIcon = 'fas fa-exclamation'

imageInput.addEventListener('change' , () => {
    var filePath = imageInput.value;

    if( imageInput.files[0]){
        if (!allowedFileExtensions.exec(filePath)){
        labelIcon.setAttribute('class' , alertIcon);
        labelIcon.style.color = '#c80000';
        labelInnerSpan.innerHTML = 'Attach a photo';
        imageInput.value = '' ;
        setTimeout(function (){
            labelIcon.setAttribute('class', attachedIcon);
        labelIcon.style.color = ''
        labelInnerSpan.innerText = 'Attach a photo'
        } , 5000)
    }else {
        labelIcon.setAttribute('class' , checkedIcon);
        labelIcon.style.color = '#57b846';
        labelInnerSpan.innerText = 'Photo attached';
    }
    }else {
        labelIcon.setAttribute('class', attachedIcon);
        labelIcon.style.color = ''
        labelInnerSpan.innerText = 'Attach a photo'

    }


})