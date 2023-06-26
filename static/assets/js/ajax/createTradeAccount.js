const addAccountBtn = document.getElementById('add-account');
const popupCreateTradeAccountForm = document.getElementById("popupCreateTradeAccountForm")
const createTradeAccountForm = document.getElementById("createTradeAccountForm")
// const createTradeAccountFormActionURL = popupCreateTradeAccountForm.action;
const cancelAccountBtn = document.getElementById("CreateBtnCancel")
const inputPlaceDiv = document.getElementById("create_input_place");
const errorList = document.getElementById("errorlist")



function openCreateTradeAccountForm() {

//get
$(document).ready(function (){
    $.ajax({
        url:urlObject.create_trade_account,
        type:'GET',
        dataType:'json',
        success: function (response){

            inputPlaceDiv.innerHTML = response.form;

            $(document).ready(function (){
                // document.getElementById("popupCreateTradeAccountForm").classList.add("show");
                showPopUp(popupCreateTradeAccountForm)
            })

        },
        error: function(jqXHR, textStatus, errorThrown) {
        if (jqXHR.status >= 400 && jqXHR.status < 500) {
            // handle 4xx errors
            alert("Error: " + errorThrown);
        } else if (jqXHR.status >= 500 && jqXHR.status < 600) {
            alert("Server error: " + errorThrown);
            // window.location.reload();
        }
    }
    })//end ajax
    })//end function

}

function closeCreateTradeAccountForm() {

$(document).ready(function (){
     // document.getElementById("popupCreateTradeAccountForm").classList.remove("show");
    hidePopUp(popupCreateTradeAccountForm)
     setTimeout(function (){
         $(inputPlaceDiv).html('')
     },550)
})

}


//event listeners
addAccountBtn.addEventListener('click',()=>{
    openCreateTradeAccountForm();
})
cancelAccountBtn.addEventListener('click',()=>{
    closeCreateTradeAccountForm()
})
//end of events



//post
$("#createTradeAccountForm").submit(function (e){
        e.preventDefault();
        var formData = $(this).serialize();
        var isValid = true
        var formDataParams = new URLSearchParams(formData)
            formDataParams.forEach((value, key)=>{
                if (key !=='title'){
                    if(isNaN(Number(value))){
                        isValid = false
                        alert('Enter a valid number for '+key)
                       return
                    }
                }
            })

    if (isValid){ $.ajax({
                url : urlObject.create_trade_account,
                type: 'POST',
                data:formData,
                processData: true,
                contentType : contentTypeNoFiles ,
                success: function (response){
            if (response.message === true){
                 closeCreateTradeAccountForm()

                if(window.location.pathname === "/home/"){
                    var buttonValue = response.newButtonSlug
                    var buttonText = response.newButtonTitle
                    // Create a new button element with the same pattern and updated value and text
                    var newButton = $('<button class="real"><span></span><i class="fa-solid fa-trash"></i></button>');
                    newButton.val(buttonValue).find('span').text(buttonText);
                    // Append the new button to the end of the existing buttons with class '.real'
                    // $('.real:last').after(newButton);
                    $(".add-page").before(newButton)

                    newButton.on('click',function (){
                        if (accountNamePreviousValue !== newButton.val()){
                         tradeAccountHiddenInput.value = newButton.val();
                         accountNamePreviousValue = newButton.val()
                     }
                 })

                }



         // setTimeout(function (){$(inputPlaceDiv).html('')} , 550);
            }else {
                var message = decodeHTMLEntities(response.message)
                alert(message)
            }

        },
                error: function(jqXHR, textStatus, errorThrown) {
        if (jqXHR.status >= 400 && jqXHR.status < 500) {
            // handle 4xx errors
            alert("Error: " + errorThrown);
        } else if (jqXHR.status >= 500 && jqXHR.status < 600) {
            alert("Server error: " + errorThrown);
            // window.location.reload();
        }
    }
     })//end ajax
        }

    })







