import torch
from transformers import AutoModel, AutoTokenizer

print(torch.__version__)

# Load the RoBERTa model and tokenizer
model_name = "roberta-base"  # You can change this to any RoBERTa variant
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

text = "This is an example sentence for RoBERTa."

# Tokenize the text
inputs = tokenizer(text, return_tensors="pt")

# Forward the input through the model
outputs = model(**inputs)
