from openai import OpenAI
import os

fireworks = OpenAI(
    api_key="fw_2vKeHWeZyu99qXudDFe9ww",
    base_url="https://api.fireworks.ai/inference/v1"
)

models = fireworks.models.list()
print([m.id for m in models.data])