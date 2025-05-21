import os
import openai
from models.base import BaseModel

class OpenAIGPTModel(BaseModel):
    def __init__(self, config):
        super().__init__(config)
        openai.api_key = os.getenv(config["api_key_env"])
        self.model = config["model"]

    def detect_metaphors(self, sentences):
        prompt = (
            "Detecta todas las expresiones metafóricas en las siguientes oraciones. "
            "Devuelve una lista JSON con cada metáfora encontrada, incluyendo el texto exacto de la expresión y la oración original.\n"
            f"Oraciones:\n{chr(10).join(sentences)}"
        )
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "Eres un experto en lenguaje figurado."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        return response.choices[0].message['content']