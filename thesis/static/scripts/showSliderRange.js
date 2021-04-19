var slider = document.getElementById("slider");
var output = document.getElementById("display");
output.innerHTML = slider.nodeValue;

slider.oninput = function() {
    output.innerHTML = this.value;
}