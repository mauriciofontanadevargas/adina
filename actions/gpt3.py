import openai
openai.api_key = "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"

# mfv:
# Simplest implementation possible
# There are lot of opportunities for improving gpt3 for our case
# E.g., using the tips from ai, i.e., explaining gpt3's goals and giving examples before sending user query
# e.g., sending entire conversation every time instead of only last sentence

def sendCompletionQuery(text):
 try:
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="\n\n" + text,
        temperature=0.7,
        logprobs=10,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=[" \n\n"]
    )

    return response['choices'][0]['text']
 except Exception as e:
    print('Error: openai request failed')

# #
# def main():
#
#     print(sendCompletionQuery("I hate you your miserable"))
#
#
# if __name__ == "__main__":
#     main()