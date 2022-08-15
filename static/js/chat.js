const roomName = JSON.parse(document.getElementById('json-roomname').textContent);
const userName = JSON.parse(document.getElementById('json-username').textContent);
const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/'
    + roomName
    + '/'
);

$(document).ready(function () {
    $('#chat-submit').attr('disabled', true);
    $('#chat-submit').css('cursor', 'no-drop');
    $('#chat-submit i').css('cursor', 'no-drop');

    $('#chat-message-input').keyup(function () {
        if ($(this).val().length != 0) {
            $('#chat-submit').attr('disabled', false);
            $('#chat-submit').css('cursor', 'pointer');
            $('#chat-submit i').css('cursor', 'pointer');
        } else {
            $('.sendButton').attr('disabled', true);
            $('#chat-submit').css('cursor', 'no-drop');
            $('#chat-submit i').css('cursor', 'no-drop');
        }
    })
});

var box = document.querySelector('.chat-area');
box.scrollTop = box.scrollHeight;

document.getElementById('hiddenFileInput').addEventListener('change', handleFileSelect, false)

function handleFileSelect(event) {
    var file = document.getElementById('hiddenFileInput').files[0];
    getBase64(file)
}

function getBase64(file) {
    var reader = new FileReader()
    reader.readAsDataURL(file)

    reader.onload = function () {
        chatSocket.send(JSON.stringify({
            "file_type": "file",
            "message": reader.result,
            'username': userName,
            'room': roomName
        }))
    }
}


document.getElementById('hiddenImageInput').addEventListener('change', handleImageSelect, false)

function handleImageSelect(event) {
    var image = document.getElementById('hiddenImageInput').files[0];
    getBaseImage64(image)
}

function getBaseImage64(file) {
    var reader = new FileReader()
    reader.readAsDataURL(file)

    reader.onload = function () {
        chatSocket.send(JSON.stringify({
            "file_type": "image",
            "message": reader.result,
            'username': userName,
            'room': roomName
        }))
    }
}

document.getElementById('hiddenVideoInput').addEventListener('change', handleVideoSelect, false)

function handleVideoSelect(event) {
    var video = document.getElementById('hiddenVideoInput').files[0];
    getBaseVideo64(video)
}

function getBaseVideo64(video) {
    var reader = new FileReader()
    reader.readAsDataURL(video)

    reader.onload = function () {
        chatSocket.send(JSON.stringify({
            "file_type": "video",
            "message": reader.result,
            'username': userName,
            'room': roomName
        }))
    }
}


document.getElementById('hiddenAudioInput').addEventListener('change', handleAudioSelect, false)

function handleAudioSelect(event) {
    var audio = document.getElementById('hiddenAudioInput').files[0];
    getBaseAudio64(audio)
}

function getBaseAudio64(audio) {
    var reader = new FileReader()
    reader.readAsDataURL(audio)

    reader.onload = function () {
        chatSocket.send(JSON.stringify({
            "file_type": "audio",
            "message": reader.result,
            'username': userName,
            'room': roomName
        }))
    }
}

chatSocket.onmessage = function (e) {

    const data = JSON.parse(e.data)

    var dateOptions = {

        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: 'numeric',
        minute: 'numeric',
        hour12: false,
    };
    var datetime = new Date(data.date_added).toLocaleString('tr', dateOptions);

    const message_type = data.file_type
    if (message_type === 'text') {
        if (data.message) {
            let html = `
                            <div class="chat-msg">
                                <div class="chat-msg-profile">
                                    <div class="chat-msg-date">${datetime}</div>
                                </div>
                                <div class="chat-msg-content">
                                    <div class="chat-msg-text">
                                        <p>${data.username}</p>
                                        <p>${data.message}</p>
                                    </div>
                                </div>
                            </div>
                       
                `

            document.querySelector('#chat-message').innerHTML += html;
            box.scrollTop = box.scrollHeight;

        } else {
            console.log("Boş mesaj")
        }
    } else if (message_type === 'file') {
        if (data.message) {
            let html = `
                            <div class="chat-msg">
                                <div class="chat-msg-profile">
                                    <div class="chat-msg-date">${datetime}</div>
                                </div>
                                <div class="chat-msg-content">
                                    <div class="chat-msg-text">
                                        <p>${data.username}</p>
                                        <a href="${data.message}" download="Forum Ekpser">
                                        <img src="/static/img/server/file.png" alt="File">
</a>
                                    </div>
                                </div>
                            </div>
                       
                `

            document.querySelector('#chat-message').innerHTML += html;
            box.scrollTop = box.scrollHeight;

        } else {
            console.log("Boş mesaj")
        }
    } else if (message_type === 'image') {
        if (data.message) {
            let html = `
                            <div class="chat-msg">
                                <div class="chat-msg-profile">
                                    <div class="chat-msg-date">${datetime}</div>
                                </div>
                                <div class="chat-msg-content">
                                    <div class="chat-msg-text">
                                        <p>${data.username}</p>
                                        <img src="${data.message}" alt="Image">
                                    </div>
                                </div>
                            </div>
                       
                `

            document.querySelector('#chat-message').innerHTML += html;
            box.scrollTop = box.scrollHeight;

        } else {
            console.log("Boş mesaj")
        }
    }else if (message_type === 'video') {
        if (data.message) {
            let html = `
                            <div class="chat-msg">
                                <div class="chat-msg-profile">
                                    <div class="chat-msg-date">${datetime}</div>
                                </div>
                                <div class="chat-msg-content">
                                    <div class="chat-msg-text">
                                        <p>${data.username}</p>
                                     
                                        <video controls width="250" height="250">
                                        <source src="${data.message}">
                                        </video>
</a>
                                    </div>
                                </div>
                            </div>
                       
                `

            document.querySelector('#chat-message').innerHTML += html;
            box.scrollTop = box.scrollHeight;

        } else {
            console.log("Boş mesaj")
        }
    }else if (message_type === 'audio') {
        if (data.message) {
            let html = `
                            <div class="chat-msg">
                                <div class="chat-msg-profile">
                                    <div class="chat-msg-date">${datetime}</div>
                                </div>
                                <div class="chat-msg-content">
                                    <div class="chat-msg-text">
                                        <p>${data.username}</p>
                                     
                                        <audio controls style="width: 250px;">
                                        <source src="${data.message}">
                                        </audio>
</a>
                                    </div>
                                </div>
                            </div>
                       
                `

            document.querySelector('#chat-message').innerHTML += html;
            box.scrollTop = box.scrollHeight;

        } else {
            console.log("Boş mesaj")
        }
    }

}

chatSocket.onclose = function (e) {
    console.log('onclose')
}

document.querySelector('#chat-message-input').onkeyup = function (e) {
    if ($(this).val().length != 0) {
        if (e.keyCode === 13) {
            document.querySelector('#chat-submit').click()
        }
    }

}

document.querySelector('#chat-submit').onclick = function (e) {
    e.preventDefault();
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;

    const dateInputDom = document.querySelector('#chat-message-input');
    const date_added = dateInputDom.value;

    chatSocket.send(JSON.stringify({
        "file_type": "text",
        'message': message,
        'username': userName,
        'room': roomName
    }));

    messageInputDom.value = '';
    return false;
}

document.querySelectorAll('.msg-img').forEach(image => {
    image.onclick = () => {
        document.querySelector('.popup-image').style.display = 'block';
        document.querySelector('.popup-image img').src = image.getAttribute('src');
    }
})

document.querySelector('.popup-image span').onclick = () => {
    document.querySelector('.popup-image').style.display = 'none';
}

