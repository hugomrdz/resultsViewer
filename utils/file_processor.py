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

# New mapping for vector and alpha values
vector_mapping = {
    1: "vector1",
    2: "vector2",
    3: "vector3",
    4: "vector4",
    5: "vector5",
    6: "reference1",
    7: "reference2",
    8: "reference3"
}

def construct_file_path(folder_name, nvar, nobj, vector, alpha, gamma, execution):
    """
    Constructs the file path based on the folder name, number of variables, number of objectives,
    vector, alpha, gamma, and execution number.

    :param folder_name: Name of the test problem folder
    :param nvar: Number of variables
    :param nobj: Number of objectives
    :param vector: The vector index (1-8)
    :param alpha: The alpha index (0-3)
    :param gamma: The gamma index (1-6)
    :param execution: The execution number (1-30)
    :return: The constructed file path
    """
    vector_str = vector_mapping[vector]
    alpha_str = f"_alpha{alpha}" if alpha > 0 else ""
    gamma_value = "{:.2f}".format(gamma_mapping[gamma])
    execution_str = f"R{execution:02d}"

    # Construct file name using the original naming convention
    file_name = f"HV-EMOA_{folder_name}_{gamma_value}_0{nobj}D_{execution_str}.pof"

    # Construct new directory structure to include vector and alpha
    file_path = f"data/{folder_name}/nvar{nvar}/nobj{nobj}/{vector_str}_{alpha_str}_{gamma_value}/{file_name}"

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

# comment