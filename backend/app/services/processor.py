# backend/app/services/processor.py

from typing import List

# Importa el Pydantic schema de salida
from app.schemas.metaphor_schema import MetaphorOut

# Importa la pipeline de detección (corrige la ruta para que Python la encuentre)
import sys
import os

# Igual que en el router, aseguramos que “src/” esté en sys.path:
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))  # .../backend/app/services → /backend
SRC_DIR  = os.path.join(BASE_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.append(SRC_DIR)

from step_one_primary_metaphor.pipeline import MetaphorPipeline  # noqa: E402


async def process_batch_logic(
    text: str,
    prompt_tokens: int,
    processing_code: str,
    batch_index: int,
    db
) -> List[MetaphorOut]:
    """
    - `text`:    el texto completo del batch (proporcionado por el front)
    - `prompt_tokens`: cuántos tokens por prompt
    - `processing_code`: código de procesamiento (shared job code)
    - `batch_index`: índice actual del batch
    - `db`: instancia de Motor (fastapi_request.app.mongodb), que NO usamos aquí

    Esta función **NO** inserta nada en MongoDB; retorna solo la lista de MetaphorOut
    con todos los resultados que genere MetaphorPipeline().run(...)
    """

    # 1) Fragmentamos `text` en pedazos de tamaño `prompt_tokens` (tokens)
    words = text.split()

    chunks = [
        " ".join(words[i : i + prompt_tokens])
        for i in range(0, len(words), prompt_tokens)
        if words[i : i + prompt_tokens]
    ]

    # 2) Ejecución de la pipeline en cada fragmento
    core_results: List[dict] = []
    pipeline = MetaphorPipeline()

    for chunk in chunks:
        # `pipeline.run(chunk)` devuelve List[dict], con keys como:
        #   "expresion", "dominio_fuente", "dominio_meta", "metafora_conceptual", "tipo"
        detected: List[dict] = pipeline.run(chunk)
        core_results.extend(detected)

    # 3) Mapeamos cada dict → MetaphorOut y devolvemos la lista
    output_list: List[MetaphorOut] = []
    for m in core_results:
        out = MetaphorOut(
            _id=None,  # No hay ObjectId real porque el enpoint no inserta en BD
            processing_code=processing_code,
            batch_index=batch_index,
            expression=m.get("expresion", ""),
            sourceDomain=m.get("dominio_fuente", ""),
            targetDomain=m.get("dominio_meta", ""),
            conceptualMetaphor=m.get("metafora_conceptual", ""),
            type=m.get("tipo", ""),
            confirmed=False
        )
        output_list.append(out)

    return output_list
