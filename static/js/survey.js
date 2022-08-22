let optionsBtn = document.querySelectorAll('.survey-option');
let surveyWrapper = document.querySelector('.survey-wrapper');
let surveyLink = document.querySelectorAll('.survey-link');
let closeModal = document.querySelectorAll('.btn-close');
let domain = "127.0.0.1:8000"


$(document).ready(function () {

    var current_fs, next_fs, previous_fs; //fieldsets
    var opacity;
    var current = 1;
    var steps = $("fieldset").length;

    setProgressBar(current);

    $(".next").click(function () {

        current_fs = $(this).parent();
        next_fs = $(this).parent().next();

//Add Class Active
        $("#progressbar li").eq($("fieldset").index(next_fs)).addClass("active");

//show the next fieldset
        next_fs.show();
//hide the current fieldset with style
        current_fs.animate({opacity: 0}, {
            step: function (now) {
// for making fielset appear animation
                opacity = 1 - now;

                current_fs.css({
                    'display': 'none',
                    'position': 'relative'
                });
                next_fs.css({'opacity': opacity});
            },
            duration: 500
        });
        setProgressBar(++current);
    });

    $(".previous").click(function () {

        current_fs = $(this).parent();
        previous_fs = $(this).parent().prev();

//Remove class active
        $("#progressbar li").eq($("fieldset").index(current_fs)).removeClass("active");

//show the previous fieldset
        previous_fs.show();

//hide the current fieldset with style
        current_fs.animate({opacity: 0}, {
            step: function (now) {
// for making fielset appear animation
                opacity = 1 - now;

                current_fs.css({
                    'display': 'none',
                    'position': 'relative'
                });
                previous_fs.css({'opacity': opacity});
            },
            duration: 500
        });
        setProgressBar(--current);
    });

    function setProgressBar(curStep) {
        var percent = parseFloat(100 / steps) * curStep;
        percent = percent.toFixed();
        $(".progress-bar")
            .css("width", percent + "%")
    }

    $(".submit").click(function () {
        return false;
    })

});


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


