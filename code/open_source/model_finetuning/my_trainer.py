import torch
import pdb

from transformers import AutoTokenizer, HfArgumentParser, AutoModelForCausalLM, BitsAndBytesConfig, TrainingArguments
from datasets import load_dataset
from peft import LoraConfig, PeftModel
from trl import SFTTrainer
import os
import random

def sft(ScriptArguments, model_id, formatting_func, datasets, save_path):
    parser = HfArgumentParser(ScriptArguments)
    script_args = parser.parse_args_into_dataclasses()[0]

    quantization_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_quant_type="nf4"
    )

    # Load model
    model = AutoModelForCausalLM.from_pretrained(
        model_id, 
        quantization_config=quantization_config, 
        torch_dtype=torch.float32,
        attn_implementation="sdpa" if not script_args.use_flash_attention_2 else "flash_attention_2"
    )

    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_id)

    lora_config = LoraConfig(
        r=script_args.lora_r,
        target_modules=["q_proj", "o_proj", "k_proj", "v_proj", "gate_proj", "up_proj", "down_proj"],
        bias="none",
        task_type="CAUSAL_LM",
        lora_alpha=script_args.lora_alpha,
        lora_dropout=script_args.lora_dropout
    )

    train_dataset = load_dataset('json', data_files={'train': datasets['train'], 'test': datasets['valid']}, split='train')

    training_arguments = TrainingArguments(
        output_dir=save_path,
        per_device_train_batch_size=script_args.per_device_train_batch_size,
        gradient_accumulation_steps=script_args.gradient_accumulation_steps,
        optim=script_args.optim,
        save_steps=script_args.save_steps,
        logging_steps=script_args.logging_steps,
        learning_rate=script_args.learning_rate,
        max_grad_norm=script_args.max_grad_norm,
        max_steps=script_args.max_steps,
        warmup_ratio=script_args.warmup_ratio,
        lr_scheduler_type=script_args.lr_scheduler_type,
        gradient_checkpointing=script_args.gradient_checkpointing,
        fp16=script_args.fp16,
        bf16=script_args.bf16,
    )

    trainer = SFTTrainer(
        model=model,
        args=training_arguments,
        train_dataset=train_dataset,
        peft_config=lora_config,
        packing=False,
        tokenizer=tokenizer,
        max_seq_length=script_args.max_seq_length,
        formatting_func=formatting_func,
    )

    trainer.train()

    # merge
    base_model = AutoModelForCausalLM.from_pretrained(
            model_id,
            load_in_8bit=False,
            torch_dtype=torch.float32,
            device_map={"": "cuda:0"},
    )

    lora_model = PeftModel.from_pretrained(
            base_model,
            os.path.join(save_path, "checkpoint-{}".format(script_args.max_steps)),
            device_map={"": "cuda:0"},
            torch_dtype=torch.float32,
    )

    model = lora_model.merge_and_unload()
    lora_model.train(False)

    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model.save_pretrained(os.path.join(save_path, "merged_model"))
    tokenizer.save_pretrained(os.path.join(save_path, "merged_model"))