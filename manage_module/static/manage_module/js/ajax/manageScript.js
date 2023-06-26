function changePageNumber(page){
    window.location.href = location.pathname +"?page="+page
}

//////////////////////////////////////// EDIT TRADE ACCOUNT ///////////////////////////////////////////
const popupEditTradeAccountForm = document.getElementById('popupEditTradeAccountForm')
const editTradeAccountForm = document.getElementById("editTradeAccountForm")
const editInputPlace = document.getElementById('edit_input_place')
const editBtn = document.querySelectorAll('.edit-note-btn')
const editBtnSubmit = document.getElementById("editBtnSubmit")
const editBtnCancel = document.querySelector("#editBtnCancel")
let parent
let formDataObjects


editBtnCancel.addEventListener('click', function (){
    // popupEditTradeAccountForm.classList.remove("show");
    hidePopUp(popupEditTradeAccountForm)
    setTimeout(function (){$(editInputPlace).html("");},550)
    parent = null
    // editTradeAccountForm.setAttribute('action' , '')

})


editBtn.forEach(button =>{
    button.addEventListener('click',function (e){
        e.preventDefault()
        var URL = urlObject.edit_trade_account;
        parent = this.parentNode.parentNode
        getForm(URL).then(function (){
            // popupEditTradeAccountForm.classList.add('show')
            showPopUp(popupEditTradeAccountForm)
        });


    })
})


function getForm(url) {
  return new Promise(function(resolve, reject) {
    $.ajax({
        data:{title:parent.querySelector(".title-column").innerText},
      url: url,
      dataType: 'json',
      type: 'GET',
      success: function(response) {
        $(editInputPlace).html(response.form);
        resolve();
      },
      error: function(jqXHR, textStatus, errorThrown) {
        reject(errorThrown);
      }
    });
  });
}

editBtnSubmit.addEventListener('click', function(e) {
  e.preventDefault();
  var formData = $(editTradeAccountForm).serialize();
    console.log(formData)
  formDataObjects = Object.fromEntries(new URLSearchParams(formData));

  $.ajax({
    url: urlObject.edit_trade_account,
    type: 'POST',
    dataType: 'json',
    data: formData,
    contentType: contentTypeNoFiles,
    processData: true,
    success: function(response) {
            if (response.message ==true){

                // after edit form submitted, we update the row
                parent.querySelector(".title-column").innerText = formDataObjects.title
                parent.querySelector(".balance-column").innerText = formDataObjects.balance
                parent.querySelector(".profit-target-column").innerText = formDataObjects.profit_target
                parent.querySelector(".daily-loss-limit-column").innerText = formDataObjects.daily_loss_limit
                parent.querySelector(".overall-loss-limit-column").innerText = formDataObjects.overal_loss_limit
                parent.querySelector(".minimum-trading-days-column").innerText = formDataObjects.minimum_trading_days
                parent=null
                formDataObjects = null
                // popupEditTradeAccountForm.classList.remove('show');
                hidePopUp(popupEditTradeAccountForm)
                setTimeout(function (){$(editInputPlace).html("")},550);
                // editTradeAccountForm.setAttribute('action','')


            }else {
                alert(response.message)
            }

        },
            error: function(jqXHR, textStatus, errorThrown) {
        if (jqXHR.status >= 400 && jqXHR.status < 500) {
            // handle 4xx errors
            var response = jqXHR.responseJSON;
        if (response && response.error) {
            alert("Error "+jqXHR.status+" : " + response.error);
        }else {
            alert("Error: " + errorThrown);
        }


        } else if (jqXHR.status >= 500 && jqXHR.status < 600) {
            alert("Server error: " + errorThrown);
            // window.location.reload();
        }
    }
    })
        })



////////////////////////////////////////////////// IS ACTIVE /////////////////////////////////////////////
const checkBoxes = document.querySelectorAll("input[type='checkbox']")

checkBoxes.forEach(checkBox =>{
    checkBox.addEventListener('change',function (e){

        var isActiceCheckBox = this
        var isChecked = isActiceCheckBox.checked;
        var clickedRow = isActiceCheckBox.parentNode.parentNode
        var account_name = clickedRow.querySelector(".title-column").innerText
        isActiceCheckBox.checked = !isChecked // prevet changing Checked Value unless the value in database changes

        $.ajax({
            url:urlObject.is_active,
            data:{is_active:isChecked , account_name : account_name },
            type:'POST',
            dataType:'json' ,
            // contentType:contentTypeNoFiles,
            // processData:true,
            success:function (response){
                    if (response.message == true){$(isActiceCheckBox).prop('checked' , isChecked);}
                    else {
                        alert(response.message);
                        $(isActiceCheckBox).prop('checked' , !isChecked);
                    }

            },
            error: function(jqXHR, textStatus, errorThrown) {
        if (jqXHR.status >= 400 && jqXHR.status < 500) {
            // handle 4xx errors
            $(isActiceCheckBox).prop('checked' , !isChecked)
            alert("Error : " + errorThrown);
        } else if (jqXHR.status >= 500 && jqXHR.status < 600) {
            $(isActiceCheckBox).prop('checked' , !isChecked)
            alert("Server error: " + errorThrown);
            // window.location.reload();
        }
    }
            }

        )
    })
})



//////////////////////////////////////**** DELETE TRADE ACCOUNT ****////////////////////////////////
const deleteAccountPopUpForm = document.getElementById("deleteAccountPopUpForm")
const deleteAccountForm = document.getElementById("deleteAccountForm")
const accountNameToDelete = document.getElementById("AccountNameToDelete")
const deleteBtnCancel = document.getElementById("deleteBtnCancel")
const deleteBtnSubmit = document.getElementById("deleteBtnSubmit")
const deleteButtons = document.querySelectorAll(".delete-btn")
let title
deleteBtnCancel.addEventListener('click', ()=>{
    // deleteAccountPopUpForm.classList.remove("show")
    hidePopUp(deleteAccountPopUpForm);
    setTimeout(function (){
        $(AccountNameToDelete).html("")
    $(deleteAccountForm).attr('action' ,"" )
    },550)
    title = null
})


deleteButtons.forEach(delButton =>{
    delButton.addEventListener('click',function (e){
        e.preventDefault();

        //get the title of account
        title = delButton.parentNode.parentNode.querySelector(".title-column").innerText
        // end of GET title
        $(accountNameToDelete).html(title);
        var parent = $(this).closest('tr')
        // Get the current index of the row to be deleted
        var index = $(this).closest('tr').index();

        showPopUp(deleteAccountPopUpForm)


    })
})// end forEach



//POST
deleteBtnSubmit.addEventListener('click', function (e){
        e.preventDefault();
    console.log(title)
        $.ajax({
            url:urlObject.delete_trade_account,
            data:{account_name: title},
            type: "POST",
            dataType: "json",
            success:function (response){
                // deleteAccountPopUpForm.classList.remove("show")
                hidePopUp(deleteAccountPopUpForm)
                title= null
                window.location.reload()
            },//end success function
            error: function(jqXHR, textStatus, errorThrown) {
        if (jqXHR.status >= 400 && jqXHR.status < 500) {
            alert('Object does not exist or is already deleted')
        }

    }
        })//end ajax post

})




// function remarkSN (){
//     var SN = document.querySelectorAll(".manage-page .data-table-container td:first-child")
//     var firstSN = SN[0].innerText
//     // var counter = 1;
//     console.log(firstSN)
//
//         for (i=1 ; i < SN.length ; i++){
//         var newSN = parseInt(firstSN) + i
//             console.log(i +" "+ newSN)
//         SN[i].innerText = newSN
//     }
//
// }