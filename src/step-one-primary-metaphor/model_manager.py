from config import active_models, model_configs
from models.hitz_deberta import HiTZDeBERTaModel
from models.lwachowiak_xlmr import LwachowiakXLMRModel
from models.openai_gpt import OpenAIGPTModel
from models.gemini import GeminiModel
from models.llama_api import LLaMAModel
from models.mistral_api import MistralAPIModel
from models.llama_quant import LLaMAQuantModel
import json

class ModelManager:
    def __init__(self):
        self.models = []
        for model_name in active_models:
            cfg = model_configs[model_name]
            if model_name == "hitz_deberta":
                self.models.append(HiTZDeBERTaModel(cfg))
            elif model_name == "lwachowiak_xlmr":
                self.models.append(LwachowiakXLMRModel(cfg))
            elif model_name == "openai_gpt":
                self.models.append(OpenAIGPTModel(cfg))
            elif model_name == "gemini":
                self.models.append(GeminiModel(cfg))
            elif model_name == "llama_api":
                self.models.append(LLaMAModel(cfg))
            elif model_name == "mistral_api":
                self.models.append(MistralAPIModel(cfg))
            elif model_name == "llama_3_70b_quant":
                self.models.append(LLaMAQuantModel(cfg))

    def detect_with_all(self, sentences):
        results = []
        for model in self.models:
            try:
                output = model.detect_metaphors(sentences)
                if isinstance(output, str):
                    try:
                        output = json.loads(output)
                    except json.JSONDecodeError:
                        continue
                elif isinstance(output, dict) and "choices" in output:
                    output = output["choices"][0].get("text")
                    output = json.loads(output)
                results.extend(output)
            except Exception as e:
                print(f"[ERROR] Modelo {model.__class__.__name__} falló: {e}")
        return results