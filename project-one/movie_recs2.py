import pymongo
import openai
import os
from dotenv import load_dotenv

load_dotenv()


password = os.environ["MongoDB_PASSWORD"]
print("password : ", password)


# Set your OpenAI API key
openai.api_key = os.environ["OPENAI_API_KEY"]
print(openai.api_key)

client = pymongo.MongoClient(f"mongodb+srv://cycloevan97:{password}@cluster0.uajphwm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client.sample_mflix
collection = db.embedded_movies

def generate_embedding(text: str) -> list[float]:

    response = openai.Embedding.create(
        model="text-embedding-ada-002", 
        input=text
    )
    return response['data'][0]['embedding']

query = "imaginary characters from outer space at war"

results = collection.aggregate([
  {"$vectorSearch": {
    "queryVector": generate_embedding(query),
    "path": "plot_embedding",
    "numCandidates": 100,
    "limit": 4,
    "index": "PlotSemanticSearch",
      }}
]);

for document in results:
    print(f'Movie Name: {document["title"]},\nMovie Plot: {document["plot"]}\n')