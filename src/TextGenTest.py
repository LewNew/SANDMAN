from transformers import AutoModelForCausalLM, AutoTokenizer
from Mood import Mood

class TextGenerator:

    def __init__(self, model_name):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, padding_side="left")
        self.model = AutoModelForCausalLM.from_pretrained(model_name, is_decoder=True)

    def generate_text(self, task, persona, mood):
        # Construct the prompt
        prompt = f"Task: {task}. Persona: {persona}. Mood: {mood}. Write the following:"

        # Tokenize the prompt
        input_ids = self.tokenizer.encode(prompt, return_tensors="pt", max_length=100, truncation=True, padding="max_length")


        # Generate text using RoBERTa
        output = self.model.generate(input_ids, max_length=150, num_return_sequences=1, pad_token_id=self.tokenizer.eos_token_id)
        generated_text = self.tokenizer.decode(output[0], skip_special_tokens=True)

        return generated_text

    def generate_file_name(self, task, persona):
        base_name = f"{persona}_{task}".replace(" ", "_")
        return f"{base_name}.txt"

if __name__ == "__main__":
    # Initialize the Mood object (assuming you've already done so)
    agent_mood = Mood()
    agent_mood.randomize_mood()

    # Define the task and persona
    task_description = "Write a report"
    persona_description = "Research Analyst"

    # Retrieve the current mood of the agent
    current_mood = agent_mood.get_mood()

    # Initialize and use the TextGenerator
    roberta_model_name = "roberta-base"  # Or any other RoBERTa variant
    text_generator = TextGenerator(model_name=roberta_model_name)
    generated_text = text_generator.generate_text(task_description, persona_description, current_mood)

    # Output the results
    print(f"Mood: {current_mood}")
    print(f"Generated Text:\n{generated_text}")
