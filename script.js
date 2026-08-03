// ================= DARK MODE =================

function toggleDarkMode(){

    document.body.classList.toggle("dark-mode");

    localStorage.setItem(
        "darkMode",
        document.body.classList.contains("dark-mode")
    );

}


window.onload = function(){

    if(localStorage.getItem("darkMode") === "true"){

        document.body.classList.add("dark-mode");

    }

};



// ================= SEARCH TRIPS =================

function searchTrips(){

    let input = document
    .getElementById("searchInput")
    .value
    .toLowerCase()
    .trim();


    let trips = document.querySelectorAll(".trip-card");


    trips.forEach(function(trip){


        let destination = trip
        .querySelector(".destination")
        .textContent
        .toLowerCase();


        if(destination.includes(input)){

            trip.style.display = "block";

        }
        else{

            trip.style.display = "none";

        }


    });

}



// ================= SAVE PLAN AS IMAGE =================

function shareImage(){


    let plan = document.getElementById("currentPlan");


    if(!plan){

        alert("Generate a plan first");

        return;

    }


    html2canvas(plan).then(function(canvas){


        let link = document.createElement("a");


        link.download = "Trip_Plan.png";


        link.href = canvas.toDataURL();


        link.click();


    });


}



// ================= WEATHER =================

function getWeather(){


    let city = document.getElementById("city").value;


    fetch("/weather/" + city)


    .then(response => response.json())


    .then(data => {


        if(data.error){


            document.getElementById("weatherResult").innerHTML =
            "Weather not available";


        }

        else{


            document.getElementById("weatherResult").innerHTML = `

            <h3>${data.city}</h3>

            <p>🌡 Temperature: ${data.temperature}°C</p>

            <p>☁ Condition: ${data.condition}</p>

            <p>💧 Humidity: ${data.humidity}%</p>

            `;


        }


    });


}