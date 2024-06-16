from model_inference import *
from config import result_parsers, dataset_files, max_tokens
from tqdm import tqdm
import json
import os

models = [chatglm2, chatglm3, deepseek7b, falcon7b, gemma2b, gemma7b, llama2_7b, mistral7b, phi2, qwen7b, vicuna7b, yi6b, chatgpt, gpt4o]
tasks = ["poi_category_recognition", "poi_identification", "urban_region_function_recognition", "administrative_region_determination", "point_trajectory", "point_region", "trajectory_region", "trajectory_identification", "trajectory_trajectory", "direction_determination", "trajectory_anomaly_detection", "trajectory_classification", "trajectory_prediction"]

if not os.path.exists("./logs"):
    os.mkdir("./logs")

for fun in models:
    model = fun()
    for task in tasks:
        error_writer = open("./logs/{}.log".format(task), 'a')
        error_writer.write(model.model_path+'\n')
        result_parser = result_parsers[task]
        for dataset_path in dataset_files[task]:
            dataset = open(dataset_path, 'r')
            dataset = dataset.readlines()

            correct = 0
            total = 0
            exception = 0

            for i, item in tqdm(enumerate(dataset), total=len(dataset)):
                item = json.loads(item)
                response = model.generate(item["Question"], max_tokens[task])
                score = result_parser(response, item["Answer"], error_writer)
                
                if task!='trajectory_prediction' or score is not None:
                    total +=1
                if score is None:
                    exception += 1
                else:
                    correct += score

                if i%100==0:
                    print("Dataset: {}\nTotal: {}, correct:{}, exception:{}, accuracy:{}\n\n".format(dataset_path, total, correct, exception, correct/total))
            
            error_writer.write("Dataset: {}\nTotal: {}, correct:{}, exception:{}, accuracy:{}\n\n".format(dataset_path, total, correct, exception, correct/total))
            error_writer.flush()
        error_writer.write("\n")
    error_writer.close()
