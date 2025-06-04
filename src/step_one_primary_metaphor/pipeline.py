#!/usr/bin/env python
# src/step_one_primary_metaphor/pipeline.py

import sys
import json
import logging

from ai_melt_core.preprocessing import Preprocessor
from ai_melt_core.postprocessing import Postprocessor
from ai_melt_core.model_manager import ModelManager
from ai_melt_core.novelty_classifier import NoveltyClassifier

# — Configuración de logging —
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class MetaphorPipeline:
    """
    Orquesta el pipeline de detección de metáforas:
     1) Preprocesa el texto en oraciones
     2) Llama al ModelManager para ejecutar todos los modelos configurados
     3) Postprocesa y clasifica cada metáfora
    """
    def __init__(self):
        self.pre = Preprocessor()
        self.manager = ModelManager()
        #self.post = Postprocessor()
        self.classifier = NoveltyClassifier()

    def run(self, text: str) -> list[dict]:
        logger.info("📥 Iniciando procesamiento de texto")
        sentences = self.pre.split_sentences(text)
        logger.info(f"Frases divididas (primeras 3): {sentences[:3]}")

        raw = self.manager.detect_with_all(sentences)
        logger.debug(f"Raw detections (primeros 3): {raw[:3]}")

        results = []
        for m in raw:
            if not isinstance(m, dict):
                logger.warning(f"⚠️ Valor inesperado recibido de modelos: {m!r}")
                continue

            # Campos esperados
            expr = m.get("expresion", "")
            word = m.get("palabra", "")
            domain_meta = m.get("dominio_meta", "")
            domain_src  = m.get("dominio_fuente", "")
            cmp        = m.get("metafora_conceptual", "")

            if not expr or not cmp:
                # omitimos entradas sin expresión o sin concepto
                continue

            label = self.classifier.label(cmp)

            results.append({
                "expresion": expr,
                "palabra": word,
                "dominio_meta": domain_meta,
                "dominio_fuente": domain_src,
                "metafora_conceptual": cmp,
                "tipo": label
            })

        logger.info(f"✅ Metáforas finales: {len(results)} detectadas")
        return results


def main():
    """
    Entry-point para consola:
      python -m step_one_primary_metaphor.pipeline < input.txt > output.json
    """
    raw = sys.stdin.buffer.read()
    text = raw.decode("utf-8", "ignore")

    pipe = MetaphorPipeline()
    results = pipe.run(text)

    # Imprime JSON a stdout
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
