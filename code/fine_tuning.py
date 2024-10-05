from model_finetuning import formatting_func_without_space, formatting_func_space, trajectory_region_formatting, flow_prediction_formatting, sft
from model_inference import gemma2b
from config import ScriptArguments, sft_files, dataset_files, max_tokens, result_parsers
from tqdm import tqdm
import json
import os

models_path = '~/.cache/modelscope/hub/AI-ModelScope/gemma-2b'
tasks2formatting = {"administrative_region_determination": formatting_func_without_space, "direction_determination": formatting_func_without_space, "trajectory_anomaly_detection": formatting_func_space, "trajectory_prediction": formatting_func_space, "trajectory_region": trajectory_region_formatting, "trajectory_trajectory": formatting_func_without_space, "flow_prediction": flow_prediction_formatting}

if not os.path.exists("./save"):
    os.mkdir("./save")

if not os.path.exists("./logs"):
    os.mkdir("./logs")

for task, formatting_func in tasks2formatting.items():
    save_path = "./save/{}/".format(task)

    if not os.path.exists(save_path):
        os.mkdir(save_path)

    sft(ScriptArguments, models_path, formatting_func, sft_files[task], save_path)

    model = gemma2b(save_path+'merged_model')

    error_writer = open("./logs/{}.log".format(task), 'a')
    error_writer.write(save_path+'\n')
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
