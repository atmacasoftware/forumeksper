let optionsBtn = document.querySelectorAll('.survey-option');
let surveyWrapper = document.querySelector('.survey-wrapper');


$(document).ready(function () {
    optionsBtn.forEach(option => {
        $(option).click(function (e) {
            e.preventDefault();
            // Ankete oy verme işlemi
            $.ajax({
                url: option.getAttribute('href'),
                method: 'POST',
                data: {
                    'csrfmiddlewaretoken': window.CSRF_TOKEN,
                },
                success: function (response) {
                    if (response.data.ok === 'ok') {
                        option.innerHTML = 'Oy Verildi'

                        // Oy verme sonucu anketin sonuçlarını gösterme

                        $.ajax({
                            url: option.getAttribute('data-target'),
                            method: 'POST',
                            data: {
                                'csrfmiddlewaretoken': window.CSRF_TOKEN,
                            },
                            success: function (response){
                                console.log(response.vote_count)
                                const options = response.data_option
                                options.map(opt => {
                                    console.log(opt)
                                })
                            }
                        })
                    }
                }
            });
        });
    });
});
