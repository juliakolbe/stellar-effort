document.addEventListener("DOMContentLoaded", function() {
    const lander = document.getElementById("lander");
    const thrusterButton = document.getElementById("thrusterButton");
    const altitudeAlert = document.getElementById("altitude-Alert");
    const velocityDisplay = document.getElementById("velocity");
    
    let landerX = 400; // Horizontal center of the lunar graphic
    let landerY = 0;   // Will be updated based on API data
    let lastAltitude = 8500; // Starting altitude from the Python backend
    const MAX_DISPLAY_HEIGHT = 800; // Height of the lunar-graphic div
    
    // Function to update lander position based on backend data
    async function updateLanderPosition() {
        try {
            const response = await fetch('/lander_status');
            const data = await response.json();
            
            // Convert altitude to display position (inverted - higher altitude = higher position)
            // Scale altitude to fit within display area
            const MAX_ALTITUDE = 10000; // Maximum altitude to display
            landerY = MAX_DISPLAY_HEIGHT * (1 - (data.altitude / MAX_ALTITUDE));
            
            // Clamp to display boundaries
            landerY = Math.max(0, Math.min(landerY, MAX_DISPLAY_HEIGHT - 40));
            
            // Update visual position
            lander.style.bottom = (MAX_DISPLAY_HEIGHT - landerY) + "px";
            lander.style.left = landerX + "px";
            
            // Update displays
            altitudeAlert.innerText = `Altitude: ${data.altitude.toFixed(2)} m`;
            velocityDisplay.innerText = `Velocity: ${data.velocity.toFixed(2)} m/s`;
            
            // Visual feedback for landing safety
            if (data.altitude < 50) {
                if (Math.abs(data.velocity) > 5) {
                    lander.style.background = "red"; // Unsafe landing velocity
                } else {
                    lander.style.background = "green"; // Safe landing velocity
                }
            } else {
                lander.style.background = "silver"; // Default color
            }
            
            // Thrust visual indication from backend
            if (data.velocity > lastAltitude - data.altitude) {
                // If velocity is positive (moving up), show thrust
                const thrustIndicator = document.createElement("div");
                thrustIndicator.className = "thrust-indicator";
                thrustIndicator.style.position = "absolute";
                thrustIndicator.style.bottom = (MAX_DISPLAY_HEIGHT - landerY - 5) + "px";
                thrustIndicator.style.left = (landerX + 10) + "px";
                thrustIndicator.style.width = "10px";
                thrustIndicator.style.height = "15px";
                thrustIndicator.style.background = "orange";
                document.querySelector(".lunar-graphic").appendChild(thrustIndicator);
                
                // Remove after animation
                setTimeout(() => {
                    thrustIndicator.remove();
                }, 200);
            }
            
            lastAltitude = data.altitude;
            
        } catch (error) {
            console.error("Error updating lander position:", error);
        }
    }
    
    // Add keyboard controls for horizontal movement
    let leftArrow = false;
    let rightArrow = false;
    
    document.addEventListener("keydown", (event) => {
        if (event.key === "ArrowLeft") {
            leftArrow = true;
        }
        if (event.key === "ArrowRight") {
            rightArrow = true;
        }
        if (event.code === "Space") {
            applyThrust();
        }
    });
    
    document.addEventListener("keyup", (event) => {
        if (event.key === "ArrowLeft") {
            leftArrow = false;
        }
        if (event.key === "ArrowRight") {
            rightArrow = false;
        }
    });
    
    // Function to handle horizontal movement
    function updateHorizontalPosition() {
        if (leftArrow) {
            landerX = Math.max(15, landerX - 3);
        }
        if (rightArrow) {
            landerX = Math.min(785, landerX + 3);
        }
        
        lander.style.left = landerX + "px";
    }
    
    // Function to apply thrust through the backend API
    async function applyThrust() {
        const thrustValue = document.getElementById("thrust").value || 1000;
        try {
            const response = await fetch('/apply_thrust', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    thrust: thrustValue, 
                    duration: 0.5 
                })
            });
            
            thrusterButton.classList.add("active");
            thrusterButton.innerText = "Thrust engaged";
            
            // Visual feedback for thrust
            lander.style.background = "orange";
            
            // Reset visual state after a delay
            setTimeout(() => {
                thrusterButton.classList.remove("active");
                thrusterButton.innerText = "Apply Thrust";
                lander.style.background = "silver";
            }, 500);
            
            // Update dashboard immediately after applying thrust
            updateLanderPosition();
            
        } catch (error) {
            console.error("Error applying thrust:", error);
        }
    }
    
    // Connect the thruster button to the apply thrust function
    thrusterButton.addEventListener("click", applyThrust);
    
    // Initialize position and start update loops
    updateLanderPosition();
    setInterval(updateLanderPosition, 100); // Update position from backend
    setInterval(updateHorizontalPosition, 1000/60); // Update horizontal movement at 60fps
    
    // Add some surface features to the lunar graphic
    function addLunarSurface() {
        const surface = document.createElement("div");
        surface.style.position = "absolute";
        surface.style.bottom = "0";
        surface.style.width = "100%";
        surface.style.height = "20px";
        surface.style.background = "#555";
        document.querySelector(".lunar-graphic").appendChild(surface);
        
        // Add some craters
        for (let i = 0; i < 5; i++) {
            const crater = document.createElement("div");
            crater.style.position = "absolute";
            crater.style.bottom = "15px";
            crater.style.left = (Math.random() * 750) + "px";
            crater.style.width = (20 + Math.random() * 30) + "px";
            crater.style.height = (5 + Math.random() * 10) + "px";
            crater.style.background = "#333";
            crater.style.borderRadius = "50%";
            document.querySelector(".lunar-graphic").appendChild(crater);
        }
    }
    
    // Initialize the surface
    addLunarSurface();
});
