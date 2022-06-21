from flask import Flask, render_template, request, jsonify
from src.blade_geometry_calculation import create_blade_section

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'

FORM_FIELDS = {
    'blade_chord': {
        'description': 'Хорда лопатки, [мм]',
        'default': 28.3}, 
    'blade_inlet_angle': {
        'description': 'Угол входа потока, [град.]',
        'default':30.},
    'blade_outlet_angle': {
        'description': 'Угол выхода потока, [град.]',
        'default': 30.},
    'blade_installation_angle': {
        'description': 'Установочный угол, [град.]',
        'default': 90.},
    'blade_inlet_opening_angle': {
        'description': 'Угол раскрытия передней кромки, [град.]',
        'default': 10.},
    'blade_outlet_opening_angle': {
        'description': 'Угол раскрытия задней кромки, [град.]',
        'default': 8.},
    'leading_edge_radius': {
        'description': 'Радиус передней кромки, [мм]',
        'default': round(28.3*0.025, 3)},
    'trailing_edge_radius': {
        'description': 'Радиус задней кромки, [мм]',
        'default': round(28.3*0.01, 3)},
    'relative_step': {
        'description': 'Относительный шаг турбинной решетки',
        'default': 0.7},
}


@app.route('/', methods=['POST', 'GET'])
def main():
    return render_template('main.html', fields=FORM_FIELDS)


@app.route('/theory', methods=['POST', 'GET'])
def theory():
    return render_template('theory.html')


@app.route('/api', methods=['POST', 'GET'])
def calculate_geometry():
    if request.method == 'POST':
        data = {k: float(v) for k, v in request.get_json().items()}
        calculated_data = create_blade_section(
            blade_chord=data['blade_chord'],
            blade_inlet_angle=data['blade_inlet_angle'],
            blade_outlet_angle=data['blade_outlet_angle'],
            blade_installation_angle=data['blade_installation_angle'],
            blade_inlet_opening_angle=data['blade_inlet_opening_angle'],
            blade_outlet_opening_angle=data['blade_outlet_opening_angle'],
            leading_edge_radius=data['leading_edge_radius'],
            trailing_edge_radius=data['trailing_edge_radius'],
        )
        plotly_data = {
            'x0': list(calculated_data['x_array']),
            'y0': list(calculated_data['y_array']),
            'x1': list(calculated_data['x_array']+data['blade_chord']*data['relative_step']),
            'y1': list(calculated_data['y_array']),
            'x2': list(calculated_data['x_array']-data['blade_chord']*data['relative_step']),
            'y2': list(calculated_data['y_array']),
        }
        return jsonify(plotly_data)
    

if __name__ == "__main__":
    app.run()
