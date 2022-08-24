const roomName = JSON.parse(document.getElementById('json-roomname').textContent);
const userName = JSON.parse(document.getElementById('json-username').textContent);
const profile = JSON.parse(document.getElementById('json-profile').textContent);
const roomID = JSON.parse(document.getElementById('json-roomid').textContent);

const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/'
    + roomName
    + '/'
);

const alertWrapper = document.querySelector('.alert-wrapper');
var isRecord = false

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
    if (file.size > 31457281) {
        alertWrapper.innerHTML = `
        <div class="alert alert-warning alert-dismissible fade show" role="alert">
                        Maksimum dosya boyutu 30 MB'dır.
                    </div>`
    } else {
        getBase64(file)
    }
}

function getBase64(file) {
    var reader = new FileReader()
    reader.readAsDataURL(file)

    reader.onload = function () {
        chatSocket.send(JSON.stringify({
            "file_type": "file",
            "message": reader.result,
            'username': userName,
            'room': roomName, 'profile': profile
        }))
    }
}


document.getElementById('hiddenImageInput').addEventListener('change', handleImageSelect, false)

function handleImageSelect(event) {
    var image = document.getElementById('hiddenImageInput').files[0];
    if (image.size > 20971521) {
        alertWrapper.innerHTML = `
        <div class="alert alert-warning alert-dismissible fade show" role="alert">
                        Maksimum resim boyutu 20 MB'dır.
                    </div>`
    } else {
        getBaseImage64(image)
    }
}

function getBaseImage64(image) {
    var reader = new FileReader()
    reader.readAsDataURL(image)

    reader.onload = function () {
        chatSocket.send(JSON.stringify({
            "file_type": "image",
            "message": reader.result,
            'username': userName,
            'room': roomName,
            'profile': profile
        }))
    }
}

document.getElementById('hiddenVideoInput').addEventListener('change', handleVideoSelect, false)

function handleVideoSelect(event) {
    var video = document.getElementById('hiddenVideoInput').files[0];
    if (video.size > 52428801) {
        alertWrapper.innerHTML = `
        <div class="alert alert-warning alert-dismissible fade show" role="alert">
                        Maksimum video boyutu 50 MB'dır.
                    </div>`
    } else {


        getBaseVideo64(video)
    }

}

function getBaseVideo64(video) {
    var reader = new FileReader()
    reader.readAsDataURL(video)

    reader.onload = function () {
        chatSocket.send(JSON.stringify({
            "file_type": "video",
            "message": reader.result,
            'username': userName,
            'room': roomName,
            'profile': profile
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
            'room': roomName,
            'profile': profile
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

    let profile_photo;

    if (data.profile === null) {
        profile_photo = '/static/img/profile/empty_profile.png'
    } else {
        profile_photo = data.profile;
    }


    if (message_type === 'text') {
        if (data.message) {
            let html = `
                            <div class="chat-msg">
                                <div class="chat-msg-profile">
                                    <div class="chat-msg-date">${datetime}</div>
                                </div>
                                <div class="chat-msg-content">
                                    <div class="chat-msg-text">
                                    <div class="chat-msg-user">
                                        <img src="${profile_photo}" alt="User"
                                                     class="user_profile_photo">
                                            <p>${data.username}</p>
                                            <div class="dropdown message-detail">
                                                        <button class="btn" type="button"
                                                                data-bs-toggle="dropdown" aria-expanded="false">
                                                            <i class="bi bi-three-dots-vertical"></i>
                                                        </button>
                                                        <ul class="dropdown-menu">
                                                            <li><a class="dropdown-item" href="#">Yanıtla</a></li>
                                                            <li><a class="dropdown-item add-fovourite"
                                                                   data-favourite-target="/favorilere-ekle/${roomID}/${data.id}/"
                                                                   data-message-id="${data.id}" href="#">Favori
                                                                Mesajlarına Ekle</a>
                                                            </li>
                                                            <li><a class="dropdown-item" href="#">Kötüye Kullanım
                                                                Bildir</a></li>
                                                        </ul>
                                                    </div>
                                    </div>
                                    
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
                                        <div class="chat-msg-user">
                                        <img src="${profile_photo}" alt="User"
                                                     class="user_profile_photo">
                                            <p>${data.username}</p>
                                            <div class="dropdown message-detail">
                                                        <button class="btn" type="button"
                                                                data-bs-toggle="dropdown" aria-expanded="false">
                                                            <i class="bi bi-three-dots-vertical"></i>
                                                        </button>
                                                        <ul class="dropdown-menu">
                                                            <li><a class="dropdown-item" href="#">Yanıtla</a></li>
                                                            <li><a class="dropdown-item add-fovourite"
                                                                   data-favourite-target="/favorilere-ekle/${roomID}/${data.id}/"
                                                                   data-message-id="${data.id}" href="#">Favori
                                                                Mesajlarına Ekle</a>
                                                            </li>
                                                            <li><a class="dropdown-item" href="#">Kötüye Kullanım
                                                                Bildir</a></li>
                                                        </ul>
                                                    </div>
                                    </div>
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
                                        <div class="chat-msg-user">
                                        <img src="${profile_photo}" alt="User"
                                                     class="user_profile_photo">
                                            <p>${data.username}</p>
                                            <div class="dropdown message-detail">
                                                        <button class="btn" type="button"
                                                                data-bs-toggle="dropdown" aria-expanded="false">
                                                            <i class="bi bi-three-dots-vertical"></i>
                                                        </button>
                                                        <ul class="dropdown-menu">
                                                            <li><a class="dropdown-item" href="#">Yanıtla</a></li>
                                                            <li><a class="dropdown-item add-fovourite"
                                                                   data-favourite-target="/favorilere-ekle/${roomID}/${data.id}/"
                                                                   data-message-id="${data.id}" href="#">Favori
                                                                Mesajlarına Ekle</a>
                                                            </li>
                                                            <li><a class="dropdown-item" href="#">Kötüye Kullanım
                                                                Bildir</a></li>
                                                        </ul>
                                                    </div>
                                    </div>
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
    } else if (message_type === 'video') {
        if (data.message) {
            let html = `
                            <div class="chat-msg">
                                <div class="chat-msg-profile">
                                    <div class="chat-msg-date">${datetime}</div>
                                </div>
                                <div class="chat-msg-content">
                                    <div class="chat-msg-text">
                                        <div class="chat-msg-user">
                                        <img src="${profile_photo}" alt="User"
                                                     class="user_profile_photo">
                                            <p>${data.username}</p>
                                            <div class="dropdown message-detail">
                                                        <button class="btn" type="button"
                                                                data-bs-toggle="dropdown" aria-expanded="false">
                                                            <i class="bi bi-three-dots-vertical"></i>
                                                        </button>
                                                        <ul class="dropdown-menu">
                                                            <li><a class="dropdown-item" href="#">Yanıtla</a></li>
                                                            <li><a class="dropdown-item add-fovourite"
                                                                   data-favourite-target="/favorilere-ekle/${roomID}/${data.id}/"
                                                                   data-message-id="${data.id}" href="#">Favori
                                                                Mesajlarına Ekle</a>
                                                            </li>
                                                            <li><a class="dropdown-item" href="#">Kötüye Kullanım
                                                                Bildir</a></li>
                                                        </ul>
                                                    </div>
                                    </div>
                                     
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
    } else if (message_type === 'audio') {
        if (data.message) {
            let html = `
                            <div class="chat-msg">
                                <div class="chat-msg-profile">
                                    <div class="chat-msg-date">${datetime}</div>
                                </div>
                                <div class="chat-msg-content">
                                    <div class="chat-msg-text">
                                        <div class="chat-msg-user">
                                        <img src="${profile_photo}" alt="User"
                                                     class="user_profile_photo">
                                            <p>${data.username}</p>
                                            <div class="dropdown message-detail">
                                                        <button class="btn" type="button"
                                                                data-bs-toggle="dropdown" aria-expanded="false">
                                                            <i class="bi bi-three-dots-vertical"></i>
                                                        </button>
                                                        <ul class="dropdown-menu">
                                                            <li><a class="dropdown-item" href="#">Yanıtla</a></li>
                                                            <li><a class="dropdown-item add-fovourite"
                                                                   data-favourite-target="/favorilere-ekle/${roomID}/${data.id}/"
                                                                   data-message-id="${data.id}" href="#">Favori
                                                                Mesajlarına Ekle</a>
                                                            </li>
                                                            <li><a class="dropdown-item" href="#">Kötüye Kullanım
                                                                Bildir</a></li>
                                                        </ul>
                                                    </div>
                                    </div>
                                     
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
    } else if (message_type === 'record') {
        if (data.message) {
            let html = `
                            <div class="chat-msg">
                                <div class="chat-msg-profile">
                                    <div class="chat-msg-date">${datetime}</div>
                                </div>
                                <div class="chat-msg-content">
                                    <div class="chat-msg-text">
                                        <div class="chat-msg-user">
                                        <img src="${profile_photo}" alt="User"
                                                     class="user_profile_photo">
                                            <p>${data.username}</p>
                                            <div class="dropdown message-detail">
                                                        <button class="btn" type="button"
                                                                data-bs-toggle="dropdown" aria-expanded="false">
                                                            <i class="bi bi-three-dots-vertical"></i>
                                                        </button>
                                                        <ul class="dropdown-menu">
                                                            <li><a class="dropdown-item" href="#">Yanıtla</a></li>
                                                            <li><a class="dropdown-item add-fovourite"
                                                                   data-favourite-target="/favorilere-ekle/${roomID}/${data.id}/"
                                                                   data-message-id="${data.id}" href="#">Favori
                                                                Mesajlarına Ekle</a>
                                                            </li>
                                                            <li><a class="dropdown-item" href="#">Kötüye Kullanım
                                                                Bildir</a></li>
                                                        </ul>
                                                    </div>
                                    </div>
                                     
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
        'room': roomName,
        'profile': profile
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

const popUpImage = document.querySelector('.popup-image');

if (popUpImage) {
    document.querySelector('.popup-image span').onclick = () => {
        document.querySelector('.popup-image').style.display = 'none';
    }
}


navigator.mediaDevices.getUserMedia({audio: true})
    .then(function (mediaStreamObject) {
        const startStop = document.getElementById("chat-microfon");
        const startStopIcon = document.querySelector('.bi-mic-fill');
        const mediaRecorder = new MediaRecorder(mediaStreamObject)
        startStop.addEventListener('click', function (e) {
            if (isRecord) {
                startStopIcon.style = ""
                isRecord = false
                mediaRecorder.stop()
            } else {
                startStopIcon.style = "color:red"
                isRecord = true
                mediaRecorder.start()
            }
        })


        mediaRecorder.ondataavailable = function (e) {
            dataArray.push(e.data)
        }

        var dataArray = []

        mediaRecorder.onstop = function (e) {
            let auidodata = new Blob(dataArray, {'type': 'audio/mp3'})
            dataArray = []
            getBaseRecord64(auidodata)
        }


    });

function getBaseRecord64(auidodata) {
    var reader = new FileReader()
    reader.readAsDataURL(auidodata)

    reader.onload = function () {
        chatSocket.send(JSON.stringify({
            "file_type": "record",
            "message": reader.result,
            'username': userName,
            'room': roomName,
            'profile': profile
        }))
    }
}

const spinnerBox = document.getElementById('spinner-box');
const loadBtn = document.getElementById('loadMore');
const loadBox = document.querySelector('.load-more-wrapper');
const chatMessage = document.querySelector('#chat-message');


(function ($) {

    $("#loadMore").click(function () {
        var directspage = document.getElementById('page_number');
        var page_number = parseInt(directspage.value);

        $.ajax({
            url: `/server/json/${roomName}/`,
            data: {
                'directspage': page_number,
                'csrfmiddlewaretoken': window.CSRF_TOKEN
            },
            cache: false,
            type: 'post',
            success: function (data) {
                if (data.empty === true) {
                    $(loadBtn).hide();
                } else {
                    box.scrollTop = box.scrollHeight;
                    const messages = data
                    setTimeout(() => {
                        messages.map(message => {
                            spinnerBox.classList.add('not-visible')

                            var dateOptions = {

                                year: 'numeric',
                                month: 'long',
                                day: 'numeric',
                                hour: 'numeric',
                                minute: 'numeric',
                                hour12: false,
                            };
                            var datetime = new Date(message.date_added).toLocaleString('tr', dateOptions);

                            const message_type = message.file_type

                            let profile_photo;

                            if (message.user__userprofile__profile_photo === null) {
                                profile_photo = '/static/img/profile/empty_profile.png'
                            } else {
                                profile_photo = `/media/${message.user__userprofile__profile_photo}`;
                            }

                            if (message_type === 'text') {

                                let html = `
                            <div class="chat-msg">
                                <div class="chat-msg-profile">
                                    <div class="chat-msg-date">${datetime}</div>
                                </div>
                                <div class="chat-msg-content">
                                    <div class="chat-msg-text">
                                    <div class="chat-msg-user">
                                        <img src="${profile_photo}" alt="User"
                                                     class="user_profile_photo">
                                           <p>${message.user__username}</p>
                                           <div class="dropdown message-detail">
                                                        <button class="btn" type="button"
                                                                data-bs-toggle="dropdown" aria-expanded="false">
                                                            <i class="bi bi-three-dots-vertical"></i>
                                                        </button>
                                                        <ul class="dropdown-menu">
                                                            <li><a class="dropdown-item" href="#">Yanıtla</a></li>
                                                            <li><a class="dropdown-item add-fovourite"
                                                                   data-message-id="${message.id}" href="/server/favorilere-ekle/${roomID}/${message.id}/">Favori
                                                                Mesajlarına Ekle</a>
                                                            </li>
                                                            <li><a class="dropdown-item" href="#">Kötüye Kullanım
                                                                Bildir</a></li>
                                                        </ul>
                                                    </div>
                                    </div>
                                  
                                        <p>${message.content}</p>
                                    </div>
                                </div>
                            </div>
                       
                `
                                document.querySelector('.chat-old-msg').innerHTML += html;
                                box.scrollTop = box.scrollHeight;

                            } else if (message_type === 'file') {
                                if (message.message) {
                                    let html = `
                            <div class="chat-msg">
                                <div class="chat-msg-profile">
                                    <div class="chat-msg-date">${datetime}</div>
                                </div>
                                <div class="chat-msg-content">
                                    <div class="chat-msg-text">
                                        <div class="chat-msg-user">
                                        <img src="${profile_photo}" alt="User"
                                                     class="user_profile_photo">
                                           <p>${message.user__username}</p>
                                    </div>
                                        <a href="${message.message}" download="Forum Ekpser">
                                        <img src="/static/img/server/file.png" alt="File">
</a>
                                    </div>
                                </div>
                            </div>
                       
                `
                                    chatMessage.innerHTML += html;
                                    box.scrollTop = box.scrollHeight;

                                } else {
                                    console.log("Boş mesaj")
                                }
                            } else if (message_type === 'image') {
                                if (message.message) {
                                    let html = `
                            <div class="chat-msg">
                                <div class="chat-msg-profile">
                                    <div class="chat-msg-date">${datetime}</div>
                                </div>
                                <div class="chat-msg-content">
                                    <div class="chat-msg-text">
                                        <div class="chat-msg-user">
                                        <img src="${profile_photo}" alt="User"
                                                     class="user_profile_photo">
                                           <p>${message.user__username}</p>
                                    </div>
                                        <img src="${data.message}" alt="Image">
                                    </div>
                                </div>
                            </div>
                       
                `
                                    chatMessage.innerHTML += html;
                                    box.scrollTop = box.scrollHeight;

                                } else {
                                    console.log("Boş mesaj")
                                }
                            } else if (message_type === 'video') {
                                if (message.message) {
                                    let html = `
                            <div class="chat-msg">
                                <div class="chat-msg-profile">
                                    <div class="chat-msg-date">${datetime}</div>
                                </div>
                                <div class="chat-msg-content">
                                    <div class="chat-msg-text">
                                        <div class="chat-msg-user">
                                        <img src="${profile_photo}" alt="User"
                                                     class="user_profile_photo">
                                           <p>${message.user__username}</p>
                                    </div>
                                     
                                        <video controls width="250" height="250">
                                        <source src="${message.message}">
                                        </video>
                                    </div>
                                </div>
                            </div>
                `
                                    chatMessage.innerHTML += html;
                                    box.scrollTop = box.scrollHeight;

                                } else {
                                    console.log("Boş mesaj")
                                }
                            } else if (message_type === 'audio') {
                                if (message.message) {
                                    let html = `
                            <div class="chat-msg">
                                <div class="chat-msg-profile">
                                    <div class="chat-msg-date">${datetime}</div>
                                </div>
                                <div class="chat-msg-content">
                                    <div class="chat-msg-text">
                                        <div class="chat-msg-user">
                                        <img src="${profile_photo}" alt="User"
                                                     class="user_profile_photo">
                                           <p>${message.user__username}</p>
                                    </div>
                                        <audio controls style="width: 250px;">
                                        <source src="${message.message}">
                                        </audio>
                                    </div>
                                </div>
                            </div>
                       
                `

                                    chatMessage.innerHTML += html;
                                    box.scrollTop = box.scrollHeight;

                                } else {
                                    console.log("Boş mesaj")
                                }
                            } else if (message_type === 'record') {
                                if (data.message) {
                                    let html = `
                            <div class="chat-msg">
                                <div class="chat-msg-profile">
                                    <div class="chat-msg-date">${datetime}</div>
                                </div>
                                <div class="chat-msg-content">
                                    <div class="chat-msg-text">
                                        <div class="chat-msg-user">
                                        <img src="${profile_photo}" alt="User"
                                                     class="user_profile_photo">
                                           <p>${message.user__username}</p>
                                    </div>
                                        <audio controls style="width: 250px;">
                                        <source src="${message.message}">
                                        </audio>
                                    </div>
                                </div>
                            </div>
                       
                `
                                    chatMessage.innerHTML += html;
                                    box.scrollTop = box.scrollHeight;
                                } else {
                                    console.log("Boş mesaj")
                                }
                            }

                        })
                    }, 500)
                }
                page_number = page_number + 15;
                $("#page_number").attr('value', page_number);
            }
        });
        return false;
    });


    // end of document ready
}(jQuery)); // end of jQuery name space


