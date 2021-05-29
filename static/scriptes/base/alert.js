function showAlert(type, message){
    span = '<span class="closebtn" onclick="this.parentElement.style.display=\'none\';">&times;</span>'
    $('#alter_pupup').html(span + message)
    $('#alter_pupup')[0].style.display = 'block'
    if(type == 0){
        $('#alter_pupup')[0].className = 'theAlert success'
    }
    if(type == 1){
        $('#alter_pupup')[0].className = 'theAlert info'
    }
    if(type == 2){
        $('#alter_pupup')[0].className = 'theAlert warning'
    }
    if(type == 3){
        $('#alter_pupup')[0].className = 'theAlert'
    }
    
}

function successAlert(message){
    showAlert(0, message)
}


function infoAlert(message){
    showAlert(1, message)
}

function warningAlert(message){
    showAlert(2, message)
}

function errorAlert(message){
    showAlert(3, message)
}

function showError(e){
    console.log(e.responseText)
    if(e.responseText.length < 100 || e.responseText.length == 0){
        errorAlert(e.responseText)
    }else{
        errorAlert("quelque chose s'est mal passé ")
    }
}

function showDefaultError(){
    errorAlert("quelque chose s'est mal passé ")
}


//==================================================
//==================================================
//==================================================

function ft_confirm(message = ""){
    if(message == ""){
        return confirm("Are you sure ??")
    }
    return confirm(message)
}