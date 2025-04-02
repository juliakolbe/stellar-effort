from flask import Flask, request, jsonify, render_template
from Algorithms1 import DoomLander, PhysicsConstants, LanderState, Vector2D, ThrustControl

app = Flask(__name__)

# Initialize simulation
doom_lander = DoomLander(empty_mass=1200.0, initial_fuel=640.0, initial_altitude=8500.0)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/thrust', methods=['POST'])
def thrust():
    data = request.get_json()
    thrust_value = data.get('thrust', 0.0)
    print(f"Thrust received: {thrust_value}")
    doom_lander.queue_thrust_command(thrust_value)
    doom_lander.update()
    return jsonify(success=True)

@app.route('/state')
def state():
    # doom_lander.queue_thrust_command(0.0)  # Apply no thrust if nothing is pressed
    doom_lander.update()  # Advance physics regardless
    thrust_status = "Inactive"
    if doom_lander.get_fuel_mass() <= 0:
        thrust_status = "Empty"
    elif doom_lander.thruster.thrust_force > 0:
        thrust_status = "Engaged"
    return jsonify({
        'altitude': doom_lander.get_altitude(),
        'velocity': doom_lander.get_velocity(),
        'fuel': doom_lander.get_fuel_mass(),
        'landed': doom_lander.has_landed(),
        'safe': doom_lander.is_landing_safe(),
        'thrust_status': thrust_status
    })

if __name__ == '__main__':
    app.run(debug=True)
