import codecs
from pprint import pprint
from flask import Flask, render_template, request, jsonify
import yaml

from src.blade_geometry_calculation import create_blade_section
from src.velocity_triangle_calculation import calculate_velocity_triangle

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'


with codecs.open('form_fields.yaml', 'r', encoding='utf8') as file: 
    FORM_FIELDS = yaml.safe_load(file)


@app.route('/', methods=['POST', 'GET'])
def main():
    return render_template('main.html', fields=FORM_FIELDS)


@app.route('/theory', methods=['POST', 'GET'])
def theory():
    return render_template('theory.html')


@app.route('/api', methods=['POST', 'GET'])
def calculate_geometry():
    if request.method == 'POST':
        data = {k: float(v) for k, v in request.get_json().items() if k != 'projectName'}

        calculation_data = {
            'stator': create_blade_section(
                blade_chord=data['stator_blade_chord'],
                blade_inlet_angle=data['stator_blade_inlet_angle'],
                blade_outlet_angle=data['stator_blade_outlet_angle'],
                blade_installation_angle=(data['stator_blade_inlet_angle']+180-data['stator_blade_outlet_angle'])/2,
                blade_inlet_opening_angle=data['stator_blade_inlet_opening_angle'],
                blade_outlet_opening_angle=data['stator_blade_outlet_opening_angle'],
                leading_edge_radius=data['stator_leading_edge_radius'],
                trailing_edge_radius=data['stator_trailing_edge_radius'],
            ),
            'rotor': create_blade_section(
                blade_chord=data['rotor_blade_chord'],
                blade_inlet_angle=data['rotor_blade_inlet_angle'],
                blade_outlet_angle=data['rotor_blade_outlet_angle'],
                blade_installation_angle=(data['rotor_blade_inlet_angle']+180-data['rotor_blade_outlet_angle'])/2,
                blade_inlet_opening_angle=data['rotor_blade_inlet_opening_angle'],
                blade_outlet_opening_angle=data['rotor_blade_outlet_opening_angle'],
                leading_edge_radius=data['rotor_leading_edge_radius'],
                trailing_edge_radius=data['rotor_trailing_edge_radius'],
            )
        }
        velocity_triangle_data = calculate_velocity_triangle(
            inlet_absolute_velocity=data['inlet_absolute_velocity'],
            outlet_absolute_velocity=data['outlet_absolute_velocity'],
            inlet_relative_velocity=data['inlet_relative_velocity'],
            outlet_relative_velocity=data['outlet_relative_velocity'],
            inlet_absolute_angle=data['stator_blade_inlet_angle'],
            outlet_absolute_angle=data['stator_blade_outlet_angle'],
            inlet_relative_angle=data['rotor_blade_inlet_angle'],
            outlet_relative_angle=data['rotor_blade_outlet_angle'])

        blade_types_to_export = ['rotor', 'stator']
        number_of_blade = 3

        plotly_data = {
            f'{_type}_blade_{index}': [
                list(
                    (calculation_data[_type]['x_array']-data[f'{_type}_blade_chord']*data[f'{_type}_relative_step'] if index==0 else \
                        calculation_data[_type]['x_array']+data[f'{_type}_blade_chord']*data[f'{_type}_relative_step'] if index==2 else \
                            calculation_data[_type]['x_array']) * (-1 if _type=='stator' else 1)
                ), list(
                    calculation_data[_type]['y_array']+(data[f'{_type}_blade_chord']/2+data['axial_gap']) if _type=='stator' else \
                        calculation_data[_type]['y_array']-(data[f'{_type}_blade_chord']/2+data['axial_gap'])
                )
            ] for index in range(number_of_blade) for _type in blade_types_to_export
        }
        return jsonify(plotly_data)
    

if __name__ == "__main__":
    app.run()
