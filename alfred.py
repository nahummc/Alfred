import os
import dotenv
import openai
import requests

dotenv.load_dotenv()
# access open api
openai.organization = os.getenv("OPENAI_ORG_KEY")
openai.api_key = os.getenv("OPENAI_API_KEY")


class AlfredChat:
    def __init__(self, prompt):
        # change the variables here to change response behaviour
        self.engine = "text-davinci-003"
        self.prompt = prompt
        self.tokens = 100
        

    def __str__(self):
        completion = openai.Completion.create(engine=self.engine, prompt=self.prompt, max_tokens=100)
        return f"{completion.choices[0].text}"


    def return_completion(self):
        completion = openai.Completion.create(engine=self.engine, prompt=self.prompt, max_tokens=self.tokens)
        print(completion.choices)
        return f"{completion.choices[0].text}"

