
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


function filterTableByActivity() {
    const filter = document.getElementById("activityFilter").value.toLowerCase();
    const table = document.getElementById("activityTable");
    const rows = table.getElementsByTagName("tr");

    for (let i = 1; i < rows.length; i++) { // start from 1 to skip header
        const activityCell = rows[i].getElementsByTagName("td")[2]; // 3rd column = Activity Type
        if (activityCell) {
            const activityText = activityCell.textContent || activityCell.innerText;
            if (filter === "all" || activityText.toLowerCase() === filter) {
                rows[i].style.display = "";
            } else {
                rows[i].style.display = "none";
            }
        }
    }
}