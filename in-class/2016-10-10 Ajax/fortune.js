var req;
function getFortune() {
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
