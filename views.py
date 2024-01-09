from flask import Flask, render_template, Blueprint, jsonify
# from .utils.file_processor import construct_file_path, read_pof_file  # Ensure correct import paths
from utils.file_processor import construct_file_path, read_pof_file
import os

views = Blueprint('views', __name__)

@views.route('/')
def home():
    folder_options = ['LAME']  # Add more options as needed
    nvar_options = [0, 2, 5]  # nvarX options
    nobj_options = [2, 3]  # nobjY options
    gamma_options = [0.25, 0.50, 0.75, 1.0, 2.0, 5.0]
    offset_options = [
        (0, 'No offset'),  # NO OFFSET
        (1, '(0, 0)'),
        (2, '(0, 1)'),
        (3, '(0.25, 0.75)'),
        (4, '(0.5, 0.5)'),
        (5, '(0.75, 0.25)'),
        (6, '(1, 0)'),
        (7, '(1, 1)'),
        (8, '(0.1, 0.1)')
    ]
    execution_options = list(range(1, 31))  # Assuming 30 executions

    return render_template('index.html', folder_options=folder_options,
                           nvar_options=nvar_options,
                           nobj_options=nobj_options,
                           gamma_options=gamma_options,
                           offset_options=offset_options,
                           execution_options=execution_options)

@views.route('/data/<folder>/<int:nvar>/<int:nobj>/<int:gamma>/<int:offset>/<int:execution>')
def get_data(folder, nvar, nobj, gamma, offset, execution):
    # This route handles AJAX requests for data
    file_path = construct_file_path(folder, nvar, nobj, gamma, offset, execution)
    if file_path and os.path.exists(file_path):
        data_points = read_pof_file(file_path)
        return jsonify(data_points)
    else:
        # If the file_path is None or file does not exist, return an error
        return jsonify({"error": "Invalid parameters or file not found"}), 404



