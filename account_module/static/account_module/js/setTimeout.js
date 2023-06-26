const Btn = document.querySelector(".btn-login");
const redirectURL = Btn.href

const span = document.querySelector(".container .timer")
const timer = 5; // seconds
span.innerText = timer

document.addEventListener('DOMContentLoaded', function (){
        let sTO = setTimeout(function (){
            window.location.href=redirectURL;
            window.clearTimeout(sTO);
        },timer*1000)
    })