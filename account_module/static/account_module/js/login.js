function forgotPassword(redirectURL){
    const emailInput = document.querySelector('#id_email');
    const email = emailInput.value;

    var mailformat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
    if(email.match(mailformat)){
        window.location.href= redirectURL+'?email='+email
    }else {
        window.location.href = redirectURL
        }
    }
