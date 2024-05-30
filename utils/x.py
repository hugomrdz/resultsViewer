# Python module for processing .pof files

# Mapping for gamma values
gamma_mapping = {
    1: 0.25,
    2: 0.50,
    3: 0.75,
    4: 1.00,
    5: 2.00,
    6: 5.00
}

# Mapping for offset values
offset_mapping = {
    0: None, # NO OFFSET
    1: (0, 0),
    2: (0, 1),
    3: (0.25, 0.75),
    4: (0.5, 0.5),
    5: (0.75, 0.25),
    6: (1, 0),
    7: (1, 1),
    8: (0.1, 0.1)
}

def construct_file_path(folder_name, nvar, nobj, gamma, offset, execution):
    """
    Constructs the file path based on the folder name, number of variables, number of objectives,
    gamma, offset, and execution number.

    :param folder_name: Name of the test problem folder
    :param nvar: Number of variables
    :param nobj: Number of objectives
    :param gamma: The gamma index (1-6)
    :param offset: The offset index (0-8)
    :param execution: The execution number (1-30)
    :return: The constructed file path
    """
    # Map gamma index to actual gamma value
    gamma_value = "{:.2f}".format(gamma_mapping[gamma])
    execution_str = f"R{execution:02d}"

    # Determine offset folder part based on offset index
    if offset == 0:  # No offset
        offset_folder_part = f"reference_gamma{gamma}/"
    else:  # With offset
        offset_tuple = offset_mapping[offset]
        offset_folder_part = f"offset{offset}_gamma{gamma}/"

    # Construct file name
    file_name = f"HV-EMOA_{folder_name}_{gamma_value}_0{nobj}D_{execution_str}.pof"
    # Construct full file path
    file_path = f"data/{folder_name}/nvar{nvar}/nobj{nobj}/{offset_folder_part}{file_name}"

    return file_path


def read_pof_file(file_path):
    """
    Reads a .pof file and extracts the data points.
    It can handle both 2D and 3D points.

    :param file_path: Path to the .pof file
    :return: List of tuples representing the data points
    """
    data_points = []
    with open(file_path, 'r') as file:
        next(file)  # Skip the first line (header)
        for line in file:
            # Splitting the line into values and converting them to float
            values = list(map(float, line.split()))
            # Depending on the number of values, append the point as a tuple
            if len(values) == 2:
                data_points.append((values[0], values[1]))  # 2D point
            elif len(values) == 3:
                data_points.append((values[0], values[1], values[2]))  # 3D point
            else:
                # Handle the case where there are not 2 or 3 values
                print(f"Unexpected number of values in line: {line}")
    return data_points

# VIEWS.PY

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