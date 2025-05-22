import os
import json
import requests
import logging
import re
from models.base import BaseModel

logger = logging.getLogger(__name__)

class GeminiModel(BaseModel):
    def __init__(self, config):
        super().__init__(config)
        self.api_key = os.getenv(config["api_key_env"])
        self.model = config["model"]

    def detect_metaphors(self, sentences):
        prompt = (
            "Detecta todas las expresiones metafóricas en las siguientes oraciones. "
            "Devuelve una lista JSON con cada expresión encontrada, incluyendo por cada expresión: 1) el texto exacto de la expresión, "
            "2) la palabra con la carga metafórica en la expresión, 3) el dominio fuente, 4) el dominio meta y 5) la metáfora conceptual, de acuerdo a "
            "la teoría de la metáfora conceptual que estructura las metáforas de la forma: DOMINIO META ES DOMINIO FUENTE.\n\n"
            "Ejemplo:\n"
            "Texto:\nCristina derrumbó todos los argumentos de la oposición respecto al déficit fiscal\n"
            "Respuesta JSON:\n"
            "[\n"
            "  {\n"
            "    \"texto_exacto_expresion\": \"Cristina derrumbó todos los argumentos\",\n"
            "    \"palabra_carga_metaforica\": \"derrumbó\",\n"
            "    \"dominio_meta\": \"LOS ARGUMENTOS\",\n"
            "    \"dominio_fuente\": \"EDIFICIOS\",\n"
            "    \"metafora_conceptual\": \"LOS ARGUMENTOS SON EDIFICIOS\"\n"
            "  }\n"
            "]\n\n"
            "Ahora, procesa el siguiente texto:\n"
            f"Texto:\n{chr(10).join(sentences)}"
        )

        response = requests.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent",
            params={"key": self.api_key},
            json={"contents": [{"parts": [{"text": prompt}]}]}
        )

        try:
            data = response.json()
            logger.info(f"📦 Respuesta completa de Gemini: {json.dumps(data, ensure_ascii=False)}")
            # Extraer el texto generado
            content = data['candidates'][0]['content']['parts'][0]['text']

            # Buscar bloque JSON dentro de Markdown ```json ... ```
            match = re.search(r"```json\s*(.*?)\s*```", content, flags=re.DOTALL | re.IGNORECASE)
            if match:
                json_text = match.group(1).strip()
            else:
                # Si no hay bloque markdown, usar todo el contenido
                json_text = content.strip()

            # Cargar JSON limpio
            metaphor_list = json.loads(json_text)

            results = []
            for metaphor in metaphor_list:
                if isinstance(metaphor, dict) and 'texto_exacto_expresion' in metaphor:
                    results.append({
                        "frase": metaphor['texto_exacto_expresion'],
                        "expresion": metaphor['texto_exacto_expresion']
                    })
            return results

        except (KeyError, IndexError, json.JSONDecodeError) as e:
            logger.warning(f"❌ Error procesando respuesta de Gemini: {e}")
            logger.debug(f"🔎 Texto a parsear tras limpieza: {json_text if 'json_text' in locals() else content}")
            return []