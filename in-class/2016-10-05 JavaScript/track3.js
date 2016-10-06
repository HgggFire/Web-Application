for (var i=0; i<1000; i++) {
  var btn = document.createElement('button');
  btn.innerHTML = i;
  btn.addEventListener('click', function(event) {
    alert('You clicked button '+ i);
  });
  document.body.appendChild(btn);
}