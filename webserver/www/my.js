function load() {
	var pinx = document.getElementById("pinx");
	var f = document.getElementById("pinselect");
	var td = document.getElementsByTagName('td');
	var fSize;
	if (window.innerHeight > window.innerWidth) {
		fSize=innerWidth;
	} else {
		fSize=innerHeight;
	}
	fSize=fSize * 0.2+"px";
	document.getElementById('btngo').disabled=true;
	f.pin.value="";
	for (var i = 0, length = td.length; i < length; i++) {
		td[i].style.fontSize=fSize;
	}
	drawPin(0);
	pinx.style.fontSize=fSize;
	
}
function drawPin(l){
	var i=0;
	var s="";
	while (i<4-l) {
		s=s+"&bull;";
		i++;
	}
	i=0;
	while (i<l) {
		s=s+"&oplus;";
		i++;
	}
	document.getElementById('pinx').innerHTML=s;
	if (s.length==4) {
		document.getElementById('btngo').disabled=false;
	} else {
		document.getElementById('btngo').disabled=true;
	}
	return;
}
function input(e) {
	var pin = document.getElementById("pin");
	if (pin.value.length<4){
		pin.value = pin.value + e;
	}
	drawPin(pin.value.length);
}
function del() {
	var pin = document.getElementById('pin');
	pin.value = pin.value.substr(0, pin.value.length - 1);
	drawPin(pin.value.length);
}
