import os
import dotenv
import openai
import requests

import log
logger = log.setup_logger()

dotenv.load_dotenv()
# access open api
openai.organization = os.getenv("OPENAI_ORG_KEY")
openai.api_key = os.getenv("OPENAI_API_KEY")


class AlfredChat:
    # change the arguments here to change response behaviour
    # def __init__(self, prompt: str, engine: str = "gpt-3.5-turbo", tokens: int = 300):
    def __init__(self, engine: str = "text-davinci-003", tokens: int = 300):
        self.engine = engine
        # self.prompt = prompt
        self.tokens = tokens

    def __str__(self):
        completion = openai.Completion.create(
            engine=self.engine, prompt=self.prompt, max_tokens=100)
        return f"{completion.choices[0].text}"

    def return_completion(self, prompt: str, custom_prompt: str = None, engine: str = None, tokens: int = None):
        if custom_prompt is not None:
            prompt = custom_prompt + prompt + "Please do not include the entire previous context in your next message unless asked about it or explicitly told to. "

        # Use the class variables instead of the non-existent _engine and _tokens
        engine = engine if engine is not None else self.engine
        tokens = tokens if tokens is not None else self.tokens

        completion = openai.Completion.create(
            engine=engine, prompt=prompt, max_tokens=tokens)
        return f"{completion.choices[0].text}"

    # def get_sentiment(self):
    #     data = {
    #         "model": self.engine,
    #         # ...
    #     }
    #     headers = {
    #         "Authorization": f"Bearer {openai.api_key}"
    #     }
    #     response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
    #     result = response.json()
    #
    #     if 'error' in result:
    #         logger.error(f"API Error: {result['error']}")
    #         return 0
    #
    #     try:
    #         score = int(result.get('choices', [{}])[0].get('message', {}).get('content', '0').strip())
    #         logger.info(f"Sentiment Score: {score}")
    #     except (ValueError, TypeError, KeyError) as e:
    #         logger.error(f"Exception occurred: {e}")
    #         score = 0
    #
    #     return score
    #
    # def analyze_sentiment(prompt: str):
    #     score = AlfredChat(prompt=prompt).get_sentiment()
    #     logger.info(f"Received score: {score}, type: {type(score)}")
    #     return score


