
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
// use the stopwatch from object lesson to calculate sleep duration
const manualSection = document.getElementById("manualInput");

function activity(clicked){
    const currentTime = `${hours}:${minutes}`
    if ((clicked === "manualLog" && manualSection.style.display === "") || (clicked === "manualLog" && manualSection.style.display === "none")){
        manualSection.style.display = "block";
    } else {
        manualSection.style.display = "none";
    }

    if (clicked === "food" || clicked === "mFood"){
        console.log('food input')
    } else if (clicked === "num1" || clicked === "num2" || clicked === "mNappy"){
        console.log('nappy input')
    } else if (clicked === "napStart" || clicked === "napFinish" || clicked === 'mSleep'){
        console.log('sleep input')
    }
}