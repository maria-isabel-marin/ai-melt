import sys
import json
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
        self.post = Postprocessor()
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
                frase = m.get("frase") or ""
                expresion = m.get("expresion") or ""
                if frase and expresion:
                    expr = self.post.expand_expression(frase, {"start": 0, "end": len(expresion), "word": expresion})
                    tipo = self.classifier.label(expr)
                    results.append({
                        "expresion": expr,
                        "tipo": tipo,
                        "frase": frase
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
    print(json.dumps(results, ensure_ascii=False, indent=2))