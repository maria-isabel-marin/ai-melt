import os
import json
import logging
from openai import OpenAI
from ai_melt_core.models.base import BaseModel
from dotenv import load_dotenv
load_dotenv()

logger = logging.getLogger(__name__)

class OpenAIGPTModel(BaseModel):
    def __init__(self, config):
        super().__init__(config)
        self.model = config.get("model", "gpt-4.1-nano")
        self.api_key = os.getenv(config["api_key_env"]) # config["api_key_env"] == "OPENAI_API_KEY"
        self.client = OpenAI(api_key=self.api_key)

    def detect_metaphors(self, sentences):
        prompt = (
            "You are a linguist specialized in Conceptual Metaphor Theory (Lakoff, Johnson, Kövecses). "
            "Your task is to identify metaphorical expressions in the following Spanish sentences, and describe each one in a strict JSON format.\n\n"
            "For each metaphor, include:\n"
            "1. \"expresion\": the exact Spanish expression that contains the metaphor.\n"
            "2. \"palabra\": the single word (typically a verb or noun) that triggers the metaphor.\n"
            "3. \"dominio_meta\": the target domain (in UPPERCASE), with determiners if they appear.\n"
            "4. \"dominio_fuente\": the source domain (in UPPERCASE), with determiners if they apply.\n"
            "5. \"metafora_conceptual\": an exact literal concatenation: DOMINIO_META + ' ES ' or 'SON' + DOMINIO_FUENTE (in UPPERCASE).\n\n"
            "Important:\n"
            "- DO NOT paraphrase or modify the domain values.\n"
            "- DO NOT omit determiners such as EL, LA, LOS, LAS.\n"
            "- The output must be valid JSON with double quotes.\n"
            "- Output must be in Spanish.\n\n"
            "Example:\n"
            "Texto:\nCristina derrumbó todos los argumentos de la oposición respecto al déficit fiscal\n"
            "Respuesta JSON:\n"
            "[\n"
            "  {\n"
            "    \"expresion\": \"Cristina derrumbó todos los argumentos\",\n"
            "    \"palabra\": \"derrumbó\",\n"
            "    \"dominio_meta\": \"LOS ARGUMENTOS\",\n"
            "    \"dominio_fuente\": \"EDIFICIOS\",\n"
            "    \"metafora_conceptual\": \"LOS ARGUMENTOS ES EDIFICIOS\"\n"
            "  }\n"
            "]\n\n"
            "Now analyze the following Spanish text:\n"
            f"Texto:\n{chr(10).join(sentences)}"
        )

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert in conceptual metaphor analysis."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=1000,
                n=1
            )

            content = response.choices[0].message.content
            logger.info(f"📦 OpenAI response:\n{content}")

            start = content.find('[')
            end = content.rfind(']')
            if start == -1 or end == -1 or end < start:
                logger.warning("❌ No JSON array found in OpenAI response")
                return []

            json_text = content[start:end+1]

            try:
                metaphor_list = json.loads(json_text)
                logger.debug(json.dumps(metaphor_list, ensure_ascii=False, indent=2))
                return metaphor_list
            except json.JSONDecodeError as e:
                logger.warning(f"❌ JSON parsing failed: {e}")
                return []

        except Exception as e:
            logger.error(f"❌ OpenAI API call failed: {e}")
            return []
