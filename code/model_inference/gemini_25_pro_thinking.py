from openai import OpenAI, APIError, OpenAI
import random
import time

class gemini_25_pro_thinking(object):

    def __init__(self):
        self.client = OpenAI(api_key="YOUR-KPI-KEY", 
                             base_url="YOUR_BASE_URL", 
                             timeout=1800)
        self.model_path = "gemini-2.5-pro-thinking"

    def generate(self, input_text, max_token):
        response = self.client.chat.completions.create(
            model="gemini-2.5-pro-thinking",
            messages=[
                {"role": "system", "content": "You are a helpful text completion assistant."},
                {"role": "user", "content": f"Please continue writing the following text: {input_text}"},
            ],
            stream=False,
            temperature=1,
        )
        return response

    def generate_with_retry(self, input_text, max_token):
        while True:
            try:
                response = self.client.chat.completions.create(
                    model="gemini-2.5-pro-thinking",
                    messages=[
                        {"role": "system", "content": "You are a helpful text completion assistant."},
                        {"role": "user", "content": f"Please continue writing the following text: {input_text}"},
                    ],
                    temperature=1,
                    stream=False,
                )
                if response.choices == None:
                    base_delay = 10
                    time.sleep(base_delay)
                    continue
            except Exception as e:
                continue
            return response

if __name__=='__main__':
    model = gemini_25_pro_thinking()
    print(model.generate_with_retry("Yesterday was Thursday, today is Friday, so tomorrow is ", 128))
    print(model.generate_with_retry("Yesterday was 2022-01-01, today is 2022-01-02, so tomorrow is ", 128))