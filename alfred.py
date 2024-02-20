import openai

class AlfredChat:
    def __init__(self, api_key):
        self.api_key = api_key

    def return_completion(self, messages):
        openai.api_key = self.api_key
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        # Assuming you want the content of the first choice's message
        return response.choices[0].message['content']
