from model_inference import *
from config import result_parsers, dataset_files
from tqdm import tqdm
import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

models = [chatgpt, gpt4o, deepseek_r1, deepseek_chat, deepseek_distill_llama_70b, gemini_25_pro_thinking, grok_4, deepseek_distill_qwen_1_5b, deepseek_distill_qwen_7b, deepseek_distill_qwen_14b, claude_sonnet_4_thinking, gpt_4_1, kimi_k2, doubao_1_5_pro_32k, qwen3_235b_a22b_thinking_2507, qwen3_235b_a22b_instruct_2507]

tasks = ["poi_category_recognition", "poi_identification", "urban_region_function_recognition", "administrative_region_determination", "point_trajectory", "point_region", "trajectory_region", "trajectory_identification", "trajectory_trajectory", "direction_determination", "navigation", "flow_prediction", "trajectory_anomaly_detection", "trajectory_classification", "trajectory_prediction"]

def process_item(model, item, task, result_parser, error_writer, result_filename):
    metrics_update = {"total": 0, "exception": 0}
    try:
        response = model.generate_with_retry(item["Question"], None)
        answer_content = response.choices[0].message.content
        reasoning_content = getattr(response.choices[0].message, 'reasoning_content', "")
        
        item_res = {
            "Question": item["Question"],
            "Answer": item["Answer"],
            "reasoning_content": reasoning_content,
            "answer_content": answer_content
        }

        with lock:
            with open(result_filename, "a") as res_writer:
                json_line = json.dumps(item_res)
                res_writer.write(json_line + "\n")

        metrics = result_parser(
            answer_content,
            item["Answer"],
            error_writer,
            {"total": 0, "exception": 0}
        )
        metrics_update.update(metrics)
        
    except Exception as e:
        error_writer.write(f"Error processing item: {str(e)}\n")

    return item_res, metrics_update

if not os.path.exists("./logs"):
    os.mkdir("./logs")
if not os.path.exists("./results"):
    os.mkdir("./results")
lock = threading.Lock()

for fun in models:
    model = fun()
    for task in tasks:
        error_writer = open("./logs/{}.log".format(task), 'a')
        error_writer.write(model.model_path+'\n')
        result_parser = result_parsers[task]
        for dataset_path in dataset_files[task]:
            subtask_name = dataset_path.split("/")[-1].replace(".jsonl", "")
            result_filename = f"./results/{subtask_name}_{model.__class__.__name__}.json"
            if not os.path.exists(result_filename):
                with open(result_filename, "w") as f:
                    pass
            finish_items = []
            with open(result_filename, "r") as res_writer:
                res_file = res_writer.readlines()
                for item in res_file:
                    item = json.loads(item)
                    finish_items.append(item['Question'])

            with open(dataset_path, "r") as f:
                dataset = [json.loads(line) for line in f.readlines()]

            metrics = {"total": 0, "exception": 0}
            results = []

            with ThreadPoolExecutor(max_workers=500) as executor:
                futures = []
                need_num = len(dataset)
                for item in dataset:
                    if item["Question"] in finish_items:
                        need_num -= 1
                        continue
                    future = executor.submit(
                        process_item,
                        model,
                        item,
                        task,
                        result_parser,
                        error_writer,
                        result_filename
                    )
                    futures.append(future)

                for future in tqdm(as_completed(futures), total=need_num):
                    try:
                        item_res, metric_update = future.result()
                        results.append(item_res)
                        for k, v in metric_update.items():
                            metrics[k] = metrics.get(k, 0) + v
                    except Exception as e:
                        error_writer.write(f"Processing failed: {str(e)}\n")

            message = f"Dataset: {dataset_path}\nTotal: {metrics['total']}, exception: {metrics['exception']}"
            for key in metrics:
                if key not in ["total", "exception"]:
                    message += f", {key}: {metrics[key]/metrics['total']:.4f}"
            message += "\n\n"
            error_writer.write(message)
            print(message)

        print(f"Completed processing for {task}")