co_auteurs = []

function addLi(co_auteur_id, co_auteur_name) {
	parent = document.getElementById("myUL");
	var li = document.createElement("li");
	
	li.className = 'list-group-item form-control'
	parent.appendChild(li);

	deleteBtn = `
	<div>
		${co_auteur_name}
	</div>
	<span class="list-group-item close" onclick='delteCoAuteur(${co_auteur_id})' >×</span>`
	
	li.innerHTML = deleteBtn;
	return li;
}

 
function refreshList(){
	p = document.getElementById("myUL")
	p.innerHTML=""
	for(var i = 0; i < co_auteurs.length; i++){
		addLi(co_auteurs[i].id, co_auteurs[i].auteur)
	}	
	input = document.getElementById("co_auteur")
	input.value = JSON.stringify(co_auteurs);
}


function isAlreadyExist(id){
	for(var i = 0; i < co_auteurs.length; i++){
		if(id == co_auteurs[i].id){
			return true
		}
	}
	return false
}

function addCoAuteur(co_auteur_id, co_auteur_name){
	isExist = isAlreadyExist(co_auteur_id) 
	if(isExist){
		alert("déjà existé")
	}else{
		if(co_auteur_id === ''){
			alert("!!!")
		}else{
			co_auteurs.push({
				'auteur' : co_auteur_name,
				'id' :co_auteur_id
			})
			refreshList()

		}
	}
}

function delteCoAuteur(co_auteur_id){
	for(var i = 0; i < co_auteurs.length; i++){
		if(co_auteur_id == co_auteurs[i].id){
			co_auteurs.splice(i, 1)
			refreshList()
			break
		}
	}
}


function newElement() {
	var sel = document.getElementById("myInput")
	var co_auteur_id = sel.options[sel.selectedIndex].value;
	var co_auteur_name = sel.options[sel.selectedIndex].text;
	
	console.log(co_auteur_id)
	console.log(co_auteur_name)
	addCoAuteur(co_auteur_id, co_auteur_name)
	
	console.log(co_auteurs)

	//li = addLi(inputValue);
}


function init(){
	input = input = document.getElementById("co_auteur")
	s = input.value
	if(s === ''){
		input.value = '[]'
	}else{
		co_auteurs = JSON.parse(s);
		refreshList()
	}
}

init()

