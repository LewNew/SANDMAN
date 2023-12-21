from openai import OpenAI

api_key = "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"

# Initialize the client with the API key
client = OpenAI(api_key=api_key)

def ChatGPT_request(prompt, system_msg):
    try:
        messages = [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": prompt}
        ]
        response = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)

        return response.choices[0].message["content"]
    except Exception as e:
        return f"ChatGPT ERROR: {e}"

'''
def GPT4_request(prompt):
    try:
        completion = client.chat.completions.create(model="gpt-4",
                                                    messages=[{"role": "user", "content": prompt}])
        return completion["choices"][0]["message"]["content"]
    except Exception as e:
        return f"ChatGPT ERROR: {e}"
'''