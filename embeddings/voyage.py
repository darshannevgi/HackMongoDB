import os

import voyageai
client = voyageai.Client(
    api_key= os.getenv("VOYAGE_API_KEY")
)

def embed(text: str):
    """
    Returns a vector embedding for the given text using Voyage AI.
    """
    result = client.embed(
        texts=[text],
        model="voyage-2"
    )
    return result.embeddings[0]