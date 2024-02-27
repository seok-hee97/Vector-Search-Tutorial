import pymongo
import os
import requests


hf_token = os.environ["HF_TOKEN"]
password = os.environ["MongoDB_PASSWORD"]
client = pymongo.MongoClient(f"mongodb+srv://cycloevan97:{password}@cluster0.uajphwm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client.sample_mflix
collection =db.movices



embedding_url = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"

def generate_embedding(text: str) -> list[float]:

  response = requests.post(
    embedding_url,
    headers={"Authorization": f"Bearer {hf_token}"},
    json={"inputs": text})

  if response.status_code != 200:
    raise ValueError(f"Request failed with status code {response.status_code}: {response.text}")

  return response.json()

print(generate_embedding("freeCodeCamp is awesome"))

# for doc in collection.find({'plot':{"$exists": True}}).limit(50):
#   doc['plot_embedding_hf'] = generate_embedding(doc['plot'])
#   collection.replace_one({'_id': doc['_id']}, doc)

# query = "imaginary characters from outer space at war"

# results = collection.aggregate([
#   {"$vectorSearch": {
#     "queryVector": generate_embedding(query),
#     "path": "plot_embedding_hf",
#     "numCandidates": 100,
#     "limit": 4,
#     "index": "PlotSemanticSearch",
#       }}
# ]);

# for document in results:
#     print(f'Movie Name: {document["title"]},\nMovie Plot: {document["plot"]}\n')