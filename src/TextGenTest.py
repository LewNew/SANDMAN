import os

api_key = os.getenv("OPENAI_API_KEY")

if api_key:
    print("Key: ", api_key)
else:
    print("Key not found")