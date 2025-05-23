# src/step_one_primary_metaphor/cli.py

import sys
import json
import csv
import io
import argparse
import logging

from step_one_primary_metaphor.pipeline import MetaphorPipeline

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def main():
    parser = argparse.ArgumentParser(
        description="Run AI-MELT Step 1: detect metaphors in Spanish text"
    )
    parser.add_argument(
        "-f", "--format",
        choices=["json", "csv"],
        default="json",
        help="Output format (default: json)"
    )
    parser.add_argument(
        "-o", "--output",
        help="Output file path (default: stdout)"
    )
    args = parser.parse_args()

    # 1) Leer todo stdin
    text = sys.stdin.read()

    # 2) Ejecutar pipeline (aquí no se pierden llamadas a la API)
    results = MetaphorPipeline().run(text)

    # 3) Formatear la salida
    if args.format == "json":
        output_text = json.dumps(results, ensure_ascii=False, indent=2)
    else:
        # CSV via StringIO
        try:
            buffer = io.StringIO()
            writer = csv.DictWriter(buffer, fieldnames=results[0].keys() if results else [])
            writer.writeheader()
            writer.writerows(results)
            output_text = buffer.getvalue()
        except Exception as e:
            # Si falla el CSV, loguea el error y haz fallback a JSON
            logger.error(f"❌ Error generando CSV: {e}")
            output_text = json.dumps(results, ensure_ascii=False, indent=2)

    # 4) Escribir a archivo o stdout
    if args.output:
        try:
            with open(args.output, "w", encoding="utf-8", newline="") as f:
                f.write(output_text)
        except Exception as e:
            # No abortes: loguea y escribe la salida por stdout
            logger.error(f"❌ Error escribiendo en {args.output}: {e}")
            print(output_text)
    else:
        print(output_text)


if __name__ == "__main__":
    main()

