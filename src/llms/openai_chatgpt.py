from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import os

load_dotenv()

class GetModel:
    def __init__(self, model_name='gpt-4o-mini'):
        self.model_name = model_name

    def load_model(self,temp = 0.5, top_p = 0.5):
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("API Key not found.")
        return ChatOpenAI(
            api_key=api_key,
            model_name=self.model_name,
            temperature=temp,
            top_p = top_p
        )
