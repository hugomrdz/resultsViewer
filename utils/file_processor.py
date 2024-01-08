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
    0: (-1,-1),
    1: (0, 0),
    2: (0, 1),
    3: (0.25, 0.75),
    4: (0.5, 0.5),
    5: (0.75, 0.25),
    6: (1, 0),
    7: (1, 1),
    8: (0.1, 0.1)
}

def construct_file_path(folder_name, gamma, offset, execution):
    """
    Constructs the file path based on gamma, offset, and execution number.

    :param gamma: The gamma value (1-6)
    :param offset: The offset value (1-8)
    :param execution: The execution number (1-30)
    :return: The constructed file path
    """

    gamma_value = "{:.2f}".format(gamma_mapping.get(gamma, 0))
    offset_value = offset_mapping.get(offset, None)
    execution_str = f"R{execution:02d}"
    
    if offset_value is not None:
        file_name = f"HV-EMOA_{folder_name}_{gamma_value}_02D_{execution_str}.pof"
        file_path = f"data/{folder_name}/outputOffset{offset}_gamma{gamma}/{file_name}"
        return file_path
    else:
        return None


def read_pof_file(file_path):
    """
    Reads a .pof file and extracts the data points.

    :param file_path: Path to the .pof file
    :return: List of tuples representing the data points
    """
    data_points = []
    with open(file_path, 'r') as file:
        next(file)  # Skip the first line (header)
        for line in file:
            if line.strip():  # Ensuring the line is not empty
                # Splitting the line into two values and converting them to float
                x, y = map(float, line.split())
                data_points.append((x, y))

    return data_points