from flask import Flask, render_template, Blueprint, jsonify
#from .utils.file_processor import construct_file_path, read_pof_file  # Ensure correct import paths
from utils.file_processor import construct_file_path, read_pof_file

views = Blueprint('views', __name__)

@views.route('/')
def home():
    folder_options = ['LAME']# , 'SCHAFFER']
    gamma_options = [0.25, 0.50, 0.75, 1.0, 2.0, 5.0]
    offset_options = ['NA',(0, 0), (0, 1), (0.25, 0.75), (0.5, 0.5), (0.75, 0.25), (1, 0), (1, 1), (0.1, 0.1)]
    execution_options = list(range(1, 31))  # Assuming 30 executions

    return render_template('index.html', folder_options=folder_options,
                           gamma_options=gamma_options,
                           offset_options=offset_options,
                           execution_options=execution_options)


@views.route('/data/<folder>/<int:gamma>/<int:offset>/<int:execution>')
def get_data(folder, gamma, offset, execution):
    # This route handles AJAX requests for data
    file_path = construct_file_path(folder, gamma, offset, execution)
    if file_path:
        data_points = read_pof_file(file_path)
        return jsonify(data_points)
    else:
        return jsonify({"error": "Invalid parameters"}), 400

# Ensure you have the correct initialization and blueprint registration in your main app file
# Example:
# app = Flask(__name__)
# app.register_blueprint(views, url_prefix='/')