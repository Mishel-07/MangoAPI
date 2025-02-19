from mango import Mango

def run_mango_client(user_input):
    client = Mango()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": user_input}]
    )
    return response.choices[0].message.content

if __name__ == "__main__":    
    print(run_mango_client("hi"))
