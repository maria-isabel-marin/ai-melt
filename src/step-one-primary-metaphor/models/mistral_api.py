import os
import requests
from models.base import BaseModel

class MistralAPIModel(BaseModel):
    def __init__(self, config):
        super().__init__(config)
        self.api_url = config["api_url"]
        self.api_key = os.getenv(config["api_key_env"])

    def detect_metaphors(self, sentences):
        prompt = (
            "Identifica y devuelve en JSON todas las expresiones metafóricas en estas oraciones:\n"
            f"\n{chr(10).join(sentences)}"
        )
        response = requests.post(
            self.api_url,
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={"prompt": prompt, "temperature": 0.3}
        )
        return response.json()