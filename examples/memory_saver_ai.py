# This AI chatbot saves all conversation history and uses it to respond to user inputs,
# allowing it to "remember" previous conversations and adapt its responses accordingly.

from mango import Mango

conversation_memory = [] 

def chat_with_assassistant(user_input):
    client = Mango()
    conversation_memory.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=conversation_memory
    )    

    conversation_memory.append({"role": "assistant", "content": response.choices[0].message.content})

    print("Assistant:", response.choices[0].message.content)

if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        chat_with_assassistant(user_input)
