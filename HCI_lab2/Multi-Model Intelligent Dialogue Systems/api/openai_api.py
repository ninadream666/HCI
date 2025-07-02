from openai import OpenAI
from config import OPENAI_API_KEY  # 从配置中读取密钥

client = OpenAI(api_key=OPENAI_API_KEY)

def call_openai(prompt, history=None):
    messages = history if history else [{"role": "user", "content": prompt}]
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",  # 你可以换成 "gpt-4" 或 "gpt-3.5-turbo"
            messages=messages,
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"[OpenAI Error] {str(e)}"
