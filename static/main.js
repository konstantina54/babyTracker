
const d = new Date();
// let minutes = d.getMinutes();
let hours = d.getHours();
let minutes = (d.getMinutes() < 10 ? '0' : '') + d.getMinutes();
document.getElementById("todayDate").innerHTML = "Date: "+d.toISOString().substring(0, 10);
document.getElementById("todayTime").innerHTML = `Time: ${hours}:${minutes}`;
// Display previous inputs below the submit button

const manualSection = document.getElementById("manualInput");
const autoSection = document.getElementById("autoInput");
// add filters and sorting for the table

function activity(){
    const currentTime = `${hours}:${minutes}`
    console.log(currentTime);
    if (manualSection.style.display === "" ||  manualSection.style.display === "none"){
        manualSection.style.display = "block";
        autoSection.style.display = "none";
    } else {
        manualSection.style.display = "none";
        autoSection.style.display = "block";
     }   
}


function filterTable() {
    let input = document.getElementById("tableFilter");
    let filter = input.value.toLowerCase();
    let table = document.getElementById("activityTable");
    let rows = table.getElementsByTagName("tr");

    for (let i = 0; i < rows.length; i++) {
        let row = rows[i];
        let text = row.textContent || row.innerText;

        if (text.toLowerCase().indexOf(filter) > -1) {
            row.style.display = "";
        } else {
            row.style.display = "none";
        }
    }
}