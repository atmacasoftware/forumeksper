const userName = JSON.parse(document.getElementById('json-username').textContent);
const forumID = JSON.parse(document.getElementById('json-forumid').textContent);
const btns = document.querySelectorAll('.reply_create')

$(document).ready(function () {
    btns.forEach(btn => {
        btn.addEventListener('click',function (e){
            e.preventDefault();
            console.log(btn)
        })
    })
});