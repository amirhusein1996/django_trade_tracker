const logOutBtn = document.getElementById("logOutBtn")
const logOutPopUpForm = document.getElementById('logOutPopUpForm')
const logOutCancel = document.getElementById("logOutCancel")


logOutBtn.addEventListener('click',()=>{
    // logOutPopUpForm.classList.add('show')
    showPopUp(logOutPopUpForm)
})

logOutCancel.addEventListener('click',()=>{
    // logOutPopUpForm.classList.remove('show')
    hidePopUp(logOutPopUpForm)
})