import os
import requests

class OpenRouterChat:
    def __init__(self, id: str):
        self.model = id
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"

    def run(self, prompt, stream=False):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "https://yourdomain.com",  # optional
            "Content-Type": "application/json"
        }
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
        }
        response = requests.post(self.base_url, json=data, headers=headers)
        content = response.json()["choices"][0]["message"]["content"]
        return type("Response", (object,), {"content": content})
