
const d = new Date();
// let minutes = d.getMinutes();
let hours = d.getHours();
let minutes = (d.getMinutes() < 10 ? '0' : '') + d.getMinutes();
document.getElementById("todayDate").innerHTML = "Date: "+d.toISOString().substring(0, 10);
document.getElementById("todayTime").innerHTML = `Time: ${hours}:${minutes}`;
// Display previous inputs below the submit button

const manualSection = document.getElementById("manualInput");
// const form = document.getElementById("mNappy");
// const clearForm = form.addEventListener("submit", resetData);



function activity(clicked){
    const currentTime = `${hours}:${minutes}`
    console.log(currentTime);
    let input =  'Automatic input';
    if (clicked === "manualLog"){
        input = "Manual Input";
        manualActivities(clicked)
        if (manualSection.style.display === "" ||  manualSection.style.display === "none"){
            manualSection.style.display = "block";
        } else {
            manualSection.style.display = "none";
        }   
    } else {
        autoInput(clicked, input)
    }
}


function manualActivities(submitted){
    if (submitted === "mNappy"){
        manualNappyActivity(submitted)
        time = document.getElementById("pottyTime").value;
        console.log("potty path "+time);
        // test()
        // document.getElementById("mNappy").reset();
        // doesn't allow input it keeps refreshing
    } else if( submitted === "mFood"){
        time = document.getElementById("foodTime").value;
        console.log("food time " + time);
        // document.getElementById(`${submitted}`).reset();
    }else if( submitted === "mSleep"){
        let stime = document.getElementById("sTime").value;
        let ftime = document.getElementById("fTime").value;
        console.log("sleep " +stime+" or "+ftime);
        // document.getElementById(`${submitted}`).reset();
    }
}

function test(){
    // why did this reset the whole thing?
    var frm = document.getElementById('mNappy');
    console.log(frm.submit())
     // Submit the form
    setInterval(frm.reset(), 5000);  
}


function manualNappyActivity(submitted){
    const one = document.querySelector("#no1").checked;
    const noTwo = document.querySelector("#no2").checked;
    console.log(one+" "+noTwo)
    // returns true/false can be added directly to file like that
}


    
    
function autoInput(activity, input){
    if (activity === "food"){
        console.log(`input is ${input} and ${activity}`);
    } else if (activity === "num1" || activity === "num2"){
        console.log(`input is ${input} and ${activity}`);
    } else if (activity=== "napStart" || activity === "napFinish"){
        console.log(`input is ${input} and ${activity}`);
    }
}

