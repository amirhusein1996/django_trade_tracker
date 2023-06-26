// setup for post method
$.ajaxSetup({
    headers: {"X-CSRFToken": $('meta[name="csrf-token"]').attr('content')}
})

const contentTypeNoFiles = 'application/x-www-form-urlencoded';
const homeViewNameArray = [
    'get_trade_record_list',
    'get_trade_overview',
    'edit_trade_account',
    'create_trade_account',
    'download_chart',
    'is_active',
    'delete_trade_account',
    'update_note',
    'delete_trade_record',
    'create_trade_record',
    'manage_page',
]

let urlObject

$.ajax({
        url: "/base/ajax-requests/get/home_and_manage_urls/",
        type: 'GET',
        async: false,
        data: JSON.stringify(homeViewNameArray),
        success: function (response) {
            var result  = JSON.parse(response.result)
            urlObject = result
        }
    });


function decodeHTMLEntities (str){
    if (str && typeof str === 'string'){
        const tempNode = document.createElement('div');
        tempNode.innerHTML = str
        var  result = tempNode.innerText
        tempNode.remove()
        return result
    }
}