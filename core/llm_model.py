from gpt4all import GPT4All
from config import MODEL_PATH

model = GPT4All(MODEL_PATH, allow_download=False)
