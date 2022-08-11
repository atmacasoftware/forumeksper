// Server Page
const uploadPictureBtn = document.getElementById("uploadPictureBtn");
const pictureScope = document.querySelector(".upload_profile_picture img");

uploadPictureBtn.addEventListener("mouseover", function () {
    pictureScope.setAttribute("style", "opacity:0.4")
})

uploadPictureBtn.addEventListener("mouseout", function () {
    pictureScope.setAttribute("style", "opacity:1")
})

const uploadBannerBtn = document.getElementById("uploadBannerBtn");
const bannerScope = document.querySelector(".upload_banner img");

uploadBannerBtn.addEventListener("mouseover", function () {
    bannerScope.setAttribute("style", "opacity:0.4")
})

uploadBannerBtn.addEventListener("mouseout", function () {
    bannerScope.setAttribute("style", "opacity:1")
})


const pictureDiv = document.querySelector(".upload_profile_picture");
const picture = document.querySelector('#picture');
const filePicture = document.querySelector("#image");

filePicture.addEventListener('change', function () {
    const chosedfilepicture = this.files[0];
    if (chosedfilepicture) {
        const reader = new FileReader();
        reader.addEventListener('load', function () {
            picture.setAttribute('src', reader.result);
        })
        reader.readAsDataURL(chosedfilepicture);
    }
})

const bannerDiv = document.querySelector(".upload_banner");
const banner = document.querySelector('#banner_picture');
const fileBanner = document.querySelector("#banner");

fileBanner.addEventListener('change', function () {
    const chosedfilebanner = this.files[0];
    if (chosedfilebanner) {
        const readerBanner = new FileReader();
        readerBanner.addEventListener('load', function () {
            banner.setAttribute('src', readerBanner.result);
        })
        readerBanner.readAsDataURL(chosedfilebanner);
    }
})


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
