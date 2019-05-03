var category = document.getElementById('id_categorys');
var name = document.getElementById('category').innerText;
for (var i=0;i<category.length;i++){
	if (category.options[i].innerText === name){
		category.options[i].setAttribute('selected', true)
	}
}