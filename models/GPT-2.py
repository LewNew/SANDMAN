from transformers import GPT2LMHeadModel, GPT2Tokenizer


def generate_text(prompt, max_length=200):
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    model = GPT2LMHeadModel.from_pretrained("gpt2")

    inputs = tokenizer.encode(prompt, return_tensors="pt")

    # Explicitly set attention_mask to avoid the warning
    attention_mask = inputs.clone().fill_(1)

    outputs = model.generate(inputs, max_length=max_length, num_return_sequences=1, attention_mask=attention_mask)

    return tokenizer.decode(outputs[0], skip_special_tokens=True)


prompt = "Discuss the role of generative AI"
generated_text = generate_text(prompt)
print(generated_text)
