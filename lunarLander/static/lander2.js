const lander = document.getElementById("lander20");
const altitudeText = document.getElementById("altitude");
const velocityText = document.getElementById("velocity");
const fuelText = document.getElementById("fuel");
const statusText = document.getElementById("status");
const thrusterbutton = document.getElementById("thrusterButton");
const altitudeAlert = document.getElementById("altitude-Alert");

let landed = false;
let Xposition = 200; 
let Yposition = 200;
let leftArrow = false;
let rightArrow = false;
let thrustOn = false;

console.log("Script is running!");

// Key down events
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

// Key up events
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
        Algorithms1.py.ThrustConrol.apply_thrust(doomlander, 1);
    }
});

function sendThrust(thrustValue) {
    fetch('/thrust', {
        method: 'POST', 
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ thrust: thrustValue })
    });
}

// Fetch lander state from server every 100ms
setInterval(getLanderState, 100); 

function getLanderState() {
    fetch('/state')
    .then(res => res.json())
    .then(data => {
        updateGUI(data);
    });
}

function updateX() {
    const graphic = document.querySelector(".lunar-graphic");
    const landerPerimeter = lander.getBoundingClientRect();
    const graphicPerimeter = graphic.getBoundingClientRect();

    if (leftArrow && landerPerimeter.left > graphicPerimeter.left)
        {
            Xposition -= 2;
        } 
    if (rightArrow && landerPerimeter.right < graphicPerimeter.right) { 
            Xposition += 2; 
        }

    lander.style.left = `${Xposition}px`;
    requestAnimationFrame(updateX);
}

function updateY() {
    /*if (thrustOn) {
        Yposition -= 3; // Move up
    } else {
        Yposition += 1; // Gravity pulls it down
    }

    if (Yposition < 0) Yposition = 0; // Prevent lander from going too high
    lander.style.top = `${Yposition}px`;
    */
    requestAnimationFrame(updateY);
}

// Call the update functions
updateX();
updateY();

// Update GUI with fetched data
function updateGUI(state) {
    const { altitude, velocity, fuel, landed: hasLanded, thrust_status, safe } = state;

    console.log("Updating GUI", Xposition, Yposition);

    altitudeText.innerText = `${altitude.toFixed(1)} m`;
    velocityText.innerText = `${velocity.toFixed(2)} m/s`;
    fuelText.innerText = `${fuel} kg`;
    document.getElementById("thrust").innerHTML = thrust_status;

    if (hasLanded && !landed) {
        landed = true;
        statusText.innerText = safe ? "Landed safely!" : "Crashed...";
    }

    altitudeAlert.innerText = (altitude < 250 && altitude > 0) ? "Low Altitude" : "";
}
