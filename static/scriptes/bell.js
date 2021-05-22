var box  = document.getElementById('box');
var down = false;
var count_element = document.getElementsByClassName("notifi-item").length

function toggleNotifi(){
	if (down) {
		box.style.height  =  '0px';
		box.style.opacity = 0;
        box.style.display = 'none';
		down = false;
	}else {

		box.style.height  = count_element * 50 + 'px';
		box.style.opacity = 1;
        box.style.display = 'block';
		down = true;
	}
}