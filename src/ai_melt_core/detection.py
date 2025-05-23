from transformers import pipeline
from ai_melt_core.config import environment
from typing import List, Dict, Any

class MetaphorDetector:
    """
    Detector de metáforas usando un modelo transformer pre-entrenado
    con agrupación de tokens en entidades completas.
    """
    def __init__(self):
        self.pipe = pipeline(
            "token-classification",
            model=environment["HUGGINGFACE_MODEL"],
            aggregation_strategy=environment["AGGREGATION_STRATEGY"]
        )

    def detect(self, sentences: List[str]) -> List[Dict[str, Any]]:
        """
        Aplica el modelo a una lista de oraciones y retorna una lista de diccionarios
        con cada expresión metafórica encontrada, incluyendo:
        - expresion: texto de la expresión metafórica
        - frase: la oración original
        - indice_inicio: posición inicial en la oración
        - indice_fin: posición final en la oración
        """
        resultados = []
        for frase in sentences:
            preds = self.pipe(frase)
            for entidad in preds:
                if entidad['entity_group'] == 'METAPHOR':
                    resultados.append({
                        "expresion": entidad['word'],
                        "frase": frase,
                        "indice_inicio": entidad['start'],
                        "indice_fin": entidad['end']
                    })
        return resultados