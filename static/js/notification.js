$(document).ready(function () {
    $('.notification .icon_wrap').click(function () {
        $(".notification-item").toggleClass('active-click')
        $(".notification_dd").slideToggle();
        $(".profile_dd").css('display', 'none');
        $(".user-item").removeClass('active-click');
        $(".profile_user").css('color', '#ffffff');
    });

    $('.profile .profile_wrap').click(function () {
        $(".profile_dd").slideToggle();
        $(".notification_dd").css('display', 'none');
        $(".profile_user").css('color', '#1d1d1d');
        $(".user-item").toggleClass('active-click');
        $(".notification-item").removeClass('active-click');

        if (!$('.user-item').hasClass('active-click')) {
           $(".profile_user").css('color', '#ffffff');
        }
    })

})