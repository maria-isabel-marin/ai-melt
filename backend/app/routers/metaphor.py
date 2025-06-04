# backend/app/routers/metaphor.py

from fastapi import APIRouter, HTTPException, Request
from typing import List

# Importa aquí tus Pydantic‐schemas
#   ProcessBatchRequest = esquema de entrada
#   MetaphorOut         = esquema de salida (sin ObjectId real, por ejemplo con _id: Optional[str])
from app.schemas.metaphor_schema import ProcessBatchRequest, MetaphorOut

# Importa la lógica que realmente detecta metáforas por batch
# Corrección: en tu estructura actual, el paquete "step_one_primary_metaphor" vive en la carpeta "src/"
# Debemos asegurar que Python lo vea dentro del path. Si arrancas Uvicorn desde "backend/", 
# tienes que añadir "../src" a sys.path. 
# Pero la forma más sencilla es usar un import absoluto si tu entorno ya está "instalando" ese módulo:
#
#   from step_one_primary_metaphor.pipeline import MetaphorPipeline
#
# Si NO lo has instalado como paquete, puedes arreglarlo así (ruta relativa con sys.path):
import sys
import os

# Añade “../../src” (dos niveles arriba) al PYTHONPATH para que Python encuentre “step_one_primary_metaphor”
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))  # .../backend/app/routers → /backend
SRC_DIR  = os.path.join(BASE_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.append(SRC_DIR)

from step_one_primary_metaphor.pipeline import MetaphorPipeline  # noqa: E402

router = APIRouter()


@router.post(
    "/process_batch",
    response_model=List[MetaphorOut],
    summary="Procesa un batch de texto y devuelve la lista de metáforas detectadas"
)
async def process_batch_endpoint(
    request: ProcessBatchRequest,
    fastapi_request: Request
):
    """
    Recibe un JSON con:
      - processing_code: str
      - batch_index: int
      - batch_text: str
      - prompt_tokens: int

    Llama internamente a `MetaphorPipeline().run(...)` para cada fragmento,
    y devuelve una lista de MetaphorOut.
    """
    print("▶▶▶ [DEBUG] Llego a /metaphor/process_batch con payload:", request)  # línea de debug
    db = fastapi_request.app.mongodb

    # 1) Validaciones básicas
    if request.prompt_tokens <= 0:
        print("▶▶▶ [DEBUG] prompt_tokens inválido:", request.prompt_tokens)
        raise HTTPException(status_code=400, detail="`prompt_tokens` must be a positive integer")
    if not request.batch_text or request.batch_text.strip() == "":
        print("▶▶▶ [DEBUG] batch_text vacío")
        raise HTTPException(status_code=400, detail="`batch_text` must not be empty")

    print("▶▶▶ [DEBUG] 2) Validaciones OK, llamando a process_batch_logic…")
    try:
        # 2) Por cada chunk (tokens por prompt) ejecuta la pipeline
        pipeline = MetaphorPipeline()
        core_results: List[dict] = []
        
        words = request.batch_text.split()
        # Genera fragmentos de `prompt_tokens` palabras cada uno
        chunks = [
            " ".join(words[i : i + request.prompt_tokens])
            for i in range(0, len(words), request.prompt_tokens)
            if words[i : i + request.prompt_tokens]
        ]

        print("▶▶▶ [DEBUG] ) Fragmentos generados:", len(chunks), "chunks")

        for chunk in chunks:
            # `pipeline.run(chunk)` devuelve List[dict] con campos como:
            #   {
            #     "expresion": "...",
            #     "dominio_fuente": "...",
            #     "dominio_meta": "...",
            #     "metafora_conceptual": "...",
            #     "tipo": "..."
            #   }
            print("▶▶▶ [DEBUG] ) Procesando chunk:", chunk)
            print("▶▶▶ [DEBUG] ) Llamando a pipeline.run(...)")
            detected: List[dict] = pipeline.run(chunk)
            print("▶▶▶ [DEBUG] ) Metáforas detectadas:", len(detected), "en este chunk")
            core_results.extend(detected)

        # 3) Mapea cada dict en core_results → MetaphorOut (sin insertar en BD)
        output_list: List[MetaphorOut] = []
        for m in core_results:
            print("▶▶▶ [DEBUG] )    Procesando metáfora:", m)
            # Creamos un MetaphorOut para cada resultado
            # Nota: _id es None porque no estamos insertando en MongoDB
            out = MetaphorOut(
                _id="",  # no hay ObjectId real porque no estamos guardando
                processing_code=request.processing_code,
                batch_index=request.batch_index,
                expression=m.get("expresion", ""),
                sourceDomain=m.get("dominio_fuente", ""),
                targetDomain=m.get("dominio_meta", ""),
                conceptualMetaphor=m.get("metafora_conceptual", ""),
                type=m.get("tipo", ""),
                confirmed=False,
            )
            print("▶▶▶ [DEBUG] )    Metáfora procesada:", out)
            output_list.append(out)
        print("▶▶▶ [DEBUG] ) Total metáforas procesadas:", len(output_list))

        return output_list

    except Exception as exc:
        # Si ocurre cualquier excepción, devolvemos un HTTP 500 con el detalle
        print("▶▶▶ [ERROR] Ocurrió un error al procesar el batch:", str(exc))
        raise HTTPException(status_code=500, detail=f"Error detecting metaphors: {str(exc)}")
