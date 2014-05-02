function load() {
	var w,h;
	var oDoc = document.documentElement;
	w=oDoc.clientWidth;
	h = w*0.1;
	p = w*0.025;
	var tag = document.getElementsByClassName('big');
	for (var i=0;i<tag.length;i++) {
		tag.item(i).style.fontSize=h+"px"; 
	};
	var tag=document.getElementsByClassName('med');
	for (i=0;i<tag.length;i++) {
		tag.item(i).style.fontSize=p+"px"; 
	};
	window.alert("w="+w+",p="+p+",h="+h);
	var tag1=document.getElementById('tsgraph1');
	if (tag1) {
		tag1.width=w*0.8;
		tag1.height=w*0.25;
		tag1.src="http://api.thingspeak.com/channels/11489/charts/1?width="+w*0.8+"&height="+w*0.25+"&average=5&results=600&days=1&dynamic=false&xaxis=Fecha&title=Temperatura";
	}
	var tag2=document.getElementById('tsgraph2');
	if (tag2) {
		tag2.width=w*0.8;
		tag2.height=w*0.25;	
		tag2.src="http://api.thingspeak.com/channels/11489/charts/2?width="+w*0.8+"&height="+w*0.25+"&average=5&results=600&days=1&dynamic=false&xaxis=Fecha&title=Temperatura 2";
	}
};
