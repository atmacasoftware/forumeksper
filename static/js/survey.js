let optionsBtn = document.querySelectorAll('.survey-option');


$(document).ready(function () {
    optionsBtn.forEach(option => {
        $(option).click(function (e) {
            e.preventDefault();
            $.ajax({
                url: option.getAttribute('href'),
                method: 'POST',
                data: {
                    'csrfmiddlewaretoken': window.CSRF_TOKEN,
                },
                success: function (response) {
                    console.log(response)
                    if (response.data.ok === 'ok') {
                        option.innerHTML = 'Oy Verildi'
                    }
                }
            });
        });
    });
});
