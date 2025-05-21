import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from models.base import BaseModel

class LLaMAQuantModel(BaseModel):
    def __init__(self, config):
        super().__init__(config)
        model_id = config["model_name"]
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_id,
            device_map="auto",
            torch_dtype=torch.float16
        )
        self.model.eval()

    def detect_metaphors(self, sentences):
        prompt = (
            "Detecta todas las expresiones metafóricas en las siguientes oraciones. "
            "Devuelve una lista JSON con cada metáfora encontrada, incluyendo el texto exacto de la expresión y la oración original.\n"
            f"Oraciones:\n{chr(10).join(sentences)}"
        )
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=512,
                temperature=0.3,
                do_sample=False
            )
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response
