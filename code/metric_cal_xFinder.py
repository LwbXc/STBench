import json
from config import dataset_files
from collections import defaultdict
from model_inference import *
from result_parser import *
from tqdm import tqdm

models = [deepseek_r1, deepseek_chat, deepseek_distill_llama_70b, gemini_25_pro_thinking, grok_4, deepseek_distill_qwen_1_5b, deepseek_distill_qwen_7b, deepseek_distill_qwen_14b, claude_sonnet_4_thinking, gpt_4_1, kimi_k2, doubao_1_5_pro_32k, qwen3_235b_a22b_thinking_2507, qwen3_235b_a22b_instruct_2507]

tasks = ["navigation"]

all_metrics = defaultdict(lambda: defaultdict(dict))

import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), "xFinder", "src"))
from  xfinder.eval import Evaluator

evaluator = Evaluator(
    model_name="xFinder-llama38it",
    inference_mode="local",
    model_path_or_url="/mnt/extent/LLM_model/xFinder/llama38it"
)

for model in models:
    fun = model()
    for task in tasks:
        error_writer = open(f"./logs/{task}_xFinder.log", 'a')
        error_writer.write(fun.model_path+'\n')
        for dataset_path in dataset_files[task]:
            subtask_name = dataset_path.split("/")[-1].replace(".jsonl", "")
            result_filename = f"./results/{subtask_name}_{fun.model_path}.json"
            metrics = {"exception": 0, "total": 0}
            with open(result_filename, "r") as f:
                total = sum(1 for _ in f)
            res_file = open(result_filename, "r").readlines()
            for i, item in tqdm(enumerate(res_file), total=len(res_file)):
                item = json.loads(item)
                question = item["Question"]
                llm_output = item["answer_content"]
                correct_answer = str(item["Answer"])
                range_type = "alphabet_option"

                if task.startswith("point_region"): standard_answer_range = extract_point_region(question)
                elif task.startswith("point_trajectory"): standard_answer_range = extract_point_trajectory(question)
                elif task.startswith("trajectory_region"): standard_answer_range = extract_option_trajectory_region(question)
                elif task == "administrative_region_determination" or task == "urban_region_function_recognition" or task == "poi_category_recognition": standard_answer_range = extract_parenthesized_options_with_colon_ard_pcr_urfr(question)
                else: standard_answer_range = extract_parenthesized_options_normal(question)
                metrics = xFinder_parser(question, llm_output, standard_answer_range, range_type, correct_answer, evaluator, error_writer, metrics)
            metrics = {'total': 100, 'exception':0, 'acc': 999}
            message = "Task: {}\nTotal: {}, exception:{}".format(task, metrics['total'], metrics['exception'])
            print(message)
            for key, value in metrics.items():
                if key != 'total' and key != 'exception':
                    message += ", {}:{}".format(key, value / metrics['total'])
            message += '\n\n'
            error_writer.write(message)
            error_writer.flush()
            print(f"{fun.model_path} {task} finish!!")

        error_writer.close()
        print("\n\n")
