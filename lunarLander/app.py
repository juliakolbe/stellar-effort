from flask import Flask, request, jsonify, render_template, redirect
from Algorithms1 import DoomLander, PhysicsConstants, LanderState, Vector2D, ThrustControl

# debugging: http://127.0.0.1:5000


app = Flask(__name__)

# Initialize simulation with proper arguments
doom_lander = DoomLander(empty_mass=1200.0, initial_fuel=640.0, initial_altitude=8500.0)

@app.route('/')
def home():
    return redirect('/loading')

@app.route('/loading')
def loading():
    return render_template('loading.html')

@app.route('/simulation')
def simulation():
    print("Loading simulation page...")
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
    doom_lander.update() # Advance physics regardless
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

@app.route('/configure', methods=['POST'])
def configure():
    global doom_lander
    data = request.get_json()
    mode = data.get('mode', 'default')

    if mode== 'empty':
        empty_mass = 1200
        fuel = 640
    elif mode == 'rover':
        empty_mass = 1500
        fuel = 800
    elif mode == 'astronauts':
        empty_mass = 1800
        fuel = 1000
    else:
        empty_mass = 1200
        fuel = 640

    doom_lander = DoomLander(empty_mass=empty_mass, initial_fuel=fuel, initial_altitude=8500)
    print(f"Configured mode: {mode}, mass={empty_mass}, fuel={fuel}")
    return jsonify(success=True)


if __name__ == '__main__':
    app.run(debug=True)
