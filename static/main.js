
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
// let checkbox = otherCheckbox.addEventListener("change", () => {

function activity(clicked){
    const currentTime = `${hours}:${minutes}`
    console.log(currentTime);
    let input =  'Automatic input';
    if (clicked === "manualLog"){
        input = "Manual Input";
        manualClick(clicked)
        if (manualSection.style.display === "" ||  manualSection.style.display === "none"){
        manualSection.style.display = "block";
        } else {
        manualSection.style.display = "none";
        }
        manualInput(clicked, input)    
    } else {
        autoInput(clicked, input)
    }
}

function manualClick(submitted){
    console.log(submitted);
}



function manualInput(activity, input){
    const one = document.querySelector("#no1");
    const noTwo = document.querySelector("#no2");
    // get a class for the manual clocks and use to get any of it when added understand how the event listener below works
    console.log(activity);
    one.addEventListener("change", (event) => {
        console.log(` it's ${event.target.value}`)
    });
    noTwo.addEventListener("change", (event) => {
        console.log(` it's ${event.target.value}`)
    });
}



    // if (activity ==="food"){
    //     let x = document.getElementById("foodTime").value
    //     console.log(x)
    // }
//     console.log(`input is ${input} and ${activity}`);
// }


function autoInput(activity, input){
    if (activity === "food"){
        console.log(`input is ${input} and ${activity}`);
    } else if (activity === "num1" || activity === "num2"){
        console.log(`input is ${input} and ${activity}`);
    } else if (activity=== "napStart" || activity === "napFinish"){
        console.log(`input is ${input} and ${activity}`);
    }
}