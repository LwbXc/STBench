from dataclasses import dataclass, field
from typing import Optional
from result_parser import yes_or_no, find_option_number, anomaly_detection, trajectory_prediction, trajectory_classification, flow_prediction

result_parsers = {
    "poi_category_recognition": find_option_number,
    "poi_identification": yes_or_no,
    "urban_region_function_recognition": find_option_number,
    "administrative_region_determination": find_option_number,
    "point_trajectory": find_option_number,
    "point_region": find_option_number,
    "trajectory_region": find_option_number,
    "trajectory_identification": yes_or_no,
    "trajectory_trajectory": find_option_number,
    "direction_determination": find_option_number,
    "trajectory_anomaly_detection": anomaly_detection,
    "trajectory_classification": trajectory_classification,
    "trajectory_prediction": trajectory_prediction,
    "flow_prediction": flow_prediction,
    "navigation": find_option_number,
    "road_level_judgment": find_option_number,
    "rush_hour_detection": yes_or_no,
    "texi_occupancy_detection": yes_or_no
}

max_tokens = {
    "poi_category_recognition": 15,
    "poi_identification": 15,
    "urban_region_function_recognition": 15,
    "administrative_region_determination": 15,
    "point_trajectory": 15,
    "point_region": 15,
    "trajectory_region": 15,
    "trajectory_identification": 15,
    "trajectory_trajectory": 15,
    "direction_determination": 15,
    "trajectory_anomaly_detection": 15,
    "trajectory_classification": 15,
    "trajectory_prediction": 50,
    "flow_prediction": 50,
    "navigation": 15,
    "road_level_judgment": 15,
    "rush_hour_detection": 15,
    "texi_occupancy_detection": 15
}

dataset_files = {
    "poi_category_recognition": ["../datasets/basic/knowledge_comprehension/poi_category_recognition.jsonl"],
    "poi_identification": ["../datasets/basic/knowledge_comprehension/poi_identification.jsonl"],
    "urban_region_function_recognition": ["../datasets/basic/knowledge_comprehension/urban_region_function_recognition.jsonl"],
    "administrative_region_determination": ["../datasets/basic/knowledge_comprehension/administrative_region_determination.jsonl"],
    "point_trajectory": ["../datasets/basic/spatiotemporal_reasoning/point_trajectory.jsonl"],
    "point_region": ["../datasets/basic/spatiotemporal_reasoning/point_region_2regions.jsonl", 
                     "../datasets/basic/spatiotemporal_reasoning/point_region_3regions.jsonl",
                     "../datasets/basic/spatiotemporal_reasoning/point_region_4regions.jsonl",
                     "../datasets/basic/spatiotemporal_reasoning/point_region_5regions.jsonl"],
    "trajectory_region": ["../datasets/basic/spatiotemporal_reasoning/trajectory_region_length2.jsonl",
                          "../datasets/basic/spatiotemporal_reasoning/trajectory_region_length4.jsonl",
                          "../datasets/basic/spatiotemporal_reasoning/trajectory_region_length6.jsonl",
                          "../datasets/basic/spatiotemporal_reasoning/trajectory_region_length8.jsonl",
                          "../datasets/basic/spatiotemporal_reasoning/trajectory_region_length10.jsonl"],
    "trajectory_identification": ["../datasets/basic/spatiotemporal_reasoning/trajectory_identification_downsampling.jsonl",
                                  "../datasets/basic/spatiotemporal_reasoning/trajectory_identification_staggered_sampling.jsonl",
                                  "../datasets/basic/spatiotemporal_reasoning/trajectory_identification_spatial_offset.jsonl",
                                  "../datasets/basic/spatiotemporal_reasoning/trajectory_identification_temporal_offset.jsonl"],
    "trajectory_trajectory": ["../datasets/basic/accurate_calculation/trajectory_trajectory.jsonl"],
    "direction_determination": ["../datasets/basic/accurate_calculation/direction_determination.jsonl"],
    "trajectory_anomaly_detection": ["../datasets/basic/downstream_applications/trajectory_anomaly_detection_abnormal.jsonl",
                                     "../datasets/basic/downstream_applications/trajectory_anomaly_detection_normal.jsonl"],
    "trajectory_classification": ["../datasets/basic/downstream_applications/trajectory_classification.jsonl"],
    "trajectory_prediction": ["../datasets/basic/downstream_applications/trajectory_prediction.jsonl"],
    "flow_prediction": ["../datasets/basic/downstream_applications/inflow_prediction.jsonl",
                        "../datasets/basic/downstream_applications/outflow_prediction.jsonl"],
    "navigation": ["../datasets/basic/accurate_calculation/navigation_with_weights_5.jsonl",
                   "../datasets/basic/accurate_calculation/navigation_with_weights_6.jsonl",
                   "../datasets/basic/accurate_calculation/navigation_with_weights_7.jsonl",
                   "../datasets/basic/accurate_calculation/navigation_with_weights_8.jsonl",
                   "../datasets/basic/accurate_calculation/navigation_without_weights_8.jsonl",
                   "../datasets/basic/accurate_calculation/navigation_without_weights_9.jsonl",
                   "../datasets/basic/accurate_calculation/navigation_without_weights_10.jsonl",
                   "../datasets/basic/accurate_calculation/navigation_without_weights_11.jsonl"],
    "road_level_judgment": ["../datasets/basic/semantic_reasoning/road_level_judgment.jsonl"],
    "rush_hour_detection": ["../datasets/basic/semantic_reasoning/rush_hour_detection.jsonl"],
    "texi_occupancy_detection": ["../datasets/basic/semantic_reasoning/taxi_occupancy_detection.jsonl"]
}

icl_files = {
    "poi_identification": "../datasets/icl/poi_identification.jsonl",
    "trajectory_region": "../datasets/icl/trajectory_region.jsonl",
    "trajectory_trajectory": "../datasets/icl/trajectory_trajectory.jsonl",
    "direction_determination": "../datasets/icl/direction_determination.jsonl",
    "trajectory_anomaly_detection": "../datasets/icl/trajectory_anomaly_detection.jsonl",
    "trajectory_prediction": "../datasets/icl/trajectory_prediction.jsonl"
}

cot_files = {
    "urban_region_function_recognition": "../datasets/cot/urban_region_function_recognition.jsonl",
    "trajectory_region": "../datasets/cot/trajectory_region.jsonl",
    "trajectory_trajectory": "../datasets/cot/trajectory_trajectory.jsonl",
    "trajectory_classification": "../datasets/cot/trajectory_classification.jsonl"
}

sft_files = {
    "administrative_region_determination": {
        "train": "../datasets/sft/administrative_region_determination_train.jsonl",
        "valid": "../datasets/sft/administrative_region_determination_valid.jsonl"
    },
    "direction_determination": {
        "train": "../datasets/sft/direction_determination_train.jsonl",
        "valid": "../datasets/sft/direction_determination_valid.jsonl"
    },
    "trajectory_anomaly_detection":{
        "train": "../datasets/sft/trajectory_anomaly_detection_train.jsonl",
        "valid": "../datasets/sft/trajectory_anomaly_detection_valid.jsonl"
    },
    "trajectory_prediction": {
        "train": "../datasets/sft/trajectory_prediction_train.jsonl",
        "valid": "../datasets/sft/trajectory_prediction_valid.jsonl"
    },
    "trajectory_region": {
        "train": "../datasets/sft/trajectory_region_train.jsonl",
        "valid": "../datasets/sft/trajectory_region_valid.jsonl"
    },
    "trajectory_trajectory": {
        "train": "../datasets/sft/trajectory_trajectory_train.jsonl",
        "valid": "../datasets/sft/trajectory_trajectory_valid.jsonl"        
    },
    "flow_prediction": {
        "train": "../datasets/sft/flow_prediction_train.jsonl",
        "valid": "../datasets/sft/flow_prediction_valid.jsonl"
    }
}

@dataclass
class ScriptArguments:
    """
    These arguments vary depending on how many GPUs you have, what their capacity and features are, and what size model you want to train.
    """
    per_device_train_batch_size: Optional[int] = field(default=4)
    per_device_eval_batch_size: Optional[int] = field(default=1)
    gradient_accumulation_steps: Optional[int] = field(default=4)
    learning_rate: Optional[float] = field(default=2e-4)
    max_grad_norm: Optional[float] = field(default=0.3)
    weight_decay: Optional[int] = field(default=0.001)
    lora_alpha: Optional[int] = field(default=16)
    lora_dropout: Optional[float] = field(default=0.1)
    lora_r: Optional[int] = field(default=8)
    max_seq_length: Optional[int] = field(default=2048)
    model_name: Optional[str] = field(
        default=None,
        metadata={
            "help": "The model that you want to train from the Hugging Face hub. E.g. gpt2, gpt2-xl, bert, etc."
        }
    )
    dataset_name: Optional[str] = field(
        default="stingning/ultrachat",
        metadata={"help": "The preference dataset to use."},
    )
    fp16: Optional[bool] = field(
        default=False,
        metadata={"help": "Enables fp16 training."},
    )
    bf16: Optional[bool] = field(
        default=False,
        metadata={"help": "Enables bf16 training."},
    )
    packing: Optional[bool] = field(
        default=True,
        metadata={"help": "Use packing dataset creating."},
    )
    gradient_checkpointing: Optional[bool] = field(
        default=True,
        metadata={"help": "Enables gradient checkpointing."},
    )
    use_flash_attention_2: Optional[bool] = field(
        default=False,
        metadata={"help": "Enables Flash Attention 2."},
    )
    optim: Optional[str] = field(
        default="paged_adamw_32bit",
        metadata={"help": "The optimizer to use."},
    )
    lr_scheduler_type: str = field(
        default="constant",
        metadata={"help": "Learning rate schedule. Constant a bit better than cosine, and has advantage for analysis"},
    )
    max_steps: int = field(default=1000, metadata={"help": "How many optimizer update steps to take"})
    warmup_ratio: float = field(default=0.03, metadata={"help": "Fraction of steps to do a warmup for"})
    save_steps: int = field(default=100, metadata={"help": "Save checkpoint every X updates steps."})
    logging_steps: int = field(default=10, metadata={"help": "Log every X updates steps."})
    output_dir: str = field(
        default="./results",
        metadata={"help": "The output directory where the model predictions and checkpoints will be written."},
    )
