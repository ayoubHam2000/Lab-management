selected_sort_by = $(".member_select")[0].selectedIndex 
selected_sort_by_order = $(".member_select")[1].selectedIndex 


//#region Modal

//#region open
function openModel(e, type){
    console.log(type)
    modal = document.getElementById(type);
    modal.style.display = "block";
}

//#endregion

//#region close and clear
function clearAjouter(modal){
    inputs = modal.getElementsByTagName("input")
    for(i = 0; i < inputs.length; i++){
        inputs[i].value = "";
    }
}



function clearOrder(modal){
    $(".member_select")[0].selectedIndex  = selected_sort_by
    $(".member_select")[1].selectedIndex  = selected_sort_by_order
}


function closeModel(){
    //console.log('close')
    var modals = $(".modal")

    /*for(var i = 0; i < modals.length; i++){
        if(modals[i].style.display == 'block'){
            if(modals[i].id == 'Ajouter')
                clearAjouter(modals[i])
            if(modals[i].id == 'order'){
                clearOrder(modals[i])
            }
        }
    }
*/
    for(i = 0; i < modals.length; i++){
        //console.log(modals[i])
        modals[i].style.display = "none";
        
    }

    
}


// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        closeModel(event)
    }
  }

//#endregion

//#endregion


//#region get add delete search
//URL_MEMBER_DATA defined in addmember.html script

function setMemberContent(data){
    //console.log(data)
    $('#member_content').html(data);
}


//get
function getDataFromUrl(url) {
    console.log("get_member")
    console.log(url)

    searsh = $("#member_search_input")[0].value 
    sortType =  $(".member_select")[0].value 
    order =  $(".member_select")[1].value
    dataform = {
        'sortType' : sortType, 
        'order' : order, 
        'search' : searsh
    }
    console.log(dataform)
    $.ajax({
        url:url,
        type:'GET',
        data:{
            'dataform' : JSON.stringify(dataform)
        },
        success: function(data){
            console.log("success get_member")
            setMemberContent(data)
            closeModel()
        },
        error: function(e, x, r){
            setMemberContent("Something went wrong")
            console.log(e.responseText)
        }
    });
}

//=====================================================


$(document).ready(function() {
    //Search
    //member_search_input

    //search
    $('#member_search_input').keypress(function (e) {
    var key = e.which;
    if(key == 13)  // the enter key code
        {
        console.log("Search")
        getDataFromUrl(URL_MEMBER_DATA)
        }
    }); 


    //Ajouter member submit
    $('#ajouter_member_form').submit(function() { // On form submit event
        console.log('submit_member')
        $.ajax({ // create an AJAX call...
            data: $(this).serialize(), // get the form data
            type: $(this).attr('method'), // GET or POST
            url: $(this).attr('action'), // the file to call
            success: function(response) { // on success..
                getDataFromUrl(URL_MEMBER_DATA)
                //successAlert('ajout effectué avec succès ')
            },
            error: function(e, x, r) { // on error..
                //console.log(e.responseText)
                showError(e)
            }
        });
        return false;
    });


    //delete member
    $('#delete_member_form').submit(function(){
        console.log('delete_member')
    
        var a = confirm("Are you sure ?? (if account exist it will be also deleted)")
        if(a){
            $.ajax({ 
                data: $(this).serialize(), 
                type: $(this).attr('method'),
                url: $(this).attr('action'), 
                success: function(response) { 
                    //console.log("delete sucees")
                    successAlert('supprimé avec succès')
                    getDataFromUrl(URL_MEMBER_DATA)
                },
                error: function(e, x, r) {
                    showDefaultError()
                    //console.log(e.responseText)
                }
            });
        }
        return false;
    })

});

getDataFromUrl(URL_MEMBER_DATA)

//#endregion


//#region buttons



function orderButton(e){
    console.log('sort')
    getDataFromUrl(URL_MEMBER_DATA)
    selected_sort_by = $(".member_select")[0].selectedIndex 
    selected_sort_by_order = $(".member_select")[1].selectedIndex 
    
    closeModel(e)
}















//#endregion

