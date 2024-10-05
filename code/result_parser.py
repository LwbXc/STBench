from geopy.distance import geodesic
import re
import numpy as np
import math
import pdb

def find_first_digit(s):
    for char in s:
        if char.isdigit():
            return char
    return None

def find_option_number(response, label, error_writer, metrics):
    predicted = find_first_digit(response)
    if predicted!=None:
        if predicted==str(label)[0]:
            metrics['accuracy'] = metrics.setdefault('accuracy', 0) + 1
        else:
            metrics.setdefault('accuracy', 0)
    else:
        error_writer.write("### response:{}, answer:{} ###\n".format(response, label))
        metrics['exception'] += 1
    metrics['total'] += 1
    return metrics

def trajectory_classification(response, label, error_writer, metrics):
    pattern = r'car|bike|bicycle|pedestrian'
    mapping = {'car': 1, 'bike': 2, 'bicycle':2, 'pedestrian': 3}
    match = re.search(pattern, response, flags=re.I)
    if match:
        predicted = match.group()
        predicted = mapping[predicted]
        if predicted==label:
            metrics['accuracy'] = metrics.setdefault('accuracy', 0) + 1
        else:
            metrics.setdefault('accuracy', 0)
    else:
        error_writer.write("### response:{}, ### answer:{} ###\n".format(response, label))
        metrics['exception'] += 1
    metrics['total'] += 1
    return metrics

def find_option_number_for_cot(response, label, error_writer, metrics):
    pattern = r'\((\d+)\)'
    match = re.search(pattern, response, flags=re.I)
    if match:
        predicted = match.group(1)
        if predicted==str(label)[0]:
            metrics['accuracy'] = metrics.setdefault('accuracy', 0) + 1
        else:
            metrics.setdefault('accuracy', 0)
    else:
        error_writer.write("### response:{}, ### answer:{} ###\n".format(response, label))
        metrics['exception'] += 1
    metrics['total'] += 1
    return metrics

def yes_or_no(response, label, error_writer, metrics):
    pattern = r'Yes|No'
    match = re.search(pattern, response, flags=re.I)
    if match:
        predicted = match.group()
        predicted = predicted.title()
        if predicted==label:
            metrics['accuracy'] = metrics.setdefault('accuracy', 0) + 1
        else:
            metrics.setdefault('accuracy', 0)
    else:
        error_writer.write("### response:{}, ### answer:{} ###\n".format(response, label))
        metrics['exception'] += 1
    metrics['total'] += 1
    return metrics


def anomaly_detection(response, label, error_writer, metrics):
    pattern = r'Normal|Anomalous|Anomaly|Abnormal'
    match = re.search(pattern, response, flags=re.I)
    if match:
        predicted = match.group()
        predicted = predicted.title()
        if predicted=="Abnormal" or predicted=="Anomaly":
            predicted=="Anomalous"
        if predicted==label:
            metrics['accuracy'] = metrics.setdefault('accuracy', 0) + 1
        else:
            metrics.setdefault('accuracy', 0)
    else:
        error_writer.write("### response:{}, ### answer:{} ###\n".format(response, label))
        metrics['exception'] += 1
    metrics['total'] += 1
    return metrics

def extract_floats(input_string):
    floats = re.findall(r'\d+\.\d+', input_string)
    if len(floats) >= 2:
        return float(floats[0]), float(floats[1])
    else:
        return None

def calculate_distance(coord1, coord2):
    distance = geodesic([coord2[1], coord2[0]], [coord1[1], coord1[0]]).meters
    return distance

def trajectory_prediction(response, label, error_writer, metrics):
    lon, lat = extract_floats(response)
    distance = calculate_distance([lon, lat], label)
    if distance>=100000:
        error_writer.write("### response:{}, answer:{} ###\n".format(response, label))
        metrics['exception'] += 1
    else:
        metrics['mae'] = metrics.setdefault('mae', 0) + distance
        metrics['total'] += 1
    return metrics

def flow_prediction(response, label, error_writer, metrics):
    mae = None
    try:
        # 解析Inflow数据
        decimal_pattern = r'-?\d+\.?\d*'
        decimals = re.findall(decimal_pattern, response)
        decimals = [float(x) for x in decimals]

        predicted = np.array(decimals[:6])

        # 根据label计算mae
        ans = np.array(label)

        mae = np.mean(np.abs(ans - predicted))
        rmse = math.sqrt(np.mean(np.power(ans - predicted, 2)))
        metrics['mae'] = metrics.setdefault('mae', 0) + mae
        metrics['rmse'] = metrics.setdefault('rmse', 0) + rmse
        metrics['total'] += 1
        
    except:
        error_writer.write("### response:{}, ### answer:{} ###\n".format(response, label))    
        metrics['exception'] += 1
    
    return metrics