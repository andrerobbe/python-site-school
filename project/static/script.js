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