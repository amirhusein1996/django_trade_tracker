

//////////////////////// ALL const WE NEED
//select all button with .real class
const buttons = document.querySelectorAll('.real');
//select all input type ='hidden'
const hiddenInputs = document.querySelectorAll('.transfer-data input[type="hidden"]')
const tradeAccountHiddenInput = document.getElementById("account_name")
let accountNamePreviousValue = tradeAccountHiddenInput.value
const timeSelectedHiddenInput = document.getElementById("time_selected")
const pageHiddenInput = document.getElementById("page")
let pagePreviousValue  = pageHiddenInput.value
//conditions
const tradeInfo = document.getElementById("trade_info")
const dailyLossLimitInfo = document.getElementById("daily_loss_limit_info")
const overalLossLimitInfo = document.getElementById("overal_loss_limit_info")
const targetProfitInfo = document.getElementById("target_profit_info")

//get timeInterval selected value and change time_selected hidden input on change event
const selectElement = document.getElementById("timeInterval");
const downloadBtn = document.querySelector('.downloadBtn')



const currencyTypeInput = document.getElementById("input-currency-type")
const inputTime =document.getElementById("input-time")
const inputLots = document.getElementById("input-lots")
const inputSL = document.getElementById("input-sl")
const inputTP = document.getElementById("input-tp")
const inputProfit = document.getElementById("input-profit")
const addTradeRecordBtn = document.getElementById("add_trade_record_btn")



const dateTimeLocalRegex = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}$/;
/////////////////////////////****    AJAX GET TRADING HISTORY ****/////////////////////////////////
function formatNumber(number){
    var parsedNumber = Number(number)
    if (!isNaN(parsedNumber)){
        if (parsedNumber %1 === 0){
            return parsedNumber.toLocaleString('en-US', {maximumFractionDigits : 0});
        }else {
            return parsedNumber.toLocaleString('en-US' , {maximumFractionDigits:2});
        }
    }else {
        return "---"
    }
}
function dollarSign(number){
    var number = Number(number);
    if( number < 0){return "-$"+formatNumber(Math.abs(number))}else {
        return "$"+formatNumber(number)
    }
}



// add or remove .active class by clicking , and also change the #account_name hidden input value
buttons.forEach(button =>{
    button.addEventListener('click', () =>{
        //remove 'active' class from all buttons
        buttons.forEach(button=> {
            button.classList.remove('active');
        });

            //add 'active' class to clicked button
        button.classList.add('active');
        // change #account_name hidden input value
        //check if it's new value , set #account_name value to new one
        if (accountNamePreviousValue !== button.value){
            tradeAccountHiddenInput.value = button.value
            accountNamePreviousValue = button.value
        }
        })
    })


selectElement.addEventListener('change',()=>{
    var selectedValue = selectElement.options[selectElement.selectedIndex].value;
    timeSelectedHiddenInput.value = selectedValue
})

function changePageNumber(page){
 if ( page !== pagePreviousValue){
     pageHiddenInput.value = page;
     pagePreviousValue = page
 }
}





// create a MutationObserver instance
const observer = new MutationObserver(mutationsList => {
  // iterate through each mutation in the mutations list
  mutationsList.forEach(mutation => {
    // check if the mutation is a change in the value of an attribute
    if (mutation.type === 'attributes') {
      // get the changed element and its id
      const changedInput = mutation.target;
      const id = changedInput.getAttribute('id');

            if (id === 'account_name' && changedInput.value !=="") {
                tradeOverView({account_name : tradeAccountHiddenInput.value})
                tradeHistoryAJAX({
                    account_name : tradeAccountHiddenInput.value ,
                    time_selected : timeSelectedHiddenInput.value,
                    page : 1

                })
      } else if (id === 'time_selected' && changedInput.value !=="") {
               if(tradeAccountHiddenInput.value !== ""){
                    tradeHistoryAJAX({
                    account_name : tradeAccountHiddenInput.value ,
                    time_selected : timeSelectedHiddenInput.value,
                    page : 1

                })
                editNoteBtns = document.querySelectorAll(".edit-note-btn")
               }
      }else if (id === 'page' && changedInput.value !==""){
                if (tradeAccountHiddenInput.value !== ""){
                    tradeHistoryAJAX({
                    account_name : tradeAccountHiddenInput.value ,
                    time_selected : timeSelectedHiddenInput.value,
                    page : pageHiddenInput.value
                })
                // reasign edit note btn
                editNoteBtns = document.querySelectorAll(".edit-note-btn")
                }
            }

    }
  });
});

// start observing changes to the hidden inputs
hiddenInputs.forEach(input => {
  observer.observe(input, { attributes: true });
});



function tradeHistoryAJAX(dataToSend){
    $.ajax({
            url : urlObject.get_trade_record_list ,
            type: 'GET' ,
            dataType: 'json',
            data : dataToSend ,
            success : function (response){
                //chech document is fully loaded
                $(document).ready(function (){
                    // replace data
                    $('.pagination').html(response.pagination);
                    $('.table-list').html(response.html);


                    // define number of rows in  .table-list
                    var numRows = $('.table-list').find('.statement-row').length;

                    //if numRows == 0 we should show a message to user
                    var message = $('.messages')
                    if (numRows == 0){
                        message.show()
                        message.text("No Trade Record")

                    }// endif
                    else {
                        message.hide()
                        message.text('')
                    }// end else statement

                }//end function in ready method
                )//end ready method

            },//end succuss function
        error: function(jqXHR, textStatus, errorThrown) {
        if (jqXHR.status >= 400 && jqXHR.status < 500) {
            // handle 4xx errors
            alert("Error: " + errorThrown);
        } else if (jqXHR.status >= 500 && jqXHR.status < 600) {
            alert("Server error: " + errorThrown);
            // window.location.reload();
        }
    }


        })//end $.ajax
}

////////////////////////////////////////////////////////
function tradeOverView(dataToSend){
    $.ajax({
            url : urlObject.get_trade_overview ,
            type: 'GET' ,
            dataType: 'json',
            data : dataToSend ,
            success : function (response){
                //chech document is fully loaded
                $(document).ready(function (){
                    var detailStat = response.detail_stat;
                    var tradingObjectives = response.trading_objectives;
                    changeDetailStats(detailStat)
                    changeTradingObjectives(tradingObjectives)
                    changeConditions(tradingObjectives)
                })//end function in ready method
            },//end succuss function
        error: function(jqXHR, textStatus, errorThrown) {
        if (jqXHR.status >= 400 && jqXHR.status < 500) {
            // handle 4xx errors
            alert("Error: " + errorThrown);
        } else if (jqXHR.status >= 500 && jqXHR.status < 600) {
            alert("Server error: " + errorThrown);
            // window.location.reload();
        }
    }
    })//end $.ajax
}//end function


function changeDetailStats(object){
    $('#detail_equity').html(dollarSign(object.equity))
    $('#detail_balance').html(dollarSign(object.balance))
    $('#detail_winning').html(dollarSign(object.avg_win))
    $('#detail_losing').html(dollarSign(object.avg_lose))
    $('#total_trades').html(object.total_trades)
    $('#detail_win_rate').html(formatNumber(object.win_rate))
    $('#average_r_r').html(formatNumber(object.r_r))
}
function changeTradingObjectives(object){
    $('#minimum_trading_days').html(object.minimum_trading_days)
    $('#days_traded').html(object.days_traded)
    $('#daily_loss_limit').html(dollarSign(object.daily_loss_limit))
    $('#daily_loss_recored').html(dollarSign(object.daily_max_loss_record))
    $('#overal_loss_limit').html(dollarSign(object.overal_loss_limit))
    $('#max_loss_record').html(dollarSign(object.max_loss_record))
    $('#profit_target').html(dollarSign(object.profit_target))
    $('#current_profit').html(dollarSign(object.current_profit))
}

function changeConditions(object){
    if(object.days_traded >= object.minimum_trading_days){
        changeSecondClassItem(tradeInfo, "successful")
    }else {changeSecondClassItem(tradeInfo,"ongoing")}

    if (Math.abs(object.daily_max_loss_record) >= Math.abs(object.daily_loss_limit)){
        changeSecondClassItem(dailyLossLimitInfo, "failed")
    }else {changeSecondClassItem(dailyLossLimitInfo , "ongoing")}

    if (Math.abs(object.max_loss_record) >= Math.abs(object.overal_loss_limit)){
        changeSecondClassItem(overalLossLimitInfo, "failed")
    }else {changeSecondClassItem(overalLossLimitInfo , "ongoing")}

    if (object.current_profit >= object.profit_target){
        changeSecondClassItem(targetProfitInfo,"successful")
    }else {changeSecondClassItem(targetProfitInfo,"ongoing")}

}
function changeSecondClassItem(element,newSecondClassName){
    if (element.classList.length === 1 ){
        element.classList.add(newSecondClassName)
    }else {
        element.classList.replace(element.classList.item(1), newSecondClassName)
    }
    element.innerText= newSecondClassName
}





///////////////////////////////// Download chart  ////////////////////////

downloadBtn.addEventListener('click',()=>{
    var account_name = tradeAccountHiddenInput.value
    if (account_name ===""){return;}
    var tradeRecordCount = document.querySelectorAll(".statement-row").length
    if (!tradeRecordCount){
        alert("There's no trade record to create your trade chart");
        return;
    }
    // Create a temporary link element
    var link = document.createElement('a');
    link.href = urlObject.download_chart + "?slug=" +account_name
    // link.target ='_blank';

    //triger a click on it
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link)
})




///////////////////////////////// AJAX ADD NEW RECORD //////////////////////////////////////



// setInterval(function (){
//     var max = new Date().toLocaleString('en-US', {hour12: false}).replace(',', '').replace(/\//g, '-'); // set max for inputTime
//     inputTime.setAttribute('max' , max)
// }, 1000)
addTradeRecordBtn.addEventListener('click', ()=>{

    var tradeAccountName =tradeAccountHiddenInput.value;
    var currencyValue = currencyTypeInput.value;
    var timeValue = inputTime.value;
    var  lotValue = inputLots.value;
    var SLValue = inputSL.value;
    var TPValue = inputTP.value;
    var profitValue = inputProfit.value;

    //check the values
    // if (isNaN(currencyValue)){alert("Currency type must be set");return}
    if (tradeAccountName ===""){alert("Choose an account first");return;}
    if(!(timeValue === "" || dateTimeLocalRegex.test(timeValue))){
    alert("Please enter a valid date and time format");return;}
    if (isNaN(parseFloat(lotValue)) || lotValue===""){
        alert("Please enter a valid number for Lots") ; return;}
    if (isNaN(parseFloat(SLValue)) || SLValue===""){
        alert("Please enter a valid number for SL") ; return;}
    if (isNaN(parseFloat(TPValue)) || TPValue===""){
        alert("Please enter a valid number for TP") ; return;}
    if (isNaN(parseFloat(profitValue)) || profitValue===""){
        alert("Please enter a valid number for Profit") ; return;}
    //checked


    data = {
    account_name : tradeAccountName,
    currency_name : currencyValue,
        time : timeValue,
        lot : lotValue,
        sl : SLValue,
        tp : TPValue,
        profit :profitValue
    }

    createAccountDetail(data);

    // //after a new record added, overview must be updated
    // tradeOverView({account_name : tradeAccountHiddenInput.value})
})



function createAccountDetail(dataToSend){
    //post
    $.ajax({
        url: urlObject.create_trade_record,
        data : dataToSend,
        dataType : 'json',
        type:'POST',
        contentType:contentTypeNoFiles ,
        processData : true,

        success:function (response){
            if (response.message === true){
                tradeOverView({account_name : tradeAccountHiddenInput.value})
                tradeHistoryAJAX({
                    account_name : tradeAccountHiddenInput.value ,
                    time_selected : timeSelectedHiddenInput.value,
                    page : pageHiddenInput.value

                })
            }else {
                alert(decodeHTMLEntities(response.message))
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

    })
}

/////////////////////////////////// deactive trade account

const deactiveTradeAccountPopUpForm= document.getElementById("deactiveTradeAccountPopUpForm")
const deactiveBtn = document.getElementById("deactiveBtn")
const deactiveCancelBtn = document.getElementById("deactiveCancelBtn")



// if new button added , addEventListener to i tag
const leftNav = document.querySelector('nav .left')

const manageSVG = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-gear" viewBox="0 0 16 16">
  <path d="M8 4.754a3.246 3.246 0 1 0 0 6.492 3.246 3.246 0 0 0 0-6.492zM5.754 8a2.246 2.246 0 1 1 4.492 0 2.246 2.246 0 0 1-4.492 0z"></path>
  <path d="M9.796 1.343c-.527-1.79-3.065-1.79-3.592 0l-.094.319a.873.873 0 0 1-1.255.52l-.292-.16c-1.64-.892-3.433.902-2.54 2.541l.159.292a.873.873 0 0 1-.52 1.255l-.319.094c-1.79.527-1.79 3.065 0 3.592l.319.094a.873.873 0 0 1 .52 1.255l-.16.292c-.892 1.64.901 3.434 2.541 2.54l.292-.159a.873.873 0 0 1 1.255.52l.094.319c.527 1.79 3.065 1.79 3.592 0l.094-.319a.873.873 0 0 1 1.255-.52l.292.16c1.64.893 3.434-.902 2.54-2.541l-.159-.292a.873.873 0 0 1 .52-1.255l.319-.094c1.79-.527 1.79-3.065 0-3.592l-.319-.094a.873.873 0 0 1-.52-1.255l.16-.292c.893-1.64-.902-3.433-2.541-2.54l-.292.159a.873.873 0 0 1-1.255-.52l-.094-.319zm-2.633.283c.246-.835 1.428-.835 1.674 0l.094.319a1.873 1.873 0 0 0 2.693 1.115l.291-.16c.764-.415 1.6.42 1.184 1.185l-.159.292a1.873 1.873 0 0 0 1.116 2.692l.318.094c.835.246.835 1.428 0 1.674l-.319.094a1.873 1.873 0 0 0-1.115 2.693l.16.291c.415.764-.42 1.6-1.185 1.184l-.291-.159a1.873 1.873 0 0 0-2.693 1.116l-.094.318c-.246.835-1.428.835-1.674 0l-.094-.319a1.873 1.873 0 0 0-2.692-1.115l-.292.16c-.764.415-1.6-.42-1.184-1.185l.159-.291A1.873 1.873 0 0 0 1.945 8.93l-.319-.094c-.835-.246-.835-1.428 0-1.674l.319-.094A1.873 1.873 0 0 0 3.06 4.377l-.16-.292c-.415-.764.42-1.6 1.185-1.184l.292.159a1.873 1.873 0 0 0 2.692-1.115l.094-.319z"></path>
</svg>`

const leftNavCallback = function (mutationsList , leftNavObserver){
    for(let mutation of mutationsList){
        if(mutation.type === 'childList'){
            deactiveTradeAccountFunction();

            var manageButton = document.getElementById("manage")
            var realButtons = document.querySelectorAll(".real")
            if (!manageButton && realButtons){
                var manageURL = urlObject.manage_page

                $('.add-page').after(`<a href="${manageURL}"><button id="manage" class="circle-btn ">${manageSVG}</button></a>`)
            }
        }
    }
}
const leftNavObserver = new MutationObserver(leftNavCallback)
leftNavObserver.observe(leftNav,{childList:true})

deactiveCancelBtn.addEventListener('click',function (e){
    e.preventDefault()
    // deactiveTradeAccountPopUpForm.classList.remove('show')
    hidePopUp(deactiveTradeAccountPopUpForm)
})


function deactiveTradeAccountFunction(){
    var TradeAccountITags = document.querySelectorAll(".fa-solid")
TradeAccountITags.forEach(iButton =>{
    iButton.addEventListener('click',()=>{
        var tradeAccountbutton = iButton.parentNode
        var account_name = tradeAccountbutton.value

        // deactiveTradeAccountPopUpForm.classList.add('show')
        showPopUp(deactiveTradeAccountPopUpForm)
        deactiveBtn.addEventListener('click', function (e){
            e.preventDefault();
            $.ajax({
                url: urlObject.is_active,
                data:{is_active: false, account_name : account_name},
                dataType:'json',
                type:'POST',
                success:function (response){
                    tradeAccountbutton.remove()
                    // deactiveTradeAccountPopUpForm.classList.remove('show')
                    hidePopUp(deactiveTradeAccountPopUpForm)


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

            })

        })


    })
})
}
deactiveTradeAccountFunction()

////////////////////////////////**** edit trade record ****/////////////////////////////////////////////////
const popUpBox = document.querySelector(".popup-box")
const updateNoteForm = document.querySelector('.popup-box form')
const updateNoteBtn = document.getElementById("upadate_note")
const deleteRecordBtn = document.getElementById("delete_record")
const closeIcon = document.querySelector(".content header .uil-times");
const rowInputPlace = document.querySelector(".popup-box form .row")

closeIcon.addEventListener('click',() => {
    // closeUpdateNoteForm()
    hidePopUp(popUpBox)
})


let imagePreview
let imageInput
let imageFile
let reader
let checkBoxRemoveImage
let descriptionInput
function editTradeRecord(button , id){
    //Get form Inputs
    $.ajax({
        url:urlObject.update_note ,
        Type:'GET',
        data:{account_name : tradeAccountHiddenInput.value , id : id} ,
        dataType : 'json' ,
        success:function (response) {
            $(rowInputPlace).html(response.form)
                callbackGET()

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
    })
    function callbackGET(){
        descriptionInput = document.querySelector('.popup .row textarea');
         checkBoxRemoveImage = document.querySelector('.popup .row .check-box');
imagePreview = document.querySelector('.form-image-preview .img-preview');
            imageInput = document.querySelector('.popup .row .image-input');
            imageInput.addEventListener('change', ()=> {
                imageFile = imageInput.files[0];
                reader = new FileReader();
                 reader.addEventListener('load', () => {
                imagePreview.src = reader.result;
                        });
                    reader.readAsDataURL(imageFile);
            });

            // showUpdateNoteForm()
        showPopUp(popUpBox)
    }

    ////////// ready to POST Update Note
updateNoteBtn.addEventListener('click',function (e){
    e.preventDefault()
    var formData = new FormData(updateNoteForm);
    formData.append('account_name', tradeAccountHiddenInput.value)
    formData.append('id' , id)
    $.ajax({
        url: urlObject.update_note,
        data : formData,
        processData: false,
        contentType: false,
        type: 'POST',
        success : function (response){
            if(response.message === true){
                // popUpBox.classList.remove('show')
                hidePopUp(popUpBox)
                if (checkBoxRemoveImage) {
            if (checkBoxRemoveImage.checked && descriptionInput.value === "") {
                button.innerText = "Add"
            }
        } else if (imageInput.files.length == 0 && descriptionInput.value === "") {
            button.innerText = "Add"
        } else {
            button.innerText = "Edit"
        }
                    callbackPOST()

            }else {
                alert(response.message)
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

    })

})//end of update note

////////////////////////////////////////// Delete Trade Record //////////////////
    deleteRecordBtn.addEventListener('click',function (e){
        e.preventDefault();
    var deleteTradeAskForm = document.getElementById("delete_trade_ask_form")
    var deleteTradeSubmit = document.getElementById("delete_trade_submit")
    var deleteTradeCancel = document.getElementById("delete_trade_cancel")

        // popUpBox.classList.remove('show')
        hidePopUp(popUpBox)
        // deleteTradeAskForm.classList.add('show')
        showPopUp(deleteTradeAskForm)
        deleteTradeSubmit.addEventListener('click',function (e){
            e.preventDefault()

            $.ajax({
                url: urlObject.delete_trade_record,
                data:{is_delete:true ,id:id , account_name :tradeAccountHiddenInput.value},
                dataType:'json',
                type:'POST',
                processData:true,
                contentType:contentTypeNoFiles,
                success:function (response){
                    tradeOverView({account_name:tradeAccountHiddenInput.value})
                    tradeHistoryAJAX({
                        account_name:tradeAccountHiddenInput.value ,
                        time_selected: timeSelectedHiddenInput.value ,
                        page:pageHiddenInput.value
                    })
                          // popUpBox.classList.remove('show')
                    hidePopUp(popUpBox)
                    // deleteTradeAskForm.classList.remove('show')
                    hidePopUp(deleteTradeAskForm)
                    callbackPOST()


                }
            })
        })
        deleteTradeCancel.addEventListener('click',function (e){
            e.preventDefault();
            // deleteTradeAskForm.classList.remove('show')
            hidePopUp(deleteTradeAskForm)
            // popUpBox.classList.add('show')
            showPopUp(popUpBox)
        })

    })


    function callbackPOST() {

        /// set null all variables to prevent possibility risks
        checkBoxRemoveImage = null
        imagePreview = null
        imageInput = null
        descriptionInput = null
        imageFile = null
        reader = null
        checkBoxRemoveImage = null

        setTimeout(function (){rowInputPlace.innerHTML = ""},500)
    }

}

