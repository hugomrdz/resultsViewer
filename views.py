from flask import Flask, render_template, Blueprint, jsonify
# from .utils.file_processor import construct_file_path, read_pof_file  # Ensure correct import paths
from utils.file_processor import construct_file_path, read_pof_file
import os

views = Blueprint('views', __name__)

@views.route('/')
def home():
    folder_options = ['LAME']  # Add more options as needed
    nvar_options = [5]  # nvarX options
    nobj_options = [2, 3]  # nobjY options
    gamma_options = [0.25, 0.50, 0.75, 1.0, 2.0, 5.0]
    vector_options = [
        (1, 'Vector 1 (0,1)'),
        (2, 'Vector 2 (0.25,0.75)'),
        (3, 'Vector 3 (0.5,0.5)'),
        (4, 'Vector 4 (0.75,0.75)'),
        (5, 'Vector 5 (1,0)'),
        (6, 'Reference 1 (1,1)'),
        (7, 'Reference 2 (1.1,1.1)'),
        (8, 'Reference 3 (2,2)')
    ]
    alpha_options = [
        (0, 'Fixed Point'),
        (1, 'Alpha 0.25'),
        (2, 'Alpha 0.50'),
        (3, 'Alpha 0.75')
    ]  # Assuming alphas are integers

    execution_options = list(range(1, 31))  # Assuming 30 executions

    return render_template('index.html', folder_options=folder_options,
                       nvar_options=nvar_options,
                       nobj_options=nobj_options,
                       vector_options=vector_options,
                       alpha_options=alpha_options,
                       gamma_options=gamma_options,
                       execution_options=execution_options)


@views.route('/data/<folder>/<int:nvar>/<int:nobj>/<int:vector>/<int:alpha>/<int:gamma>/<int:execution>')
def get_data(folder, nvar, nobj, vector, alpha, gamma, execution):
    # Adjust construct_file_path call to include alpha and use the new vector naming
    file_path = construct_file_path(folder, nvar, nobj, vector, alpha, gamma, execution)
    if os.path.exists(file_path):
        data_points = read_pof_file(file_path)
        return jsonify(data_points)
    else:
        return jsonify({"error": "Invalid parameters or file not found"}), 404

