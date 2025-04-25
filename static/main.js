
//Filter activity results on main.html from a dropdown
document.addEventListener("DOMContentLoaded", function () {
    const filterSelect = document.getElementById("activityFilter");
    const table = document.getElementById("activityTable");

    // Check that both the dropdown and table exist before doing anything
    if (filterSelect && table) {
        filterSelect.addEventListener("change", function () {
            const selectedActivity = this.value.toLowerCase();
            const rows = table.getElementsByTagName("tr");

            for (let i = 1; i < rows.length; i++) {  // skip header row
                const activityCell = rows[i].getElementsByTagName("td")[2];  // 3rd column = activity
                if (activityCell) {
                    const activity = activityCell.textContent.trim().toLowerCase();
                    rows[i].style.display =
                        selectedActivity === "all" || activity === selectedActivity ? "" : "none";
                }
            }
        });
    } else {
        console.log(" No filter dropdown or table found — skipping filter logic.");
    }
});


//On the index.html display date & time and show/hide manual block
const d = new Date();
let hours = d.getHours();
let minutes = (d.getMinutes() < 10 ? '0' : '') + d.getMinutes();
document.getElementById("todayDate").innerHTML = "Date: "+d.toISOString().substring(0, 10);
document.getElementById("todayTime").innerHTML = `Time: ${hours}:${minutes}`;


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

