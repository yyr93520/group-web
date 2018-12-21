/**
 * Created by yangyaru on 2018/12/14.
 */
var div = document.getElementById('background');
var close = document.getElementById('close-button');

function session_info() {

	div.style.display = "block";
}

close.onclick = function close() {
	div.style.display = "none";
}

window.onclick = function close(e) {
	if (e.target == div) {
		div.style.display = "none";
	}
}