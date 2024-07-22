import replicate
import os
from dotenv import load_dotenv

dotenv_path = '.config.env'
load_dotenv(dotenv_path=dotenv_path)
api_token = os.getenv('REPLICATE_API_TOKEN')

prompt = input('')

output = replicate.run(
    "mighty303/martin-gpt:3d0c1a4514314a426d213c0d2b6553356866b79fad520ba601b55fca4a47343d",
    input={
        "debug": False,
        "top_k": 50,
        "top_p": 0.9,
        "prompt": prompt,
        "temperature": 0.75,
        "max_new_tokens": 128,
        "min_new_tokens": -1
    }
)

# The mighty303/martin-gpt model can stream output as it's running.
# The predict method returns an iterator, and you can iterate over that output.

response = ''
for item in output:
    response += item
print(f'MartinGPT: {response}')