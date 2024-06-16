from geopy.distance import geodesic
import re

def find_first_digit(s):
    for char in s:
        if char.isdigit():
            return char
    return None

def find_option_number(response, label, error_writer):
    predicted = find_first_digit(response)
    if predicted!=None:
        if predicted==str(label)[0]:
            return 1
        else:
            return 0
    else:
        error_writer.write(r"### response:{}, answer:{} ###\n".format(response, label))
        return None

def trajectory_classification(response, label, error_writer):
    pattern = r'car|bike|bicycle|pedestrian'
    mapping = {'car': 1, 'bike': 2, 'bicycle':2, 'pedestrian': 3}
    match = re.search(pattern, response, flags=re.I)
    if match:
        predicted = match.group()
        predicted = mapping[predicted]
        if predicted==label:
            return 1
        else:
            return 0
    else:
        error_writer.write(r"### response:{}, ### answer:{} ###\n".format(response, label))
        return None

def find_option_number_for_cot(response, label, error_writer):
    pattern = r'\((\d+)\)'
    match = re.search(pattern, response, flags=re.I)
    if match:
        predicted = match.group(1)
        if predicted==str(label)[0]:
            return 1
        else:
            return 0
    else:
        error_writer.write(r"### response:{}, ### answer:{} ###\n".format(response, label))
        return None

def yes_or_no(response, label, error_writer):
    pattern = r'Yes|No'
    match = re.search(pattern, response, flags=re.I)
    if match:
        predicted = match.group()
        predicted = predicted.title()
        if predicted==label:
            return 1
        else:
            return 0
    else:
        error_writer.write(r"### response:{}, ### answer:{} ###\n".format(response, label))
        return None

def anomaly_detection(response, label, error_writer):
    pattern = r'Normal|Anomalous|Anomaly|Abnormal'
    match = re.search(pattern, response, flags=re.I)
    if match:
        predicted = match.group()
        predicted = predicted.title()
        if predicted=="Abnormal" or predicted=="Anomaly":
            predicted=="Anomalous"
        if predicted==label:
            return 1
        else:
            return 0
    else:
        error_writer.write(r"### response:{}, ### answer:{} ###\n".format(response, label))
        return None

def extract_floats(input_string):
    floats = re.findall(r'\d+\.\d+', input_string)
    if len(floats) >= 2:
        return float(floats[0]), float(floats[1])
    else:
        return None

def calculate_distance(coord1, coord2):
    distance = geodesic([coord2[1], coord2[0]], [coord1[1], coord1[0]]).meters
    return distance

def trajectory_prediction(response, label, error_writer):
    lon, lat = extract_floats(response)
    distance = calculate_distance([lon, lat], label)
    if distance>=100000:
        error_writer.write("### response:{}, answer:{} ###\n".format(response, label))
        return None
    return distance
