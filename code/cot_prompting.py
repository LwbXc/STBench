from model_inference import *
from config import dataset_files, cot_files
from result_parser import find_option_number_for_cot
from tqdm import tqdm
import json
import os

models = [gemma2b]
tasks = ["urban_region_function_recognition", "trajectory_region", "trajectory_trajectory", "trajectory_classification"]

if not os.path.exists("./logs"):
    os.mkdir("./logs")

for fun in models:
    model = fun()
    for task in tasks:
        error_writer = open("./logs/cot_{}.log".format(task), 'a')
        error_writer.write(model.model_path+'\n')

        context_samples = open(cot_files[task])
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
                response = model.generate(prompt+item["Question"], 100)
                score = find_option_number_for_cot(response, item["Answer"], error_writer)
                
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
