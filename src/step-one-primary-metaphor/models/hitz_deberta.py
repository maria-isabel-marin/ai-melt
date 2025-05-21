from transformers import pipeline
from models.base import BaseModel

class HiTZDeBERTaModel(BaseModel):
    def __init__(self, config):
        super().__init__(config)
        self.pipe = pipeline(
            "token-classification",
            model=config["model_name"],
            aggregation_strategy=config.get("aggregation_strategy", "simple")
        )

    def detect_metaphors(self, sentences):
        results = []
        for sent in sentences:
            preds = self.pipe(sent)
            for entity in preds:
                if entity["entity_group"] == "METAPHOR":
                    results.append({
                        "expresion": entity["word"],
                        "frase": sent,
                        "indice_inicio": entity["start"],
                        "indice_fin": entity["end"]
                    })
        return results