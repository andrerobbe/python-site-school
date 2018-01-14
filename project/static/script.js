function ShowMoreInfo(e){
	var buttons = document.getElementsByClassName("dropdown");
	if (buttons){
		for (var i = 0, btnCount = buttons.length; i < btnCount; i++) {
			buttons[i].onclick = function(e) {
				this.classList.toggle("show");
			};
		}
	}
}
ShowMoreInfo();

/* page refreshes anyway */
function askConfirmOnDelete(e){
	var buttons = document.getElementsByClassName("deletebtn");
	if (buttons){
		for (var i = 0, btnCount = buttons.length; i < btnCount; i++) {
			buttons[i].onclick = function(e) {
				var input_field = this;
				window.confirm("Are you sure?");
			};
		}
	}
}
askConfirmOnDelete();