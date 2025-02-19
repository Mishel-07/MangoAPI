from mango import Mango

client = Mango()

while True:  
    user_input = input("You: ")
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": user_input}]
    )
    print("chatbot:", response.choices[0].message.content)
