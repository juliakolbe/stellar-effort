const lander = document.getElementById("lander20");
const altitudeText = document.getElementById("altitude");
const velocityText = document.getElementById("velocity");
const fuelText = document.getElementById("fuel");
const statusText = document.getElementById("status");
const thrusterbutton = document.getElementById("thrusterButton");
const altitudeAlert = document.getElementById("altitude-Alert");

let landed = false;
let Xposition = 200; 
let leftArrow = false;
let rightArrow = false;

console.log("Script is running!");

document.addEventListener("keydown", (event) => { /* keydown = button pushed */ 
    if (event.key === "ArrowLeft") {
        leftArrow = true;
    }
    if (event.key === "ArrowRight") {
        rightArrow = true;
    }
    if (event.code === "Space" && !landed) {
        sendThrust(1000);
        thrustOn = true; 
        thrusterbutton.classList.add("active");
        thrusterbutton.innerHTML = "Engaged";
    }
});

document.addEventListener("keyup", (event) => { /* keyup = button released */
    if (event.key === "ArrowLeft") {
        leftArrow = false;
        console.log("Key pressed:", event.code);
    }
    if (event.key === "ArrowRight") {
        rightArrow = false;
    }
    if (event.code === "Space") {
        thrustOn = false;
        thrusterbutton.classList.remove("active");
        thrusterbutton.innerHTML = "Inactive";
    }
});

function sendThrust(thrustValue) {
    fetch('/thrust', {
        method: 'POST', 
        headers: { 'Content-Type': 'application/json' }, /* this tells the server that we are sending JSON data */
        body: JSON.stringify({ /* this sends JSON data to the server */
            thrust: thrustValue })/* this is the value of the thrust */
        });
}

setInterval(getLanderState, 100); 

function getLanderState() {
    fetch('/state') /* this asks "server" for stats */
    .then(res => res.json()) /* converts the python's response into JSON format */
    .then(data => {
        updateGUI(data); /* this function will update the GUI with the data */
    });
}

document.addEventListener("keydown", event => {
    if (event.code === "Space" && !landed) {
        sendThrust(1000); /* 1000 is rando number. This sends a request to the server to apply thrust */
        console.log("hitting the space bar, baby")
    }
});

function updateX() {
    if (leftArrow) Xposition -= 2;
    if (rightArrow) Xposition += 2; 
    lander.style.left = `${Xposition}px`;
    requestAnimationFrame(updateX);
}

updateX();

/* this function below pulls from the flask python connection and fetches these values */
function updateGUI(state) {
    const { altitude, velocity, fuel, landed: hasLanded, thrust_status, safe } = state; /* i loooove this, this is so sexy and efficient. so slay.  */

    console.log("Updating GUI", Xposition);

    altitudeText.innerText = `${altitude.toFixed(1)} m`; /* updates the altitude */
    velocityText.innerText = `${velocity.toFixed(2)} m/s`; /* updates the velocity */
    fuelText.innerText = `${fuel} kg`; /* this updates the fuel */
    document.getElementById("thrust").innerHTML = thrust_status;

    lander.style.bottom = (altitude * 0.05) + "px"; /* this moves the lander down based on the altitude. 0.05 is a scaling factor to make it fit on the screen. */

    if (hasLanded && !landed) {
        landed = true;
        if (safe) {
            statusText.innerText = "Landed safely!"; 
        }
        else {
            statusText.innerText = "Crashed...";
        }
    }

    if (altitude < 250 && altitude > 0) {
        altitudeAlert.innerText = "Low Altitude";
    } else {
        altitudeAlert.innerText = "";
    }
}
