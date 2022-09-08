function displayTime() {
    var datetime = new Date();
    var hrs = datetime.getHours();
    var min = datetime.getMinutes();

    if (hrs < 10){
        document.getElementById("hours").innerHTML = "0"+hrs;
    }else{
        document.getElementById("hours").innerHTML = hrs;
    }

    if(min < 10){
        document.getElementById("minutes").innerHTML = "0"+min;
    }else{
        document.getElementById("minutes").innerHTML = min;
    }

}

setInterval(displayTime, 10);