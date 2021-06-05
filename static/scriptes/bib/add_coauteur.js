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




function init(data){
	data = data['auteurs']
	pr_auteur = document.getElementById('pr_auteur')

	pr_auteurs_op = pr_auteur.options

	f_co_auteurs = []
	for(i = 0; i < data.length; i++){
		id = data[i]['id']
		auteur = data[i]['auteur']
		type = data[i]['type']


		if(type == 0){
			for(j = 0; j < pr_auteurs_op.length; j++){
				if(pr_auteurs_op[j].value == id){
					console.log(pr_auteurs_op[j].value)
					pr_auteur.value = pr_auteurs_op[j].value
					break
				}
			}
		}else{
			f_co_auteurs.push({
				'auteur' : `${auteur} #${id}`,
				'id' : id
			})
		}
	}
	if(f_co_auteurs.length == 0){
		input.value = '[]'
	}else{
		co_auteurs = f_co_auteurs;
		refreshList()
	}
}

function getAuteurs(){
	$.ajax({
        url:GET_AUTEURS_UPDATE,
        type:'GET',
        success: function(data){
			init(data)
        },
        error: function(e, x, r){
            //console.log(e.responseText)
        }
    });
}


$(document).ready(function() {
    console.log(GET_AUTEURS_UPDATE)
	if(GET_AUTEURS_UPDATE != ""){
		console.log("Update")
		getAuteurs()
	}

});



