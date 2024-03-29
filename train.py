import os
import torch
from datasets import load_from_disk
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    TrainingArguments,
)
from peft import LoraConfig, PeftModel
from trl import SFTTrainer

from datasets import load_dataset, Dataset, DatasetDict

def read_text_file(file_path):
  """
  Reads the contents of a text file and returns it as a string.
  Args:
      file_path: The path to the text file.
  Returns:
      A string containing the contents of the text file.
  """
  with open(file_path, "r") as f:
    text = f.read()
  return text

# Function Usage

file_path = "/content/drive/MyDrive/record_fact.txt"
text = read_text_file(file_path)

def create_dataset_from_text(text):
    texts = [text]  # Split or preprocess your text as needed
    train_dataset = Dataset.from_dict({"text": texts})
    dataset_dict = DatasetDict({"train": train_dataset})
    return dataset_dict

# # Create dataset dict
dataset_dict = create_dataset_from_text(text)

# Define model and data path
model_name = "NousResearch/Llama-2-7b-chat-hf"
# file_path = '/path/to/your/data'  # Update this path accordingly

# Training parameters
output_dir = "./results"
num_train_epochs = 20
per_device_train_batch_size = 2
gradient_accumulation_steps = 1
learning_rate = 2e-4
weight_decay = 0.001
optim = "paged_adamw_32bit"
lr_scheduler_type = "cosine"
warmup_ratio = 0.03
group_by_length = True
logging_steps = 25
max_grad_norm = 0.3

# LoRA and bitsandbytes parameters
lora_r = 64
lora_alpha = 16
lora_dropout = 0.1
use_4bit = True
bnb_4bit_compute_dtype = "float16"
bnb_4bit_quant_type = "nf4"
use_nested_quant = False

# Load data
data = dataset_dict

# Training setup

compute_dtype = getattr(torch, bnb_4bit_compute_dtype)
bnb_config = BitsAndBytesConfig(
    load_in_4bit=use_4bit,
    bnb_4bit_quant_type=bnb_4bit_quant_type,
    bnb_4bit_compute_dtype=compute_dtype,
    bnb_4bit_use_double_quant=use_nested_quant,
)

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    quantization_config=bnb_config,
    device_map={"": 0},
    load_in_4bit=True  # Add this line
)
model.config.use_cache = False
model.config.pretraining_tp = 1

tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right"

peft_config = LoraConfig(
    lora_alpha=lora_alpha,
    lora_dropout=lora_dropout,
    r=lora_r,
    bias="none",
    task_type="CAUSAL_LM",
)

training_arguments = TrainingArguments(
    output_dir=output_dir,
    num_train_epochs=num_train_epochs,
    per_device_train_batch_size=per_device_train_batch_size,
    gradient_accumulation_steps=gradient_accumulation_steps,
    optim=optim,
    save_steps=0,
    logging_steps=logging_steps,
    learning_rate=learning_rate,
    weight_decay=weight_decay,
    fp16=False,
    bf16=False,
    max_grad_norm=max_grad_norm,
    max_steps=-1,
    warmup_ratio=warmup_ratio,
    group_by_length=group_by_length,
    lr_scheduler_type=lr_scheduler_type,
    # lr_scheduler_type=lr_scheduler_type,
    report_to="tensorboard"
)

train_dataset = data["train"]

trainer = SFTTrainer(
    model=model,
    train_dataset=train_dataset,
    peft_config=peft_config,
    dataset_text_field="text",
    max_seq_length=None,
    tokenizer=tokenizer,
    args=training_arguments,
    packing=False,
)

trainer.train()
new_model = "llama-2-7b-NFLGPT"
trainer.model.save_pretrained(new_model)

