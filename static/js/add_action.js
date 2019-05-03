/* JavaScript version to check empty fields
document.getElementById('submit_form').addEventListener('submit', function(e){
	var inputs = document.getElementsByClassName('time_check'), result

	for(var i=0; i<inputs.length; i++ ){
		if(inputs[i].value){

			result = true;
			break;
		}else{
			inputs[i].setAttribute('value',0)
		}

	}
	if(!result){
		e.preventDefault();
		alert('You must fill out at least one field');
	}
})*/
box = document.getElementsByClassName('checkboxinput')[0]
curently_time = document.getElementsByClassName('currently')[0]
box.addEventListener('click', function(e){
	if (box.checked ===true){
		curently_time.style.display='none'
	}else{
		curently_time.style.display='flex'
}})
