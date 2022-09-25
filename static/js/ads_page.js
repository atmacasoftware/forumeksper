$(document).ready(function () {
    $("#adsSelect").hide();
    $("#adsNews").hide();
    $("#isPrivateCheck").hide();
    let selectCategory = $('#selectCategory');
    selectCategory.attr('required', false)
    let newsTitle = $('#title');
    newsTitle.attr('required', false)
    let isPrivate = $('#isPrivateCheckInput');
    isPrivate.attr('required', false)
    let messageArea = $('#messageAreaLabel');

    $('#adsType').on('change', function () {
        let select_value = $("#adsType option:selected").text()
        if (select_value === "Reklam") {
            $("#adsSelect").show()
            $("#adsNews").hide()
            $("#isPrivateCheck").hide();
            selectCategory.attr('required', true)
            newsTitle.attr('required', false)
            isPrivate.attr('required', false)
            messageArea.html("Mesaj *")
        } else if (select_value === "Haber") {
            $("#adsSelect").hide()
            $("#adsNews").show()
            $("#isPrivateCheck").show();
            selectCategory.attr('required', false)
            newsTitle.attr('required', true)
            messageArea.html("Haber İçeriği *")
            isPrivate.attr('required', false)
        } else {
            $("#adsSelect").hide()
            $("#adsNews").hide()
            $("#isPrivateCheck").show();
            messageArea.html("Mesaj")
            selectCategory.attr('required', false)
            newsTitle.attr('required', false)
            isPrivate.attr('required', false)
        }
    });
    $(":input").inputmask();

    $("#phone").inputmask({"mask": "(999) 999-9999"});


})


