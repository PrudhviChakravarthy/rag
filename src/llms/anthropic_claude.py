import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic

load_dotenv()

class GetModel:
    def __init__(self, model_name='claude-3-opus-20240229'):
        self.model_name = model_name

    def load_model(self,temp = 0.2,top_p = 0.5):
        if temp < 0 or top_p < 0:
            raise ValueError("temperature or top_p cannot be less than 0")
        elif temp > 1 or top_p > 1:
            raise ValueError("temperature or top_p cannot be greater than 1")
        
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            raise ValueError("API Key not found.")
        return ChatAnthropic(
            api_key=api_key,
            model_name=self.model_name,
            temperature=temp,
            top_p = top_p
        )
    