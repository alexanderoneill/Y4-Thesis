var confslider = document.getElementById("confslider");
var confoutput = document.getElementById("confdisplay");
confoutput.innerHTML = confslider.nodeValue;

var sizeslider = document.getElementById("sizeslider");
var sizeoutput = document.getElementById("sizedisplay");
sizeoutput.innerHTML = sizeslider.nodeValue;

var blobslider = document.getElementById("blobslider");
var bloboutput = document.getElementById("blobdisplay");
bloboutput.innerHTML = blobslider.nodeValue;

confslider.oninput = function() {
    confoutput.innerHTML = this.value;
}

sizeslider.oninput = function() {
    sizeoutput.innerHTML = this.value;
}

blobslider.oninput = function() {
    bloboutput.innerHTML = this.value;
}