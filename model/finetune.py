import replicate
import os
import json
from dotenv import load_dotenv

dotenv_path = '.config.env'
load_dotenv(dotenv_path=dotenv_path)
api_token = os.getenv('REPLICATE_API_TOKEN')

# if api_token is None:
#     raise ValueError("API token is not set in the environment variables.")
# else:
#     print("API Token retrieved successfully!")



# GET VERSION OF MODEL
import requests

def list_model_versions(model_owner, model_name):
    url = f"https://api.replicate.com/v1/models/{model_owner}/{model_name}"
    headers = {'Authorization': f'Bearer {api_token}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        versions = response.json()
        print(json.dumps(versions, indent=4))
        # for version in versions['results']:
            # print(f"Version ID: {version['id']}, Created At: {version['created_at']}")
    else:
        print("Failed to retrieve model versions:", response.status_code)

# # Example usage
# list_model_versions("meta", "meta-llama-3-8b")


training = replicate.trainings.create(
  version="meta/llama-2-7b:73001d654114dad81ec65da3b834e2f691af1e1526453189b7bf36fb3f32d0f9",
  input={
    "train_data": "https://mighty303.github.io/discord-dataset/training_data.jsonl",
    "num_train_epochs": 3
  },
  destination="mighty303/martin-gpt"
)

# print(training)

