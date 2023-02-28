import openai
openai.api_key = "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"



class gpt3Interface:
    prompt= "The following is a conversation with an AI assistant that plays the role of a virtual nurse in a home care facility for seniors. The assistant is helpful, creative, clever, and very friendly. The assistant does not talk about controversial topics; rather, it cleverly steers the conversation to a more pleasant topic. After ten conversational turns, the assistant should terminate the conversation."

    def sendCompletionQuery(self, text):
     gpt3Interface.prompt = gpt3Interface.prompt + " Human: "+ text + ". AI assistant:"
     print("Sending prompt:")
     print(gpt3Interface.prompt)

     try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=gpt3Interface.prompt,
            temperature=0.7,
            logprobs=10,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=[" \n\n"]
        )

        gpt3_response =  response['choices'][0]['text']
        gpt3Interface.prompt = gpt3Interface.prompt + gpt3_response
        return gpt3_response
     except Exception as e:
        print('Error: openai request failed')

#
def main():
    gp = gpt3Interface()

    while(True):
        text = input("Type:")
        print(gp.sendCompletionQuery(text))


if __name__ == "__main__":
    main()