# Simple Fine-Tuning Example using Hugging Face Transformers
# Install first:
# pip install transformers datasets torch accelerate

from datasets import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    Trainer,
    TrainingArguments
)

# Small training data
training_data = [
    {"text": "Question: What is Python? Answer: Python is a programming language."},
    {"text": "Question: What is RAG? Answer: RAG stands for Retrieval-Augmented Generation."},
    {"text": "Question: What is OpenRouter? Answer: OpenRouter provides access to multiple AI models using one API."}
]

# Convert to dataset
train_dataset = Dataset.from_list(training_data)

# Small model for demo
model_name = "distilgpt2"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# GPT2 models need pad token
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

# Tokenization function
def tokenize_function(example):
    tokens = tokenizer(
        example["text"],
        truncation=True,
        padding="max_length",
        max_length=128
    )
    tokens["labels"] = tokens["input_ids"].copy()
    return tokens

# Tokenize dataset
tokenized_dataset = train_dataset.map(tokenize_function)

# Training arguments
training_args = TrainingArguments(
    output_dir="./fine_tuned_model",
    per_device_train_batch_size=2,
    num_train_epochs=3,
    save_strategy="epoch",
    logging_steps=1,
    report_to="none"
)

# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset
)

print("Starting fine-tuning...\n")
trainer.train()

# Save model
trainer.save_model("./fine_tuned_model")
tokenizer.save_pretrained("./fine_tuned_model")

print("\nFine-tuning completed!")
print("Model saved in ./fine_tuned_model")