from flask import Flask, request, jsonify, render_template, redirect
from Algorithms1 import DoomLander, PhysicsConstants

app = Flask(__name__)

# Global variable for the lander instance (initially None)
doom_lander = None

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
    global doom_lander
    if doom_lander is None:
        return jsonify(error="Lander not configured yet."), 400

    data = request.get_json()
    thrust_value = data.get('thrust', 0.0)
    print(f"Thrust received: {thrust_value}")
    doom_lander.queue_thrust_command(thrust_value)
    doom_lander.update()
    return jsonify(success=True)

@app.route('/state')
def state():
    global doom_lander
    if doom_lander is None:
        return jsonify(error="Lander not configured yet."), 400

    doom_lander.update()
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

    if mode == 'empty':
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
