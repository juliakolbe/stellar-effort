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
//stuff I added to get the lander to move properly
let running = true;
let currentAltitude = 1;
let touchdown = null;
let currentFuel =0;
let finalAlt = null;
let finalVel = null;

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
        // sendThrust(1000);
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
    }
});

function sendThrust(thrustValue) {
    console.log("Sending thrust:", thrustValue); 
    fetch('/thrust', {
            method: 'POST', 
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ thrust: thrustValue })
    });
}

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
    if (running) {
        Yposition = currentAltitude;
    } else {
        Yposition = touchdown !== null ? touchdown : Yposition;
    }

    if (Yposition < 0) Yposition = 0;
    if (Yposition > 750) Yposition = 750;

    lander.style.top = `${Yposition}px`;
    requestAnimationFrame(updateY);
}

// Update GUI with fetched data
function updateGUI(state) {
    const { altitude, velocity, fuel, landed: hasLanded, thrust_status, safe } = state;

    console.log("Updating GUI", Xposition, Yposition);
    console.log("altitude:", altitude, "hasLanded:", hasLanded, "landed:", landed, "running:", running);


    altitudeText.innerText = landed ? `${finalAlt} m` : `${altitude.toFixed(1)} m`;
    velocityText.innerText = landed ? `${finalVel} m/s` : `${velocity.toFixed(2)} m/s`;
    console.log("Final altitude:", finalAlt, "Final velocity:", finalVel);

    // assuming the altitude starts at 8,500 m
    // divide by 10 (assumes roughly 850px on screen)
    // invert
    currentAltitude = (8500 - altitude) / 12; 
    currentFuel = fuel;

    velocityText.innerText = `${velocity.toFixed(2)} m/s`;
    fuelText.innerText = `${fuel} kg`;
    document.getElementById("thrust").innerHTML = thrust_status;

    /* this will give the fuel status a red glow when fuel is low */
    if (fuel > 150) {
        fuelText.style.color = "#f480ff";
        fuelText.style.textShadow = "0 0 8px #f480ff";
        statusText.innerText = "FUEL SUPPLY NORMAL";
    } else if (fuel > 0 && fuel <= 150) {
        fuelText.style.color = "crimson";
        fuelText.style.textShadow = "0 0 5px red";
        statusText.innerText = "LOW FUEL";
    } else {
        fuelText.style.color = "gray";
        fuelText.style.textShadow = "0 0 5px gray";
        statusText.innerText = "FUEL DEPLETED";

    }

    if (hasLanded && !landed) {
        landed = true;
        touchdown = currentAltitude;
        statusText.innerText = safe ? "Landed safely!" : "Crashed...";
        running = false;

        finalAlt= altitude.toFixed(1);
        finalVel= velocity.toFixed(2);
    }

    altitudeAlert.innerText = (altitude < 250 && altitude > 0) ? "Low Altitude" : "";
}

updateX();
updateY();
setInterval(getLanderState, 100);
setInterval(() => {
    if (thrustOn && !landed && currentFuel > 0) {
        sendThrust(8000);
    }
}, 100);