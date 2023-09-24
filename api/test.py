# import os
#
# key = os.environ.get("OPENAI_API_KEY")
# print(key)


import os
import openai

#temporary variable to store my api key
api_key = [REDACTED]

# Set OpenAI API key
openai.api_key = api_key

def interactive_script():
    # Prompt the user for input
    user_input = input("Please type something: ")

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user", "content": user_input
            }
        ]
    )



    print(response['choices'][0]['message']['content'])

# Call the function
interactive_script()