let optionsBtn = document.querySelectorAll('.survey-option');
let surveyWrapper = document.querySelector('.survey-wrapper');
let surveyLink = document.querySelectorAll('.survey-link');
let closeModal = document.querySelectorAll('.btn-close');
let domain = "127.0.0.1:8000"


$(document).ready(function () {

    optionsBtn.forEach(option => {
        $(option).click(function (e) {
            e.preventDefault();
            // Ankete oy verme işlemi
            $.ajax({
                url: option.getAttribute('href'),
                type: 'GET',
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
                            success: function (response) {
                                surveyWrapper.innerHTML = '';
                                const options = response.data_option
                                options.map(opt => {
                                    let html = `
                                        <div class="survey-result">
                                        <h5>Toplam Oy: ${opt.countSurveyVote}</h5>
                                                                            <p>${opt.options}
                                                                                -> ${opt.countOptionVote} Oy</p>
                                                                            <div class="progress">
                                                                                <div class="progress-bar"
                                                                                     role="progressbar"
                                                                                     aria-label="Example with label"
                                                                                     style="width: ${opt.rateVate}%;"
                                                                                     aria-valuenow="{{ o.rateVate }}%"
                                                                                     aria-valuemin="0"
                                                                                     aria-valuemax="100">${opt.rateVate}%
                                                                                </div>
                                                                            </div>
                                                                        </div>
                                                                        <hr>
                                    `
                                    surveyWrapper.innerHTML += html;
                                })
                            }
                        })
                    }
                },
                error(err) {
                    console.log(url)
                }
            });
        });
    });

})


