const favouriteBtns = document.querySelectorAll('.add-fovourite');
const favouriteList = document.getElementById("favoriteList");

$(document).ready(function () {
    favouriteBtns.forEach(btn => {
        $(btn).click(function (e) {
            e.preventDefault();
            //Favorilere Ekleme İşlemi
            $.ajax({
                url: btn.getAttribute('href'),
                type: 'GET',
                data: {
                    'room_id': roomID,
                    'message_id': btn.getAttribute('data-message-id'),
                    'csrfmiddlewaretoken': window.CSRF_TOKEN,
                },
                success: function (response) {
                    const data = response.data
                    let li_item;
                    li_item = `
                                    <li>
                                        <a href="#" data-bs-toggle="modal" data-bs-target="#favourite-${data[0].id}"
                                           class="survey-link"
                                           role="button">
                                            <span>${data[0].message__content}</span>
                                        </a>
                                        <div class="modal fade" id="favourite-${data[0].id}" tabindex="-1"
                                             aria-labelledby="favourite-${data[0].id}-label" aria-hidden="true">
                                            <div class="modal-dialog">
                                                <div class="modal-content">
                                                    <div class="modal-header">
                                                        <h5 class="modal-title" id="favourite-${data[0].id}-label">Yazar: ${data[0].message__user__username}</h5>
                                                        <button type="button" class="btn-close" data-bs-dismiss="modal"
                                                                aria-label="Close"></button>
                                                    </div>
                                                    <div class="modal-body">
                                                        ${data[0].message__content}
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </li>
                    `
                    favouriteList.innerHTML += li_item
                }
            })
        })
    })
});