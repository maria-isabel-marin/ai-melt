import os
import requests
from models.base import BaseModel

class LLaMAModel(BaseModel):
    def __init__(self, config):
        super().__init__(config)
        self.api_url = config["api_url"]
        self.api_key = os.getenv(config["api_key_env"])

    def detect_metaphors(self, sentences):
        prompt = (
            "Lista todas las metáforas presentes en las siguientes frases, indicando la frase y la expresión metafórica.\n"
            f"Frases:\n{chr(10).join(sentences)}"
        )
        response = requests.post(
            self.api_url,
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={"prompt": prompt, "max_tokens": 1024}
        )
        return response.json()