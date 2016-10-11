var req;
var count = 0;
function getFortune() {
    // count++;
    // var p = document.getElementById("info");
    // p.innerHTML = count;//req.readyState;
    sendRequest();
}
// Sends a new request to update the to-do list
function sendRequest() {
    if (window.XMLHttpRequest) {
        req = new XMLHttpRequest();
    } else {
        req = new ActiveXObject("Microsoft.XMLHTTP");
    }
    req.onreadystatechange = handleResponse;
    req.open("GET", "http://garrod.isri.cmu.edu/webapps/fortune", true);
    req.send(); 
}

function handleResponse() {
    var p = document.getElementById("content");
    p.innerHTML = req.responseText;
}
