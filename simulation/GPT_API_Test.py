from openai import OpenAI

client = OpenAI(api_key='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')

def main():
    prompt = "True or false: a banana is smaller than a lemon.\n\n"

    response = client.completions.create(
        prompt=prompt,
        model="gpt-3.5-turbo-instruct",
        top_p=0.5, max_tokens=50,
        stream=True)

    # Iterating over
    for part in response:
        print(part.choices[0].text or "")


if __name__ == "__main__":
    main()
