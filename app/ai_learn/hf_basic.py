from transformers import pipeline

message = [
    {"role": "system", "content": "You are a pirate chatbot who always responds in pirate speak!"},
    {"role": "user", "content": "Who are you?"},
]

prompt = "You are a pirate. Answer like a pirate: Who are you?"

chatbot = pipeline("text-generation", model="gpt2")
# response = chatbot(message, max_new_tokens=100)
response = chatbot(prompt, max_new_tokens=100)

print(response)

