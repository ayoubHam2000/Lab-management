function openMenu(e, id, state){
    //state 0 => not active
    //state 1 => active
    //state 2 => not signed

    console.log("Open Menu")
    var fun_1 = `member_Account(event, ${id})`
    var fun_2 = `deactivate_activate_member(event, ${id})`
    var fun_3 = `member_associerte_encadrant(event, ${id})`
    var fun_4 = `member_associerte_co_encadrant(event, ${id})`

    result = ""
    if(state != 2){
        result += `<button onclick="${fun_1}">account</button>`
        result += `<button onclick="${fun_3}">Accocier Doctorant</button>`
        result += `<button onclick="${fun_4}">Accocier Co.Encadrant</button>`
    }else if(state == 2){
        infoAlert("User has't yet create an account")
    }
    if(state == 0){
        result += `<button onclick="${fun_2}">activer account</button>`  
    }
    else if(state == 1){
        result += `<button onclick="${fun_2}">Désactiver account</button>` 
    }


    createMenu(e.target, result)
    e.stopPropagation()
}




