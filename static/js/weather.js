function GetInfo() {
    var newName = document.getElementById("cityInput");
    var cityName = document.querySelector('.weather-city').textContent;

    fetch(`https://api.openweathermap.org/data/2.5/forecast?q=${cityName}&appid=37a3b97ba41dfc38e67661578a88798d`)
        .then(response => response.json())
        .then(data => {
            //Getting the min and max values for each day
            for (i = 0; i < 5; i++) {
                document.getElementById("day" + (i + 1) + "Min").innerHTML =Number(data.list[i].main.temp_min - 273.15).toFixed(1) + "°";
            }

            for (i = 0; i < 5; i++) {
                document.getElementById("day" + (i + 1) + "Max").innerHTML = Number(data.list[i].main.temp_max - 273.15).toFixed(1) + "°";
            }
            //------------------------------------------------------------

            //Getting Weather Icons
            for (i = 0; i < 5; i++) {
                document.getElementById("img" + (i + 1)).src = "http://openweathermap.org/img/wn/" +
                    data.list[i].weather[0].icon
                    + ".png";
            }
            //------------------------------------------------------------
        })

        .catch(err => alert("Something Went Wrong: Try Checking Your Internet Coneciton"))
}

function DefaultScreen() {
    document.getElementById("cityInput").defaultValue = "London";
    GetInfo();
}


//Getting and displaying the text for the upcoming five days of the week
var d = new Date();
var weekday = ["Pazar", "Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi",];

//Function to get the correct integer for the index of the days array
function CheckDay(day) {
    if (day + d.getDay() > 6) {
        return day + d.getDay() - 7;
    } else {
        return day + d.getDay();
    }
}

for (i = 0; i < 5; i++) {
    document.getElementById("day" + (i + 1)).innerHTML = weekday[CheckDay(i)];
}

//------------------------------------------------------------