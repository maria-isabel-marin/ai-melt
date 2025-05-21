import os
import requests
from models.base import BaseModel

class GeminiModel(BaseModel):
    def __init__(self, config):
        super().__init__(config)
        self.api_key = os.getenv(config["api_key_env"])
        self.model = config["model"]

    def detect_metaphors(self, sentences):
        prompt = (
            "Detecta todas las expresiones metafóricas en las siguientes oraciones. "
            "Devuelve una lista JSON con cada expresión encontrada, incluyendo el texto exacto de la expresión, la palabra con la carga metafórica en la expresión, el dominio fuente y el dominio meta de acuerdo a la estructura de la teoría de la metáfora: DOMINIO META ES DOMINIO FUENTE.\n"
            f"Texto:\n{chr(10).join(sentences)}"
        )
        response = requests.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent",
            params={"key": self.api_key},
            json={"contents": [{"parts": [{"text": prompt}]}]}
        )
        return response.json()