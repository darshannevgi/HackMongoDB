import voyageai
client = voyageai.Client(
    api_key= "pa-f2CwBqGGP4uJUJ7UTyqybb2wx3gXPAHVKpHNLw-WuOO"
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