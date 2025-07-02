from openai import OpenAI
from config import DEEPSEEK_API_KEY  # 从配置文件读取 API key

# 注意：DeepSeek 用 OpenAI SDK，但 base_url 改为 deepseek 的
client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com"
)

def call_deepseek(prompt, history=None):
    messages = history if history else [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"[DeepSeek Error] {str(e)}"
