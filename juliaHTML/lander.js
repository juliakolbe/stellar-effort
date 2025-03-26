const lander = document.getElementById("lander");
const thrusterbutton = document.getElementById("thrusterButton");
const altitudeAlert = document.getElementById("altitude-Alert");

let Xposition = 200;
let Yposition = 700; /* i want it to start at the top of the screen */ 
let velocity = 0;
let gravity = -8.02;
let thrust = 2.7;
let leftArrow = false;
let rightArrow = false;
let thrustOn = false;

console.log("Script is running!");

document.addEventListener("keydown", (event) => { /* keydown = button pushed */ 
    if (event.key === "ArrowLeft") {
        leftArrow = true;
    }
    if (event.key === "ArrowRight") {
        rightArrow = true;
    }
    if (event.code === "Space") {
        thrustOn = true;
        thrusterbutton.classList.add("active");
        thrusterbutton.innerHTML = "Thrust engaged";
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
        thrusterbutton.innerHTML = "Thrust disengaged";
    }
});

function updateLander() {
    if (leftArrow) {
        Xposition -= 1;
    }
    if (rightArrow) {
        Xposition += 1;
    }

    velocity += gravity;

    if (thrustOn) {
        velocity += thrust;
        lander.style.background = "orange"; /* thrust on */
    } else {
        lander.style.background = "silver"; /* thrust off */ 
    }

    Yposition += velocity;

    const maxHeight = 800;
/* once it hits the moon's surface, it'll stop moving down */ 
    if (Yposition < 0) {
        Yposition = 0;
        velocity = 0;
    }
    if (Yposition > maxHeight) {
        Yposition = maxHeight;
        velocity = 0;
    }

    lander.style.bottom = Yposition + "px";
    lander.style.left = Xposition + "px";
}

if (Yposition < 250 && Yposition > 0) {
    altitudeAlert.innerHTML = "Warning: Low Altitude.";
}
else {
    altitudeAlert.innerHTML = "";
}

setInterval(updateLander, 1000 / 60); /* 60 frames per second */


