//get deactivate delete addMember search


function getMemberData() {
    console.log("getMemberData")
    searsh = $("#member_search_input")[0].value 
    sortType =  $(".member_select")[0].value 
    order =  $(".member_select")[1].value
    dataform = {
        'sortType' : sortType, 
        'order' : order, 
        'search' : searsh
    }

    //console.log(dataform)
    $.ajax({
        url:URL_MEMBER_DATA,
        type:'GET',
        data:{
            'dataform' : JSON.stringify(dataform)
        },
        success: function(data){
            console.log("success get_member")
            $('#member_content').html(data);
            closeModel()
        },
        error: function(e, x, r){
            setMemberContent("Something went wrong")
            console.log(e.responseText)
        }
    });
}

function searchMember(){
    $('#member_search_input').keypress(function (e) {
        var key = e.which;
        if(key == 13)  // the enter key code
        {
            console.log("Search")
            getMemberData()
        }
    }); 
}

function orderButton(e){
    console.log('sort')
    getMemberData()
    //defined in member/modal.js
    selected_sort_by = $(".member_select")[0].selectedIndex 
    selected_sort_by_order = $(".member_select")[1].selectedIndex 
    
    closeModel(e)
}

function addMember(){
    $('#ajouter_member_form').submit(function() { // On form submit event
        console.log('submit_member')
        $.ajax({ // create an AJAX call...
            data: $(this).serialize(), // get the form data
            type: $(this).attr('method'), // GET or POST
            url: $(this).attr('action'), // the file to call
            success: function(response) { // on success..
                getMemberData()
                //successAlert('ajout effectué avec succès ')
            },
            error: function(e, x, r) {
                //console.log(e.responseText)
                showError(e)
            }
        });
        return false;
    });
}

function deactivate_activate_member(e, id){
    console.log("deactivate_member")
    //console.log(id)

    var a = ft_confirm()
    if(a){
        data = getPostDict()
        data['id'] = id

        $.ajax({ 
            data: data, 
            type: 'POST',
            url: URL_MEMBER_DEACTIVATE, 
            success: function(response) { 
                console.log("deactivate success")
                getMemberData()
            },
            error: function(e, x, r) {
                showDefaultError()
                console.log(e.responseText)
            }
        });
    }
}

function delete_member(e, id){
    console.log('delete_member')
    
    var a = ft_confirm("Are you sure ?? (if account exist it will be also deleted)")
    if(a){
        data = getPostDict()
        data['id'] = id

        $.ajax({ 
            data: data, 
            type: 'POST',
            url: URL_MEMBER_DELETE, 
            success: function(response) { 
                //console.log("delete sucees")
                successAlert('supprimé avec succès')
                getMemberData()
            },
            error: function(e, x, r) {
                showError(e)
                //console.log(e.responseText)
            }
        });
    }
    return false;
}

function member_Account(e, id){
    console.log("member_Account")
    console.log(id)

    data = {
        'id' : id
    }
    $.ajax({ 
        data: data, 
        type: 'GET',
        url: URL_MEMBER_ACCOUNT, 
        success: function(response) { 
            console.log(response)
            $(location).attr('href', response)           
        },
        error: function(e, x, r) {
            showError(e)
            //console.log(e.responseText)
        }
    });
    
    closeMenu(e)
}

$(document).ready(function() {
    //to define functions
    searchMember()
    addMember()

    //to init
    getMemberData()
});