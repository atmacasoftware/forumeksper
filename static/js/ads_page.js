$(document).ready(function () {
    $("#adsSelect").hide()
    $("#adsNews").hide()
    let selectCategory = $('#selectCategory');
    selectCategory.attr('required',false)
    let newsTitle = $('#title');
    newsTitle.attr('required',false)
    let messageArea = $('#messageAreaLabel');
    $('#adsType').on('change', function () {
        let select_value = this.value
        if(select_value === "1"){
            $("#adsSelect").show()
            $("#adsNews").hide()
            selectCategory.attr('required',true)
            newsTitle.attr('required',false)
            messageArea.html("Mesaj")
        }else if(select_value === "2"){
            $("#adsSelect").hide()
            $("#adsNews").show()
            selectCategory.attr('required',false)
            newsTitle.attr('required',true)
            messageArea.html("Haber İçeriği")
        } else{
            $("#adsSelect").hide()
            $("#adsNews").hide()
            messageArea.html("Mesaj")
            selectCategory.attr('required',false)
            newsTitle.attr('required',false)
        }
    });
})