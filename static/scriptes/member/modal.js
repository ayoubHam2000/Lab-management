selected_sort_by = $(".member_select")[0].selectedIndex 
selected_sort_by_order = $(".member_select")[1].selectedIndex 


function openModel(e, type){
    //console.log(type)
    modal = document.getElementById(type);
    modal.style.display = "block";
}

function clearOrder(modal){
    $(".member_select")[0].selectedIndex  = selected_sort_by
    $(".member_select")[1].selectedIndex  = selected_sort_by_order
}

function closeModel(){
    //console.log('close')
    var modals = $(".modal")

    for(var i = 0; i < modals.length; i++){
        if(modals[i].style.display == 'block'){
            if(modals[i].id == 'order'){
                clearOrder(modals[i])
            }
        }
    }

    for(i = 0; i < modals.length; i++){
        modals[i].style.display = "none";
    }
    
}

