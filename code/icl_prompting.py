from model_inference import *
from config import result_parsers, dataset_files, max_tokens, icl_files
from tqdm import tqdm
import json
import os

models = [gemma2b, llama2_7b]
tasks = ["poi_identification", "trajectory_region", "trajectory_trajectory", "direction_determination", "trajectory_anomaly_detection", "trajectory_prediction"]

if not os.path.exists("./logs"):
    os.mkdir("./logs")

for fun in models:
    model = fun()
    for task in tasks:
        error_writer = open("./logs/icl_{}.log".format(task), 'a')
        error_writer.write(model.model_path+'\n')
        result_parser = result_parsers[task]
        
        context_samples = open(icl_files[task])
        prompt = ""
        for _i, sample in enumerate(context_samples.readlines()):
            sample = json.loads(sample)
            prompt += "{}{}\n".format(sample['Question'], sample['Answer'])

        for dataset_path in dataset_files[task]:
            dataset = open(dataset_path, 'r')
            dataset = dataset.readlines()

            correct = 0
            total = 0
            exception = 0

            for i, item in tqdm(enumerate(dataset), total=len(dataset)):
                item = json.loads(item)
                response = model.generate(prompt+item["Question"], max_tokens[task])
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
