import random

def formatting_func_space(example):
    output_texts = []
    for i in range(len(example['Question'])):
        text = f"{example['Question'][i]} {example['Answer'][i]}"
        output_texts.append(text)
    random.shuffle(output_texts)
    return output_texts

def formatting_func_without_space(example):
    output_texts = []
    for i in range(len(example['Question'])):
        text = f"{example['Question'][i]}{example['Answer'][i]}"
        output_texts.append(text)
    random.shuffle(output_texts)
    return output_texts

def trajectory_region_formatting(example):
    output_texts = []
    for i in range(len(example['Question'])):
        text = f"{example['Question'][i]}({example['Answer'][i]}"
        output_texts.append(text)
    random.shuffle(output_texts)
    return output_texts