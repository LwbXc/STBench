from geopy.distance import geodesic
import re
import numpy as np
import math

def extract_parenthesized_options_with_colon_ard_pcr_urfr(text, skip_zero=False):
    pattern = re.compile(r'\((\d+)\)\s*(?::)?\s*([^\(]+?)(?=(?:\s*\(\d+\))|["\'}]|$)', flags=re.S)
    matches = pattern.findall(text)
    results = []
    for num, label in matches:
        if skip_zero and num == '0':
            continue
        label_clean = label.strip().rstrip('.,;"\' ')
        results.append([str(num), label_clean])
    return results

def extract_parenthesized_options_normal(text, skip_zero=False):
    # Finds patterns like (1): Label text (up to next '(' with a digit and ':' or end)
    pattern = re.compile(r'\((\d+)\)\s*([^,()\.]+)')
    matches = pattern.findall(text)
    results = []
    for num, label in matches:
        if skip_zero and num == '0':
            continue
        results.append([str(num), label.strip()])
    return results

def extract_point_region(text):
    pattern = re.compile(r'Region\s*(\d+)\s*:\s*(\[[^\]]*\])', flags=re.S)
    matches = pattern.findall(text)
    return [[num, poly] for num, poly in matches]

def extract_point_trajectory(text):
    parts = text.split(';')
    results = []
    for part in parts:
        m = re.search(r'\b([1-9]\d?)\)\s*(.*)', part, flags=re.S)
        if m:
            num = m.group(1)
            label = m.group(2).strip()
            if label:
                results.append([num, label])
    return results

def extract_option_trajectory_region(text):
    pattern = re.compile(r'\(\s*([1-9]\d?)\s*\)\s*(\[[^\]]*\])')
    matches = pattern.findall(text)
    return [[num, lst.strip()] for num, lst in matches]

def xFinder_parser(question, llm_output, standard_answer_range, key_answer_type, correct_answer, evaluator, error_writer, metrics):
    
    result = evaluator.evaluate_single_example(
        question,
        llm_output,
        standard_answer_range,
        key_answer_type,
        correct_answer
    )
    if result == "Correct": metrics['accuracy'] = metrics.setdefault('accuracy', 0) + 1
    elif result == "Incorrect": metrics.setdefault('accuracy', 0)
    else: 
        error_writer.write("### response:{}, answer:{} ###\n".format(llm_output, correct_answer))
        metrics['exception'] += 1
    metrics['total'] = metrics.setdefault('total', 0) + 1
    return metrics

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

def extract_coordinates(text: str):
    lon_min, lon_max = 105, 110
    lat_min, lat_max = 30, 36

    matches = re.findall(r"\(([-+]?\d+\.\d+),\s*([-+]?\d+\.\d+)(?:,\s*[-+]?\d+)?\)", text)
    for lon, lat in matches[::-1]:
        lon, lat = float(lon), float(lat)
        if lon_min <= lon <= lon_max and lat_min <= lat <= lat_max:
            return (lon, lat)

    nums = re.findall(r"[-+]?\d+\.\d+", text)
    nums = list(map(float, nums))

    coord = (None, None)
    for i in range(len(nums)-2, -1, -1):
        if lon_min <= nums[i] <= lon_max and coord[0] == None: coord[0] = nums[i]
        if lat_min <= nums[i] <= lat_max and coord[1] == None: coord[1] = nums[i]
    if coord[0] and coord[1]: return coord

    return None

def calculate_distance(coord1, coord2):
    distance = geodesic([coord2[1], coord2[0]], [coord1[1], coord1[0]]).meters
    return distance

def trajectory_prediction(response, label, error_writer, metrics):
    try:
        lon, lat = extract_coordinates(response)
        distance = calculate_distance([lon, lat], label)
    except Exception as e:
        error_writer.write("### response:{}, answer:{} ###\n".format(response, label))
        metrics['exception'] = metrics.get('exception', 0) + 1
        return metrics
    if distance>=100000:
        error_writer.write("### response:{}, answer:{} ###\n".format(response, label))
        metrics['exception'] += 1
    else:
        metrics['mae'] = metrics.setdefault('mae', 0) + distance
        metrics['total'] += 1
    return metrics

def flow_prediction(response, label, error_writer, metrics):
    try:
        seq_pattern = r'(\[?\s*-?\d+\.?\d*(?:\s*,\s*-?\d+\.?\d*){5}\s*\]?)'
        seq_match = re.search(seq_pattern, response)
        
        if not seq_match:
            raise ValueError("No valid 6-number sequence found")

        seq_str = seq_match.group(1).strip("[]")
        decimals = [float(x) for x in seq_str.split(",")]
        
        predicted = np.array(decimals)

        # 根据label计算mae和rmse
        ans = np.array(label)
        mae = np.mean(np.abs(ans - predicted))
        rmse = math.sqrt(np.mean(np.power(ans - predicted, 2)))
        
        metrics['mae'] = metrics.setdefault('mae', 0) + mae
        metrics['rmse'] = metrics.setdefault('rmse', 0) + rmse
        metrics['total'] += 1

    except Exception as e:
        error_writer.write(f"### response:{response}, ### answer:{label}, error:{e} ###\n")    
        metrics['exception'] += 1
    
    return metrics