from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

class GetModel:
    def __init__(self, model_name='gemini-pro'):
        self.model_name = model_name
        

    def load_model(self,temp, top_p):
        if temp < 0 or top_p < 0:
            raise ValueError("temperature or top_p cannot be less than 0")
        elif temp > 1 or top_p < 0:
            raise ValueError("temperature or top_p cannot be greater than 1")
        
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            raise ValueError("API Key not found.")

        return ChatGoogleGenerativeAI(
            api_key=api_key,
            model=self.model_name,
            temperature=temp,
            top_p=top_p,
        )
    
