var addBtn = document.getElementById("addBtn");
var todolist = document.getElementById("todolist");


function del(todolist, li)  {
    todolist.removeChild(li);
}

addBtn.addEventListener("click", function () {
    var LI = document.createElement('li');
    LI.innerHTML = document.getElementById("textfield").value;
    todolist.appendChild(LI);

    var delBtn = document.createElement('button');
    delBtn.innerHTML = "Delete";
    LI.appendChild(delBtn);
    delBtn.addEventListener("click", function () {
        todolist.removeChild(LI);
    });
})
