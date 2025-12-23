# pip install tiktoken

import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o")
# enc = tiktoken.get_encoding("gpt-5")



text = "Hey There! My name is Om Prakash"
token = enc.encode(text)

# Token: [25216, 3274, 0, 3673, 1308, 382, 17105, 2284, 129178]
print(f"Token: {token}")


decoded = enc.decode(token)
print(f"decoded: {decoded}")



