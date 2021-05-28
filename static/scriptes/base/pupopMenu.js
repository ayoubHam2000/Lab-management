function createMenu(parent, result){
    if(result == "")
        return
    menu = $("#main_drop_menu")[0]

    if(menu && menu.parentElement == parent)
        return
    if(menu)
        menu.remove()

    ele = document.createElement('div')
    ele.id = "main_drop_menu"
    ele.className = "main_drop_menu"
    ele.innerHTML = result
    parent.appendChild(ele)
}

function closeMenu(e){
    ele = $("#main_drop_menu")
    if(ele){
        ele.remove()
        e.stopPropagation()
    } 
}


$(window).click(function(event) {
    closeMenu(event)
});
  
  
  