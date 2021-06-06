function refreshInput(parent){
	var result = []
	var input = document.getElementById("co_auteur")

	//console.log('ADD')

	var liElements = parent.getElementsByTagName("li");
	//console.log(parent)

	for(i = 0; i < liElements.length; i++){
		value = liElements[i].getElementsByTagName("div")[0].innerHTML
		result.push(value)
	}
	//console.log(result)
	input.value = result.toString()
}

function removeElement() {
	var elem = this.parentElement;
	var parent = elem.parentElement;
	elem.parentNode.removeChild(elem);
	refreshInput(parent);
}

function add_co_auteur(li) {
	var parent = li.parentElement;
	refreshInput(parent);
}

function addLi(inputValue) {
	parent = document.getElementById("myUL");
	var li = document.createElement("li");
	
	var valueDiv = document.createElement("div");
	valueDiv.innerHTML = inputValue;
	li.appendChild(valueDiv);
	li.className = 'list-group-item form-control'
	parent.appendChild(li);
	
		var span = document.createElement("SPAN");
	var txt = document.createTextNode("\u00D7");
	span.className = "list-group-item close";
	span.onclick = removeElement;
	span.appendChild(txt);
	li.appendChild(span);
	return li;
}

// Create a new list item when clicking on the "Add" button
function newElement() {
	var inputValue = document.getElementById("myInput").value;

	if (inputValue === '') {
		alert("You must write something!");
	} else {
		li = addLi(inputValue);
		add_co_auteur(li);    
		document.getElementById("myInput").value = "";
	}

}


function init()     {
	var parent = document.getElementById("myUL")

	var input = document.getElementById("co_auteur");
	var auteurs = input.value.split(",")
	for (i = 0; i < auteurs.length; i++) {
		
		if (!(auteurs[i].length === 0 )) {
			//console.log(auteurs[i])
            addLi(auteurs[i])
		}
			
	}
	
	var close = parent.getElementsByClassName("close");
	for (var i = 0; i < close.length; i++) {
		close[i].onclick = removeElement
	}

}

init()
