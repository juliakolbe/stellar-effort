const lander = document.getElementById("lander20");
const altitudeText = document.getElementById("altitude");
const velocityText = document.getElementById("velocity");
const fuelText = document.getElementById("fuel");
const statusText = document.getElementById("status");
const thrusterbutton = document.getElementById("thrusterButton");
const altitudeAlert = document.getElementById("altitude-Alert");

let landed = false;
let Xposition = 200;
let Yposition = 300;
let leftArrow = false;
let rightArrow = false;
let thrustOn = false;

console.log("Script is running!");

document.addEventListener("keydown", (event) => {
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

document.addEventListener("keyup", (event) => {
    if (event.key === "ArrowLeft") {
        leftArrow = false;
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
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ thrust: thrustValue })
    });
}

setInterval(getLanderState, 100);

function getLanderState() {
    fetch('/state')
    .then(res => res.json())
    .then(data => {
        updateGUI(data);
    });
}

document.addEventListener("keydown", event => {
    if (event.code === "Space" && !landed) {
        sendThrust(1000);
        console.log("hitting the space bar, baby");
    }
});

function updatePosition() {
    if (leftArrow) Xposition -= 2;
    if (rightArrow) Xposition += 2;
    if (thrustOn) Yposition += 3; // Increase Y when thrust is applied
    else Yposition -= 1; // Simulating gravity pulling the lander down

    lander.style.left = `${Xposition}px`;
    lander.style.bottom = `${Yposition}px`;
    requestAnimationFrame(updatePosition);
}

updatePosition();

function updateGUI(state) {
    const { altitude, velocity, fuel, landed: hasLanded, thrust_status, safe } = state;

    console.log("Updating GUI", Xposition, Yposition);

    altitudeText.innerText = `${altitude.toFixed(1)} m`;
    velocityText.innerText = `${velocity.toFixed(2)} m/s`;
    fuelText.innerText = `${fuel} kg`;
    document.getElementById("thrust").innerHTML = thrust_status;

    if (hasLanded && !landed) {
        landed = true;
        if (safe) {
            statusText.innerText = "Landed safely!";
        } else {
            statusText.innerText = "Crashed...";
        }
    }

    if (altitude < 250 && altitude > 0) {
        altitudeAlert.innerText = "Low Altitude";
    } else {
        altitudeAlert.innerText = "";
    }
}
