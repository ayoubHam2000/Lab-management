//get deactivate delete addMember search
doctorant_id = null;

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
            //console.log("success get_member")
            $('#member_content').html(data);
            closeModel()
        },
        error: function(e, x, r){
            $('#member_content').html("Something went wrong");
            //console.log(e.responseText)
        }
    });
}

function searchMember(){
    $('#member_search_input').keypress(function (e) {
        var key = e.which;
        if(key == 13)  // the enter key code
        {
            //console.log("Search")
            getMemberData()
        }
    }); 
}

function orderButton(e){
    //console.log('sort')
    getMemberData()
    //defined in member/modal.js
    selected_sort_by = $(".member_select")[0].selectedIndex 
    selected_sort_by_order = $(".member_select")[1].selectedIndex 
    
    closeModel(e)
}

function addMember(){
    $('#ajouter_member_form').submit(function() { // On form submit event
        //console.log('submit_member')
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
    //console.log("deactivate_member")
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
                //console.log("deactivate success")
                getMemberData()
            },
            error: function(e, x, r) {
                showDefaultError()
                //console.log(e.responseText)
            }
        });
    }
}

function encadrant_switch_admin(e, id){
    //("encadrant_switch_admin")
    //console.log(id)

    var a = ft_confirm()
    if(a){
        data = getPostDict()
        data['id'] = id

        $.ajax({ 
            data: data, 
            type: 'POST',
            url: URL_MEMBER_SWITCH_ADMIN, 
            success: function(response) { 
                //console.log("encadrant_switch_admin success")
                successAlert("Succès")
                getMemberData()
            },
            error: function(e, x, r) {
                showDefaultError()
                //console.log(e.responseText)
            }
        });
    }
}

function delete_member(e, id){
    //console.log('ask delete_member')
    var a = ft_confirm("Are you sure ?? (if account exist it will be also deleted)")
    if(a){
        //console.log('delete_member')
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

function noAccount(){
    infoAlert('le membre n\'a pas encore de compte')
}



//=================================================
//Member associate

function getAndsetRelations(id){
    //console.log(`getAndsetRelations for ${id}`)
    data = {
        'id' : id
    }

    $.ajax({
        url:URL_MEMBER_GET_RELATION,
        type:'GET',
        data: data,
        success: function(data){
            //console.log("success get relations")
            $('#list_relation_section').html(data);
        },
        error: function(e, x, r){
            $('#list_relation_section').html("Un problème est survenu");
            //console.log(e.responseText)
        }
    });
}

function member_associate(e){
    //console.log('Associer Encadrant')

    data = getPostDict()
    data['id'] = doctorant_id
    data['memberEmail'] = $('#memberEmail_email')[0].value
    data['relationType'] = $('#relationtype_input')[0].value

    $.ajax({ 
        data: data, 
        type: 'POST',
        url: URL_MEMBER_ASSOCIER, 
        success: function(response) { 
            //console.log("Accoier success")
            successAlert(response)
            getAndsetRelations(doctorant_id)
        },
        error: function(e, x, r) {
            showError(e)
            //console.log(e.responseText)
        }
    });
    return false;
}


function deleteAssociation(e, id){
    //console.log('delete relation')

    data = getPostDict()
    data['id'] = id

    $.ajax({ 
        data: data, 
        type: 'POST',
        url: URL_MEMBER_DELETE_RELATION, 
        success: function(response) { 
            //console.log("delete relation success")
            successAlert(response)
            getAndsetRelations(doctorant_id)
        },
        error: function(e, x, r) {
            showError(e)
            //console.log(e.responseText)
        }
    });
    return false;
}

function member_relations_mg(e, id){
    doctorant_id = id
    openModel(e, 'co_encadrant')
    getAndsetRelations(id)
}

//=================================================
//Document


$(document).ready(function() {
    //to define functions
    searchMember()
    addMember()

    //to init
    getMemberData()
});

$('#myModal').on('shown.bs.modal', function () {
    $('#myInput').trigger('focus')
  })