
const d = new Date();
let minutes = d.getMinutes();
let hours = d.getHours();
document.getElementById("todayDate").innerHTML = "Date: "+d.toISOString().substring(0, 10);
document.getElementById("todayTime").innerHTML = `Time: ${hours}:${minutes}`;
// document.getElementById("foodTime").value = `${hours}:${minutes}`;
// document.getElementById("sTime").value = `${hours}:${minutes}`;
// document.getElementById("fTime").value = `${hours}:${minutes}`;
// Display previous inputs below the submit button

// end of every day it adds a line between the days
// get current time from the innitual block and then collect times from manual
const manualSection = document.getElementById("manualInput");

function activity(clicked){
    const currentTime = `${hours}:${minutes}`
    if ((clicked === "manualLog" && manualSection.style.display === "") || (clicked === "manualLog" && manualSection.style.display === "none")){
        manualSection.style.display = "block";
    } else {
        manualSection.style.display = "none";
    }

    if (clicked === "mNappy" || clicked === "mFood" || clicked === 'mSleep'){
        console.log(logData('manual input'))
    } else if (clicked === "food"){
        console.log(logData('food input'))
    } else if (clicked === "num1" || clicked === "num2"){
        console.log(logData('nappy input'))
    } else if (clicked === "napStart" || clicked === "napFinish"){
        console.log(logData('sleep input'))
    }
}

