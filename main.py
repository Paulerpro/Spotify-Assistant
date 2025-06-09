from langchain_mistralai.chat_models import ChatMistralAI

import os
from dotenv import load_dotenv

load_dotenv()
mistal_key = os.getenv("MISTRAL_API_KEY")

llm = ChatMistralAI(api_key=mistal_key, model_name="mistral-medium-2505", temperature=0, max_retries=2)

messages = [
    (
        "system",
        "You are a helpful assistant that translates English to French. Translate the user sentence.",
    ),
    ("human", "I love programming."),
]

response = llm.invoke(messages)

print(response.content)