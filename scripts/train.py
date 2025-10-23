import logging
import os
from datetime import datetime
from datasets import load_dataset
from trl import SFTConfig, SFTTrainer
from utils.args import parse_args
from unsloth import FastLanguageModel
import torch

from utils.dataset import parse_str_to_dict
from utils.prompt import format_alpaca_prompt_style


class CustomTrainer(SFTTrainer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    def log(self, logs):
        super().log(logs)
        logging.info(f"Logs: {logs}")

if __name__ == '__main__':
    args = parse_args()
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        model_name = args.model.replace("/", "-").lower()

        log_filename = f"logs/train/{args.rubric_item}/{model_name}_{timestamp}.log"
        log_dir = f"logs/train/{args.rubric_item}"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        logging.basicConfig(filename=log_filename, level=logging.INFO)
        logging.info("starting training")

        max_seq_length = 16784 # Choose any! We auto support RoPE Scaling internally!
        dtype = None # None for auto detection. Float16 for Tesla T4, V100, Bfloat16 for Ampere+
        load_in_4bit = True # Use 4bit quantization to reduce memory usage. Can be False.

        model, tokenizer = FastLanguageModel.from_pretrained(
            model_name = args.model,
            max_seq_length = max_seq_length,
            load_in_4bit = load_in_4bit,     # 4bit uses much less memory
            dtype = dtype,
            load_in_8bit = False,    # A bit more accurate, uses 2x memory
            full_finetuning = False,
        )

        model = FastLanguageModel.get_peft_model(
            model,
            r = 32,
            target_modules = [
                "q_proj",
                "k_proj",
                "v_proj",
                "o_proj",
                "gate_proj",
                "up_proj",
                "down_proj",
            ],
            lora_alpha = 32,
            lora_dropout = 0,
            bias = "none",
            # [NEW] "unsloth" uses 30% less VRAM, fits 2x larger batch sizes!
            use_gradient_checkpointing = "unsloth", # True or "unsloth" for very long context
            random_state = 3407,
            use_rslora = False,   # We support rank stabilized LoRA
            loftq_config = None,  # And LoftQ
        )

        logging.info(f"preparing dataset for rubric item: {args.rubric_item}")



        train = load_dataset("maczg/coat-dataset", args.rubric_item, split="train")
        train = train.map(parse_str_to_dict)

        train = train.map(format_alpaca_prompt_style, batched=True, fn_kwargs={"tokenizer": tokenizer})

        trainer = CustomTrainer(
            model = model,
            tokenizer = tokenizer,
            train_dataset = train,
            dataset_text_field = "text",
            max_seq_length = max_seq_length,
            args = SFTConfig(
                per_device_train_batch_size = 2,
                gradient_accumulation_steps = 4,
                # Use num_train_epochs = 1, warmup_ratio for full training runs!
                warmup_steps = 5,
                max_steps = 60,
                learning_rate = 2e-4,
                logging_steps = 1,
                optim = "adamw_8bit",
                weight_decay = 0.01,
                lr_scheduler_type = "linear",
                seed = 3407,
                output_dir = "outputs",
                report_to = "none", # Use TrackIO/WandB etc
            ),
        )

        # @title Show current memory stats
        gpu_stats = torch.cuda.get_device_properties(0)
        start_gpu_memory = round(torch.cuda.max_memory_reserved() / 1024 / 1024 / 1024, 3)
        max_memory = round(gpu_stats.total_memory / 1024 / 1024 / 1024, 3)
        logging.info(f"GPU = {gpu_stats.name}. Max memory = {max_memory} GB.")
        logging.info(f"{start_gpu_memory} GB of memory reserved.")

        trainer_stats = trainer.train()

        # @title Show final memory and time stats
        used_memory = round(torch.cuda.max_memory_reserved() / 1024 / 1024 / 1024, 3)
        used_memory_for_lora = round(used_memory - start_gpu_memory, 3)
        used_percentage = round(used_memory / max_memory * 100, 3)
        lora_percentage = round(used_memory_for_lora / max_memory * 100, 3)
        logging.info(f"{trainer_stats.metrics['train_runtime']} seconds used for training.")
        logging.info(
            f"{round(trainer_stats.metrics['train_runtime']/60, 2)} minutes used for training."
        )
        logging.info(f"Peak reserved memory = {used_memory} GB.")
        logging.info(f"Peak reserved memory for training = {used_memory_for_lora} GB.")
        logging.info(f"Peak reserved memory % of max memory = {used_percentage} %.")
        logging.info(f"Peak reserved memory for training % of max memory = {lora_percentage} %.")

        model.save_pretrained("lora_model")  # Local saving
        tokenizer.save_pretrained("lora_model")
    except Exception as e:
        logging.error(f"error during training: {e}")
        import torch
        import gc
        torch.cuda.empty_cache()
        gc.collect()
        exit(1)






