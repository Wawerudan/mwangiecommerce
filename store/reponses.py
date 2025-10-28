
import openai

def get_bot_reply(user_input):
    prompt = f"""
    You are Dan, the owner of an eCommerce store in Kenya. You speak warmly, confidently, and helpfully.
    Always introduce yourself as Dan when chatting with customers.
    Answer questions based on the catalog, policies, and common eCommerce queries.
    User: {user_input}
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    return response['choices'][0]['message']['content']