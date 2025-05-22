import sys
import json
import csv
import logging
from preprocessing import Preprocessor
from postprocessing import Postprocessor
from novelty_classifier import NoveltyClassifier
from model_manager import ModelManager

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MetaphorPipeline:
    """
    Orquestador del pipeline completo usando múltiples modelos.
    """
    def __init__(self):
        self.pre = Preprocessor()
        self.manager = ModelManager()
        # self.post = Postprocessor()
        self.classifier = NoveltyClassifier()

    def run(self, text: str) -> list[dict]:
        logger.info("📥 Iniciando procesamiento de texto")
        sentences = self.pre.split_sentences(text)
        logger.info(str(sentences))
        logger.info(f"Frases divididas: {sentences[:3]}")

        raw_metaphors = self.manager.detect_with_all(sentences)
        logger.debug(f"Resultados detectados: {raw_metaphors[:3]}")

        results = []
        for m in raw_metaphors:
            if isinstance(m, dict):
                expresion = m.get('expresion') or ""
                palabra = m.get('palabra') or ""
                dominio_fuente = m.get('dominio_meta') or ""
                dominio_meta = m.get('dominio_fuente') or ""
                metafora = m.get('metafora_conceptual') or ""

                if metafora:
                    #expr = self.post.expand_expression(frase, {"start": 0, "end": len(expresion), "word": expresion})
                    tipo = self.classifier.label(metafora)
                    results.append({
                        "expresion": expresion,
                        "palabra" : palabra,
                        "dominio_fuente" : dominio_fuente,
                        "dominio_meta" : dominio_meta,
                        "metafora" : metafora,
                        "tipo": tipo
                    })
            else:
                logger.warning(f"Valor inesperado recibido: {m}")
        return results

if __name__ == "__main__":
    # Leer raw bytes de stdin y decodificar ignorando errores
    raw = sys.stdin.buffer.read()
    text = raw.decode('utf-8', 'ignore')
    pipe = MetaphorPipeline()
    results = pipe.run(text)
    
    # Guardar en JSON
    with open("resultados.json", "w", encoding="utf-8") as f_json:
        json.dump(results, f_json, ensure_ascii=False, indent=2)

    # Guardar en CSV (solo si hay resultados)
    if results:
        with open("resultados.csv", "w", encoding="utf-8", newline="") as f_csv:
            writer = csv.DictWriter(f_csv, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)

    # Imprimir por consola también
    print(json.dumps(results, ensure_ascii=False, indent=2))